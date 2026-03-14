#!/usr/bin/env python3
"""
generate_images.py — The Machine Stops image generator
Reads prompts from IMAGE_PROMPTS.md and generates images via the Gemini API.

Usage:
  python generate_images.py                   # generate all missing images
  python generate_images.py --dry-run         # preview prompts, no API calls
  python generate_images.py --cluster cell    # generate one cluster only
  python generate_images.py --force           # regenerate even if file exists
  python generate_images.py --list-clusters   # show available clusters

Requirements:
  pip install google-genai Pillow

API key:
  export GEMINI_API_KEY="your_key_from_aistudio.google.com"
  (or pass --api-key KEY)
"""

import argparse
import base64
import os
import re
import sys
import time
from io import BytesIO
from pathlib import Path

# ─── Model selection ──────────────────────────────────────────────────────────
#
# gemini-3.1-flash-image-preview  (Nano Banana 2)
#   - Free tier: ~500 images/day via Google AI Studio key
#   - Supports reference images for cluster consistency
#   - Best choice for this project
#
# gemini-3-pro-image-preview  (Nano Banana Pro)
#   - Reasoning-enhanced, handles complex compositions better
#   - Paid; check current status at aistudio.google.com before using
#   - Worth trying for kuno_cell_shaft and corridor_dark if flash results
#     are compositionally weak
#
MODEL = "gemini-3.1-flash-image-preview"

PROMPTS_FILE = Path(__file__).parent / "IMAGE_PROMPTS.md"
IMAGES_DIR   = Path(__file__).parent / "images"

# Seconds between API calls — free tier is generous but not unlimited
RATE_LIMIT_DELAY = 4

# ─── Cluster generation order (matches GENERATION ORDER in IMAGE_PROMPTS.md) ─
# Each cluster is a list of filenames in the order they should be generated.
# The first image in each cluster is generated standalone; subsequent images
# receive the previous result as a reference image for consistency.
CLUSTER_ORDER = [
    ("cell",      ["cell_normal.jpg", "cell_restless.jpg",
                   "cell_flickering.jpg", "cell_dark.jpg"]),
    ("airship",   ["airship_peaceful.jpg", "airship_blind.jpg",
                   "airship_night.jpg"]),
    ("book",      ["book_reverenced.jpg", "book_stained.jpg"]),
    ("plate",     ["plate_active.jpg", "plate_static.jpg"]),
    ("kuno",      ["kuno_cell.jpg", "kuno_cell_conversation.jpg",
                   "kuno_cell_shaft.jpg"]),
    ("corridors", ["corridor.jpg", "corridor_failing.jpg",
                   "corridor_dark.jpg"]),
    ("surface",   ["surface_glimpse.jpg", "surface_top.jpg"]),
]

# ─── Reference prompt prefixes for cluster follow-ons ─────────────────────────
# When passing a reference image, we prepend this to the full prompt so the
# model understands it's producing a variant, not an unrelated new image.
REFERENCE_PREFIX = (
    "Here is the previous image in this cluster for visual consistency. "
    "Generate a variant using the same base composition, architectural style, "
    "Art Nouveau decorative vocabulary, and colour palette, with only the "
    "specific changes described below:\n\n"
)

# ─────────────────────────────────────────────────────────────────────────────

