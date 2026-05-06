#!/usr/bin/env python3
"""Generate slides for Slideshow 9 — Innocent Hot Take (E3)
Brand callout: "Innocent smoothies are basically dessert"

Slides:
1. Hook text: "Hot take: Innocent smoothies are basically dessert 🍬"
2. Sugar comparison: "26g sugar = more than a Krispy Kreme"
3. Math breakdown: "26g sugar ÷ 4 = 6.5 teaspoons"
4. Transition: "What a REAL juice looks like ⬇️"
5. Vita Press bottle CTA: "Cold-pressed. No concentrates. No BS."
"""

import base64, json, os, pathlib, sys, time
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

# Load API key
for line in (pathlib.Path.home() / ".hermes/.env").read_text().splitlines():
    if line.startswith("OPENAI_API_KEY="):
        os.environ["OPENAI_API_KEY"] = line.split("=", 1)[1].strip()

KEY = os.environ["OPENAI_API_KEY"]
OUT = pathlib.Path("/tmp/VitaPress/tiktok/2026-05-06/slideshow-9")
OUT.mkdir(parents=True, exist_ok=True)
BOTTLE_PATH = pathlib.Path("/tmp/VitaPress/vita-press-video/public/liver-kidney-bottle.png")

# Shared visual language
BASE = (
    "Important details: Vertical 9:16 (1024x1536). Moody dark food photography aesthetic. "
    "Dark slate/charcoal surface with dramatic warm rim light from upper-left. "
    "50mm lens feel, shallow depth of field, subtle film grain. Generous negative space "
    "in upper 40% of frame for text overlay. Premium wellness brand aesthetic.\n"
    "Use case: TikTok slideshow image.\n"
    "Constraints: NO text, NO labels, NO writing, NO logos, NO brand names, "
    "NO numbers, NO price tags, NO words anywhere in the image."
)

SLIDES_PROMPTS = {
    "01": (
        f"Scene: Dark moody flat-lay. A half-empty Innocent smoothie bottle (orange/yellow "
        f"packaging, recognisable shape) tipped on its side with the bright coloured smoothie "
        f"pooling/spilling across the dark slate surface. Scattered candy and sugar cubes nearby. "
        f"Pink and yellow sweets scattered around the bottle.\n"
        f"Subject: The spilled smoothie and candy — evoking 'this is basically dessert'.\n{BASE}"
    ),
    "02": (
        f"Scene: Close-up overhead shot of a dark surface. A single glazed donut "
        f"(Krispy Kreme style, shiny sugar glaze) sitting next to a small glass of bright "
        f"orange smoothie. Dramatic side lighting making the sugar glaze glisten. A few loose "
        f"sugar crystals scattered on the surface between them.\n"
        f"Subject: The donut and smoothie side by side — visual comparison.\n{BASE}"
    ),
    "03": (
        f"Scene: Overhead flat-lay on dark slate. Six white sugar cubes arranged in a neat "
        f"line across the center of the frame. One sugar cube is crumbling/crushed at the end. "
        f"Warm directional light casting long shadows from each cube. Clean, minimal, "
        f"almost scientific presentation.\n"
        f"Subject: Sugar cubes as a visual representation of hidden sugar.\n{BASE}"
    ),
    "04": (
        f"Scene: Pure matte black background with a single dramatic shaft of warm golden "
        f"light cutting diagonally across the frame from upper left. Dust particles visible "
        f"in the light beam. Very dark, cinematic, anticipatory mood. Nearly entirely black "
        f"with just the light shaft.\n"
        f"Subject: The light beam — a visual transition/reveal moment.\n{BASE}"
    ),
}

# Text overlay config
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
TEXT_COLOR = (255, 255, 255)
STROKE_COLOR = (0, 0, 0)
STROKE_WIDTH = 6

SLIDE_TEXT = {
    "01": "Hot take:\nInnocent smoothies\nare basically dessert 🍬",
    "02": "26g sugar per bottle\n= more than a\nKrispy Kreme donut",
    "03": "26g sugar ÷ 4\n= 6.5 teaspoons\n\nThis is your\n'healthy' breakfast",
    "04": "What a REAL juice\nlooks like ⬇️",
    "05": "Cold-pressed.\nNo concentrates.\nNo BS.\n\nComment 🧃 to try\nthe real thing",
}


