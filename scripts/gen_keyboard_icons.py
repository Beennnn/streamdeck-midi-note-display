#!/usr/bin/env python3
"""12 one-octave piano keyboard icons, one per note (pitch class), each
highlighting that note's key. Output: images/keyboard-icons/kbd_0..11.png
Used on the Stream Deck+ dial via {iconright:.../kbd_#value%12#.png}."""
import os
from PIL import Image, ImageDraw
WHITE="#eef0f3"; BLACK="#22252b"; HL="#3b82f6"; BORD="#3a3f49"
WHITE_IDX=[0,2,4,5,7,9,11]
BLACK_BETWEEN={1:0,3:1,6:3,8:4,10:5}   # note idx -> left white position
def render(n, W=150, H=96):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
    nW=7; ww=W/nW
    hlW = n in WHITE_IDX; hlpos=WHITE_IDX.index(n) if hlW else None
    for i in range(nW):
        x=i*ww
        d.rectangle([x,0,x+ww-1,H-1], fill=HL if (hlW and i==hlpos) else WHITE, outline=BORD, width=1)
    bw=ww*0.62; bh=H*0.60
    for note_idx,leftpos in BLACK_BETWEEN.items():
        x0=(leftpos+1)*ww - bw/2
        d.rectangle([x0,0,x0+bw,bh], fill=HL if (not hlW and note_idx==n) else BLACK, outline=BORD, width=1)
    return img
if __name__=="__main__":
    out=os.path.join(os.path.dirname(__file__),"..","images","keyboard-icons")
    os.makedirs(out,exist_ok=True)
    for n in range(12): render(n).save(os.path.join(out,f"kbd_{n}.png"))
    print("wrote 12 keyboard icons ->", out)
