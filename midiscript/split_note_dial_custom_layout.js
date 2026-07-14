/// <reference path="./streamdeck-midi.d.ts" />
//
// Split-point note display on a Scripted Dial, using a CUSTOM LAYOUT.
// ------------------------------------------------------------------
// A custom layout lets you place the note letter and the octave together as
// one "G#3" unit on the left, with the piano on the right (Gunnar's tip: each
// object's position comes from its own rect + "alignment" in the layout JSON).
//
// Because the layout uses its own object keys (note_letter / note_octave /
// keyboard), the plugin's MidiScript title/text commands can't fill them -
// custom-key layouts are driven by the JS "layout" API instead. This is the
// JS engine (Jint) shipped with the plugin; the API is documented in the
// bundled streamdeck-midi.d.ts.
//
// HOW TO ENABLE (in the dial's Property Inspector):
//   1. "Custom layout" section -> tick "Use a custom layout"
//      -> in "Layout file", pick  ts_note_split.json.
//   2. "Script" section -> paste this JS (it's a JavaScript action, not a
//      MidiScript one). The plugin loads the JSON and this script fills it.
//   3. Set CH/CC and ICONS below to your own split control + icon folder.

var CH = 2;      // MIDI channel of the split control
var CC = 103;    // CC number of the split control

// Sharp = U+266F (real MUSIC SHARP SIGN), not ASCII '#'.
var NOTES = ["C", "C♯", "D", "D♯", "E", "F", "F♯",
             "G", "G♯", "A", "A♯", "B"];

// path.documents ends with a separator. Point ICONS at YOUR kbd_0..11.png folder.
var LAYOUT = path.documents + "Trevliga Spel/Layouts/ts_note_split.json";
var ICONS  = path.documents + "Trevliga Spel/keyboard-icons/";

var loaded = false;
function ensureLayout() {
    if (!loaded) { layout.load(LAYOUT); loaded = true; }
}

function draw(v) {
    ensureLayout();
    v = Math.max(0, Math.min(127, v | 0));
    var n = v % 12;
    var oct = Math.floor(v / 12) - 1;   // C4 = middle C = 60

    layout.note_letter.set("enabled", true);
    layout.note_letter.value(NOTES[n]);

    layout.note_octave.set("enabled", true);
    layout.note_octave.value(String(oct));

    layout.keyboard.set("enabled", true);
    layout.keyboard.value(ICONS + "kbd_" + n + ".png");
}

// Show the current split point as soon as the script starts.
function OnInit() { draw(midi.getCC(CH, CC)); }

// External changes to the split point (e.g. from the keyboard/host).
function OnControlChangeReceived(channel, control, value) {
    if (channel === CH && control === CC) draw(value);
}

// Turning the dial adjusts the split and sends it out.
function OnDialRotated(ticks, value) {
    var v = Math.max(0, Math.min(127, midi.getCC(CH, CC) + ticks));
    midi.sendCC(CH, CC, v);
    draw(v);
}
