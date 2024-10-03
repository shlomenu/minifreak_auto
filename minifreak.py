from enum import Enum, auto
from typing import Union

from pywinauto import Application, mouse
import mido

# Based on experimental measurements on 4K screen
def norm_coord(x, y):
    """
    Based on empirical measurements with 4K monitor.
    Window location: (L4, T23, R1946, B1318)
    Clickable area: (x, y)
    returns: (x_norm, y_norm)
    """ 
    x_norm = (x - 4) / (1946 - 4)
    y_norm = (y - 23) / (1318 - 23)
    return (x_norm, y_norm)


# Midi_*: values are control numbers
class Midi_Sliders(Enum):
    mod_wheel = 1
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

class Midi_Buttons(Enum):
    hold = 64

# Clickable_*: values are (H, W) in [0, 1] X [0, 1]
class Clickable_Buttons(Enum):
    open_tab_advanced = norm_coord(1586, 102)
    open_tab_sequencer = norm_coord(1716, 103)
    open_tab_fx1 = norm_coord(1598, 200)
    open_tab_fx2 = norm_coord(1718, 197)
    open_tab_fx3 = norm_coord(1840, 198)
    open_tab_settings_voices = norm_coord(524, 712)
    open_tab_settings_cycenv = norm_coord(1427, 712)
    open_tab_settings_envelope = norm_coord(1882, 713)
    open_tab_settings_wheels = norm_coord(165, 948)
    open_tab_settings_macros_matrix = norm_coord(1103, 893)
    open_tab_lfo_shaper = norm_coord(1470, 897)
    open_tab_lfo1_lfo_shaper = norm_coord(410, 955)
    open_tab_lfo2_lfo_shaper = norm_coord(549, 953)
    open_tab_chord = norm_coord(83, 543)
    open_tab_scale = norm_coord(243, 541)
    close_tab_settings_voices = norm_coord(523, 587)
    close_tab_settings_cycenv = norm_coord(1427, 585)
    close_tab_settings_envelope = norm_coord(1882, 586)
    close_tab_settings_wheels = norm_coord(163, 1241)
    toggle_fx1 = norm_coord(1556, 199)
    toggle_fx2 = norm_coord(1677, 199)
    toggle_fx3 = norm_coord(1799, 199)
    toggle_tempo_sync_settings_run_cycenv = norm_coord(1411, 617)
    toggle_tempo_sync_settings_loop_cycenv = norm_coord(1412, 612)
    toggle_vibrato_settings_wheels = norm_coord(239, 1005)
    toggle_legato_settings_mono_voices = norm_coord(510, 689)
    toggle_legato_settings_uni_voices = norm_coord(510, 636)
    clickthru_rate_type_lfo1 = norm_coord(771, 710)
    clickthru_rate_type_lfo2 = norm_coord(1034, 710)
    clickthru_rise_curve_settings_env_cycenv = norm_coord(1350, 665)
    clickthru_fall_curve_settings_env_cycenv = norm_coord(1353, 701)
    open_menu_type_osc_1 = norm_coord(476, 200)
    open_menu_type_osc_2 = norm_coord(1005, 200)
    open_menu_type_filter = norm_coord(1395, 198)
    open_menu_type_fx = norm_coord(1524, 241)
    open_menu_presets_fx = norm_coord(1526, 429)
    open_menu_mode_voices = norm_coord(421, 711)
    open_menu_retrigger_lfo1 = norm_coord(689, 711)
    open_menu_retrigger_lfo2 = norm_coord(943, 712)
    open_menu_mode_cycenv = norm_coord(1193, 712)
    open_menu_retrigger_env = norm_coord(1606, 711)
    open_menu_glide_mode_settings_mono_voices = norm_coord(478, 639)
    open_menu_glide_mode_settings_uni_voices = norm_coord(479, 616)
    open_menu_uni_mode_settings_uni_voices = norm_coord(478, 662)
    open_menu_glide_mode_settings_polypara_voices = norm_coord(481, 627)
    open_menu_allocation_settings_polypara_voices = norm_coord(480, 664)
    open_menu_note_steal_settings_polypara_voices = norm_coord(474, 700)
    open_menu_mode_settings_voices = norm_coord(461, 586)
    open_menu_retrigger_settings_env_cycenv = norm_coord(1351, 626)
    open_menu_stage_order_settings_run_cycenv = norm_coord(1350, 646)
    open_menu_retrigger_settings_loop_cycenv = norm_coord(1352, 637)
    open_menu_stage_order_settings_loop_cycenv = norm_coord(1346, 659)
    open_menu_mode_settings_cycenv = norm_coord(1327, 586)
    open_menu_attack_curve_settings_envelope = norm_coord(1631, 619)
    open_menu_decay_curve_settings_envelope = norm_coord(1625, 647)
    open_menu_release_curve_settings_envelope = norm_coord(1626, 678)
    open_menu_retrigger_settings_env = norm_coord(1653, 586)