def generate_image(prompt, size="1024x1536"):
    """Call gpt-image-2 generations endpoint."""
    r = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"model": "gpt-image-2", "prompt": prompt, "size": size, "quality": "high", "n": 1},
        timeout=240,
    )
    r.raise_for_status()
    b64 = r.json()["data"][0]["b64_json"]
    return Image.open(BytesIO(base64.b64decode(b64)))


def generate_product_slide(bottle_path, prompt, size="1024x1536"):
    """Call gpt-image-2 edits endpoint with product reference."""
    with open(bottle_path, "rb") as f:
        r = requests.post(
            "https://api.openai.com/v1/images/edits",
            headers={"Authorization": f"Bearer {KEY}"},
            files=[("image[]", ("bottle.png", f, "image/png"))],
            data={"model": "gpt-image-2", "prompt": prompt, "size": size, "quality": "high"},
            timeout=240,
        )
    r.raise_for_status()
    b64 = r.json()["data"][0]["b64_json"]
    return Image.open(BytesIO(base64.b64decode(b64)))


def overlay_text(img, text, font_size=90):
    """Add centered white text with black stroke to top portion of image."""
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, font_size)

    # Calculate text block height
    lines = text.split("\n")
    line_height = font_size * 1.3
    total_height = len(lines) * line_height

    # Position: centered horizontally, ~20% from top
    y_start = int(img.height * 0.15)

    for i, line in enumerate(lines):
        if not line.strip():
            continue
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img.width - text_width) // 2
        y = y_start + int(i * line_height)
        # Draw stroke
        draw.text((x, y), line, font=font, fill=TEXT_COLOR,
                  stroke_width=STROKE_WIDTH, stroke_fill=STROKE_COLOR)

    return img


def main():
    print("🎬 Generating Slideshow 9 — Innocent Hot Take")
    print("=" * 50)

    # Generate slides 1-4 (text-free scenes)
    for slide_num, prompt in sorted(SLIDES_PROMPTS.items()):
        print(f"\n📸 Slide {slide_num}...")
        start = time.time()
        img = generate_image(prompt)
        elapsed = time.time() - start
        print(f"   Generated in {elapsed:.0f}s")

        # Overlay text
        text = SLIDE_TEXT.get(slide_num, "")
        if text:
            img = overlay_text(img.convert("RGBA"), text)

        out_path = OUT / f"{slide_num}.png"
        img.convert("RGB").save(out_path, quality=95)
        print(f"   Saved: {out_path}")

    # Slide 5: Product reveal with bottle reference
    print(f"\n📸 Slide 05 (product reveal)...")
    if BOTTLE_PATH.exists():
        product_prompt = (
            "Scene: Dark slate surface, warm rim light from upper-left, moody premium product shot. "
            "The provided juice bottle positioned center-right, standing upright, with dramatic lighting. "
            "A few fresh ingredients (beetroot slice, ginger root) scattered artfully nearby.\n"
            "Subject: The provided product bottle as hero, lit dramatically.\n"
            "Important details: Preserve the bottle's exact shape, label, cap. Add realistic contact "
            "shadow. Match warm rim light on glass. Vertical 9:16 (1024x1536). Generous space in "
            "upper portion for text.\n"
            "Use case: TikTok product reveal slide.\n"
            "Constraints: Do NOT redesign the bottle. Do NOT add any text or logos."
        )
        start = time.time()
        img = generate_product_slide(BOTTLE_PATH, product_prompt)
        elapsed = time.time() - start
        print(f"   Generated in {elapsed:.0f}s")
    else:
        # Fallback: generate without bottle reference
        fallback_prompt = (
            f"Scene: Dark slate surface with a tall glass bottle of deep burgundy/red "
            f"cold-pressed juice, standing upright. Fresh beetroot slices and ginger root "
            f"scattered artfully nearby. Warm rim light, moody premium product shot.\n"
            f"Subject: A beautiful cold-pressed juice bottle as the hero product.\n{BASE}"
        )
        start = time.time()
        img = generate_image(fallback_prompt)
        elapsed = time.time() - start
        print(f"   Generated (fallback) in {elapsed:.0f}s")

    text = SLIDE_TEXT.get("05", "")
    if text:
        img = overlay_text(img.convert("RGBA"), text, font_size=85)

    out_path = OUT / "05.png"
    img.convert("RGB").save(out_path, quality=95)
    print(f"   Saved: {out_path}")

    print(f"\n✅ All 5 slides generated in {OUT}")
    print("Files:", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
