#!/usr/bin/env python3
"""
Regenerate TikTok slideshow backgrounds using Gemini Imagen
and recomposite text overlays.
"""

import os
import sys
import json
import base64
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

GEMINI_API_KEY = "os.environ["GEMINI_API_KEY"]"
IMAGEN_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict"

# Slide definitions for each slideshow
SLIDESHOWS = {
    1: {
        "name": "PT Pre-Workout Swap (K&L)",
        "product": "liver-kidney",
        "slides": [
            {"text": "My PT said replace\npre-workout with this\n£3.50 bottle", "bg_prompt": "Overhead shot of bright red pre-workout powder tub on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "129g beetroot\n125g carrot\n129g apple\n27g ginger", "bg_prompt": "Overhead shot of fresh beetroot whole and sliced on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "£3.50 vs £35\nfor a tub of powder", "bg_prompt": "Overhead shot of fresh carrots in a bunch on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "No jitters\nNo crash\nJust energy", "bg_prompt": "Overhead shot of fresh ginger root on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Fresh cold-pressed\nevery Sunday\nin London", "bg_prompt": "Overhead shot of Granny Smith green apples on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "VITA PRESS", "is_bottle": True}
        ]
    },
    2: {
        "name": "What's Actually In This Bottle (K&L)",
        "product": "liver-kidney",
        "slides": [
            {"text": "What's actually in\nyour £3.50 juice?", "bg_prompt": "Overhead shot of fresh beetroot whole and sliced showing deep red color on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "129g\nbeetroot", "bg_prompt": "Close-up overhead shot of fresh beetroot whole and half sliced on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "125g\ncarrot", "bg_prompt": "Overhead shot of fresh carrots in a bunch with green tops on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "129g\napple", "bg_prompt": "Overhead shot of Granny Smith green apples whole and sliced on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "27g\nginger", "bg_prompt": "Overhead shot of fresh ginger root knob on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Fresh every Sunday\nLocal London delivery", "bg_prompt": "Overhead shot of mixed fresh vegetables beetroot carrot apple ginger arranged on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "VITA PRESS", "is_bottle": True}
        ]
    },
    3: {
        "name": "Iron Deficient Authority (K&L)",
        "product": "liver-kidney",
        "slides": [
            {"text": "My nutritionist told me\nto drink this\nevery morning", "bg_prompt": "Overhead shot of fresh leafy greens and beetroot on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "I was always tired\nLow iron\nLow energy", "bg_prompt": "Overhead shot of morning kitchen counter with natural light streaming in, dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "129g beetroot\nNatural iron boost", "bg_prompt": "Close-up overhead shot of fresh beetroot whole and sliced showing vibrant red on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "No more\nsupplement pills", "bg_prompt": "Overhead shot of vitamin bottles and supplement pills scattered on dark moody slate surface being pushed aside, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Fresh cold-pressed\nevery Sunday\n£3.50", "bg_prompt": "Overhead shot of fresh beetroot carrot apple and ginger arranged neatly on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "VITA PRESS", "is_bottle": True}
        ]
    },
    4: {
        "name": "London Girlies Fridge (Skin Boost)",
        "product": "skin-boost",
        "slides": [
            {"text": "London girlies —\nwhat's in my fridge\ninstead of skincare", "bg_prompt": "Overhead shot of luxury skincare bottles on white bathroom counter with cold-pressed juice bottle on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "I stopped buying\n£40 serums", "bg_prompt": "Overhead shot of expensive skincare bottles being replaced on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Started drinking\nthis instead\n£3.50", "bg_prompt": "Overhead shot of fresh oranges whole and sliced on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Orange + Lime\nNatural vitamin C", "bg_prompt": "Overhead shot of fresh limes and oranges together on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Fresh every Sunday\nLocal London delivery", "bg_prompt": "Close-up overhead shot of fresh citrus slices oranges and limes on dark moody slate surface, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "VITA PRESS", "is_bottle": True}
        ]
    },
    5: {
        "name": "Boomer-Bait Mistake (K&L)",
        "product": "liver-kidney",
        "slides": [
            {"text": "introducting\nVita Press\ncold-pressed juice", "bg_prompt": "Overhead shot of fresh beetroot whole on dark moody slate surface slightly off-center, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "129g beetroot\n125g carrot\n129g apple\n27g ginger", "bg_prompt": "Overhead shot of fresh carrots bunch on dark moody slate surface slightly angled, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Fresh every Sunday\nin London", "bg_prompt": "Overhead shot of Granny Smith apples on dark moody slate surface cropped asymmetrically, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "£3.50 per bottle\nLocal delivery", "bg_prompt": "Overhead shot of fresh ginger root on dark moody slate surface off-center composition, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "Comment 🧃\nto pre-order", "bg_prompt": "Overhead shot of mixed vegetables beetroot carrot apple ginger on dark moody slate surface slightly rotated, warm natural light, slight shadow, real-feeling, shot on iPhone, vertical composition"},
            {"text": "VITA PRESS", "is_bottle": True}
        ]
    }
}

def generate_imagen_background(prompt):
    """Generate a background image using Gemini Imagen API"""
    url = f"{IMAGEN_ENDPOINT}?key={GEMINI_API_KEY}"
    
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "9:16"
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        if "predictions" in data and len(data["predictions"]) > 0:
            image_b64 = data["predictions"][0].get("bytesBase64Encoded")
            if image_b64:
                image_data = base64.b64decode(image_b64)
                return Image.open(BytesIO(image_data))
        
        print(f"Error: Unexpected response format: {data}")
        return None
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def create_fallback_background():
    """Create a fallback dark slate gradient background"""
    img = Image.new('RGB', (1080, 1920), (44, 62, 80))
    draw = ImageDraw.Draw(img)
    
    # Add subtle gradient
    for y in range(1920):
        shade = int(44 + (y / 1920) * 20)
        draw.line([(0, y), (1080, y)], fill=(shade, shade + 18, shade + 36))
    
    return img

def add_text_overlay(img, text):
    """Add text overlay to image using Larry's formula"""
    draw = ImageDraw.Draw(img)
    
    # Try to load a bold font, fall back to default
    try:
        # Try common system fonts
        font_paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial Bold.ttf",
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 90)
                break
        if not font:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Position: centered, 28% from top
    y_position = int(1920 * 0.28)
    
    # Draw text with black stroke
    lines = text.split('\n')
    line_height = 110
    
    total_height = len(lines) * line_height
    current_y = y_position - (total_height // 2)
    
    for line in lines:
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (1080 - text_width) // 2
        
        # Draw black stroke (outline)
        stroke_width = 4
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx*dx + dy*dy <= stroke_width*stroke_width:
                    draw.text((x_position + dx, current_y + dy), line, 
                             font=font, fill=(0, 0, 0))
        
        # Draw white text
        draw.text((x_position, current_y), line, font=font, fill=(255, 255, 255))
        
        current_y += line_height
    
    return img

def create_bottle_slide(product_name):
    """Create the final bottle hero slide"""
    # Create dark slate background
    bg = Image.new('RGB', (1080, 1920), (44, 62, 80))
    
    # Load bottle PNG
    bottle_path = f"/tmp/VitaPress/vita-press-video/public/{product_name}-bottle.png"
    
    if os.path.exists(bottle_path):
        bottle = Image.open(bottle_path)
        
        # Resize bottle to fit nicely in frame (about 60% of height)
        target_height = int(1920 * 0.6)
        aspect_ratio = bottle.width / bottle.height
        target_width = int(target_height * aspect_ratio)
        
        bottle = bottle.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Center the bottle
        x_pos = (1080 - target_width) // 2
        y_pos = (1920 - target_height) // 2
        
        # Composite bottle onto background (handle transparency)
        if bottle.mode == 'RGBA':
            bg.paste(bottle, (x_pos, y_pos), bottle)
        else:
            bg.paste(bottle, (x_pos, y_pos))
    
    # Add "VITA PRESS" text
    bg = add_text_overlay(bg, "VITA PRESS")
    
    return bg

def process_slideshow(slideshow_num, slideshow_data):
    """Process a single slideshow"""
    folder = f"/tmp/VitaPress/tiktok/2026-05-04/slideshow-{slideshow_num}"
    slides = slideshow_data["slides"]
    product = slideshow_data["product"]
    
    print(f"\n{'='*60}")
    print(f"Processing Slideshow {slideshow_num}: {slideshow_data['name']}")
    print(f"{'='*60}")
    
    fallback_count = 0
    imagen_count = 0
    
    for idx, slide in enumerate(slides, 1):
        slide_num = f"{idx:02d}"
        output_path = f"{folder}/{slide_num}.png"
        
        print(f"\nSlide {slide_num}: {slide['text'][:30]}...")
        
        if slide.get("is_bottle"):
            # Create bottle hero slide
            print("  → Creating bottle hero slide")
            img = create_bottle_slide(product)
        else:
            # Generate background via Imagen
            print(f"  → Generating Imagen background...")
            bg = generate_imagen_background(slide["bg_prompt"])
            
            if bg is None:
                print("  → Imagen failed, retrying once...")
                bg = generate_imagen_background(slide["bg_prompt"])
            
            if bg is None:
                print("  → Imagen failed twice, using fallback gradient")
                bg = create_fallback_background()
                fallback_count += 1
            else:
                imagen_count += 1
                # Resize to exact dimensions
                bg = bg.resize((1080, 1920), Image.Resampling.LANCZOS)
            
            # Add text overlay
            print("  → Adding text overlay")
            img = add_text_overlay(bg, slide["text"])
        
        # Save
        img.save(output_path, "PNG", optimize=True)
        print(f"  ✓ Saved to {output_path}")
    
    return imagen_count, fallback_count

def main():
    total_imagen = 0
    total_fallback = 0
    
    for slideshow_num in sorted(SLIDESHOWS.keys()):
        slideshow_data = SLIDESHOWS[slideshow_num]
        imagen_count, fallback_count = process_slideshow(slideshow_num, slideshow_data)
        total_imagen += imagen_count
        total_fallback += fallback_count
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total Imagen API calls: {total_imagen}")
    print(f"Total fallback slides: {total_fallback}")
    print(f"All slideshows regenerated successfully!")

if __name__ == "__main__":
    main()
