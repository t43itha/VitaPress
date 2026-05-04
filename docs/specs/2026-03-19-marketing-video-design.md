# Vita Press — Marketing Video / Slideshow Design

**Date**: 2026-03-19
**Context**: Table-top marketing video for weekend juice sales. Looping MP4 displayed on laptop or tablet at the sales table. Educates customers about the 4 juice blends, their ingredients, and health benefits.

---

## 1. Overview

A 90-second looping video (6 slides x 15 seconds each) showcasing the Vita Press juice range. Built as an HTML slideshow first for design control, then screen-recorded to MP4 for universal offline playback.

**Primary goal**: Educate — show what's in each juice and why it's good for you.
**Secondary goal**: Build trust — fresh-pressed, no additives, real ingredients from the market.

---

## 2. Technical Specs

| Property | Value |
|----------|-------|
| Aspect ratio | 16:9 landscape |
| Resolution | 1920x1080 (Full HD) |
| Duration | ~90 seconds (loop) |
| Slide duration | 15 seconds each |
| Transition | Crossfade, 1.5 seconds |
| Frame rate | 30fps |
| Codec | H.264, target under 50MB |
| Final format | MP4 (screen-recorded from HTML) |
| Playback | Laptop or tablet, looping, no interaction |

---

## 3. Visual Style

- **Background**: Dark (#1a1815)
- **Typography**: Instrument Serif (headings), DM Sans (body)
- **Accent colours**: Per juice blend (see slide details)
- **Image style**: AI-generated market stall images for ingredients, real photos for intro/closing
- **Footer**: Consistent "Fresh-pressed · No additives · No compromise" on every slide
- **Overall feel**: Bold, dark, premium — juice colours pop against dark background

---

## 4. Slide Sequence

### Slide 1 — Intro (15s)

- **Visual**: Real photo — market stall (IMG_4130 or IMG_4131) with dark gradient overlay
- **Text**: Vita Press wordmark (large, centred, rendered in Instrument Serif — no separate logo file) + tagline "Fresh-pressed. No additives. No compromise."
- **Accent**: Orange (#d4700a)
- **Animation**: Fade in wordmark, then tagline

### Slide 2 — Skin Boost (15s)

- **Visual**: AI-generated market stall image — oranges, limes, carrots, apples arranged in rustic crates
- **Layout**: Image left half, text right half
- **Juice name**: "Skin Boost" in amber/orange (#f5a623)
- **Ingredients**: Orange · Lime · Carrot · Apple
- **Benefit**: "Beta-carotene rich. Supports healthy, glowing skin from the inside out."
- **Footer**: "Fresh-pressed · No additives · No compromise"

### Slide 3 — Detox (15s)

- **Visual**: AI-generated market stall image — celery, limes, cucumbers, apples
- **Layout**: Image left half, text right half
- **Juice name**: "Detox" in green (#4caf50)
- **Ingredients**: Celery · Lime · Cucumber · Apple
- **Benefit**: "Clean & refreshing. Hydration and gentle cleansing."
- **Footer**: "Fresh-pressed · No additives · No compromise"

### Slide 4 — Immunity Boost (15s)

- **Visual**: AI-generated market stall image — ginger, limes, oranges, carrots
- **Layout**: Image left half, text right half
- **Juice name**: "Immunity Boost" in warm amber (#e6960a)
- **Ingredients**: Ginger · Lime · Orange · Carrot
- **Benefit**: "Punchy ginger-citrus kick. Natural immune support."
- **Footer**: "Fresh-pressed · No additives · No compromise"

### Slide 5 — Liver & Kidney (15s)

- **Visual**: AI-generated market stall image — beetroot, ginger, carrots, apples
- **Layout**: Image left half, text right half
- **Juice name**: "Liver & Kidney" in deep beetroot red (#ad1457)
- **Ingredients**: Beetroot · Ginger · Carrot · Apple
- **Benefit**: "Deep cleansing. Supports liver & kidney function naturally."
- **Footer**: "Fresh-pressed · No additives · No compromise"

### Slide 6 — Closing (15s)

- **Visual**: Real photo — fridge packed with all 4 juice colours (IMG_4172) or daughter pouring juice (IMG_4150), with dark gradient overlay
- **Text**: "Let food be thy medicine and medicine be thy food" + Vita Press wordmark
- **Accent**: None — uses default brand orange (#d4700a) for wordmark
- **Animation**: Fade in quote, then wordmark

### Loop → back to Slide 1

---

## 5. AI Image Generation

**4 images needed** — one per juice blend, showing that blend's ingredients in a market stall style.

### Prompt template:
> "Overhead photograph of fresh [ingredient 1], [ingredient 2], [ingredient 3], and [ingredient 4] arranged together on a rustic wooden market stall, natural daylight, abundant and colourful, warm tones, photorealistic, shallow depth of field"

### Specific prompts:

1. **Skin Boost**: "...fresh whole oranges, green limes, bright orange carrots, and green Granny Smith apples arranged together on a rustic wooden market stall..."
2. **Detox**: "...fresh celery stalks, green limes, whole cucumbers, and green Granny Smith apples arranged together on a rustic wooden market stall..."
3. **Immunity Boost**: "...fresh ginger root, green limes, whole oranges, and bright orange carrots arranged together on a rustic wooden market stall..."
4. **Liver & Kidney**: "...fresh whole beetroot (deep purple-red), ginger root, bright orange carrots, and green Granny Smith apples arranged together on a rustic wooden market stall..."

### Image specs:
- **Aspect ratio**: ~4:5 portrait (to fill left half of 16:9 slide)
- **Resolution**: At least 800x1000px
- **Tool**: ChatGPT image generation, Midjourney, or similar. Generate before building the slideshow.

---

## 6. Real Photos Used

| Photo | Usage | Slide |
|-------|-------|-------|
| IMG_4130 or IMG_4131 | Market stall — intro background | Slide 1 |
| IMG_4172 or IMG_4150 | Fridge shot or pouring shot — closing background | Slide 6 |

Photos will have a dark gradient overlay applied in CSS to ensure text readability.

---

## 7. Implementation Approach

1. **Generate AI images** (4 market stall images via ChatGPT or similar)
2. **Build HTML slideshow** — single self-contained HTML file with embedded CSS animations, crossfade transitions, 15-second auto-advance, infinite loop
3. **Embed images** — real photos and AI images as base64 or relative file references
4. **Test in browser** — open in Chrome fullscreen, verify timing and transitions
5. **Screen-record to MP4** — use OBS, browser extension, or built-in screen recorder to capture one full loop at 1080p
6. **Deliver MP4** — ready to play on laptop/tablet at the table

### File structure:
```
VitaPress/
  video/
    vita-press-slideshow.html    (the slideshow)
    images/                       (AI-generated + real photos)
      skin-boost-market.jpg
      detox-market.jpg
      immunity-boost-market.jpg
      liver-kidney-market.jpg
      market-stall-bg.jpg        (from IMG_4130/4131)
      closing-bg.jpg             (from IMG_4172/4150)
    vita-press-promo.mp4          (final exported video)
```

---

## 8. Fonts

Loaded from Google Fonts (embedded/inlined for offline use):
- **Instrument Serif** — juice names, wordmark, quote
- **DM Sans** — ingredients, benefits, footer

---

## 9. Timeline

- **Day 1**: Generate AI images, build HTML slideshow
- **Day 2**: Test, adjust timing/text, screen-record to MP4
- **Weekend**: Play on loop at the sales table
