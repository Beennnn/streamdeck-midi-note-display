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

# --- Geometry mirrors the custom layout ts_note_split.json (200x100 canvas) ---
# note_letter: right-aligned to a fixed seam so the letter grows leftward;
# note_octave: left-aligned from that same seam so the octave never moves;
# keyboard:    pinned on the right. Result: the letter + octave read as one
# "G#3" unit on the left, next to the piano. The seam is at x=90/200.
SEAM = 89/200          # fraction of width where letter ends and octave begins
                       # (matches layouts/ts_note_split.json: letter rect ends x=88,
                       #  octave rect starts x=90, keyboard pinned at x=122)

def dial(value, W=1200, H=600, pad=28):
    n=value%12; octv=value//12-1
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    d.rounded_rectangle([pad,pad,W-pad,H-pad], radius=40, fill=SCREEN, outline=BORD, width=4)
    seam=int(W*SEAM); base=int(H*0.68)   # shared baseline for letter + octave
    # note letter: BIG, right-aligned, ends at the seam (grows leftward to fill the
    # whole space left of the piano)
    fL=f(345); lt=NOTES[n]
    d.text((seam, base), lt, font=fL, fill=LETTER, anchor="rs")
    # octave: left-aligned, starts right after the seam so it reads as one "F♯1" unit
    fO=f(250); ot=str(octv)
    d.text((seam+10, base), ot, font=fO, fill=OCTAVE, anchor="ls")
    # keyboard: pinned on the right (x 122->196 of 200, y 18->82 of 100)
    draw_keyboard(d, int(W*122/200), int(H*0.18), int(W*196/200), int(H*0.82), n)
    return img

def layout(W=1200, H=800):
    img=dial(56, W, 600); big=Image.new("RGB",(W,H),BG); big.paste(img,(0,0))  # 56 = G#3
    d=ImageDraw.Draw(big); fa=f(30, bold=False)
    # leader lines to the three elements (letter, octave, keyboard)
    for start,tip in [((150,640),(430,340)),((150,685),(600,340)),((150,730),(880,300))]:
        d.line([start,tip], fill=MUTE, width=2)
        d.ellipse([tip[0]-6,tip[1]-6,tip[0]+6,tip[1]+6], fill=MUTE)
    rows=[("{@note_letter}", "= note letter, right-aligned (formula on value % 12)", LETTER),
          ("{@note_octave}", "= octave, left-aligned at a fixed x (INT(value/12)-1)", OCTAVE),
          ("{@keyboard}",    "= one piano image per note, pinned right",            LIT)]
    for i,(a,b,col) in enumerate(rows):
        y=628+i*45
        d.text((165,y), a, font=f(30), fill=col)
        d.text((470,y), b, font=fa, fill=WHITE)
    return big

if __name__=="__main__":
    out=os.path.join(os.path.dirname(__file__),"..","images","vision"); os.makedirs(out,exist_ok=True)
    dial(56).save(os.path.join(out,"dial-Gsharp3.png"))   # G#3 (value 56) - the example
    dial(61).save(os.path.join(out,"dial-Csharp4.png"))   # C#4
    dial(60).save(os.path.join(out,"dial-C4.png"))
    dial(93).save(os.path.join(out,"dial-Fsharp6.png"))   # A6 example (wide/tall check)
    layout().save(os.path.join(out,"layout.png"))
    print("wrote vision images ->", out)
