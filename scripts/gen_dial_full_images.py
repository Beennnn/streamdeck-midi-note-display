from PIL import Image, ImageDraw, ImageFont
FONT="/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONTB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
BG="#15171c"; WHITE="#eef0f3"; BLACK="#22252b"; HL="#3b82f6"; TXT="#f4f5f7"; ACC="#5b9dff"; BORD="#3a3f49"
NOTES=["C","C♯","D","D♯","E","F","F♯","G","G♯","A","A♯","B"]
WHITE_IDX=[0,2,4,5,7,9,11]; BLACK_BETWEEN={1:0,3:1,6:3,8:4,10:5}
def font(sz, bold=True):
    try: return ImageFont.truetype(FONTB if bold else FONT, sz)
    except: return ImageFont.truetype(FONT, sz)
def render(value, W=400, H=200):
    n=value%12; octv=value//12-1
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    # --- big note letter, left, top zone ---
    fL=font(96)
    letter=NOTES[n]
    lb=d.textbbox((0,0),letter,font=fL)
    d.text((10-lb[0], 2-lb[1]), letter, font=fL, fill=TXT)
    # --- octave, big, RIGHT-ALIGNED (flush right) ---
    fO=font(84)
    ot=str(octv)
    ob=d.textbbox((0,0),ot,font=fO)
    d.text((W-8-(ob[2]-ob[0])-ob[0], 8-ob[1]), ot, font=fO, fill=ACC)
    # --- keyboard, full width, bottom, bigger ---
    kx0,kx1=6,W-6; ky0,ky1=104,H-6; nW=7; ww=(kx1-kx0)/nW
    hlW=n in WHITE_IDX; hlpos=WHITE_IDX.index(n) if hlW else None
    for i in range(nW):
        x=kx0+i*ww
        d.rectangle([x,ky0,x+ww-2,ky1],fill=HL if (hlW and i==hlpos) else WHITE,outline=BORD,width=2)
    bw=ww*0.62; bh=(ky1-ky0)*0.62
    for ni,lp in BLACK_BETWEEN.items():
        cx=kx0+(lp+1)*ww; x0=cx-bw/2
        d.rectangle([x0,ky0,x0+bw,ky0+bh],fill=HL if (not hlW and ni==n) else BLACK,outline=BORD,width=2)
    return img
if __name__=="__main__":
    for v in (61,60,47,0):
        render(v).save(f"dial_big_{v}.png")
    print("samples: 61(C♯4) 60(C4) 47(B3) 0(C-1)")
