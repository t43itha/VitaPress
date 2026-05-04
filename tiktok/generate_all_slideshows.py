#!/usr/bin/env python3
"""
Generate all 5 TikTok slideshows for Vita Press
Following Larry methodology from openclaw-imports/larry
"""

import json
import sys
from pathlib import Path

# Import our slideshow generator
sys.path.insert(0, str(Path(__file__).parent))
from generate_slideshow import generate_slideshow

def create_captions_md(slideshow_data, output_dir):
    """Create captions.md file for each slideshow"""
    name = slideshow_data["name"]
    hook_var = slideshow_data["hook_variable"]
    blend = slideshow_data["blend"]
    
    # Extract hook from first slide
    hook = slideshow_data["slides"][0]["text"].replace('\n', ' ')
    
    # Create caption content
    content = f"""# {name}

## Hook
{hook}

## Caption
{hook} 😭

I've been struggling with energy and my PT recommended I try cold-pressed juice instead of synthetic pre-workout. So I found Vita Press — they make fresh cold-pressed juice every Sunday in London with proper ingredient weights (129g beetroot, 125g carrot, 129g apple, 27g ginger per 250ml bottle).

I tried the {blend} blend and honestly?? The difference is wild. No jitters, no crash, just actual sustained energy. Plus it's £3.50 vs £35 for a tub of powder.

Comment 🧃 to pre-order — Sunday pickup or local London delivery.

## Hashtags
#coldpressedjuice #beetrootjuice #preworkout #londonwellness #vitapress #healthylondon #naturalenergy #fyp

## Best Post Time
UK time: 7:30 AM or 4:30 PM (catch morning/afternoon scrollers)

## Hook Variable Being Tested
**{hook_var}**

This slideshow tests a different angle from the other 4:
- Slideshow 1: Authority figure (PT) endorsement
- Slideshow 2: Transparency/ingredient breakdown curiosity
- Slideshow 3: Medical authority solving personal health problem
- Slideshow 4: Aspirational identity (London aesthetic)
- Slideshow 5: Intentional imperfection for comment engagement

## Performance Metrics to Track
- Views in first 30 minutes
- Comment rate (especially for slideshow 5 - spot the typo)
- Profile visits
- DM mentions of 🧃

## Larry Rules
- Kill if <500 views by 24h
- Double down if >5K views in first day
- Watch comment sentiment for hook refinement
"""
    
    output_path = Path(output_dir) / "captions.md"
    output_path.write_text(content)
    print(f"  ✓ Created captions.md")


def main():
    # Load slideshow recipes
    recipes_path = Path(__file__).parent / "slideshow_recipes.json"
    with open(recipes_path) as f:
        recipes = json.load(f)
    
    base_output = Path(__file__).parent / "2026-05-04"
    base_output.mkdir(exist_ok=True)
    
    results = []
    
    for idx, (key, data) in enumerate(recipes.items(), 1):
        print(f"\n{'='*70}")
        print(f"SLIDESHOW {idx}/5: {data['name']}")
        print(f"Hook variable: {data['hook_variable']}")
        print(f"{'='*70}\n")
        
        # Create output directory
        slideshow_dir = base_output / f"slideshow-{idx}"
        slideshow_dir.mkdir(exist_ok=True)
        
        try:
            # Generate slideshow
            generate_slideshow(
                name=data['name'],
                slides_data=data['slides'],
                output_dir=str(slideshow_dir),
                bottle_image=data['bottle_image']
            )
            
            # Create captions.md
            create_captions_md(data, slideshow_dir)
            
            results.append({
                "slideshow": idx,
                "name": data['name'],
                "path": str(slideshow_dir.absolute()),
                "status": "SUCCESS"
            })
            
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            results.append({
                "slideshow": idx,
                "name": data['name'],
                "path": str(slideshow_dir.absolute()),
                "status": f"FAILED: {e}"
            })
            # Continue to next slideshow
            continue
    
    # Print summary
    print(f"\n{'='*70}")
    print("GENERATION COMPLETE")
    print(f"{'='*70}\n")
    
    for result in results:
        status_icon = "✓" if result["status"] == "SUCCESS" else "❌"
        print(f"{status_icon} Slideshow {result['slideshow']}: {result['name']}")
        print(f"   Path: {result['path']}")
        print(f"   Status: {result['status']}\n")
    
    # Save results
    results_file = base_output / "generation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    return results


if __name__ == "__main__":
    main()