def parse_prompts(md_path: Path) -> tuple[str, dict[str, str]]:
    """
    Parse IMAGE_PROMPTS.md and return:
      (style_foundation: str, prompts: dict[filename -> full_prompt])

    The style foundation is extracted once and substituted for [STYLE FOUNDATION]
    in every prompt. The markdown structure is:
      - Style foundation in a blockquote under ## STYLE FOUNDATION
      - Each image under a ### heading like: ### ✓ `cell_normal.jpg`
      - Prompt in a blockquote immediately after **Prompt:**
    """
    text = md_path.read_text(encoding="utf-8")

    # ── Extract style foundation ─────────────────────────────────────────────
    style_match = re.search(
        r"## STYLE FOUNDATION.*?Prepend this block verbatim to every prompt:\s*\n\n"
        r"((?:^> .*\n)+)",
        text, re.MULTILINE | re.DOTALL
    )
    if not style_match:
        raise ValueError("Could not find STYLE FOUNDATION block in IMAGE_PROMPTS.md")

    style_foundation = "\n".join(
        line[2:] for line in style_match.group(1).strip().splitlines()
    )

    # ── Extract per-image prompts ────────────────────────────────────────────
    prompts = {}

    # Find all image sections: ### ✓/★ `filename.jpg`
    sections = re.split(r"^### [✓★] `", text, flags=re.MULTILINE)

    for section in sections[1:]:  # skip preamble before first ###
        # Extract filename
        filename_match = re.match(r"([a-z0-9_]+\.jpg)", section)
        if not filename_match:
            continue
        filename = filename_match.group(1)

        # Extract blockquote prompt (the one under **Prompt:** or just the
        # first blockquote in the section that starts with [STYLE FOUNDATION])
        quote_match = re.search(
            r"^(?:> \[STYLE FOUNDATION\].*?\n)((?:^> .*\n)*)",
            section, re.MULTILINE
        )
        if not quote_match:
            # Try alternate: blockquote that starts directly with [STYLE FOUNDATION]
            quote_match = re.search(
                r"((?:^> \[STYLE FOUNDATION\].*\n)(?:^> .*\n)*)",
                section, re.MULTILINE
            )
        if not quote_match:
            print(f"  ⚠ No prompt blockquote found for {filename}, skipping")
            continue

        # Collect all > lines as the prompt body
        raw_lines = re.findall(r"^> (.*)", section, re.MULTILINE)
        if not raw_lines:
            continue

        # Reconstruct the prompt, substituting [STYLE FOUNDATION]
        raw_prompt = " ".join(raw_lines).strip()
        full_prompt = raw_prompt.replace("[STYLE FOUNDATION]", style_foundation + " —")

        # Clean up any double spaces and trailing dashes
        full_prompt = re.sub(r"  +", " ", full_prompt).strip()
        prompts[filename] = full_prompt

    return style_foundation, prompts


def generate_image(
    client,
    prompt: str,
    model: str,
    reference_bytes: bytes | None = None,
    retries: int = 3,
    debug: bool = False,
) -> bytes | None:
    """
    Call the Gemini API. If reference_bytes is provided, passes it as the
    first part of the content (enables cluster consistency).
    Returns raw image bytes, or None on failure.
    """
    from google import genai
    from google.genai import types

    contents = []

    if reference_bytes:
        contents.append(
            types.Part.from_bytes(data=reference_bytes, mime_type="image/jpeg")
        )
        contents.append(REFERENCE_PREFIX + prompt)
    else:
        contents.append(prompt)

    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                ),
            )

            if debug:
                print(f"\n    [DEBUG] Response candidates: {len(response.candidates)}")
                for ci, cand in enumerate(response.candidates):
                    print(f"    [DEBUG] Candidate {ci}: finish_reason={cand.finish_reason}")
                    for pi, part in enumerate(cand.content.parts):
                        if part.inline_data is not None:
                            d = part.inline_data
                            data_type = type(d.data).__name__
                            data_len  = len(d.data) if d.data else 0
                            print(f"    [DEBUG]   Part {pi}: inline_data "
                                  f"mime={d.mime_type} "
                                  f"data_type={data_type} "
                                  f"data_len={data_len}")
                        elif part.text is not None:
                            print(f"    [DEBUG]   Part {pi}: text={part.text[:120]!r}")
                        else:
                            print(f"    [DEBUG]   Part {pi}: (other) {part}")

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    data = part.inline_data.data

                    # SDK ≥1.x returns raw bytes directly — do NOT base64-decode.
                    # Guard: if someone is on an older SDK that returns a string,
                    # decode it; otherwise use as-is.
                    if isinstance(data, str):
                        data = base64.b64decode(data)
                    elif isinstance(data, bytes) and len(data) > 4:
                        # Sanity-check: if it looks like base64 text stored as
                        # bytes (all ASCII, no null bytes) try to decode it.
                        # Real image bytes will have non-ASCII values near the start.
                        if all(32 <= b < 127 for b in data[:16]):
                            try:
                                data = base64.b64decode(data)
                            except Exception:
                                pass  # leave as-is if decode fails

                    return data

            # No image part found — print text response if present, for diagnosis
            text_parts = [
                p.text for p in response.candidates[0].content.parts
                if p.text is not None
            ]
            if text_parts:
                print(f"    ⚠ Model returned text instead of image "
                      f"(attempt {attempt}): {' '.join(text_parts)[:200]!r}")
            else:
                print(f"    ⚠ No image in response (attempt {attempt})")

        except Exception as e:
            err = str(e)
            if "SAFETY" in err.upper() or "RECITATION" in err.upper():
                print(f"    ✗ Content filter triggered: {err[:200]}")
                print("      Try softening vocabulary — see notes in IMAGE_PROMPTS.md")
                return None  # Don't retry safety blocks
            if "NOT_FOUND" in err.upper() or "404" in err:
                print(f"    ✗ Model not found: {model!r}")
                print(f"      Check available models at aistudio.google.com")
                print(f"      Try: --model gemini-2.0-flash-exp")
                return None  # Don't retry bad model names
            print(f"    ⚠ API error (attempt {attempt}/{retries}): {err[:200]}")
            if attempt < retries:
                time.sleep(RATE_LIMIT_DELAY * attempt)

    return None


