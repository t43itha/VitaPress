#!/usr/bin/env python3
"""
Generate TikTok slideshow with OpenAI images + text overlays
Following Larry methodology: gpt-image-2, 1080x1920, text-driven reveals
"""

import os
import sys
import json
import base64
import time
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

OPENAI_API_KEY = "os.environ["OPENAI_API_KEY"]"

def generate_image_openai(prompt, model="gpt-image-2"):
    """Generate image with OpenAI gpt-image-2"""
    print(f"  Generating image with {model}...")
    print(f"  Prompt: {prompt[:80]}...")
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": "1024x1536",  # Portrait for TikTok (will upscale to 1080x1920)
        "quality": "high",
        "n": 1
    }
    
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload,
        timeout=120
    )
    
    if response.status_code != 200:
        print(f"  ERROR: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    
    # Handle both b64_json and url responses
    if "data" in data and len(data["data"]) > 0:
        if "b64_json" in data["data"][0]:
            img_data = base64.b64decode(data["data"][0]["b64_json"])
            return Image.open(BytesIO(img_data))
        elif "url" in data["data"][0]:
            img_response = requests.get(data["data"][0]["url"])
            return Image.open(BytesIO(img_response.content))
    
    return None


def resize_to_tiktok(img):
    """Resize image to 1080x1920 (TikTok portrait)"""
    return img.resize((1080, 1920), Image.Resampling.LANCZOS)


def add_text_overlay(img, text, output_path):
    """
    Add text overlay following Larry's proven formula:
    - White text with thick black outline
    - Centered at 28% from top
    - Dynamic sizing based on text length
    - 4-6 words per line
    """
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
    
    # Try to load a bold system font, fallback to default
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
        
        # Get text bbox for centering
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
    print(f"  ✓ Saved: {output_path}")


def composite_bottle(background_path, bottle_path, output_path):
    """Composite bottle image on background for final CTA slide"""
    bg = Image.open(background_path).convert('RGBA')
    bottle = Image.open(bottle_path).convert('RGBA')
    
    # Resize bottle to fit nicely (about 60% of background height)
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


def generate_slideshow(name, slides_data, output_dir, bottle_image=None):
    """
    Generate complete slideshow
    slides_data = [
        {"prompt": "...", "text": "..."},
        ...
    ]
    """
    print(f"\n{'='*60}")
    print(f"GENERATING SLIDESHOW: {name}")
    print(f"{'='*60}\n")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for idx, slide in enumerate(slides_data, 1):
        print(f"\nSlide {idx}/{len(slides_data)}")
        
        # Special handling for last slide (CTA with bottle)
        if idx == len(slides_data) and bottle_image:
            print(f"  Creating CTA slide with bottle...")
            # Generate background
            img = generate_image_openai(slide["prompt"])
            if not img:
                print(f"  FAILED to generate slide {idx}")
                continue
            
            img = resize_to_tiktok(img)
            temp_bg = output_path / f"temp_bg_{idx}.png"
            img.save(temp_bg)
            
            # Composite bottle
            composite_path = output_path / f"temp_composite_{idx}.png"
            composite_bottle(temp_bg, bottle_image, composite_path)
            
            # Add text overlay
            final_img = Image.open(composite_path)
            add_text_overlay(final_img, slide["text"], output_path / f"{idx:02d}.png")
            
            # Cleanup
            temp_bg.unlink()
            composite_path.unlink()
        else:
            # Generate base image
            img = generate_image_openai(slide["prompt"])
            if not img:
                print(f"  FAILED to generate slide {idx}")
                continue
            
            # Resize to TikTok dimensions
            img = resize_to_tiktok(img)
            
            # Add text overlay
            add_text_overlay(img, slide["text"], output_path / f"{idx:02d}.png")
        
        # Rate limiting
        if idx < len(slides_data):
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"✓ SLIDESHOW COMPLETE: {output_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Test with a simple slideshow
    test_slides = [
        {
            "prompt": "iPhone photo of fresh beetroot and carrots on dark slate surface, moody lighting, raw vegetables, natural texture, realistic phone camera quality",
            "text": "My PT said replace\npre-workout with this\n£3.50 bottle"
        },
        {
            "prompt": "iPhone photo of whole beetroot on dark slate surface, moody lighting, deep purple color, natural texture, realistic phone camera quality",
            "text": "129g beetroot\nper bottle"
        }
    ]
    
    generate_slideshow("test", test_slides, "/tmp/test_slideshow")
