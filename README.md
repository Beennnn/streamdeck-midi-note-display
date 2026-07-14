# Stream Deck+ — MIDI value as a note name (+ piano)

Show a raw **MIDI value** (0–127) as a **note name** — and optionally a little
**one-octave piano** with the current key lit — on a **Stream Deck +** dial (or
key), using the [Trevliga Spel MIDI plugin](https://trevligaspel.se/streamdeck/midi/).

My use case: a **keyboard split point** sent as `CC 103 / channel 2`. On stage
"split at 60" means nothing; **"C4"** (with the key lit on a mini-keyboard) reads
instantly.

![Note name + piano on the dial](images/vision/dial-Csharp4.png)

*Clean render of the dial display — split point at C♯4. (Actual on-device screen is
tiny/low-res; these are high-res mockups. See `images/vision/`.)*

**How the display is built** — three fields, all driven from the raw MIDI value:

![Layout](images/vision/layout.png)

---

## Two ways to do it

### A. Note name from a formula — on a Scripted Dial *(what I use)*

A dial can be turned +/- to adjust the split, so the control lives on a dial.
A `Scripted Dial` computes the note name straight from the value — no lookup file:

- **letter** from `value % 12` → shown in `{title}`
- **octave** from `INT(value / 12) - 1` → shown in `{text}`  (C4 = middle C = 60)
- **piano** via `{iconright:.../kbd_#value%12#.png}` — one small image per note

Full script: [`midiscript/split_note_dial.midiscript`](midiscript/split_note_dial.midiscript).
The note-letter formula (the interesting bit):

```
IF(v%12=0,"C",IF(v%12=1,"C♯",IF(v%12=2,"D",IF(v%12=3,"D♯",IF(v%12=4,"E",
IF(v%12=5,"F",IF(v%12=6,"F♯",IF(v%12=7,"G",IF(v%12=8,"G♯",IF(v%12=9,"A",
IF(v%12=10,"A♯","B"))))))))))
```
`v` = `@e_ccvalue` on receive, `@e_value` on rotate.

### B. Note name from a translation file — on a Cycle key

The plugin author (Gunnar) suggested a **translation file**: an XML mapping every
value 0–127 to a display string (and/or image). That works on a **Cycle key**
(the whole key face is the image). Generated here:
[`translation-files/note-names-C4-60.xml`](translation-files/note-names-C4-60.xml)
(plus a `C3=60` variant).

---

## One image per note

For the piano I render **12 small images**, one per note of the octave —
`kbd_0.png` = C lit, `kbd_1.png` = C♯ … `kbd_11.png` = B. The script picks the
right one with `value % 12` in the path, so the lit key follows the split point.
See [`images/keyboard-icons/`](images/keyboard-icons/).

---

## Gotchas learned the hard way

- **Sharp must be `♯` (U+266F), NOT ASCII `#`.** A literal `#` inside a note name
  terminates the surrounding `#…#` expression and breaks the MidiScript parser.
  Use the real MUSIC SHARP SIGN glyph.
- **Tabs are not honoured** by the dial screen — `\t` won't align anything.
- **Keep letter and octave in separate fields** (`{title}` + `{text}`). Then the
  width of the sharp never shifts the octave — it stays put as you turn.
- **A dial cannot show a big, per-value full-screen image.** Per value you only get
  text + small side icons (`{iconleft}`/`{iconright}`). "Show large icons" only
  enlarges the static on/off **state** icon (an XML, not per value) — not a
  per-value keyboard. A big per-value image needs a **key** (`{image:}` fills the
  face). A key, though, can't do +/- — so for a split you stay on the dial.
- Wishlist / feature request sent to the author: let `{title}` **and** `{text}`
  both sit on the left, next to the keyboard.

---

## Reproduce

```bash
pip install pillow
python3 scripts/gen_keyboard_icons.py     # -> images/keyboard-icons/kbd_0..11.png
python3 scripts/gen_note_translation.py   # -> translation-files/note-names-*.xml
python3 scripts/gen_dial_full_images.py    # -> optional full landscape dial images
```

Then, in Stream Deck:
1. Copy `images/keyboard-icons/` into `~/Documents/Trevliga Spel/keyboard-icons/`.
2. Add a **Scripted Dial** (Trevliga Spel > Midi), paste
   `midiscript/split_note_dial.midiscript`, adjust CC/channel + the icon path.
3. (or the translation-file route: a **Cycle key** with `translation-files/…xml`.)

Fonts: images use a system font that includes `♯` (e.g. *Arial Unicode*).

---

## Links

- Forum thread (feature request + write-up):
  https://forum.trevligaspel.se/t/feature-request-note-value-display-for-the-generic-button-show-a-midi-value-as-c4/124
- Trevliga Spel MIDI plugin: https://trevligaspel.se/streamdeck/midi/

Thanks to **Gunnar** (Trevliga Spel) for the plugin and the translation-file pointer.
