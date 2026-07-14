#!/usr/bin/env python3
"""Generate a Trevliga Spel MIDI-plugin translation file mapping every MIDI
value 0-127 to its note name (C4 = middle C = 60). Output: translation-files/.
NOTE: display uses the real sharp glyph U+266F, not ASCII '#'."""
import os
S="♯"  # MUSIC SHARP SIGN
NOTES=["C","C"+S,"D","D"+S,"E","F","F"+S,"G","G"+S,"A","A"+S,"B"]
def name(v,c4=True): return NOTES[v%12]+str(v//12-(1 if c4 else 2))
def build(c4=True):
    L=['<?xml version="1.0" encoding="utf-8" ?>','<MidiSteps version="1.1">',
       '  <Default send="yes" receive="yes" display="" image="" displayonsend="yes" useclosestvalueonreceive="yes"/>',
       '  <StepValues>']
    L+= [f'    <Step value="{v}" display="{name(v,c4)}"/>' for v in range(128)]
    L+=['  </StepValues>','</MidiSteps>']
    return "\n".join(L)+"\n"
if __name__=="__main__":
    out=os.path.join(os.path.dirname(__file__),"..","translation-files")
    os.makedirs(out,exist_ok=True)
    open(os.path.join(out,"note-names-C4-60.xml"),"w",encoding="utf-8").write(build(True))
    open(os.path.join(out,"note-names-C3-60.xml"),"w",encoding="utf-8").write(build(False))
    print("wrote note-name translation files ->", out)
