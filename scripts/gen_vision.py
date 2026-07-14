#!/usr/bin/env python3
"""High-resolution 'vision' mockups of the dial display (the low-res on-device
capture is not enough). Produces clean dial renders + an annotated layout.
Output: images/vision/"""
import os
from PIL import Image, ImageDraw, ImageFont

FONT   = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONTB  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
BG="#15171c"; SCREEN="#0f1115"; WHITE="#eef0f3"; BLACK="#22252b"; BORD="#3a3f49"
LETTER="#ff5a5a"      # note letter (matches the on-device red)
OCTAVE="#33d17a"      # octave (matches the on-device green)
LIT="#3b82f6"         # highlighted key
MUTE="#8a93a3"

NOTES=["C","C♯","D","D♯","E","F","F♯","G","G♯","A","A♯","B"]
WHITE_IDX=[0,2,4,5,7,9,11]; BLACK_BETWEEN={1:0,3:1,6:3,8:4,10:5}

def f(sz, bold=True):
    try: return ImageFont.truetype(FONTB if bold else FONT, sz)
    except: return ImageFont.truetype(FONT, sz)

def draw_keyboard(d, x0, y0, x1, y1, n):
    nW=7; ww=(x1-x0)/nW
    hlW=n in WHITE_IDX; hp=WHITE_IDX.index(n) if hlW else None
    for i in range(nW):
        x=x0+i*ww
        d.rounded_rectangle([x,y0,x+ww-4,y1], radius=4,
            fill=LIT if (hlW and i==hp) else WHITE, outline=BORD, width=3)
    bw=ww*0.62; bh=(y1-y0)*0.62
    for ni,lp in BLACK_BETWEEN.items():
        cx=x0+(lp+1)*ww; bx=cx-bw/2
        d.rounded_rectangle([bx,y0,bx+bw,y0+bh], radius=3,
            fill=LIT if (not hlW and ni==n) else BLACK, outline=BORD, width=3)

def dial(value, W=1200, H=600, pad=28):
    n=value%12; octv=value//12-1
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.rounded_rectangle([pad,pad,W-pad,H-pad], radius=40, fill=SCREEN, outline=BORD, width=4)
    # note letter (left)
    fL=f(300); lt=NOTES[n]; lb=d.textbbox((0,0),lt,font=fL)
    d.text((90, 60-lb[1]), lt, font=fL, fill=LETTER)
    # octave (right, flush)
    fO=f(230); ot=str(octv); ob=d.textbbox((0,0),ot,font=fO)
    d.text((W-100-(ob[2]-ob[0]), 90-ob[1]), ot, font=fO, fill=OCTAVE)
    # keyboard (bottom)
    draw_keyboard(d, 90, 360, W-90, H-70, n)
    return img

def layout(W=1200, H=780):
    img=dial(61, W, 600); big=Image.new("RGB",(W,H),BG); big.paste(img,(0,0))
    d=ImageDraw.Draw(big); fa=f(30, bold=False)
    # leader lines to the three elements
    for start,tip in [((150,630),(230,150)),((150,675),(1010,170)),((150,720),(600,470))]:
        d.line([start,tip], fill=MUTE, width=2)
        d.ellipse([tip[0]-6,tip[1]-6,tip[0]+6,tip[1]+6], fill=MUTE)
    rows=[("{title}",  "= note letter   (formula on value % 12)", LETTER),
          ("{text}",   "= octave        (INT(value/12)-1)",       OCTAVE),
          ("{iconright}","= one piano image per note",            LIT)]
    for i,(a,b,col) in enumerate(rows):
        y=618+i*45
        d.text((165,y), a, font=f(30), fill=col)
        d.text((360,y), b, font=fa, fill=WHITE)
    return big

if __name__=="__main__":
    out=os.path.join(os.path.dirname(__file__),"..","images","vision"); os.makedirs(out,exist_ok=True)
    dial(61).save(os.path.join(out,"dial-Csharp4.png"))   # C#4
    dial(93).save(os.path.join(out,"dial-Fsharp6.png"))   # F#6-ish (93 = A6? -> just an example)
    dial(60).save(os.path.join(out,"dial-C4.png"))
    layout().save(os.path.join(out,"layout.png"))
    print("wrote vision images ->", out)
