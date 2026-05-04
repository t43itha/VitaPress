# Vita Press Marketing Video Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a looping HTML slideshow showcasing the 4 Vita Press juice blends, then export to MP4 for table-top playback.

**Architecture:** Single self-contained HTML file with CSS keyframe animations for slide transitions and auto-advance timing. Images referenced as relative paths. No JavaScript frameworks — pure HTML/CSS with minimal JS for the slideshow loop. Font CSS inlined for offline use.

**Tech Stack:** HTML, CSS (keyframes/animations), vanilla JS (slide timer), Google Fonts (Instrument Serif, DM Sans)

**Spec:** `docs/specs/2026-03-19-marketing-video-design.md`

---

## File Structure

```
VitaPress/
  video/
    vita-press-slideshow.html    — the slideshow (single file, all CSS/JS inline)
    images/
      market-stall-bg.jpg        — real photo for intro (copied from Images/IMG_4131.jpeg)
      closing-bg.jpg             — real photo for closing (copied from Images/IMG_4172.jpeg)
      skin-boost-market.jpg      — AI-generated (user creates externally)
      detox-market.jpg           — AI-generated (user creates externally)
      immunity-boost-market.jpg  — AI-generated (user creates externally)
      liver-kidney-market.jpg    — AI-generated (user creates externally)
```

---

## Chunk 1: Setup and Image Preparation

### Task 1: Create directory structure and copy real photos

**Files:**
- Create: `video/images/` directory
- Copy: `Images/IMG_4131.jpeg` → `video/images/market-stall-bg.jpg`
- Copy: `Images/IMG_4172.jpeg` → `video/images/closing-bg.jpg`

- [ ] **Step 1: Create the video directory structure**

```bash
mkdir -p video/images
```

- [ ] **Step 2: Copy real photos into the video images folder**

```bash
cp "Images/IMG_4131.jpeg" video/images/market-stall-bg.jpg
cp "Images/IMG_4172.jpeg" video/images/closing-bg.jpg
```

- [ ] **Step 3: Verify files exist**

```bash
ls -la video/images/
```

Expected: `market-stall-bg.jpg` and `closing-bg.jpg` present, both several hundred KB to a few MB.

- [ ] **Step 4: Commit**

```bash
git add video/images/market-stall-bg.jpg video/images/closing-bg.jpg
git commit -m "chore: add real photos for marketing slideshow intro/closing"
```

### Task 2: Generate AI market stall images (manual — user action)

**No code for this task.** The user generates 4 images using ChatGPT image generation or similar tool, then saves them into `video/images/`.

- [ ] **Step 1: Generate Skin Boost image**

Use this prompt in ChatGPT (or similar):
> "Overhead photograph of fresh whole oranges, green limes, bright orange carrots, and green Granny Smith apples arranged together on a rustic wooden market stall, natural daylight, abundant and colourful, warm tones, photorealistic, shallow depth of field"

Save as: `video/images/skin-boost-market.jpg`
Target: ~4:5 portrait, at least 800x1000px.

- [ ] **Step 2: Generate Detox image**

Prompt:
> "Overhead photograph of fresh celery stalks, green limes, whole cucumbers, and green Granny Smith apples arranged together on a rustic wooden market stall, natural daylight, abundant and colourful, warm tones, photorealistic, shallow depth of field"

Save as: `video/images/detox-market.jpg`

- [ ] **Step 3: Generate Immunity Boost image**

Prompt:
> "Overhead photograph of fresh ginger root, green limes, whole oranges, and bright orange carrots arranged together on a rustic wooden market stall, natural daylight, abundant and colourful, warm tones, photorealistic, shallow depth of field"

Save as: `video/images/immunity-boost-market.jpg`

- [ ] **Step 4: Generate Liver & Kidney image**

Prompt:
> "Overhead photograph of fresh whole beetroot with deep purple-red skin, ginger root, bright orange carrots, and green Granny Smith apples arranged together on a rustic wooden market stall, natural daylight, abundant and colourful, warm tones, photorealistic, shallow depth of field"

Save as: `video/images/liver-kidney-market.jpg`

- [ ] **Step 5: Verify all 6 images are in place**

```bash
ls -la video/images/
```

Expected: 6 files — `market-stall-bg.jpg`, `closing-bg.jpg`, `skin-boost-market.jpg`, `detox-market.jpg`, `immunity-boost-market.jpg`, `liver-kidney-market.jpg`.

