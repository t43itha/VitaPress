from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

ROOT = Path('/private/tmp/VitaPress-main')
OUT = ROOT / 'tiktok/2026-05-16/day-9-batch-reality'
OUT.mkdir(parents=True, exist_ok=True)
W,H = 1080,1920
BG = (9, 17, 18)
CREAM = (244, 235, 216)
MUTED = (190, 173, 145)
GREEN = (123, 157, 116)
ORANGE = (219, 132, 63)
RED = (145, 55, 59)

def font(size, serif=False):
    paths = [
        '/System/Library/Fonts/Supplemental/Georgia.ttf' if serif else '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()

SERIF_BIG = font(86, True)
SERIF_MED = font(62, True)
SANS_BIG = font(64)
SANS_MED = font(50)
SANS_SMALL = font(40)
SANS_TINY = font(30)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines=[]; line=''
    for w in words:
        test = (line+' '+w).strip()
        if draw.textbbox((0,0), test, font=fnt)[2] <= max_w:
            line=test
        else:
            if line: lines.append(line)
            line=w
    if line: lines.append(line)
    return lines

def draw_wrapped(draw, text, xy, fnt, fill, max_w, line_gap=10, anchor=None):
    x,y = xy
    lines = wrap(draw,text,fnt,max_w)
    for ln in lines:
        bbox=draw.textbbox((0,0),ln,font=fnt)
        tx=x
        if anchor=='center': tx=x-(bbox[2]-bbox[0])//2
        draw.text((tx,y),ln,font=fnt,fill=fill)
        y += (bbox[3]-bbox[1]) + line_gap
    return y

def gradient():
    img=Image.new('RGB',(W,H),BG)
    px=img.load()
    for y in range(H):
        for x in range(W):
            t=y/H
            r=int(9+18*t); g=int(17+12*t); b=int(18+8*t)
            px[x,y]=(r,g,b)
    return img

def add_noise(img, alpha=20):
    import random
    noise=Image.new('RGBA',(W,H),(0,0,0,0))
    p=noise.load()
    for _ in range(22000):
        x=random.randrange(W); y=random.randrange(H)
        val=random.randrange(255)
        p[x,y]=(val,val,val,random.randrange(alpha))
    return Image.alpha_composite(img.convert('RGBA'),noise)

def add_brand(draw):
    draw.text((70,70),'VITA PRESS',font=SANS_TINY,fill=MUTED)
    draw.line((70,115,1010,115),fill=(52,67,62),width=2)

def bottle_strip(img):
    xs=[165,375,585,795]
    files=['docs/assets/bottle-kl.png','docs/assets/bottle-sb.png','docs/assets/bottle-ib.png','docs/assets/bottle-dx.png']
    for x,f in zip(xs,files):
        b=Image.open(ROOT/f).convert('RGBA')
        bb=b.getbbox()
        if bb: b=b.crop(bb)
        b.thumbnail((170,410),Image.LANCZOS)
        shadow=Image.new('RGBA',b.size,(0,0,0,0))
        sd=ImageDraw.Draw(shadow); sd.ellipse((15,b.height-28,b.width-15,b.height-2),fill=(0,0,0,85))
        img.alpha_composite(shadow,(x-b.width//2,1345))
        img.alpha_composite(b,(x-b.width//2,980))

def make_slide(n, title, body, footer=None, accent=GREEN, bottles=False, photo=None, chips=None):
    img=add_noise(gradient())
    d=ImageDraw.Draw(img)
    add_brand(d)
    d.rounded_rectangle((62,150,1018,1770),radius=48,outline=(56,68,61),width=3,fill=(13,25,25,210))
    d.rectangle((62,150,78,1770),fill=accent)
    y=245
    y=draw_wrapped(d,title,(110,y),SERIF_BIG,CREAM,860,16)
    y+=55
    if photo:
        ph=Image.open(ROOT/photo).convert('RGB')
        ph.thumbnail((860,620),Image.LANCZOS)
        canvas=Image.new('RGB',(860,620),(20,25,24))
        canvas.paste(ph,((860-ph.width)//2,(620-ph.height)//2))
        canvas=canvas.filter(ImageFilter.UnsharpMask(radius=1,percent=110))
        img.alpha_composite(canvas.convert('RGBA'),(110,y))
        y+=670
    if chips:
        cx=110; cy=y
        for label,col in chips:
            tw=d.textbbox((0,0),label,font=SANS_SMALL)[2]
            d.rounded_rectangle((cx,cy,cx+tw+48,cy+60),radius=30,fill=col)
            d.text((cx+24,cy+16),label,font=SANS_SMALL,fill=(255,248,232))
            cx += tw+70
            if cx>780: cx=110; cy+=82
        y=cy+92
    y=draw_wrapped(d,body,(110,y),SANS_BIG if len(body)<90 else SANS_MED,CREAM,860,14)
    if bottles:
        bottle_strip(img)
    if footer:
        d.rounded_rectangle((110,1515,970,1635),radius=32,fill=(244,235,216,24),outline=(91,104,92),width=2)
        draw_wrapped(d,footer,(150,1545),SANS_SMALL,MUTED,780,8)
    img.convert('RGB').save(OUT/f'{int(n):02d}.png',quality=95)

slides = [
    ('01','POV: you are planning a tiny juice batch with 4 followers','No fake wellness claims. Just bottles, ingredients, price, and whether London actually wants it.', 'Tomorrow’s test: make the small-business reality more specific.', RED, True, None, None),
    ('02','The honest problem','People are seeing the videos… but not enough people are commenting yet. So the next post has to ask for a decision, not applause.', 'Under 500 views + zero shares = keep testing formats.', ORANGE, False, None, None),
    ('03','What should be filmed next?','Comment a letter and your area. The next proof video gets built around the vote.', 'Comment A/B/C/D + area if you want local London delivery.', GREEN, False, None, [('A batch prep',(115,76,67)),('B taste test',(97,123,85)),('C receipts',(155,91,45)),('D packing',(69,104,112))]),
    ('04','The price is still £3.50','That is the debate. Not “will juice change your life?” Just: would you choose a fresh local bottle over a supermarket juice drink?', '3 for £10 stays the only bundle.', ORANGE, True, None, None),
    ('05','This is the next proof format','Prep table. Bottle. Ingredients. Then let comments choose what to make more of.', 'No cures. No detox promises. Food ingredients only.', GREEN, False, 'Images/IMG_4172.jpeg', None),
    ('06','London, pick the next video','If 10 people comment a letter + area, the next batch-day post gets made around that vote.', 'Link in bio for pre-orders: t43itha.github.io/VitaPress', RED, True, None, None),
]
for s in slides:
    make_slide(*s)

# contact sheet
thumbs=[]
for i in range(1,7):
    im=Image.open(OUT/f'{i:02d}.png').resize((180,320))
    thumbs.append(im)
sheet=Image.new('RGB',(540,640),(12,18,18))
for idx,im in enumerate(thumbs):
    sheet.paste(im,((idx%3)*180,(idx//3)*320))
sheet.save(OUT/'contact-sheet.jpg',quality=90)

# make silent mp4, 2.1s/slide
listfile=OUT/'ffmpeg-list.txt'
listfile.write_text(''.join([f"file '{OUT}/{i:02d}.png'\nduration 2.1\n" for i in range(1,7)]) + f"file '{OUT}/06.png'\n")
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(listfile),'-vf','format=yuv420p,scale=1080:1920','-r','30',str(OUT/'vita-press-day9-batch-reality.mp4')],check=True)

posting = '''# Vita Press TikTok — Day 9 batch reality / vote pack

## Decision

Snapshot on 2026-05-15 17:28 shows 7 videos, 4 followers, no new pre-order signals, and every post still below 500 views with 0 shares. The newer raw-proof posts are too young to kill, but today's cadence is already at 3 posts, so this run should not public-post again. The concrete move is to queue tomorrow's proof/poll asset: batch-reality + audience vote.

## Asset

- `vita-press-day9-batch-reality.mp4` — 1080×1920 silent slideshow/video, ~13s.
- Source slides: `01.png`–`06.png`.
- `contact-sheet.jpg` — QA preview.

## On-video copy

1. POV: you are planning a tiny juice batch with 4 followers
2. The honest problem: views are coming in, comments are not
3. What should be filmed next? A batch prep / B taste tests / C receipts / D packing orders
4. The price is still £3.50 — would you choose fresh local juice over a supermarket juice drink?
5. Next proof format: prep table, bottle, comments choose the next batch
6. London, pick the next video — comment letter + area

## Caption

TikTok humbled this tiny juice launch, so tomorrow's content is getting built by comments instead of fake wellness hooks.

Pick the next proof video:
A = batch prep chaos
B = taste test reactions
C = ingredient shop receipt
D = packing Sunday orders

Comment A/B/C/D + your area if you want Sunday pickup or local London delivery. Link in bio to pre-order.

#coldpressedjuice #londonsmallbusiness #smallbusinessuk #londonfood #juicetok #vitapress

## Optional pinned comment

No medical claims here — just cold-pressed juice, transparent pricing, and a tiny London batch trying to prove demand. Vote A/B/C/D.
'''
(OUT/'POSTING.md').write_text(posting)
print(OUT)