def save_image(image_bytes: bytes, path: Path) -> None:
    """Save image bytes as JPEG, converting if necessary."""
    try:
        from PIL import Image
        img = Image.open(BytesIO(image_bytes))
        # Ensure square — crop to smaller dimension if needed
        w, h = img.size
        if w != h:
            side = min(w, h)
            left = (w - side) // 2
            top  = (h - side) // 2
            img  = img.crop((left, top, left + side, top + side))
        img = img.convert("RGB")
        img.save(str(path), "JPEG", quality=92)
    except ImportError:
        # Pillow not available — save raw bytes
        path.write_bytes(image_bytes)


def run(args):
    IMAGES_DIR.mkdir(exist_ok=True)

    # ── List models mode ──────────────────────────────────────────────────────
    if args.list_models:
        api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("✗ No API key. Set GEMINI_API_KEY or pass --api-key KEY")
            sys.exit(1)
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            print("Models supporting IMAGE output:\n")
            for m in client.models.list():
                caps = getattr(m, 'supported_generation_methods', []) or []
                output_types = getattr(m, 'output_modalities', []) or []
                # Check both attribute styles across SDK versions
                if ('generateContent' in caps or 'generate_content' in caps) and (
                    'IMAGE' in (output_types or []) or
                    'image' in str(m).lower()
                ):
                    print(f"  {m.name}")
                    if hasattr(m, 'description') and m.description:
                        print(f"    {m.description[:100]}")
            print("\nAll models (for reference):")
            for m in client.models.list():
                print(f"  {m.name}")
        except Exception as e:
            print(f"✗ Error listing models: {e}")
        return

    # ── Parse prompts ─────────────────────────────────────────────────────────
    print(f"Parsing {PROMPTS_FILE.name}...")
    try:
        style_foundation, prompts = parse_prompts(PROMPTS_FILE)
    except Exception as e:
        print(f"✗ Failed to parse prompts: {e}")
        sys.exit(1)

    print(f"  Found {len(prompts)} prompts")

    # ── List clusters mode ────────────────────────────────────────────────────
    if args.list_clusters:
        print("\nAvailable clusters:")
        for name, files in CLUSTER_ORDER:
            existing = sum(1 for f in files if (IMAGES_DIR / f).exists())
            print(f"  {name:12s}  {len(files)} images  ({existing} already exist)")
        return

    # ── Filter to requested cluster ───────────────────────────────────────────
    clusters = CLUSTER_ORDER
    if args.cluster:
        clusters = [(n, f) for n, f in CLUSTER_ORDER if n == args.cluster]
        if not clusters:
            names = [n for n, _ in CLUSTER_ORDER]
            print(f"✗ Unknown cluster '{args.cluster}'. Available: {', '.join(names)}")
            sys.exit(1)

    # ── Build work queue in cluster order ─────────────────────────────────────
    work = []  # list of (cluster_name, filename, is_first_in_cluster)
    for cluster_name, files in clusters:
        for i, filename in enumerate(files):
            out_path = IMAGES_DIR / filename
            if out_path.exists() and not args.force:
                print(f"  skip  {filename}  (exists — use --force to regenerate)")
                continue
            if filename not in prompts:
                print(f"  skip  {filename}  (no prompt found in markdown)")
                continue
            work.append((cluster_name, filename, i == 0))

    if not work:
        print("\nNothing to generate. All images exist (use --force to regenerate).")
        return

    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Generating {len(work)} image(s):\n")

    # ── Dry run: just show prompts ────────────────────────────────────────────
    if args.dry_run:
        current_cluster = None
        for cluster_name, filename, is_first in work:
            if cluster_name != current_cluster:
                print(f"  ── Cluster: {cluster_name} ──")
                current_cluster = cluster_name
            marker = "(standalone)" if is_first else "(+ reference)"
            print(f"  {filename}  {marker}")
            print(f"    {prompts[filename][:140]}...")
            print()
        return

    # ── Live generation ───────────────────────────────────────────────────────
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("✗ No API key found. Set GEMINI_API_KEY or pass --api-key KEY")
        print("  Get a key at: https://aistudio.google.com/apikey")
        sys.exit(1)

    try:
        from google import genai
    except ImportError:
        print("✗ google-genai not installed. Run: pip install google-genai Pillow")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    current_cluster   = None
    last_image_bytes  = None  # reference for next image in same cluster

    for cluster_name, filename, is_first in work:
        # Reset reference image when cluster changes
        if cluster_name != current_cluster:
            print(f"\n── Cluster: {cluster_name} ──")
            current_cluster  = cluster_name
            last_image_bytes = None

            # If the first image of this cluster already exists on disk,
            # load it as the reference for subsequent images
            first_file = next(
                (f for n, files in CLUSTER_ORDER if n == cluster_name
                 for f in files), None
            )
            if first_file and is_first is False:
                first_path = IMAGES_DIR / first_file
                if first_path.exists():
                    last_image_bytes = first_path.read_bytes()
                    print(f"  Using {first_file} as cluster reference")

        out_path = IMAGES_DIR / filename
        ref_label = " (with reference)" if last_image_bytes and not is_first else ""
        print(f"  Generating {filename}{ref_label}...", end=" ", flush=True)

        image_bytes = generate_image(
            client,
            prompts[filename],
            model=args.model,
            reference_bytes=last_image_bytes if not is_first else None,
            debug=getattr(args, 'debug', False),
        )

        if image_bytes:
            save_image(image_bytes, out_path)
            print(f"✓  saved to images/{filename}")
            last_image_bytes = out_path.read_bytes()  # use saved JPEG as next reference
        else:
            print("✗  failed — skipping")
            # Don't update last_image_bytes so the next image still has a reference

        if work.index((cluster_name, filename, is_first)) < len(work) - 1:
            time.sleep(RATE_LIMIT_DELAY)

    print(f"\nDone. Images saved to: {IMAGES_DIR.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images for The Machine Stops from IMAGE_PROMPTS.md"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview prompts without making API calls"
    )
    parser.add_argument(
        "--cluster", metavar="NAME",
        help="Generate only one cluster (cell, airship, book, plate, kuno, corridors, surface)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Regenerate images even if they already exist"
    )
    parser.add_argument(
        "--list-clusters", action="store_true",
        help="List available clusters and exit"
    )
    parser.add_argument(
        "--api-key", metavar="KEY",
        help="Gemini API key (default: $GEMINI_API_KEY env var)"
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Print raw API response structure — useful for diagnosing image data issues"
    )
    parser.add_argument(
        "--list-models", action="store_true",
        help="Query the API and list models that support image generation, then exit"
    )
    parser.add_argument(
        "--model", metavar="MODEL", default=MODEL,
        help=f"Model to use (default: {MODEL})"
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