- [ ] **Step 6: Commit AI images**

```bash
git add video/images/
git commit -m "chore: add AI-generated market stall images for juice slides"
```

---

## Chunk 2: Build the HTML Slideshow

### Task 3: Create the slideshow HTML file

**Files:**
- Create: `video/vita-press-slideshow.html`

This is a single self-contained HTML file. All CSS is inline. A small JS script handles slide advancing. Fonts are loaded from Google Fonts via `<link>` tags. **Important:** Open the HTML file once while connected to the internet before the event so fonts are cached. If the laptop/tablet will definitely have no internet, download the font files and inline them as a polish step in Task 4.

**Photo choices:** Using IMG_4131 (citrus market stall) for intro and IMG_4172 (fridge packed with bottles) for closing. Swap to IMG_4130 or IMG_4150 if preferred.

The slideshow has 6 slides:
1. **Intro** — market stall background photo, dark overlay, wordmark + tagline
2. **Skin Boost** — AI image left, text right, amber/orange accent
3. **Detox** — AI image left, text right, green accent
4. **Immunity Boost** — AI image left, text right, warm amber accent
5. **Liver & Kidney** — AI image left, text right, beetroot red accent
6. **Closing** — fridge photo background, dark overlay, quote + wordmark

Each slide shows for 15 seconds. Crossfade transition is 1.5 seconds. Loops infinitely.

- [ ] **Step 1: Create the slideshow HTML file**

Create `video/vita-press-slideshow.html` with this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Vita Press — Marketing Slideshow</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #1a1815;
      color: #fff;
      font-family: 'DM Sans', sans-serif;
      overflow: hidden;
      width: 1920px;
      height: 1080px;
    }

    /* --- Slideshow container --- */
    .slideshow {
      position: relative;
      width: 1920px;
      height: 1080px;
      overflow: hidden;
    }

    .slide {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      opacity: 0;
      transition: opacity 1.5s ease-in-out;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .slide.active {
      opacity: 1;
    }

    /* --- Intro & Closing slides (full-bleed photo + overlay) --- */
    .slide--photo {
      background-size: cover;
      background-position: center;
      flex-direction: column;
      gap: 24px;
    }

    .slide--photo::before {
      content: '';
      position: absolute;
      inset: 0;
      background: rgba(26, 24, 21, 0.75);
    }

    .slide--photo > * {
      position: relative;
      z-index: 1;
    }

    /* --- Juice slides (image left, text right) --- */
    .slide--juice {
      display: grid;
      grid-template-columns: 1fr 1fr;
      background: #1a1815;
    }

    .slide--juice .slide-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .slide--juice .slide-text {
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 80px 80px 80px 60px;
      gap: 28px;
    }

    /* --- Typography --- */
    .wordmark {
      font-family: 'Instrument Serif', serif;
      font-size: 96px;
      letter-spacing: -0.03em;
      line-height: 1;
      opacity: 0;
      animation: fadeUp 1.2s ease forwards;
    }

    .tagline {
      font-size: 28px;
      font-weight: 300;
      color: rgba(255, 255, 255, 0.7);
      letter-spacing: 0.02em;
      opacity: 0;
      animation: fadeUp 1.2s 0.6s ease forwards;
    }

    .juice-name {
      font-family: 'Instrument Serif', serif;
      font-size: 72px;
      letter-spacing: -0.02em;
      line-height: 1.05;
      opacity: 0;
      animation: fadeUp 0.8s 0.3s ease forwards;
    }

    .ingredients {
      font-size: 22px;
      font-weight: 400;
      color: rgba(255, 255, 255, 0.6);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      opacity: 0;
      animation: fadeUp 0.8s 0.6s ease forwards;
    }

    .benefit {
      font-size: 26px;
      font-weight: 300;
      line-height: 1.6;
      color: rgba(255, 255, 255, 0.85);
      max-width: 520px;
      opacity: 0;
      animation: fadeUp 0.8s 0.9s ease forwards;
    }

    .footer {
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.35);
      position: absolute;
      bottom: 40px;
      right: 60px;
      opacity: 0;
      animation: fadeUp 0.8s 1.2s ease forwards;
    }

    .quote {
      font-family: 'Instrument Serif', serif;
      font-style: italic;
      font-size: 44px;
      line-height: 1.4;
      max-width: 800px;
      text-align: center;
      opacity: 0;
      animation: fadeUp 1.2s ease forwards;
    }

    .closing-wordmark {
      font-family: 'Instrument Serif', serif;
      font-size: 48px;
      letter-spacing: -0.02em;
      color: #d4700a;
      opacity: 0;
      animation: fadeUp 1.2s 0.8s ease forwards;
    }

    /* --- Accent line on juice slides --- */
    .accent-line {
      width: 60px;
      height: 3px;
      border-radius: 2px;
      opacity: 0;
      animation: fadeUp 0.8s 0.15s ease forwards;
    }

    /* --- Animations --- */
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Reset animations when slide becomes active */
    .slide:not(.active) .wordmark,
    .slide:not(.active) .tagline,
    .slide:not(.active) .juice-name,
    .slide:not(.active) .ingredients,
    .slide:not(.active) .benefit,
    .slide:not(.active) .footer,
    .slide:not(.active) .quote,
    .slide:not(.active) .closing-wordmark,
    .slide:not(.active) .accent-line {
      animation: none;
      opacity: 0;
    }
  </style>
