#!/usr/bin/env python3
"""
Generate TikTok slideshow with built-in image generation + text overlays
Using MCP image generation which handles model routing automatically
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def add_text_overlay(img_path, text, output_path):
    """
    Add text overlay following Larry's proven formula
    """
    img = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Dynamic font sizing based on text length
    word_count = len(text.split())
    if word_count <= 5:
        font_size = int(width * 0.075)  # 75px on 1080w
    elif word_count <= 12:
        font_size = int(width * 0.065)  # 66px
    else:
        font_size = int(width * 0.050)  # 51px
    
    # Try to load a bold system font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    outline_width = int(font_size * 0.15)
    max_width = width * 0.75
    line_height = font_size * 1.3
    
    # Word wrap
    lines = []
    manual_lines = text.split('\n')
    
    for ml in manual_lines:
        words = ml.strip().split()
        current = ''
        for word in words:
            test = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    
    # Position: centered at 28% from top
    total_height = len(lines) * line_height
    start_y = (height * 0.28) - (total_height / 2)
    x = width / 2
    
    # Draw each line
    for i, line in enumerate(lines):
        y = start_y + (i * line_height)
        
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = x - (text_width / 2)
        
        # Black outline
        for adj_x in range(-outline_width, outline_width+1):
            for adj_y in range(-outline_width, outline_width+1):
                draw.text((text_x + adj_x, y + adj_y), line, font=font, fill='#000000')
        
        # White fill
        draw.text((text_x, y), line, font=font, fill='#FFFFFF')
    
    img.save(output_path)
    print(f"  ✓ Saved with text: {output_path}")


def composite_bottle(background_path, bottle_path, output_path):
    """Composite bottle image on background for final CTA slide"""
    bg = Image.open(background_path).convert('RGBA')
    bottle = Image.open(bottle_path).convert('RGBA')
    
    # Resize bottle to fit nicely
    bottle_height = int(bg.height * 0.6)
    aspect = bottle.width / bottle.height
    bottle_width = int(bottle_height * aspect)
    bottle = bottle.resize((bottle_width, bottle_height), Image.Resampling.LANCZOS)
    
    # Center bottle
    x = (bg.width - bottle_width) // 2
    y = (bg.height - bottle_height) // 2
    
    bg.paste(bottle, (x, y), bottle)
    bg.convert('RGB').save(output_path)
    return output_path


def resize_to_tiktok(img_path, output_path):
    """Resize image to 1080x1920"""
    img = Image.open(img_path)
    img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
    img.save(output_path)
    return output_path


# Slide definitions for all 5 slideshows
SLIDESHOWS = {
    "slideshow-1": {
        "name": "PT Pre-Workout Swap (K&L)",
        "hook_variable": "Authority figure reveal hook",
        "bottle": "/tmp/VitaPress/vita-press-video/public/liver-kidney-bottle.png",
        "slides": [
            ("iPhone photo of gym pre-workout powder tub and a 250ml juice bottle side by side on dark moody slate surface, dramatic lighting, raw unpolished feel, slight shadow, realistic phone camera quality",
             "My PT said replace\npre-workout with this\n£3.50 bottle"),
            ("iPhone photo of whole fresh beetroot on dark slate surface, moody lighting, deep purple-red color, natural earthy texture, slightly imperfect, realistic phone camera quality",
             "129g beetroot\nper bottle\nnatural nitrates"),
            ("iPhone photo of fresh carrots on dark slate surface, moody lighting, orange vegetables, natural texture, slightly muddy, realistic phone camera quality",
             "125g carrot\npacked with\nvitamin A"),
            ("iPhone photo of Granny Smith apples and fresh ginger root on dark slate surface, moody dramatic lighting, green apples and tan ginger, natural rustic feel, realistic phone camera quality",
             "129g apple\n27g ginger\nno powder\nno fillers"),
            ("iPhone photo of expensive pre-workout supplement tub with price tag vs small juice bottle on dark slate, moody lighting, price comparison setup, realistic phone camera quality",
             "£3.50 vs\n£35 a tub\nsame energy\nno chemicals"),
            ("Dark moody slate background with warm subtle lighting, minimal texture, empty centered space, realistic phone camera quality",
             "Comment 🧃\nto pre-order\nSunday pickup or\nLondon delivery\n£3.50 / 3 for £10")
        ]
    },
    "slideshow-2": {
        "name": "What's Actually In This Bottle (K&L)",
        "hook_variable": "Transparency/curiosity hook",
        "bottle": "/tmp/VitaPress/vita-press-video/public/liver-kidney-bottle.png",
        "slides": [
            ("iPhone photo of a 250ml juice bottle on dark slate surface with scattered vegetables around it, moody lighting, questioning composition, realistic phone camera quality",
             "What's actually\nin your £3.50\njuice?"),
            ("iPhone photo of whole beetroot being weighed on kitchen scale showing 129g, dark moody background, natural lighting, real kitchen setup feel, realistic phone camera quality",
             "129g beetroot\nweighed fresh\nevery bottle"),
            ("iPhone photo of fresh carrots being weighed on kitchen scale showing 125g, dark background, natural lighting, imperfect vegetables, realistic phone camera quality",
             "125g carrot\nmore veg than\nyour dinner"),
            ("iPhone photo of Granny Smith apples on scale showing 129g, dark moody slate surface, natural lighting, realistic phone camera quality",
             "129g Granny Smith\napple base"),
            ("iPhone photo of fresh ginger root on scale showing 27g, dark background, natural texture close-up, realistic phone camera quality",
             "27g ginger\nmore veg than most\nrestaurant sides"),
            ("iPhone photo of fresh produce ingredients laid out together on dark slate, moody lighting, all vegetables visible, realistic phone camera quality",
             "410g fresh produce\nin every 250ml\ncold-pressed\nnothing added"),
            ("Dark moody slate background with warm subtle lighting, minimal texture, empty centered space, realistic phone camera quality",
             "Comment 🧃\nto pre-order\nSunday pickup or\nLondon delivery\n£3.50 / 3 for £10")
        ]
    },
    "slideshow-3": {
        "name": "Iron Deficient Authority (K&L)",
        "hook_variable": "Medical authority + personal problem hook",
        "bottle": "/tmp/VitaPress/vita-press-video/public/liver-kidney-bottle.png",
        "slides": [
            ("iPhone photo of doctor's notepad with 'iron deficiency' written on it next to a juice bottle, dark moody background, realistic phone camera quality",
             "My nutritionist\ntold me to drink\nthis every morning"),
            ("iPhone photo of beetroot cut in half showing deep purple interior on dark slate, moody lighting, natural iron-rich food, realistic phone camera quality",
             "Beetroot = natural\niron without\nsynthetic supplements"),
            ("iPhone photo of fresh beetroot juice in glass showing deep red color, dark background, natural lighting, realistic phone camera quality",
             "Natural nitrates\nbetter than pills"),
            ("iPhone photo split comparison: tired person morning vs energized person afternoon, natural phone photo feel, realistic lighting",
             "Before: tired\nall day\nAfter: actually\nhave energy"),
            ("iPhone photo of supplement pill bottles vs fresh juice bottle on dark slate, moody lighting, natural vs synthetic comparison, realistic phone camera quality",
             "No synthetic iron\nno stomach issues\njust real food"),
            ("Dark moody slate background with warm subtle lighting, minimal texture, empty centered space, realistic phone camera quality",
             "Comment 🧃\nto pre-order\nSunday pickup or\nLondon delivery\n£3.50 / 3 for £10")
        ]
    },
    "slideshow-4": {
        "name": "London Girlies Fridge (Skin Boost)",
        "hook_variable": "Aspirational identity hook",
        "bottle": "/tmp/VitaPress/vita-press-video/public/skin-boost-bottle.png",
        "slides": [
            ("iPhone photo of open fridge with skincare products on shelf next to juice bottles, London flat aesthetic, natural lighting, realistic phone camera quality",
             "London girlies —\nwhat's in my fridge\ninstead of skincare"),
            ("iPhone photo of fresh oranges cut open on dark slate surface, moody lighting, vibrant orange color, vitamin C rich, realistic phone camera quality",
             "182g orange\nper bottle\nvitamin C bomb"),
            ("iPhone photo of fresh limes and carrots on dark slate, moody lighting, green and orange vegetables, natural texture, realistic phone camera quality",
             "38g lime\n87g carrot\napple base"),
            ("iPhone photo of expensive vitamin C serum bottle next to juice bottle on dark slate, price comparison, moody lighting, realistic phone camera quality",
             "Vitamin C serum:\n£40 topical\nVita Press:\n£3.50 from inside"),
            ("iPhone photo of fresh glowing skin close-up, natural lighting, no filters, realistic phone camera quality",
             "Drink your skincare\nactual results"),
            ("Dark moody slate background with warm subtle lighting, minimal texture, empty centered space, realistic phone camera quality",
             "Comment 🧃\nto pre-order\nSunday pickup or\nLondon delivery\n£3.50 / 3 for £10")
        ]
    },
    "slideshow-5": {
        "name": "Boomer-Bait Mistake (K&L)",
        "hook_variable": "Intentional imperfection for engagement",
        "bottle": "/tmp/VitaPress/vita-press-video/public/liver-kidney-bottle.png",
        "slides": [
            ("iPhone photo of fresh juice bottle on dark slate surface with vegetables scattered around, moody lighting, raw unpolished feel, realistic phone camera quality",
             "introducting\nVita Press\ncold-pressed juice"),
            ("iPhone photo of beetroot and carrots on dark slate, moody lighting, natural vegetables, realistic phone camera quality",
             "Beetroot + carrot\n+ apple + ginger\n250ml bottles"),
            ("iPhone photo of fresh produce being cold-pressed in juicer, dark background, natural process shot, realistic phone camera quality",
             "Cold-pressed\nevery Sunday\nno HPP\nno pasterization"),
            ("iPhone photo of three juice bottles lined up on dark slate, moody lighting, product shot, realistic phone camera quality",
             "£3.50 each or\n3 for £10\nLondon delivery"),
            ("iPhone photo of fresh ingredients with price breakdown visible on dark slate, moody lighting, transparency shot, realistic phone camera quality",
             "Fresh ingredients\nsame day pressed\nno preservatives"),
            ("Dark moody slate background with warm subtle lighting, minimal texture, empty centered space, realistic phone camera quality",
             "Comment 🧃\nto pre-order\nSunday pickup or\nLondon delivery\nWhat did you spot?")
        ]
    }
}


if __name__ == "__main__":
    base_dir = Path("/tmp/VitaPress/tiktok/2026-05-04")
    
    # We'll generate placeholders using simple colored backgrounds since image gen failed
    # This ensures deliverables are ready even if images need regeneration
    
    for slideshow_id, data in SLIDESHOWS.items():
        print(f"\n{'='*60}")
        print(f"Creating {slideshow_id}: {data['name']}")
        print(f"{'='*60}\n")
        
        slideshow_dir = base_dir / slideshow_id
        slideshow_dir.mkdir(exist_ok=True, parents=True)
        
        for idx, (prompt, text) in enumerate(data['slides'], 1):
            output_file = slideshow_dir / f"{idx:02d}.png"
            
            print(f"Slide {idx}/{len(data['slides'])}")
            print(f"  Creating base image...")
            
            # Create a dark moody placeholder
            img = Image.new('RGB', (1080, 1920), color='#2c3e50')
            temp_path = slideshow_dir / f"temp_{idx}.png"
            img.save(temp_path)
            
            # If last slide, composite bottle
            if idx == len(data['slides']) and data['bottle']:
                print(f"  Adding bottle...")
                composite_path = slideshow_dir / f"temp_composite_{idx}.png"
                composite_bottle(temp_path, data['bottle'], composite_path)
                add_text_overlay(composite_path, text, output_file)
                composite_path.unlink()
            else:
                add_text_overlay(temp_path, text, output_file)
            
            temp_path.unlink()
        
        print(f"\n✓ Complete: {slideshow_dir}\n")
    
    print("\n" + "="*60)
    print("ALL SLIDESHOWS CREATED")
    print("="*60)
    print("\nNOTE: Images are dark slate placeholders.")
    print("Replace with actual product photos before posting.")
    print("Text overlays are production-ready.\n")
