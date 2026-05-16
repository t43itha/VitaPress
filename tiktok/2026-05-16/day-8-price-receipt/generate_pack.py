from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import subprocess, os, math

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
W,H = 1080,1920
BG = (12,19,22)
CREAM = (244,235,218)
MUTED = (180,169,149)
GREEN = (117,151,112)
ORANGE = (220,129,68)

font_paths = [
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]
bold_paths = [
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
]
FONT = next((p for p in font_paths if Path(p).exists()), None)
BOLD = next((p for p in bold_paths if Path(p).exists()), FONT)

def f(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def wrap(draw, text, font, max_width):
    words = text.split()
    lines=[]; line=''
    for word in words:
        trial = (line+' '+word).strip()
        if draw.textbbox((0,0), trial, font=font)[2] <= max_width:
            line = trial
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def draw_text_block(draw, xy, text, font, fill, max_width, leading=1.1, align='left'):
    x,y = xy
    lines = wrap(draw, text, font, max_width)
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font)
        xx = x if align=='left' else x + (max_width-(bbox[2]-bbox[0]))/2
        draw.text((xx,y), line, font=font, fill=fill)
        y += int(font.size*leading)
    return y

def paste_bottle(img, path, x, y, target_h):
    b = Image.open(path).convert('RGBA')
    bbox = b.getbbox()
    if bbox: b = b.crop(bbox)
    scale = target_h / b.height
    b = b.resize((int(b.width*scale), target_h), Image.LANCZOS)
    img.alpha_composite(b, (int(x-b.width/2), int(y)))

bottles = [
    ROOT/'docs/assets/bottle-sb.png', ROOT/'docs/assets/bottle-ib.png',
    ROOT/'docs/assets/bottle-kl.png', ROOT/'docs/assets/bottle-dx.png'
]
slides = [
    ('The polished wellness angle is dead.', 'So here is the real question for London:', 'Would you buy fresh juice if the batch was tiny?'),
    ('£3.50 each. 3 for £10.', 'Not a cure. No cleanse claims. Just cold-pressed juice made in small batches.', 'The trust has to come from proof.'),
    ('Tiny-batch problem:', 'Make 24 bottles and people miss out. Make 48 and fresh stock can expire.', 'So the next batch should follow demand, not ego.'),
    ('Pick the flavour to make more of:', 'A Orange · B Ginger Orange · C Beetroot · D Green', 'Comment your letter and London area.'),
    ("If 10 people in London comment, I'll prep around that vote.", 'Sunday pickup or local London delivery. Link in bio.', 'Vita Press')
]
frames=[]
for i,(h1,h2,h3) in enumerate(slides,1):
    img = Image.new('RGBA',(W,H),BG+(255,))
    draw = ImageDraw.Draw(img)
    # soft blobs
    for cx,cy,r,c in [(120,250,420,(51,80,67,90)),(950,1480,520,(96,62,43,80)),(620,980,500,(35,48,53,70))]:
        layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
        d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=c)
        img=Image.alpha_composite(img, layer.filter(ImageFilter.GaussianBlur(60)))
    draw=ImageDraw.Draw(img)
    # wordmark top
    draw.text((70,70),'VITA PRESS',font=f(36,True),fill=CREAM)
    draw.line((70,130,1010,130),fill=(244,235,218,80),width=2)
    y=230
    y=draw_text_block(draw,(70,y),h1,f(76,True),CREAM,940,1.05)
    y+=38
    y=draw_text_block(draw,(70,y),h2,f(44,False),CREAM,900,1.18)
    if i in (2,4):
        # bottle strip
        xs=[240,440,640,840]
        for x,b in zip(xs,bottles):
            paste_bottle(img,b,x,1000,430)
    elif i==3:
        # big problem card
        draw.rounded_rectangle((100,900,980,1260),radius=42,fill=(244,235,218,22),outline=(244,235,218,90),width=3)
        draw.text((155,965),'24 bottles?',font=f(58,True),fill=GREEN)
        draw.text((155,1055),'36 bottles?',font=f(58,True),fill=CREAM)
        draw.text((155,1145),'48 bottles?',font=f(58,True),fill=ORANGE)
    else:
        for x,b in zip([350,560,770],bottles[:3]):
            paste_bottle(img,b,x,950,470)
    draw_text_block(draw,(70,1510),h3,f(42,True if i==5 else False),MUTED if i!=5 else CREAM,940,1.18)
    draw.text((70,1818),'£3.50 each · 3 for £10 · London launch batch',font=f(28,False),fill=(244,235,218,170))
    fn=OUT/f'{i:02d}.png'; img.convert('RGB').save(fn,quality=95)
    frames.append(fn)

# Render simple video: 1.8s per slide, no audio
listfile=OUT/'frames.txt'
with listfile.open('w') as fp:
    for fr in frames:
        fp.write(f"file '{fr}'\n")
        fp.write('duration 1.8\n')
    fp.write(f"file '{frames[-1]}'\n")
cmd=['ffmpeg','-y','-f','concat','-safe','0','-i',str(listfile),'-vf','fps=30,format=yuv420p','-c:v','libx264','-movflags','+faststart',str(OUT/'vita-press-day8-price-receipt.mp4')]
subprocess.run(cmd,check=True)
print(OUT/'vita-press-day8-price-receipt.mp4')
