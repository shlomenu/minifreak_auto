from enum import Enum
from typing import Union

from pywinauto import Application, mouse
import mido

class Element(Enum):
    # Controls
    mod_wheel = 1
    hold = 64
    glide = 5
    tune_osc_1 = 70
    wave_osc_1 = 14
    timbre_osc_1 = 15
    shape_osc_1 = 16
    volume_osc_1 = 17
    tune_osc_2 = 73
    wave_osc_2 = 18
    timbre_osc_2 = 19
    shape_osc_2 = 20
    volume_osc_2 = 21
    cutoff = 74
    resonance = 71
    env_mod = 94
    env_amt = 24
    rise = 76
    rise_shape = 68
    fall = 77
    fall_shape = 69
    hold = 78
    attack = 80
    decay = 81
    sustain = 82
    release = 83
    rate_lfo_1 = 85
    rate_lfo_2 = 87
    time_fx_1 = 22
    intensity_fx_1 = 23
    amount_fx_1 = 25
    time_fx_2 = 26
    intensity_fx_2 = 27
    amount_fx_2 = 28
    time_fx_3 = 29
    intensity_fx_3 = 30
    amount_fx_3 = 31
    gate = 115
    spice = 116
    macro_1 = 117
    macro_2 = 118
    # Mouse-manipulated
    note_on = 119
    note_off = 120
    
    @property
    def is_control(self):
        return self.value <= 118




class MiniFreak:
    def __init__(
            self, 
            executable_path="C:\Program Files\Arturia\MiniFreak V\MiniFreak V.exe",
            outport_name="loopMIDI Port 1"):
        self.app = Application()
        self.executable_path = executable_path
        self.outport_name = outport_name

    def __enter__(self):
        self.app.start(self.executable_path)
        self._outport = mido.open_output(self.outport_name)                
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.app.kill()
        self._outport.close()
        return False
    
    def _send(self, elt: Element, **kwargs):
        if isinstance(self._outport, mido.ports.BaseOutput) and not self._outport.closed:
            if elt.is_control:
                msg = mido.Message("control_change", control=elt.value, **kwargs)
            else:
                msg = mido.Message(elt.name, **kwargs)
            self._outport.send(msg)

    def note_on(self, note, velocity):
        self._send(Element.note_on, note=note, velocity=velocity)

    def note_off(self, note, velocity):
        self._send(Element.note_off, note=note, velocity=velocity)

    def hold_on(self):
        self._send(Element.hold, value=127)

    def hold_off(self):
        self._send(Element.hold, value=0)

    def set_control(self, elt: Union[Element, str], value):
        if isinstance(elt, str):
            elt = Element[elt]
        if isinstance(elt, Element) and \
                elt.is_control and elt is not Element.hold:
            self._send(elt, value=value)
        else:
            raise ValueError(f"invalid input: {elt}")