</head>
<body>

<div class="slideshow">

  <!-- Slide 1: Intro -->
  <div class="slide slide--photo active" style="background-image: url('images/market-stall-bg.jpg');">
    <div class="wordmark" style="color: #d4700a;">Vita Press</div>
    <div class="tagline">Fresh-pressed. No additives. No compromise.</div>
    <div class="footer">Fresh-pressed · No additives · No compromise</div>
  </div>

  <!-- Slide 2: Skin Boost -->
  <div class="slide slide--juice">
    <img class="slide-image" src="images/skin-boost-market.jpg" alt="Oranges, limes, carrots, and apples on a market stall" />
    <div class="slide-text">
      <div class="accent-line" style="background: #f5a623;"></div>
      <div class="juice-name" style="color: #f5a623;">Skin Boost</div>
      <div class="ingredients">Orange · Lime · Carrot · Apple</div>
      <div class="benefit">Beta-carotene rich. Supports healthy, glowing skin from the inside out.</div>
      <div class="footer">Fresh-pressed · No additives · No compromise</div>
    </div>
  </div>

  <!-- Slide 3: Detox -->
  <div class="slide slide--juice">
    <img class="slide-image" src="images/detox-market.jpg" alt="Celery, limes, cucumbers, and apples on a market stall" />
    <div class="slide-text">
      <div class="accent-line" style="background: #4caf50;"></div>
      <div class="juice-name" style="color: #4caf50;">Detox</div>
      <div class="ingredients">Celery · Lime · Cucumber · Apple</div>
      <div class="benefit">Clean & refreshing. Hydration and gentle cleansing.</div>
      <div class="footer">Fresh-pressed · No additives · No compromise</div>
    </div>
  </div>

  <!-- Slide 4: Immunity Boost -->
  <div class="slide slide--juice">
    <img class="slide-image" src="images/immunity-boost-market.jpg" alt="Ginger, limes, oranges, and carrots on a market stall" />
    <div class="slide-text">
      <div class="accent-line" style="background: #e6960a;"></div>
      <div class="juice-name" style="color: #e6960a;">Immunity Boost</div>
      <div class="ingredients">Ginger · Lime · Orange · Carrot</div>
      <div class="benefit">Punchy ginger-citrus kick. Natural immune support.</div>
      <div class="footer">Fresh-pressed · No additives · No compromise</div>
    </div>
  </div>

  <!-- Slide 5: Liver & Kidney -->
  <div class="slide slide--juice">
    <img class="slide-image" src="images/liver-kidney-market.jpg" alt="Beetroot, ginger, carrots, and apples on a market stall" />
    <div class="slide-text">
      <div class="accent-line" style="background: #ad1457;"></div>
      <div class="juice-name" style="color: #ad1457;">Liver & Kidney</div>
      <div class="ingredients">Beetroot · Ginger · Carrot · Apple</div>
      <div class="benefit">Deep cleansing. Supports liver & kidney function naturally.</div>
      <div class="footer">Fresh-pressed · No additives · No compromise</div>
    </div>
  </div>

  <!-- Slide 6: Closing -->
  <div class="slide slide--photo" style="background-image: url('images/closing-bg.jpg');">
    <div class="quote">"Let food be thy medicine<br>and medicine be thy food"</div>
    <div class="closing-wordmark">Vita Press</div>
    <div class="footer">Fresh-pressed · No additives · No compromise</div>
  </div>

