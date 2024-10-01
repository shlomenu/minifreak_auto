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
"""
    