"""
BUTTON MAPPING LOG FOR MOUSE MANIPULATION:

>>> app.minifreak.rectangle(); win32api.GetCu
rsorPos(); print("`Advanced`")
<RECT L4, T23, R1946, B1318>
(1586, 102)
`Advanced`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Sequencer`")
<RECT L4, T23, R1946, B1318>
(1716, 103)
`Sequencer`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Osc 1 Type`")
<RECT L4, T23, R1946, B1318>
(476, 200)
`Osc 1 Type`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Osc 2 Type`")
<RECT L4, T23, R1946, B1318>
(1005, 200)
`Osc 2 Type`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Analog Filter Type`")
<RECT L4, T23, R1946, B1318>
(1395, 198)
`Analog Filter Type`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX1 on/off`")
<RECT L4, T23, R1946, B1318>
(1556, 199)
`FX1 on/off`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX2 on/off`")
<RECT L4, T23, R1946, B1318>
(1677, 199)
`FX2 on/off`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX3 on/off`")
<RECT L4, T23, R1946, B1318>
(1799, 199)
`FX3 on/off`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX1 select`")
<RECT L4, T23, R1946, B1318>
(1598, 200)
`FX1 select`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX2 select`")
<RECT L4, T23, R1946, B1318>
(1718, 197)
`FX2 select`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX3 select`")
<RECT L4, T23, R1946, B1318>
(1840, 198)
`FX3 select`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX3 Type`")
<RECT L4, T23, R1946, B1318>
(1524, 241)
`FX3 Type`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`FX Presets`")
<RECT L4, T23, R1946, B1318>
(1526, 429)
`FX Presets`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Voice Mode`")
<RECT L4, T23, R1946, B1318>
(421, 711)
`Voice Mode`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`LFO1 Retrig`")
<RECT L4, T23, R1946, B1318>
(689, 711)
`LFO1 Retrig`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`LFO2 Retrig`")
<RECT L4, T23, R1946, B1318>
(943, 712)
`LFO2 Retrig`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`LFO1 Rate Type Toggle`")
<RECT L4, T23, R1946, B1318>
(771, 710)
`LFO1 Rate Type Toggle`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`LFO2 Rate Type Toggle`")
<RECT L4, T23, R1946, B1318>
(1034, 710)
`LFO2 Rate Type Toggle`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Mode`")
<RECT L4, T23, R1946, B1318>
(1193, 712)
`CycEnv Mode`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Retrig`")
<RECT L4, T23, R1946, B1318>
(1606, 711)
`Envelope Retrig`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Voices Settings Menu`")
<RECT L4, T23, R1946, B1318>
(524, 712)
`Voices Settings Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Voices Settings Menu > Glide Mode`")
<RECT L4, T23, R1946, B1318>
(481, 627)
`Voices Settings Menu > Glide Mode`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Voices Settings Menu > Allocation`")
<RECT L4, T23, R1946, B1318>
(480, 664)
`Voices Settings Menu > Allocation`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Voices Settings Menu > Note Steal`")
<RECT L4, T23, R1946, B1318>
(474, 700)
`Voices Settings Menu > Note Steal`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu`")
<RECT L4, T23, R1946, B1318>
(1427, 712)
`CycEnv Settings Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu > Tempo Sync on/off`")
<RECT L4, T23, R1946, B1318>
(1410, 616)
`CycEnv Settings Menu > Tempo Sync on/off`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu > Retrig`")
<RECT L4, T23, R1946, B1318>
(1352, 637)
`CycEnv Settings Menu > Retrig`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu > Stage Order`")
<RECT L4, T23, R1946, B1318>
(1346, 659)
`CycEnv Settings Menu > Stage Order`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu > Rise Curve`")
<RECT L4, T23, R1946, B1318>
(1347, 686)
`CycEnv Settings Menu > Rise Curve`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu > Fall Curve`")
<RECT L4, T23, R1946, B1318>
(1346, 715)
`CycEnv Settings Menu > Fall Curve`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`CycEnv Settings Menu > Close Menu`")
<RECT L4, T23, R1946, B1318>
(1427, 585)
`CycEnv Settings Menu > Close Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Voices Settings Menu > Clo
se Menu`")
<RECT L4, T23, R1946, B1318>
(523, 587)
`Voices Settings Menu > Close Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu`")
<RECT L4, T23, R1946, B1318>
(1882, 713)
`Envelope Settings Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Attack Curve`")
<RECT L4, T23, R1946, B1318>
(1631, 619)
`Envelope Settings Menu > Attack Curve`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Decay Curve`")
<RECT L4, T23, R1946, B1318>
(1625, 647)
`Envelope Settings Menu > Decay Curve`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Release Curve`")
<RECT L4, T23, R1946, B1318>
(1626, 678)
`Envelope Settings Menu > Release Curve`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Vel > VCA`")
<RECT L4, T23, R1946, B1318>
(1836, 620)
`Envelope Settings Menu > Vel > VCA`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Vel > VCF`")
<RECT L4, T23, R1946, B1318>
(1836, 650)
`Envelope Settings Menu > Vel > VCF`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Vel > ENV`")
<RECT L4, T23, R1946, B1318>
(1836, 677)
`Envelope Settings Menu > Vel > ENV`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Vel > TIME`")
<RECT L4, T23, R1946, B1318>
(1835, 708)
`Envelope Settings Menu > Vel > TIME`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Envelope Settings Menu > Vel > Menu Close`")
<RECT L4, T23, R1946, B1318>
(1882, 586)
`Envelope Settings Menu > Vel > Menu Close`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Wheels Settings Menu`")
<RECT L4, T23, R1946, B1318>
(165, 948)
`Wheels Settings Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Wheels Settings Menu > Vibrato on/off`")
<RECT L4, T23, R1946, B1318>
(239, 1005)
`Wheels Settings Menu > Vibrato on/off`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Wheels Settings Menu > Vibrato Rate`")
<RECT L4, T23, R1946, B1318>
(210, 1047)
`Wheels Settings Menu > Vibrato Rate`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Wheels Settings Menu > Vibrato Depth`")
<RECT L4, T23, R1946, B1318>
(209, 1091)
`Wheels Settings Menu > Vibrato Depth`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Wheels Settings Menu > Bend Range`")
<RECT L4, T23, R1946, B1318>
(209, 1134)
`Wheels Settings Menu > Bend Range`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Wheels Settings Menu > Close Menu`")
<RECT L4, T23, R1946, B1318>
(163, 1241)
`Wheels Settings Menu > Close Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Macros Settings Menu`")
<RECT L4, T23, R1946, B1318>
(166, 947)
`Macros Settings Menu`
>>> app.minifreak.rectangle(); win32api.GetCursorPos(); print("`Macro/Matrix`")
<RECT L4, T23, R1946, B1318>
(1103, 893)
`Macro/Matrix`
>>> get("`Chord Octave Select Down`")
(L4, T23, R1946, B1318)
 (61, 649)
 `Chord Octave Select Down`
>>> get("`Chord Octave Select Up`")
(L4, T23, R1946, B1318)
 (266, 650)
 `Chord Octave Select Up`
>>> get("`Chord Selection > C`")
(L4, T23, R1946, B1318)
 (92, 651)
 `Chord Selection > C`
>>> get("`Chord Selection > C Sharp`")
(L4, T23, R1946, B1318)
 (101, 624)
 `Chord Selection > C Sharp`
>>> get("`Chord Selection > D`")
(L4, T23, R1946, B1318)
 (113, 648)
 `Chord Selection > D`
>>> get("`Chord Selection > D Sharp`")
(L4, T23, R1946, B1318)
 (125, 623)
 `Chord Selection > D Sharp`
>>> get("`Chord Selection > E`")
(L4, T23, R1946, B1318)
 (140, 649)
 `Chord Selection > E`
>>> get("`Chord Selection > F`")
(L4, T23, R1946, B1318)
 (163, 648)
 `Chord Selection > F`
>>> get("`Chord Selection > F Sharp`")
(L4, T23, R1946, B1318)
 (173, 624)
 `Chord Selection > F Sharp`
>>> get("`Chord Selection > G`")
(L4, T23, R1946, B1318)
 (186, 648)
 `Chord Selection > G`
>>> get("`Chord Selection > G Sharp`")
(L4, T23, R1946, B1318)
 (199, 625)
 `Chord Selection > G Sharp`
>>> get("`Chord Selection > A`")
(L4, T23, R1946, B1318)
 (211, 648)
 `Chord Selection > A`
>>> get("`Chord Selection > A Sharp`")
(L4, T23, R1946, B1318)
 (220, 623)
 `Chord Selection > A Sharp`
>>> get("`Chord Selection > B`")
(L4, T23, R1946, B1318)
 (235, 648)
 `Chord Selection > B`
>>> get("`Chord Selection > -5`")
(L4, T23, R1946, B1318)
 (60, 707)
 `Chord Selection > -5`
>>> get("`Chord Selection > -4`")
(L4, T23, R1946, B1318)
 (82, 708)
 `Chord Selection > -4`
>>> get("`Chord Selection > -3`")
(L4, T23, R1946, B1318)
 (101, 706)
 `Chord Selection > -3`
>>> get("`Chord Selection > -2`")
(L4, T23, R1946, B1318)
 (124, 708)
 `Chord Selection > -2`
>>> get("`Chord Selection > -1`")
(L4, T23, R1946, B1318)
 (142, 709)
 `Chord Selection > -1`
>>> get("`Chord Selection > 0`")
(L4, T23, R1946, B1318)
 (162, 708)
 `Chord Selection > 0`
>>> get("`Chord Selection > 1`")
(L4, T23, R1946, B1318)
 (183, 709)
 `Chord Selection > 1`
>>> get("`Chord Selection > 2`")
(L4, T23, R1946, B1318)
 (204, 708)
 `Chord Selection > 2`
>>> get("`Chord Selection > 3`")
(L4, T23, R1946, B1318)
 (223, 708)
 `Chord Selection > 3`
>>> get("`Chord Selection > 4`")
(L4, T23, R1946, B1318)
 (245, 710)
 `Chord Selection > 4`
>>> get("`Chord Selection > 5`")
(L4, T23, R1946, B1318)
 (266, 709)
 `Chord Selection > 5`
>>> get("`Chord tab select`")
(L4, T23, R1946, B1318)
 (83, 543)
 `Chord tab select`
>>> get("`Scale tab select`")
(L4, T23, R1946, B1318)
 (243, 541)
 `Scale tab select`
>>> get("`Scale Selection > C`")
(L4, T23, R1946, B1318)
 (97, 675)
 `Scale Selection > C`
>>> get("`Scale Selection > C Sharp`")
(L4, T23, R1946, B1318)
 (109, 649)
 `Scale Selection > C Sharp`
>>> get("`Scale Selection > D`")
(L4, T23, R1946, B1318)
 (119, 674)
 `Scale Selection > D`
>>> get("`Scale Selection > D Sharp`")
(L4, T23, R1946, B1318)
 (132, 646)
 `Scale Selection > D Sharp`
>>> get("`Scale Selection > E`")
(L4, T23, R1946, B1318)
 (141, 673)
 `Scale Selection > E`
>>> get("`Scale Selection > F`")
(L4, T23, R1946, B1318)
 (160, 675)
 `Scale Selection > F`
>>> get("`Scale Selection > F Sharp`")
(L4, T23, R1946, B1318)
 (174, 647)
 `Scale Selection > F Sharp`
>>> get("`Scale Selection > G`")
(L4, T23, R1946, B1318)
 (183, 673)
 `Scale Selection > G`
>>> get("`Scale Selection > G Sharp`")
(L4, T23, R1946, B1318)
 (195, 648)
 `Scale Selection > G Sharp`
>>> get("`Scale Selection > A`")
(L4, T23, R1946, B1318)
 (202, 673)
 `Scale Selection > A`
>>> get("`Scale Selection > A Sharp`")
(L4, T23, R1946, B1318)
 (216, 649)
 `Scale Selection > A Sharp`
>>> get("`Scale Selection > B`")
(L4, T23, R1946, B1318)
 (225, 674)
 `Scale Selection > B`
>>> get("`Chord on/off`")
(L4, T23, R1946, B1318)
 (98, 773)
 `Chord on/off`
>>> get("`Chord Root Menu`")
(L4, T23, R1946, B1318)
 (168, 776)
 `Chord Root Menu`
>>> get("`Scale Mode Menu`")
(L4, T23, R1946, B1318)
 (226, 771)
 `Scale Mode Menu`
>>> get("`Macro 1 > Parameter 1`")
(L4, T23, R1946, B1318)
 (422, 1032)
 `Macro 1 > Parameter 1`
>>> get("`Macro 1 > Parameter 2`")
(L4, T23, R1946, B1318)
 (425, 1094)
 `Macro 1 > Parameter 2`
>>> get("`Macro 1 > Parameter 3`")
(L4, T23, R1946, B1318)
 (434, 1151)
 `Macro 1 > Parameter 3`
>>> get("`Macro 1 > Parameter 4`")
(L4, T23, R1946, B1318)
 (439, 1212)
 `Macro 1 > Parameter 4`
>>> get("`Macro 2 > Parameter 1`")
(L4, T23, R1946, B1318)
 (718, 1032)
 `Macro 2 > Parameter 1`
>>> get("`Macro 2 > Parameter 2`")
(L4, T23, R1946, B1318)
 (710, 1094)
 `Macro 2 > Parameter 2`
>>> get("`Macro 2 > Parameter 3`")
(L4, T23, R1946, B1318)
 (711, 1153)
 `Macro 2 > Parameter 3`
>>> get("`Macro 2 > Parameter 4`")
(L4, T23, R1946, B1318)
 (715, 1215)
 `Macro 2 > Parameter 4`
>>> get("`Macro 1 > Amount 1`")
(L4, T23, R1946, B1318)
 (549, 1032)
 `Macro 1 > Amount 1`
>>> get("`Macro 1 > Amount 2`")
(L4, T23, R1946, B1318)
 (551, 1089)
 `Macro 1 > Amount 2`
>>> get("`Macro 1 > Amount 3`")
(L4, T23, R1946, B1318)
 (552, 1151)
 `Macro 1 > Amount 3`
>>> get("`Macro 1 > Amount 4`")
(L4, T23, R1946, B1318)
 (552, 1210)
 `Macro 1 > Amount 4`
>>> get("`Macro 2 > Amount 1`")
(L4, T23, R1946, B1318)
 (843, 1031)
 `Macro 2 > Amount 1`
>>> get("`Macro 2 > Amount 2`")
(L4, T23, R1946, B1318)
 (841, 1090)
 `Macro 2 > Amount 2`
>>> get("`Macro 2 > Amount 3`")
(L4, T23, R1946, B1318)
 (842, 1153)
 `Macro 2 > Amount 3`
>>> get("`Macro 2 > Amount 4`")
(L4, T23, R1946, B1318)
 (842, 1211)
 `Macro 2 > Amount 4`
>>> get("`Matrix Mod 1:1`")
(L4, T23, R1946, B1318)
 (1089, 1046)
 `Matrix Mod 1:1`
>>> get("`Matrix Mod 7:1`")
(L4, T23, R1946, B1318)
 (1088, 1231)
 `Matrix Mod 7:1`
>>> get("`Matrix Mod 1:13`")
(L4, T23, R1946, B1318)
 (1764, 1043)
 `Matrix Mod 1:13`
>>> get("`Matrix Mod 7:13`")
(L4, T23, R1946, B1318)
 (1763, 1230)
 `Matrix Mod 7:13`
>>> get("`Custom Matrix Slot 1`")
(L4, T23, R1946, B1318)
 (1326, 1003)
 `Custom Matrix Slot 1`
>>> get("`Custom Matrix Slot 2`")
(L4, T23, R1946, B1318)
 (1386, 998)
 `Custom Matrix Slot 2`
>>> get("`Custom Matrix Slot 3`")
(L4, T23, R1946, B1318)
 (1444, 998)
 `Custom Matrix Slot 3`
>>> get("`Custom Matrix Slot 4`")
(L4, T23, R1946, B1318)
 (1496, 1001)
 `Custom Matrix Slot 4`
>>> get("`Custom Matrix Slot 5`")
(L4, T23, R1946, B1318)
 (1556, 997)
 `Custom Matrix Slot 5`
>>> get("`Custom Matrix Slot 6`")
(L4, T23, R1946, B1318)
 (1607, 1009)
 `Custom Matrix Slot 6`
>>> get("`Custom Matrix Slot 7`")
(L4, T23, R1946, B1318)
 (1664, 1003)
 `Custom Matrix Slot 7`
>>> get("`Custom Matrix Slot 8`")
(L4, T23, R1946, B1318)
 (1724, 1000)
 `Custom Matrix Slot 8`
>>> get("`Custom Matrix Slot 9`")
(L4, T23, R1946, B1318)
 (1782, 1000)
 `Custom Matrix Slot 9`
>>> get("`Reverb/Delay > Insert Mode`")
(L4, T23, R1946, B1318)
 (1505, 366)
 `Reverb/Delay > Insert Mode`
>>> get("`Reverb/Delay > Send Mode`")
(L4, T23, R1946, B1318)
 (1558, 369)
 `Reverb/Delay > Send Mode`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Tune`")
(L4, T23, R1946, B1318)
 (97, 432)
 `Matrix Routing Slot Assignment > Osc 1 Tune`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Interval`"
)
(L4, T23, R1946, B1318)
 (195, 431)
 `Matrix Routing Slot Assignment > Osc 1 Interval`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Wave`")
(L4, T23, R1946, B1318)
 (195, 431)
 `Matrix Routing Slot Assignment > Osc 1 Wave`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Timbre`")
(L4, T23, R1946, B1318)
 (292, 430)
 `Matrix Routing Slot Assignment > Osc 1 Timbre`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Shape`")
(L4, T23, R1946, B1318)
 (380, 431)
 `Matrix Routing Slot Assignment > Osc 1 Shape`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Volume`")
(L4, T23, R1946, B1318)
 (474, 432)
 `Matrix Routing Slot Assignment > Osc 1 Volume`
>>> get("`Matrix Routing Slot Assignment > Osc 2 Tune`")
(L4, T23, R1946, B1318)
 (627, 432)
 `Matrix Routing Slot Assignment > Osc 2 Tune`
>>> get("`Matrix Routing Slot Assignment > Osc 2 Wave`")
(L4, T23, R1946, B1318)
 (725, 431)
 `Matrix Routing Slot Assignment > Osc 2 Wave`
>>> get("`Matrix Routing Slot Assignment > Osc 2 Timbre`")
(L4, T23, R1946, B1318)
 (818, 433)
 `Matrix Routing Slot Assignment > Osc 2 Timbre`
>>> get("`Matrix Routing Slot Assignment > Osc 2 Shape`")
(L4, T23, R1946, B1318)
 (907, 428)
 `Matrix Routing Slot Assignment > Osc 2 Shape`
>>> get("`Matrix Routing Slot Assignment > Osc 2 Volume`")
(L4, T23, R1946, B1318)
 (999, 433)
 `Matrix Routing Slot Assignment > Osc 2 Volume`
>>> get("`Matrix Routing Slot Assignment > Osc 1 Type`")
(L4, T23, R1946, B1318)
 (468, 198)
 `Matrix Routing Slot Assignment > Osc 1 Type`
>>> get("`Matrix Routing Slot Assignment > Osc 2 Type`")
(L4, T23, R1946, B1318)
 (1001, 197)
 `Matrix Routing Slot Assignment > Osc 2 Type`
>>> get("`Matrix Routing Slot Assignment > Analog Filter Cutoff`")
(L4, T23, R1946, B1318)
 (1169, 431)
 `Matrix Routing Slot Assignment > Analog Filter Cutoff`
>>> get("`Matrix Routing Slot Assignment > Analog Filter Reso`")
(L4, T23, R1946, B1318)
 (1269, 433)
 `Matrix Routing Slot Assignment > Analog Filter Reso`
>>> get("`Matrix Routing Slot Assignment > Analog Filter Env Amt`")
(L4, T23, R1946, B1318)
 (1374, 430)
 `Matrix Routing Slot Assignment > Analog Filter Env Amt`
>>> get("`Matrix Routing Slot Assignment > FX Time`")
(L4, T23, R1946, B1318)
 (1640, 428)
 `Matrix Routing Slot Assignment > FX Time`
>>> get("`Matrix Routing Slot Assignment > FX Intensity5`")

(L4, T23, R1946, B1318)
 (1729, 432)
 `Matrix Routing Slot Assignment > FX Intensity5`
>>> get("`Matrix Routing Slot Assignment > FX Intensity`")
(L4, T23, R1946, B1318)
 (1729, 432)
 `Matrix Routing Slot Assignment > FX Intensity`
>>> get("`Matrix Routing Slot Assignment > FX Amount`")
(L4, T23, R1946, B1318)
 (1827, 431)
 `Matrix Routing Slot Assignment > FX Amount`
>>> get("`Matrix Routing Slot Assignment > Glide`")
(L4, T23, R1946, B1318)
 (470, 776)
 `Matrix Routing Slot Assignment > Glide`
>>> get("`Matrix Routing Slot Assignment > LFO1 Rate`")
(L4, T23, R1946, B1318)
 (639, 773)
 `Matrix Routing Slot Assignment > LFO1 Rate`
>>> get("`Matrix Routing Slot Assignment > LFO2 Rate`")
(L4, T23, R1946, B1318)
 (900, 774)
 `Matrix Routing Slot Assignment > LFO2 Rate`
>>> get("`Matrix Routing Slot Assignment > LFO1 Wave`")
(L4, T23, R1946, B1318)
 (741, 776)
 `Matrix Routing Slot Assignment > LFO1 Wave`
>>> get("`Matrix Routing Slot Assignment > LFO2 Wave`")
(L4, T23, R1946, B1318)
 (1003, 773)
 `Matrix Routing Slot Assignment > LFO2 Wave`
>>> get("`Matrix Routing Slot Assignment > CycEnv Rise`")
(L4, T23, R1946, B1318)
 (1165, 774)
 `Matrix Routing Slot Assignment > CycEnv Rise`
>>> get("`Matrix Routing Slot Assignment > CycEnv Fall`")
(L4, T23, R1946, B1318)
 (1272, 777)
 `Matrix Routing Slot Assignment > CycEnv Fall`
>>> get("`Matrix Routing Slot Assignment > CycEnv Hold`")
(L4, T23, R1946, B1318)
 (1376, 777)
 `Matrix Routing Slot Assignment > CycEnv Hold`
>>> get("`Matrix Routing Slot Assignment > Env Attack`")
(L4, T23, R1946, B1318)
 (1540, 774)
 `Matrix Routing Slot Assignment > Env Attack`
>>> get("`Matrix Routing Slot Assignment > Env Decay`")
(L4, T23, R1946, B1318)
 (1637, 777)
 `Matrix Routing Slot Assignment > Env Decay`
>>> get("`Matrix Routing Slot Assignment > Env Sustain`")
(L4, T23, R1946, B1318)
 (1735, 776)
 `Matrix Routing Slot Assignment > Env Sustain`
>>> get("`Matrix Routing Slot Assignment > Env Release`")
(L4, T23, R1946, B1318)
 (1837, 776)
 `Matrix Routing Slot Assignment > Env Release`
>>> get("`Brightness`")
(L4, T23, R1946, B1318)
 (1389, 1283)
 `Brightness`
>>> get("`Timbre`")
(L4, T23, R1946, B1318)
 (1524, 1285)
 `Timbre`
>>> get("`LFO Shaper`")
(L4, T23, R1946, B1318)
 (1470, 897)
 `LFO Shaper`
>>> get("`LFO Shaper > LFO1 Tab select`")
(L4, T23, R1946, B1318)
 (410, 955)
 `LFO Shaper > LFO1 Tab select`
>>> get("`LFO Shaper > LFO2 Tab select`")
(L4, T23, R1946, B1318)
 (549, 953)
 `LFO Shaper > LFO2 Tab select`
>>> get("`LFO Shaper > Reset Shaper`")
(L4, T23, R1946, B1318)
 (466, 999)
 `LFO Shaper > Reset Shaper`
>>> get("`LFO Shaper > Grid Length`")
(L4, T23, R1946, B1318)
 (556, 1042)
 `LFO Shaper > Grid Length`
>>> get("`LFO Shaper > Rate`")
(L4, T23, R1946, B1318)
 (549, 1085)
 `LFO Shaper > Rate`
>>> get("`LFO Shaper > Slope Upward`")
(L4, T23, R1946, B1318)
 (401, 1162)
 `LFO Shaper > Slope Upward`
>>> get("`LFO Shaper > Slope Downward`")
(L4, T23, R1946, B1318)
 (492, 1164)
 `LFO Shaper > Slope Downward`
>>> get("`LFO Shaper > Curve`")
(L4, T23, R1946, B1318)
 (398, 1204)
 `LFO Shaper > Curve`
>>> get("`LFO Shaper > Flat`")
(L4, T23, R1946, B1318)
 (496, 1207)
 `LFO Shaper > Flat`
>>> get("`LFO Shaper > Amplitude`")
(L4, T23, R1946, B1318)
 (563, 1191)
 `LFO Shaper > Amplitude`
>>> get("`LFO Shaper > Time Segment 1`")
(L4, T23, R1946, B1318)
 (725, 1097)
 `LFO Shaper > Time Segment 1`
>>> get("`LFO Shaper > Time Segment 16`")
(L4, T23, R1946, B1318)
 (1761, 1093)
 `LFO Shaper > Time Segment 16`
>>> get("`LFO Shaper > Canvas Border Left`")
(L4, T23, R1946, B1318)
 (691, 1097)
 `LFO Shaper > Canvas Border Left`
>>> get("`LFO Shaper > Canvas Border Right`")
(L4, T23, R1946, B1318)
 (1796, 1092)
 `LFO Shaper > Canvas Border Right`
>>> get("`LFO Shaper > Eraser Button Height`")
(L4, T23, R1946, B1318)
 (734, 969)
 `LFO Shaper > Eraser Button Height`
>>> get("`LFO Shaper > Canvas Mid Height`")
(L4, T23, R1946, B1318)
 (1043, 1094)
 `LFO Shaper > Canvas Mid Height`
>>> get("`Sequencer > on/off`")
(L4, T23, R1946, B1318)
 (99, 265)
 `Sequencer > on/off`
>>> get("`Sequencer > Arpeggiator on/off`")
(L4, T23, R1946, B1318)
 (182, 260)
 `Sequencer > Arpeggiator on/off`
>>> get("`Sequencer > Sequencer on/off`")
(L4, T23, R1946, B1318)
 (265, 261)
 `Sequencer > Sequencer on/off`
>>> get("`Sequencer > Arpegggiator Up on/off`")
(L4, T23, R1946, B1318)
 (401, 259)
 `Sequencer > Arpegggiator Up on/off`
>>> get("`Sequencer > Arpegggiator Down on/off`")
(L4, T23, R1946, B1318)
 (472, 262)
 `Sequencer > Arpegggiator Down on/off`
>>> get("`Sequencer > Arpegggiator Up/Down on/off`")
(L4, T23, R1946, B1318)
 (544, 261)
 `Sequencer > Arpegggiator Up/Down on/off`
>>> get("`Sequencer > Arpegggiator Random on/off`")
(L4, T23, R1946, B1318)
 (619, 262)
 `Sequencer > Arpegggiator Random on/off`
>>> get("`Sequencer > Arpegggiator Order on/off`")
(L4, T23, R1946, B1318)
 (688, 262)
 `Sequencer > Arpegggiator Order on/off`
>>> get("`Sequencer > Arpegggiator Poly on/off`")
(L4, T23, R1946, B1318)
 (759, 266)
 `Sequencer > Arpegggiator Poly on/off`
>>> get("`Sequencer > Arpegggiator Walk on/off`")
(L4, T23, R1946, B1318)
 (831, 262)
 `Sequencer > Arpegggiator Walk on/off`
>>> get("`Sequencer > Arpegggiator Pattern on/off`")
(L4, T23, R1946, B1318)
 (906, 264)
 `Sequencer > Arpegggiator Pattern on/off`
>>> get("`Sequencer > Arpegggiator Oct1 on/off`")
(L4, T23, R1946, B1318)
 (976, 263)
 `Sequencer > Arpegggiator Oct1 on/off`
>>> get("`Sequencer > Arpegggiator Oct2 on/off`")
(L4, T23, R1946, B1318)
 (1044, 261)
 `Sequencer > Arpegggiator Oct2 on/off`
>>> get("`Sequencer > Arpegggiator Oct3 on/off`")
(L4, T23, R1946, B1318)
 (1114, 263)
 `Sequencer > Arpegggiator Oct3 on/off`
>>> get("`Sequencer > Arpegggiator Oct4 on/off`")
(L4, T23, R1946, B1318)
 (1188, 263)
 `Sequencer > Arpegggiator Oct4 on/off`
>>> get("`Sequencer > Arpegggiator Repeat on/off`")
(L4, T23, R1946, B1318)
 (1257, 260)
 `Sequencer > Arpegggiator Repeat on/off`
>>> get("`Sequencer > Arpegggiator Ratchet on/off`")
(L4, T23, R1946, B1318)
 (1322, 261)
 `Sequencer > Arpegggiator Ratchet on/off`
>>> get("`Sequencer > Arpegggiator Rand Oct on/off`")
(L4, T23, R1946, B1318)
 (1399, 266)
 `Sequencer > Arpegggiator Rand Oct on/off`
>>> get("`Sequencer > Arpegggiator Mutate on/off`")
(L4, T23, R1946, B1318)
 (1474, 261)
 `Sequencer > Arpegggiator Mutate on/off`
>>> get("`Sequencer > Gate`")
(L4, T23, R1946, B1318)
 (1588, 263)
 `Sequencer > Gate`
>>> get("`Sequencer > Spice`")
(L4, T23, R1946, B1318)
 (1641, 262)
 `Sequencer > Spice`
>>> get("`Sequencer > Gate Top`")
(L4, T23, R1946, B1318)
 (1588, 237)
 `Sequencer > Gate Top`
>>> get("`Sequencer > Gate Bottom`")
(L4, T23, R1946, B1318)
 (1586, 288)
 `Sequencer > Gate Bottom`
>>> get("`Sequencer > Spice Top`")
(L4, T23, R1946, B1318)
 (1639, 238)
 `Sequencer > Spice Top`
>>> get("`Sequencer > Spice Bottom`")
(L4, T23, R1946, B1318)
 (1640, 287)
 `Sequencer > Spice Bottom`
>>> get("`Sequencer > Roll Dice`")
(L4, T23, R1946, B1318)
 (1695, 260)
 `Sequencer > Roll Dice`
>>> get("`Sequencer > Swing`")
(L4, T23, R1946, B1318)
 (1782, 266)
 `Sequencer > Swing`
>>> get("`Sequencer > Tempo`")
(L4, T23, R1946, B1318)
 (1840, 192)
 `Sequencer > Tempo`
>>> get("`Sequencer > TimeDiv`")
(L4, T23, R1946, B1318)
 (1855, 264)
 `Sequencer > TimeDiv`
>>> get("`Sequencer > TimeDiv Up Button`")
(L4, T23, R1946, B1318)
 (1830, 240)
 `Sequencer > TimeDiv Up Button`
>>> get("`Sequencer > TimeDiv Down Button`")
(L4, T23, R1946, B1318)
 (1828, 296)
 `Sequencer > TimeDiv Down Button`
>>> get("`Sequencer > Sequencer Auto Play`")
(L4, T23, R1946, B1318)
 (637, 264)
 `Sequencer > Sequencer Auto Play`
>>> get("`Sequencer > Sequencer Overdub`")
(L4, T23, R1946, B1318)
 (723, 263)
 `Sequencer > Sequencer Overdub`
>>> get("`Sequencer > Sequencer Play/Stop`")
(L4, T23, R1946, B1318)
 (808, 259)
 `Sequencer > Sequencer Play/Stop`
>>> get("`Sequencer > Sequencer Record`")
(L4, T23, R1946, B1318)
 (894, 262)
 `Sequencer > Sequencer Record`
>>> get("`Sequencer > Sequencer Modulation`")
(L4, T23, R1946, B1318)
 (980, 259)
 `Sequencer > Sequencer Modulation`
>>> get("`Sequencer > Sequencer 1 Bar`")
(L4, T23, R1946, B1318)
 (1051, 276)
 `Sequencer > Sequencer 1 Bar`
>>> get("`Sequencer > Sequencer 2 Bar`")
(L4, T23, R1946, B1318)
 (1148, 259)
 `Sequencer > Sequencer 2 Bar`
>>> get("`Sequencer > Sequencer 3 Bar`")
(L4, T23, R1946, B1318)
 (1231, 263)
 `Sequencer > Sequencer 3 Bar`
>>> get("`Sequencer > Sequencer 4 Bar`")
(L4, T23, R1946, B1318)
 (1315, 264)
 `Sequencer > Sequencer 4 Bar`
>>> get("`Sequencer > Scroll Bar C-2 + C-1`")
(L4, T23, R1946, B1318)
 (1879, 923)
 `Sequencer > Scroll Bar C-2 + C-1`
>>> get("`Sequencer > Scroll Bar C1 C2`")
(L4, T23, R1946, B1318)
 (1880, 737)
 `Sequencer > Scroll Bar C1 C2`
>>> get("`Sequencer > Scroll Bar C4 C5`")
(L4, T23, R1946, B1318)
 (1880, 605)
 `Sequencer > Scroll Bar C4 C5`
>>> get("`Sequencer > Scroll Bar C7 C8`")
(L4, T23, R1946, B1318)
 (1880, 472)
 `Sequencer > Scroll Bar C7 C8`
>>> get("`Sequencer > Add Note Segment 1 Low`")
(L4, T23, R1946, B1318)
 (286, 929)
 `Sequencer > Add Note Segment 1 Low`
>>> get("`Sequencer > Add Note Segment 1 High`")
(L4, T23, R1946, B1318)
 (289, 413)
 `Sequencer > Add Note Segment 1 High`
>>> get("`Sequencer > Add Note Segment 16 High`")
(L4, T23, R1946, B1318)
 (1818, 407)
 `Sequencer > Add Note Segment 16 High`
>>> get("`Sequencer > Add Note Segment 16 Low`")
(L4, T23, R1946, B1318)
 (1828, 929)
 `Sequencer > Add Note Segment 16 Low`
>>> get("`Sequencer > Segment 1 Modulation Level Top`")
(L4, T23, R1946, B1318)
 (291, 1043)
 `Sequencer > Segment 1 Modulation Level Top`
>>> get("`Sequencer > Segment 1 Modulation Level Bottom`")
(L4, T23, R1946, B1318)
 (291, 1204)
 `Sequencer > Segment 1 Modulation Level Bottom`
>>> get("`Sequencer > Segment 16 Modulation Level Top`")
(L4, T23, R1946, B1318)
 (1835, 1046)
 `Sequencer > Segment 16 Modulation Level Top`
>>> get("`Sequencer > Segment 16 Modulation Level Bottom`")

(L4, T23, R1946, B1318)
 (1833, 1205)
 `Sequencer > Segment 16 Modulation Level Bottom`
>>> get("`Sequencer > Mod Type Row 1`")
(L4, T23, R1946, B1318)
 (141, 1042)
 `Sequencer > Mod Type Row 1`
>>> get("`Sequencer > Mod Type Row 2`")
(L4, T23, R1946, B1318)
 (137, 1095)
 `Sequencer > Mod Type Row 2`
>>> get("`Sequencer > Mod Type Row 3`")
(L4, T23, R1946, B1318)
 (139, 1148)
 `Sequencer > Mod Type Row 3`
>>> get("`Sequencer > Mod Type Row 4`")
(L4, T23, R1946, B1318)
 (138, 1206)
 `Sequencer > Mod Type Row 4`
>>> get("`Sequencer > Auto Smooth Toggle Row 1 `")
(L4, T23, R1946, B1318)
 (87, 1043)
 `Sequencer > Auto Smooth Toggle Row 1 `
>>> get("`Sequencer > Auto Smooth Toggle Row 2 `")
(L4, T23, R1946, B1318)
 (88, 1097)
 `Sequencer > Auto Smooth Toggle Row 2 `
>>> get("`Sequencer > Auto Smooth Toggle Row 3 `")
(L4, T23, R1946, B1318)
 (89, 1149)
 `Sequencer > Auto Smooth Toggle Row 3 `
>>> get("`Sequencer > Auto Smooth Toggle Row 4 `")
(L4, T23, R1946, B1318)
 (88, 1203)
 `Sequencer > Auto Smooth Toggle Row 4 `
"""
    