</div>

<script>
  const slides = document.querySelectorAll('.slide');
  const SLIDE_DURATION = 15000; // 15 seconds
  let current = 0;

  function nextSlide() {
    slides[current].classList.remove('active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('active');
  }

  setInterval(nextSlide, SLIDE_DURATION);
</script>

</body>
</html>
```

- [ ] **Step 2: Open in Chrome and verify**

```bash
# On Windows, open the file in Chrome
start chrome "C:/Users/tabit/_Projects/VitaPress/video/vita-press-slideshow.html"
```

Press F11 for fullscreen. Verify:
- Slide 1 shows market stall background with "Vita Press" wordmark and tagline
- Slides 2-5 show image left, text right with correct juice names, colours, ingredients, and benefits
- Slide 6 shows closing photo with quote and wordmark
- Each slide holds for 15 seconds
- Crossfade transitions are smooth (1.5s)
- Text animations (fade up) restart on each slide
- After slide 6, loops back to slide 1

**Note:** AI-generated images must be in `video/images/` for slides 2-5 to display. If not yet generated, those slides will show a broken image — that's expected until Task 2 is complete.

- [ ] **Step 3: Commit the slideshow**

```bash
git add video/vita-press-slideshow.html
git commit -m "feat: add marketing slideshow HTML for weekend sales"
```

---

## Chunk 3: Test, Polish, and Export

### Task 4: Test and polish the slideshow

- [ ] **Step 1: Open slideshow in Chrome fullscreen and watch one full loop**

Watch all 6 slides cycle through. Check:
- Text is readable at arm's length (simulating someone at a table)
- Image/text split looks balanced on juice slides
- Colours and fonts match the Vita Press brand
- No visual glitches on transitions

- [ ] **Step 2: Adjust any timing, text, or colours as needed**

If any text needs tweaking (e.g., benefit copy, font sizes), edit `video/vita-press-slideshow.html` directly. The spec values:
- Juice name: 72px Instrument Serif
- Ingredients: 22px DM Sans uppercase
- Benefit: 26px DM Sans light
- Footer: 14px DM Sans uppercase

- [ ] **Step 3: Commit any adjustments**

```bash
git add video/vita-press-slideshow.html
git commit -m "fix: polish slideshow text and timing"
```

### Task 5: Export to MP4

This is a manual step. The user screen-records the slideshow playing in Chrome fullscreen.

- [ ] **Step 1: Set up screen recording**

Options (pick one):
- **OBS Studio** (free): Set canvas to 1920x1080, record the Chrome window in fullscreen, output H.264 MP4
- **Windows Game Bar** (built-in): Press Win+G, then record — simpler but less control
- **Chrome extension**: "Screen Recorder" or similar

- [ ] **Step 2: Record one full loop**

1. Open `video/vita-press-slideshow.html` in Chrome
2. Press F11 for fullscreen
3. Start recording
4. Wait for all 6 slides to play through (~90 seconds)
5. Stop recording after it loops back to slide 1

- [ ] **Step 3: Save the recording**

Save as: `video/vita-press-promo.mp4`
Target: H.264, 1080p, 30fps, under 50MB.

- [ ] **Step 4: Test playback**

Open `video/vita-press-promo.mp4` in Windows Media Player or VLC. Verify:
- Plays smoothly
- Colours and text are crisp
- Set player to loop mode — confirm it loops cleanly

- [ ] **Step 5: Commit the final video**

**Note:** The MP4 may be large (up to 50MB). For this small project that's fine. If the repo grows, consider adding `video/*.mp4` to `.gitignore` and storing videos separately.

```bash
git add video/vita-press-promo.mp4
git commit -m "feat: add exported MP4 marketing video for weekend sales"
```

---

## Summary

| Task | Description | Who | Time |
|------|------------|-----|------|
| 1 | Create dirs, copy real photos | Agent | 2 min |
| 2 | Generate 4 AI market stall images | User (manual) | 15-20 min |
| 3 | Build HTML slideshow | Agent | 5 min |
| 4 | Test and polish | User + Agent | 10 min |
| 5 | Screen-record to MP4 | User (manual) | 5 min |

**Total: ~40 minutes** (plus AI image generation time)