class Clickable_Sliders(Enum):
    slider_rise_curve_settings_run_cycenv = 149
    slider_fall_curve_settings_run_cycenv = 150
    slider_vel_vca_settings_envelope = 161
    slider_vel_vcf_settings_envelope = 162
    slider_vel_env_settings_envelope = 163
    slider_vel_time_settings_envelope = 164
    slider_vibrato_rate_settings_wheels = 168
    slider_vibrato_depth_settings_wheels = 169
    slider_bend_range_settings_wheels = 170


    

    
    


    
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

    def note(self, note, velocity, release=False):
        self._send(
            Element.note_off if release else Element.note_on, 
            note=note, 
            velocity=velocity)

    def hold(self, release=False):
        self._send(Element.hold, value=(0 if release else 127))

    def set(self, elt: Union[Element, str], value):
        if isinstance(elt, str):
            elt = Element[elt]
        if isinstance(elt, Element) and \
                elt.is_control and elt is not Element.hold:
            self._send(elt, value=value)
        else:
            raise ValueError(f"invalid input: {elt}")
    
    


"""
BUTTON MAPPING LOG FOR MOUSE MANIPULATION:

(L4, T23, R1946, B1318)


(1586, 102)
`Advanced`


(1716, 103)
`Sequencer`


(476, 200)
`Osc 1 Type`


(1005, 200)
`Osc 2 Type`


(1395, 198)
`Analog Filter Type`


(1556, 199)
`FX1 on/off`


(1677, 199)
`FX2 on/off`


(1799, 199)
`FX3 on/off`


(1598, 200)
`FX1 select`


(1718, 197)
`FX2 select`


(1840, 198)
`FX3 select`


(1524, 241)
`FX Type`


(1526, 429)
`FX Presets`


(421, 711)
`Voice Mode`


(689, 711)
`LFO1 Retrig`


(943, 712)
`LFO2 Retrig`


(771, 710)
`LFO1 Rate Type Toggle`


(1034, 710)
`LFO2 Rate Type Toggle`


(1193, 712)
`CycEnv Mode`


(1606, 711)
`Envelope Retrig`


(524, 712)
`Voices Settings Menu`


(461, 586)
 Voice Settings > Mode


(478, 639)
 `Voice Mono Settings > Glide Mode Menu`


(510, 689)
 `Voice Mono Settings > Legato on/off`


(479, 616)
 `Voice Uni Settings > Glide Mode Menu`


(510, 636)
 `Voice Uni Settings > Legato on/off`


(478, 662)
 `Voice Uni Settings > Uni Mode`


(476, 688)
 `Voice Uni Settings > Uni Count`


(479, 712)
 `Voice Uni Settings > Uni Spread`

 
(479, 713)
 `Matrix Routing Slot Assignment > Voices Uni Settings > Uni Spread`

 
(210, 1047)
 `Matrix Routing Slot Assignment > Wheel Settings > Vibrato Rate`


(481, 627)
`Voices Settings Poly/Para Menu > Glide Mode`


(480, 664)
`Voices Settings Poly/Para Menu > Allocation`


(474, 700)
`Voices Settings Poly/Para Menu > Note Steal`


(1427, 712)
`CycEnv Settings Menu`


(1351, 626)
 `CycEnv Env Settings Tab > Retrig Menu`

 
(1350, 665)
 `CycEnv Env Settings Tab > Rise Curve`

 
(1353, 701)
 `CycEnv Env Settings Tab > Fall Curve`


(1411, 617)
 CycEnv Run Settings > Tempo Sync


(1350, 646)
 CycEnv Run Settings > Stage Order


(1349, 680)
 CycEnv Run Settings > Rise Curve


(1348, 707)
 CycEnv Run Settings > Fall Curve


(1412, 612)
 CycEnv Loop Settings > Tempo Sync


(1352, 637)
`CycEnv Loop Settings Menu > Retrig`


(1346, 659)
`CycEnv Loop Settings Menu > Stage Order`


(1347, 686)
`CycEnv Loop Settings Menu > Rise Curve`


(1346, 715)
`CycEnv Loop Settings Menu > Fall Curve`


(1327, 586)
 `CycEnv Settings Tab > Mode`


(1427, 585)
`CycEnv Settings Menu > Close Menu`


(523, 587)
`Voices Settings Menu > Close Menu`


(1882, 713)
`Envelope Settings Menu`


(1631, 619)
`Envelope Settings Menu > Attack Curve`


(1625, 647)
`Envelope Settings Menu > Decay Curve`


(1626, 678)
`Envelope Settings Menu > Release Curve`


(1836, 620)
`Envelope Settings Menu > Vel > VCA`


(1836, 650)
`Envelope Settings Menu > Vel > VCF`


(1836, 677)
`Envelope Settings Menu > Vel > ENV`


(1835, 708)
`Envelope Settings Menu > Vel > TIME`


(1882, 586)
`Envelope Settings Menu > Vel > Menu Close`


(1653, 586)
 Envelope Settings Menu > Retrig Menu


(165, 948)
`Wheels Settings Menu`


(239, 1005)
`Wheels Settings Menu > Vibrato on/off`


(210, 1047)
`Wheels Settings Menu > Vibrato Rate`


(209, 1091)
`Wheels Settings Menu > Vibrato Depth`


(209, 1134)
`Wheels Settings Menu > Bend Range`


(163, 1241)
`Wheels Settings Menu > Close Menu`


(1103, 893)
`Macro/Matrix`


 (61, 649)
 `Chord Octave Select Down`


 (266, 650)
 `Chord Octave Select Up`


 (92, 651)
 `Chord Selection > C`


 (101, 624)
 `Chord Selection > C Sharp`


 (113, 648)
 `Chord Selection > D`


 (125, 623)
 `Chord Selection > D Sharp`


 (140, 649)
 `Chord Selection > E`


 (163, 648)
 `Chord Selection > F`


 (173, 624)
 `Chord Selection > F Sharp`


 (186, 648)
 `Chord Selection > G`


 (199, 625)
 `Chord Selection > G Sharp`


 (211, 648)
 `Chord Selection > A`


 (220, 623)
 `Chord Selection > A Sharp`


 (235, 648)
 `Chord Selection > B`


 (60, 707)
 `Chord Selection > -5`


 (82, 708)
 `Chord Selection > -4`


 (101, 706)
 `Chord Selection > -3`


 (124, 708)
 `Chord Selection > -2`


 (142, 709)
 `Chord Selection > -1`


 (162, 708)
 `Chord Selection > 0`


 (183, 709)
 `Chord Selection > 1`


 (204, 708)
 `Chord Selection > 2`


 (223, 708)
 `Chord Selection > 3`


 (245, 710)
 `Chord Selection > 4`


 (266, 709)
 `Chord Selection > 5`


 (83, 543)
 `Chord tab select`


 (243, 541)
 `Scale tab select`


 (97, 675)
 `Scale Selection > C`


 (109, 649)
 `Scale Selection > C Sharp`


 (119, 674)
 `Scale Selection > D`


 (132, 646)
 `Scale Selection > D Sharp`


 (141, 673)
 `Scale Selection > E`


 (160, 675)
 `Scale Selection > F`


 (174, 647)
 `Scale Selection > F Sharp`


 (183, 673)
 `Scale Selection > G`


 (195, 648)
 `Scale Selection > G Sharp`


 (202, 673)
 `Scale Selection > A`


 (216, 649)
 `Scale Selection > A Sharp`


 (225, 674)
 `Scale Selection > B`


 (98, 773)
 `Chord on/off`


 (168, 776)
 `Chord Root Menu`


 (226, 771)
 `Scale Mode Menu`


 (422, 1032)
 `Macro 1 > Parameter 1`


 (425, 1094)
 `Macro 1 > Parameter 2`


 (434, 1151)
 `Macro 1 > Parameter 3`


 (439, 1212)
 `Macro 1 > Parameter 4`


 (718, 1032)
 `Macro 2 > Parameter 1`


 (710, 1094)
 `Macro 2 > Parameter 2`


 (711, 1153)
 `Macro 2 > Parameter 3`


 (715, 1215)
 `Macro 2 > Parameter 4`


 (549, 1032)
 `Macro 1 > Amount 1`


 (551, 1089)
 `Macro 1 > Amount 2`


 (552, 1151)
 `Macro 1 > Amount 3`


 (552, 1210)
 `Macro 1 > Amount 4`


 (843, 1031)
 `Macro 2 > Amount 1`


 (841, 1090)
 `Macro 2 > Amount 2`


 (842, 1153)
 `Macro 2 > Amount 3`


 (842, 1211)
 `Macro 2 > Amount 4`


 (1089, 1046)
 `Matrix Mod 1:1`


 (1088, 1231)
 `Matrix Mod 7:1`


 (1764, 1043)
 `Matrix Mod 1:13`


 (1763, 1230)
 `Matrix Mod 7:13`


 (1326, 1003)
 `Custom Matrix Slot 1`


 (1386, 998)
 `Custom Matrix Slot 2`


 (1444, 998)
 `Custom Matrix Slot 3`


 (1496, 1001)
 `Custom Matrix Slot 4`


 (1556, 997)
 `Custom Matrix Slot 5`


 (1607, 1009)
 `Custom Matrix Slot 6`


 (1664, 1003)
 `Custom Matrix Slot 7`


 (1724, 1000)
 `Custom Matrix Slot 8`


 (1782, 1000)
 `Custom Matrix Slot 9`


 (1505, 366)
 `Reverb/Delay > Insert Mode`


 (1558, 369)
 `Reverb/Delay > Send Mode`


 (97, 432)
 `Matrix Routing Slot Assignment > Osc 1 Tune`

)

 (195, 431)
 `Matrix Routing Slot Assignment > Osc 1 Interval`


 (195, 431)
 `Matrix Routing Slot Assignment > Osc 1 Wave`


 (292, 430)
 `Matrix Routing Slot Assignment > Osc 1 Timbre`


 (380, 431)
 `Matrix Routing Slot Assignment > Osc 1 Shape`


 (474, 432)
 `Matrix Routing Slot Assignment > Osc 1 Volume`


 (627, 432)
 `Matrix Routing Slot Assignment > Osc 2 Tune`


 (725, 431)
 `Matrix Routing Slot Assignment > Osc 2 Wave`


 (818, 433)
 `Matrix Routing Slot Assignment > Osc 2 Timbre`


 (907, 428)
 `Matrix Routing Slot Assignment > Osc 2 Shape`


 (999, 433)
 `Matrix Routing Slot Assignment > Osc 2 Volume`


 (468, 198)
 `Matrix Routing Slot Assignment > Osc 1 Type`


 (1001, 197)
 `Matrix Routing Slot Assignment > Osc 2 Type`


 (1169, 431)
 `Matrix Routing Slot Assignment > Analog Filter Cutoff`


 (1269, 433)
 `Matrix Routing Slot Assignment > Analog Filter Reso`


 (1374, 430)
 `Matrix Routing Slot Assignment > Analog Filter Env Amt`


 (1640, 428)
 `Matrix Routing Slot Assignment > FX Time`



 (1729, 432)
 `Matrix Routing Slot Assignment > FX Intensity5`


 (1729, 432)
 `Matrix Routing Slot Assignment > FX Intensity`


 (1827, 431)
 `Matrix Routing Slot Assignment > FX Amount`


 (470, 776)
 `Matrix Routing Slot Assignment > Glide`


 (639, 773)
 `Matrix Routing Slot Assignment > LFO1 Rate`


 (900, 774)
 `Matrix Routing Slot Assignment > LFO2 Rate`


 (741, 776)
 `Matrix Routing Slot Assignment > LFO1 Wave`


 (1003, 773)
 `Matrix Routing Slot Assignment > LFO2 Wave`


 (1165, 774)
 `Matrix Routing Slot Assignment > CycEnv Rise`


 (1272, 777)
 `Matrix Routing Slot Assignment > CycEnv Fall`


 (1376, 777)
 `Matrix Routing Slot Assignment > CycEnv Hold`


 (1540, 774)
 `Matrix Routing Slot Assignment > Env Attack`


 (1637, 777)
 `Matrix Routing Slot Assignment > Env Decay`


 (1735, 776)
 `Matrix Routing Slot Assignment > Env Sustain`


 (1837, 776)
 `Matrix Routing Slot Assignment > Env Release`


 (1389, 1283)
 `Brightness`


 (1524, 1285)
 `Timbre`


 (1470, 897)
 `LFO Shaper`


 (410, 955)
 `LFO Shaper > LFO1 Tab select`


 (549, 953)
 `LFO Shaper > LFO2 Tab select`


 (466, 999)
 `LFO Shaper > Reset Shaper`


 (556, 1042)
 `LFO Shaper > Grid Length`


 (549, 1085)
 `LFO Shaper > Rate`


 (401, 1162)
 `LFO Shaper > Slope Upward`


 (492, 1164)
 `LFO Shaper > Slope Downward`


 (398, 1204)
 `LFO Shaper > Curve`


 (496, 1207)
 `LFO Shaper > Flat`


 (563, 1191)
 `LFO Shaper > Amplitude`


 (725, 1097)
 `LFO Shaper > Time Segment 1`


 (1761, 1093)
 `LFO Shaper > Time Segment 16`


 (691, 1097)
 `LFO Shaper > Canvas Border Left`


 (1796, 1092)
 `LFO Shaper > Canvas Border Right`


 (734, 969)
 `LFO Shaper > Eraser Button Height`


 (1043, 1094)
 `LFO Shaper > Canvas Mid Height`


 (99, 265)
 `Sequencer > on/off`


 (182, 260)
 `Sequencer > Arpeggiator on/off`


 (265, 261)
 `Sequencer > Sequencer on/off`


 (401, 259)
 `Sequencer > Arpegggiator Up on/off`


 (472, 262)
 `Sequencer > Arpegggiator Down on/off`


 (544, 261)
 `Sequencer > Arpegggiator Up/Down on/off`


 (619, 262)
 `Sequencer > Arpegggiator Random on/off`


 (688, 262)
 `Sequencer > Arpegggiator Order on/off`


 (759, 266)
 `Sequencer > Arpegggiator Poly on/off`


 (831, 262)
 `Sequencer > Arpegggiator Walk on/off`


 (906, 264)
 `Sequencer > Arpegggiator Pattern on/off`


 (976, 263)
 `Sequencer > Arpegggiator Oct1 on/off`


 (1044, 261)
 `Sequencer > Arpegggiator Oct2 on/off`


 (1114, 263)
 `Sequencer > Arpegggiator Oct3 on/off`


 (1188, 263)
 `Sequencer > Arpegggiator Oct4 on/off`


 (1257, 260)
 `Sequencer > Arpegggiator Repeat on/off`


 (1322, 261)
 `Sequencer > Arpegggiator Ratchet on/off`


 (1399, 266)
 `Sequencer > Arpegggiator Rand Oct on/off`


 (1474, 261)
 `Sequencer > Arpegggiator Mutate on/off`


 (1588, 263)
 `Sequencer > Gate`


 (1641, 262)
 `Sequencer > Spice`


 (1588, 237)
 `Sequencer > Gate Top`


 (1586, 288)
 `Sequencer > Gate Bottom`


 (1639, 238)
 `Sequencer > Spice Top`


 (1640, 287)
 `Sequencer > Spice Bottom`


 (1695, 260)
 `Sequencer > Roll Dice`


 (1782, 266)
 `Sequencer > Swing`


 (1840, 192)
 `Sequencer > Tempo`


 (1855, 264)
 `Sequencer > TimeDiv`


 (1830, 240)
 `Sequencer > TimeDiv Up Button`


 (1828, 296)
 `Sequencer > TimeDiv Down Button`


 (637, 264)
 `Sequencer > Sequencer Auto Play`


 (723, 263)
 `Sequencer > Sequencer Overdub`


 (808, 259)
 `Sequencer > Sequencer Play/Stop`


 (894, 262)
 `Sequencer > Sequencer Record`


 (980, 259)
 `Sequencer > Sequencer Modulation`


 (1051, 276)
 `Sequencer > Sequencer 1 Bar`


 (1148, 259)
 `Sequencer > Sequencer 2 Bar`


 (1231, 263)
 `Sequencer > Sequencer 3 Bar`


 (1315, 264)
 `Sequencer > Sequencer 4 Bar`


 (1879, 923)
 `Sequencer > Scroll Bar C-2 + C-1`


 (1880, 737)
 `Sequencer > Scroll Bar C1 C2`


 (1880, 605)
 `Sequencer > Scroll Bar C4 C5`


 (1880, 472)
 `Sequencer > Scroll Bar C7 C8`


 (286, 929)
 `Sequencer > Add Note Segment 1 Low`


 (289, 413)
 `Sequencer > Add Note Segment 1 High`


 (1818, 407)
 `Sequencer > Add Note Segment 16 High`


 (1828, 929)
 `Sequencer > Add Note Segment 16 Low`


 (291, 1043)
 `Sequencer > Segment 1 Modulation Level Top`


 (291, 1204)
 `Sequencer > Segment 1 Modulation Level Bottom`


 (1835, 1046)
 `Sequencer > Segment 16 Modulation Level Top`



 (1833, 1205)
 `Sequencer > Segment 16 Modulation Level Bottom`


 (141, 1042)
 `Sequencer > Mod Type Row 1`


 (137, 1095)
 `Sequencer > Mod Type Row 2`


 (139, 1148)
 `Sequencer > Mod Type Row 3`


 (138, 1206)
 `Sequencer > Mod Type Row 4`


 (87, 1043)
 `Sequencer > Auto Smooth Toggle Row 1 `


 (88, 1097)
 `Sequencer > Auto Smooth Toggle Row 2 `


 (89, 1149)
 `Sequencer > Auto Smooth Toggle Row 3 `


 (88, 1203)
 `Sequencer > Auto Smooth Toggle Row 4 `
"""
    