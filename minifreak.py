from enum import Enum
from typing import Union

from pywinauto import Application, mouse
import mido

from options import *


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
    hold = 64


class Midi_Buttons(Enum):
    note_on = auto()
    note_off = auto()

class MiniFreak:

    def __init__(
            self, 
            executable_path="C:\Program Files\Arturia\MiniFreak V\MiniFreak V.exe",
            outport_name="loopMIDI Port 1",
            L=4,
            T=23,
            R=1946,
            B=1318,
            affordances='midi_toggle midi_slider midi_cc_toggle click_select click_toggle click_hold_toggle click_refresh click_cycle click_dropdown click_slider'
    ):
        self.app = Application()
        self.executable_path = executable_path
        self.outport_name = outport_name
        self.affordances = Enum('affordances', names=affordances)
        for affordance in self.affordances:
            v = []
            setattr(self, f"_{affordance.name}_unf", v)
        self.L = L
        self.T = T 
        self.R = R
        self.B = B        


    def _add_action(self, x_coord, y_coord, afford, *conditions):
        x_norm = (x_coord - self.L) / (self.R - self.L)
        y_norm = (y_coord - self.T) / (self.B - self.T)
        if   afford is self.affordances.midi_toggle:
            self._midi_toggle_unf.append(afford, )
        elif afford is self.affordances.midi_slider:
            self._midi_slider_unf.append((afford, conditions[0]))
        elif afford is self.affordance.midi_cc_toggle:
            self._midi_cc_toggle_unf.append((f"{afford}_on", conditions[0]))
            self._midi_cc_toggle_unf.append((f"{afford}_off", conditions[0]))
        elif afford is self.affordances.click_select:
            value, paths = conditions[0], conditions[1:]
        elif afford is self.affordances.click_toggle:
            paths = conditions
        elif afford is self.affordances.click_hold_toggle:
            paths = conditions
        elif afford is self.affordances.click_refresh:
            paths = conditions
        elif afford is self.affordances.click_cycle:
            pass
        elif afford is self.affordances.click_dropdown:
            menu, paths = conditions[0], conditions[1:]
        elif afford is self.affordances.click_slider:
            ticks, paths = conditions[0], conditions[1:]

    def _finalize_actions(self):
        


    def __enter__(self):
        self.app.start(self.executable_path)
        self._outport = mido.open_output(self.outport_name)         
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.app.kill()
        self._outport.close()
        return False
    
    def _send(self, elt, **kwargs):
        if isinstance(self._outport, mido.ports.BaseOutput) and not self._outport.closed:
            if elt in Midi_Sliders:
                self._outport.send(mido.Message("control_change", control=elt.value, **kwargs))
            elif elt in Midi_Toggleable_Buttons:
                self._outport.send(mido.Message(elt.name, **kwargs))

    def note(self, note, velocity, release=False):
        self._send(
            Midi_Toggleable_Buttons.note_off if release else Midi_Toggleable_Buttons.note_on, 
            note=note, 
            velocity=velocity)

    def hold(self, release=False):
        self._send(Midi_Toggleable_Buttons.hold, value=(0 if release else 127))

    def set(self, elt: Midi_Sliders, value):
        self._send(elt, value=value)


class Clickable_Openable_Tabs(Enum):
    advanced = norm_coord(1586, 102, primary_tabs.Advanced, ())
    sequencer = norm_coord(1716, 103, primary_tabs.Sequencer, ())
    fx1 = norm_coord(1598, 200, fx_tabs.FX_1, (Options.primary_advanced, Options.fx_2_3))
    fx2 = norm_coord(1718, 197, fx_tabs.FX_2, (Options.primary_advanced, Options.fx_1_3,))
    fx3 = norm_coord(1840, 198, fx_tabs.FX_3, (Options.primary_advanced, Options.fx_1_2,))
    chord = norm_coord(83, 543, chord_scale_tabs.Chord, (Options.primary_advanced,))
    scale = norm_coord(243, 541, chord_scale_tabs.Scale, (Options.primary_advanced,))
    settings_voices = norm_coord(524, 712, voices_panel.settings, (Options.primary_advanced,))
    settings_cycenv = norm_coord(1427, 712, cycenv_panel.settings, (Options.primary_advanced,))
    settings_envelope = norm_coord(1882, 713, env_panel.settings, (Options.primary_advanced,))
    settings_wheels = norm_coord(165, 948, wheels_panel.settings, (Options.primary_advanced,))
    macros_matrix = norm_coord(1103, 893, secondary_tabs.Macro__slash__Matrix, (Options.primary_advanced,))
    lfo_shaper = norm_coord(1470, 897, secondary_tabs.LFO_Shaper, (Options.primary_advanced,))
    lfo1_lfo_shaper = norm_coord(410, 955, lfo_tabs.LFO_1, (Options.primary_advanced, Options.secondary_shaper,))
    lfo2_lfo_shaper = norm_coord(549, 953, lfo_tabs.LFO_2, (Options.primary_advanced, Options.secondary_shaper,))

class Clickable_Closable_Tabs(Enum):
    settings_voices = norm_coord(523, 587, voices_panel.controls, (Options.primary_advanced, Options.stg_voices))
    settings_cycenv = norm_coord(1427, 585, cycenv_panel.controls, (Options.primary_advanced, Options.stg_cycenv))
    settings_envelope = norm_coord(1882, 586, env_panel.controls, (Options.primary_advanced, Options.stg_env,))
    settings_wheels = norm_coord(163, 1241, wheels_panel.controls, (Options.primary_advanced, Options.stg_wheels,))

class Clickable_Toggleable_Buttons(Enum):
    fx1 = norm_coord(1556, 199, (Options.primary_advanced,))
    fx2 = norm_coord(1677, 199, (Options.primary_advanced,))
    fx3 = norm_coord(1799, 199, (Options.primary_advanced,))
    tempo_sync_settings_run_cycenv = norm_coord(1411, 617, (Options.primary_advanced, Options.stg_cycenv, cycenv_modes.Run))
    tempo_sync_settings_loop_cycenv = norm_coord(1412, 612, (Options.primary_advanced, Options.stg_cycenv, cycenv_modes.Loop,))
    vibrato_settings_wheels = norm_coord(239, 1005, (Options.primary_advanced, Options.stg_wheels,))
    legato_settings_mono_voices = norm_coord(510, 689, (Options.primary_advanced, Options.stg_voices, voice_modes.Mono,))
    legato_settings_uni_voices = norm_coord(510, 636, (Options.primary_advanced, Options.stg_voices, voice_modes.Unison,))
    c_chord_selection = norm_coord(92, 651, (Options.primary_advanced, Options.chord_tab,))
    c_shp_chord_selection = norm_coord(101, 624, (Options.primary_advanced, Options.chord_tab,))
    d_chord_selection = norm_coord(113, 648, (Options.primary_advanced, Options.chord_tab,))
    d_shp_chord_selection = norm_coord(125, 623, (Options.primary_advanced, Options.chord_tab,))
    e_chord_selection = norm_coord(140, 649, (Options.primary_advanced, Options.chord_tab,))
    f_chord_selection = norm_coord(163, 648, (Options.primary_advanced, Options.chord_tab,))
    f_shp_chord_selection = norm_coord(173, 624, (Options.primary_advanced, Options.chord_tab,))
    g_chord_selection = norm_coord(186, 648, (Options.primary_advanced, Options.chord_tab,))
    g_shp_chord_selection = norm_coord(199, 625, (Options.primary_advanced, Options.chord_tab,))
    a_chord_selection = norm_coord(211, 648, (Options.primary_advanced, Options.chord_tab,))
    a_shp_chord_selection = norm_coord(220, 623, (Options.primary_advanced, Options.chord_tab,))
    b_chord_selection = norm_coord(235, 648, (Options.primary_advanced, Options.chord_tab,))
    c_scale_selection = norm_coord(97, 675, (Options.primary_advanced, Options.scale_tab,))
    c_shp_scale_selection = norm_coord(109, 649, (Options.primary_advanced, Options.scale_tab,))
    d_scale_selection = norm_coord(119, 674, (Options.primary_advanced, Options.scale_tab,))
    d_shp_scale_selection = norm_coord(132, 646, (Options.primary_advanced, Options.scale_tab,))
    e_scale_selection = norm_coord(141, 673, (Options.primary_advanced, Options.scale_tab,))
    f_scale_selection = norm_coord(160, 675, (Options.primary_advanced, Options.scale_tab,))
    f_shp_scale_selection = norm_coord(174, 647, (Options.primary_advanced, Options.scale_tab,))
    g_scale_selection = norm_coord(183, 673, (Options.primary_advanced, Options.scale_tab,))
    g_shp_scale_selection = norm_coord(195, 648, (Options.primary_advanced, Options.scale_tab,))
    a_scale_selection = norm_coord(202, 673, (Options.primary_advanced, Options.scale_tab,))
    a_shp_scale_selection = norm_coord(216, 649, (Options.primary_advanced, Options.scale_tab,))
    b_scale_selection = norm_coord(225, 674, (Options.primary_advanced, Options.scale_tab,))
    chord = norm_coord(98, 773, (Options.primary_advanced,))
    rand_oct_arp = norm_coord(1399, 266, (Options.primary_sequencer, Options.seq_arp_arp,))
    row_1_auto_smooth_seq = norm_coord(87, 1043, (Options.primary_sequencer,))
    row_2_auto_smooth_seq = norm_coord(88, 1097, (Options.primary_sequencer,))
    row_3_auto_smooth_seq = norm_coord(89, 1149, (Options.primary_sequencer,))
    row_4_auto_smooth_seq = norm_coord(88, 1203, (Options.primary_sequencer,))
    autoplay_seq = norm_coord(637, 264, (Options.primary_sequencer, Options.seq_arp_seq,))
    overdub_seq = norm_coord(723, 263, (Options.primary_sequencer, Options.seq_arp_seq,))
    pause_play_seq = norm_coord(808, 259, (Options.primary_sequencer, Options.seq_arp_seq,))
    record_seq = norm_coord(894, 262, (Options.primary_sequencer, Options.seq_arp_seq,))

class Clickable_Single_Select_Single_Option_Buttons(Enum):
    sub_5_chord_oct = norm_coord(60, 707, chord_octaves.__minus__5, (Options.primary_advanced, Options.chord_tab,))
    sub_4_chord_oct = norm_coord(82, 708, chord_octaves.__minus__4, (Options.primary_advanced, Options.chord_tab,))
    sub_3_chord_oct = norm_coord(101, 706, chord_octaves.__minus__3, (Options.primary_advanced, Options.chord_tab,))
    sub_2_chord_oct = norm_coord(124, 708, chord_octaves.__minus__2, (Options.primary_advanced, Options.chord_tab,))
    sub_1_chord_oct = norm_coord(142, 709, chord_octaves.__minus__1, (Options.primary_advanced, Options.chord_tab,))
    mid_0_chord_oct = norm_coord(162, 708, chord_octaves._0, (Options.primary_advanced, Options.chord_tab,))
    sup_1_chord_oct = norm_coord(183, 709, chord_octaves.__plus__1, (Options.primary_advanced, Options.chord_tab,))
    sup_2_chord_oct = norm_coord(204, 708, chord_octaves.__plus__1, (Options.primary_advanced, Options.chord_tab,))
    sup_3_chord_oct = norm_coord(223, 708, chord_octaves.__plus__1, (Options.primary_advanced, Options.chord_tab,))
    sup_4_chord_oct = norm_coord(245, 710, chord_octaves.__plus__1, (Options.primary_advanced, Options.chord_tab,))
    sup_5_chord_oct = norm_coord(266, 709, chord_octaves.__plus__1, (Options.primary_advanced, Options.chord_tab,))
    arp_and_seq_off = norm_coord(99, 265, sequencer_arpeggiator_modes.Off, (Options.primary_sequencer,))
    arp_on_seq = norm_coord(182, 260, sequencer_arpeggiator_modes.Arp, (Options.primary_sequencer,))
    seq_on_seq = norm_coord(265, 261, sequencer_arpeggiator_modes.Seq, (Options.primary_sequencer,))
    up_arp_seq = norm_coord(401, 259, arpeggiator_progression_modes.Up, (Options.primary_sequencer, Options.seq_arp_arp,))
    down_arp_seq = norm_coord(472, 262, arpeggiator_progression_modes.Down, (Options.primary_sequencer, Options.seq_arp_arp,))
    up_and_down_arp_seq = norm_coord(544, 261, arpeggiator_progression_modes.Up__slash__Down, (Options.primary_sequencer, Options.seq_arp_arp,))
    random_arp_seq = norm_coord(619, 262, arpeggiator_progression_modes.Random, (Options.primary_sequencer, Options.seq_arp_arp,))
    order_arp_seq = norm_coord(688, 262, arpeggiator_progression_modes.Order, (Options.primary_sequencer, Options.seq_arp_arp,))
    poly_arp_seq = norm_coord(759, 266, arpeggiator_progression_modes.Poly, (Options.primary_sequencer, Options.seq_arp_arp,))
    walk_arp_seq = norm_coord(831, 262, arpeggiator_progression_modes.Walk, (Options.primary_sequencer, Options.seq_arp_arp,))
    pattern_arp_seq = norm_coord(906, 264, arpeggiator_progression_modes.Pattern, (Options.primary_sequencer, Options.seq_arp_arp,))
    oct1_arp_seq = norm_coord(976, 263, arpeggiator_octave_modes.Oct1, (Options.primary_sequencer, Options.seq_arp_arp,))
    oct2_arp_seq = norm_coord(1044, 261, arpeggiator_octave_modes.Oct2, (Options.primary_sequencer, Options.seq_arp_arp,))
    oct3_arp_seq = norm_coord(1114, 263, arpeggiator_octave_modes.Oct3, (Options.primary_sequencer, Options.seq_arp_arp,))
    oct4_arp_seq = norm_coord(1188, 263, arpeggiator_octave_modes.Oct4, (Options.primary_sequencer, Options.seq_arp_arp,))
    send_reverb_delay = norm_coord(1558, 369, ("",))
    insert_reverb_delay = norm_coord(1505, 366, ("",))
    param_1_macro_1 = norm_coord(422, 1032, routing_slot.Macro_1_1, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_2_macro_1 = norm_coord(425, 1094, routing_slot.Macro_1_2, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_3_macro_1 = norm_coord(434, 1151, routing_slot.Macro_1_3, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_4_macro_1 = norm_coord(439, 1212, routing_slot.Macro_1_4, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_1_macro_2 = norm_coord(718, 1032, routing_slot.Macro_2_1, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_2_macro_2 = norm_coord(710, 1094, routing_slot.Macro_2_2, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_3_macro_2 = norm_coord(711, 1153, routing_slot.Macro_2_3, (Options.primary_advanced, Options.secondary_macro_matrix,))
    param_4_macro_2 = norm_coord(715, 1215, routing_slot.Macro_2_4, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_1_customize_matrix = norm_coord(1326, 1003, routing_slot.Matrix_5, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_2_customize_matrix = norm_coord(1386, 998, routing_slot.Matrix_6, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_3_customize_matrix = norm_coord(1444, 998, routing_slot.Matrix_7, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_4_customize_matrix = norm_coord(1496, 1001, routing_slot.Matrix_8, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_5_customize_matrix = norm_coord(1556, 997, routing_slot.Matrix_9, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_6_customize_matrix = norm_coord(1607, 1009, routing_slot.Matrix_10, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_7_customize_matrix = norm_coord(1664, 1003, routing_slot.Matrix_11, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_8_customize_matrix = norm_coord(1724, 1000, routing_slot.Matrix_12, (Options.primary_advanced, Options.secondary_macro_matrix,))
    slot_9_customize_matrix = norm_coord(1782, 1000, routing_slot.Matrix_13, (Options.primary_advanced, Options.secondary_macro_matrix,))
    uni_spread_settings_uni_voices_assign_routing = norm_coord(479, 713, routing_assignments.uni_spread, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    vibrato_rate_settings_wheel_assign_routing = norm_coord(210, 1047, routing_assignments.vibrato_rate, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    type_osc_1_assign_routing = norm_coord(468, 198, routing_assignments.type_osc_1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    tune_osc_1_assign_routing = norm_coord(97, 432, routing_assignments.tune_osc_1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    wave_osc_1_assign_routing = norm_coord(195, 431, routing_assignments.wave_osc_1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    timbre_osc_1_assign_routing = norm_coord(292, 430, routing_assignments.timbre_osc_1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    shape_osc_1_assign_routing = norm_coord(380, 431, routing_assignments.shape_osc_1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    volume_osc_1_assign_routing = norm_coord(474, 432, routing_assignments.volume_osc_1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    type_osc_2_assign_routing = norm_coord(1001, 197, routing_assignments.type_osc_2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    tune_osc_2_assign_routing = norm_coord(627, 432, routing_assignments.tune_osc_2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    wave_osc_2_assign_routing = norm_coord(725, 431, routing_assignments.wave_osc_2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    timbre_osc_2_assign_routing = norm_coord(818, 433, routing_assignments.timbre_osc_2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    shape_osc_2_assign_routing = norm_coord(907, 428, routing_assignments.shape_osc_2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    volume_osc_2_assign_routing = norm_coord(999, 433, routing_assignments.volume_osc_2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    cutoff_filter_assign_routing = norm_coord(1169, 431, routing_assignments.cutoff_filter, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    reso_filter_assign_routing = norm_coord(1269, 433, routing_assignments.reso_filter, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    env_amt_filter_assign_routing = norm_coord(1374, 430, routing_assignments.env_amt_filter, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    time_fx_assign_routing = norm_coord(1640, 428, routing_assignments.time_fx, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    intensity_fx_assign_routing = norm_coord(1729, 432, routing_assignments.intensity_fx, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    amount_fx_assign_routing = norm_coord(1827, 431, routing_assignments.amount_fx, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    glide_assign_routing = norm_coord(470, 776, routing_assignments.glide, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    rate_lfo1_assign_routing = norm_coord(639, 773, routing_assignments.rate_lfo1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    wave_lfo1_assign_routing = norm_coord(741, 776, routing_assignments.wave_lfo1, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    rate_lfo2_assign_routing = norm_coord(900, 774, routing_assignments.rate_lfo2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    wave_lfo2_assign_routing = norm_coord(1003, 773, routing_assignments.wave_lfo2, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    rise_cycenv_assign_routing = norm_coord(1165, 774, routing_assignments.rise_cycenv, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    fall_cycenv_assign_routing = norm_coord(1272, 777, routing_assignments.fall_cycenv, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    hold_cycenv_assign_routing = norm_coord(1376, 777, routing_assignments.hold_cycenv, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    attack_env_assign_routing = norm_coord(1540, 774, routing_assignments.attack_env, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    decay_env_assign_routing = norm_coord(1637, 777, routing_assignments.decay_env, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    sustain_env_assign_routing = norm_coord(1735, 776, routing_assignments.sustain_env, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    release_env_assign_routing = norm_coord(1837, 776, routing_assignments.release_env, (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), (Options.primary_sequencer, Options.mde_routing_seq,))
    up_slope_lfo_shaper = norm_coord(401, 1162, lfo_shapes.up, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
    down_slope_lfo_shaper = norm_coord(492, 1164, lfo_shapes.down, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
    curve_lfo_shaper = norm_coord(398, 1204, lfo_shapes.curve, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
    flat_lfo_shaper = norm_coord(496, 1207, lfo_shapes.flat, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
    lowest_scroll_note_seq = norm_coord(1879, 923, scroll_positions.lowest, (Options.primary_sequencer,))
    lower_scroll_note_seq = norm_coord(1880, 737, scroll_positions.lower, (Options.primary_sequencer,))
    higher_scroll_note_seq = norm_coord(1880, 605, scroll_positions.higher, (Options.primary_sequencer,))
    highest_scroll_note_seq = norm_coord(1880, 472, scroll_positions.highest, (Options.primary_sequencer,))
    mod_src_1_seq = norm_coord(141, 1042, routing_slot.seq_mod_src_1, (Options.primary_sequencer,))
    mod_src_2_seq = norm_coord(137, 1095, routing_slot.seq_mod_src_2, (Options.primary_sequencer,))
    mod_src_3_seq = norm_coord(139, 1148, routing_slot.seq_mod_src_3, (Options.primary_sequencer,))
    mod_src_4_seq = norm_coord(138, 1206, routing_slot.seq_mod_src_4, (Options.primary_sequencer,))
    n_bars_1_seq = norm_coord(1051, 276, n_bars._1_Bar, (Options.primary_sequencer,))
    n_bars_2_seq = norm_coord(1148, 259, n_bars._2_Bar, (Options.primary_sequencer,))
    n_bars_3_seq = norm_coord(1231, 263, n_bars._3_Bar, (Options.primary_sequencer,))
    n_bars_4_seq = norm_coord(1315, 264, n_bars._4_Bar, (Options.primary_sequencer,))

class Clickable_Holdable_Single_Option_Buttons(Enum):
    repeat_arp_seq = norm_coord(1257, 260, (Options.primary_sequencer, Options.seq_arp_arp,))
    ratchet_arp_seq = norm_coord(1322, 261, (Options.primary_sequencer, Options.seq_arp_arp,))
    mutate_arp_seq = norm_coord(1474, 261, (Options.primary_sequencer, Options.seq_arp_arp,))

class Clickable_Nonholdable_Single_Option_Buttons(Enum):
    roll_dice_seq = norm_coord(1695, 260, (Options.primary_sequencer,))
    reset_lfo_shaper = norm_coord(466, 999, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
    incr_time_div_seq = norm_coord(1830, 240, (Options.primary_sequencer, Options.btn_trigger,))
    decr_time_div_seq = norm_coord(1828, 296, (Options.primary_sequencer, Options.btn_trigger,))

class Clickable_Single_Select_Multi_Option_Buttons(Enum):
    rate_type_lfo1 = norm_coord(771, 710, Options.typ_lfo_rate, (Options.primary_advanced,))
    rate_type_lfo2 = norm_coord(1034, 710, Options.typ_lfo_rate, (Options.primary_advanced,))
    rise_curve_settings_env_cycenv = norm_coord(1350, 665, Options.typ_falling_curve, (Options.primary_advanced, Options.stg_cycenv,))
    fall_curve_settings_env_cycenv = norm_coord(1353, 701, Options.typ_falling_curve, (Options.primary_advanced, Options.stg_cycenv,))

class Clickable_Dropdown_Menu_Areas(Enum):
    type_osc_1 = norm_coord(476, 200, (Options.primary_advanced, Options.typ_osc_1,))
    type_osc_2 = norm_coord(1005, 200, (Options.primary_advanced, Options.typ_osc_2,))
    type_filter = norm_coord(1395, 198, (Options.primary_advanced, Options.typ_filter),)
    type_fx = norm_coord(1524, 241, (Options.primary_advanced, Options.tab_fx, Options.typ_fx),)
    presets_fx = norm_coord(1526, 429, ("",))
    mode_voices = norm_coord(421, 711, (Options.primary_advanced, Options.mde_voices,))
    retrigger_lfo1 = norm_coord(689, 711, (Options.primary_advanced, Options.mde_lfo1_retrigger,))
    retrigger_lfo2 = norm_coord(943, 712, (Options.primary_advanced, Options.mde_lfo2_retrigger,))
    mode_cycenv = norm_coord(1193, 712, (Options.primary_advanced, Options.mde_cycenv,))
    retrigger_env = norm_coord(1606, 711, (Options.primary_advanced, Options.mde_env_retrigger,))
    glide_mode_settings_mono_voices = norm_coord(478, 639, (Options.primary_advanced, Options.stg_voices, Options.mono_mode, Options.mde_glide_voices,))
    glide_mode_settings_uni_voices = norm_coord(479, 616, (Options.primary_advanced, Options.stg_voices, Options.uni_mode, Options.mde_glide_voices,))
    uni_mode_settings_uni_voices = norm_coord(478, 662, (Options.primary_advanced, Options.stg_voices, Options.uni_mode, Options.mde_uni_voices,))
    glide_mode_settings_poly_voices = norm_coord(481, 627, (Options.primary_advanced, Options.stg_voices, Options.polypara_mode, Options.mde_glide_voices,))
    allocation_settings_poly_voices = norm_coord(480, 664, (Options.primary_advanced, Options.stg_voices, Options.polypara_mode, Options.mde_allocation_voices,))
    note_steal_settings_poly_voices = norm_coord(474, 700, (Options.primary_advanced, Options.stg_voices, Options.polypara_mode, Options.mde_note_steal_voices,))
    mode_settings_voices = norm_coord(461, 586, (Options.primary_advanced, Options.stg_voices, Options.mde_voices,))
    retrigger_settings_env_cycenv = norm_coord(1351, 626, (Options.primary_advanced, Options.stg_cycenv, Options.env_mode, Options.mde_cycenv_retrigger,))
    stage_order_settings_run_cycenv = norm_coord(1350, 646, (Options.primary_advanced, Options.stg_cycenv, Options.run_mode, Options.mde_stage_order,))
    retrigger_settings_loop_cycenv = norm_coord(1352, 637, (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode, Options.mde_cycenv_retrigger,))
    stage_order_settings_loop_cycenv = norm_coord(1346, 659, (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode, Options.mde_stage_order,))
    mode_settings_cycenv = norm_coord(1327, 586, (Options.primary_advanced, Options.stg_cycenv, Options.mde_cycenv,))
    attack_curve_settings_envelope = norm_coord(1631, 619, (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger, Options.typ_attack_curve,))
    decay_curve_settings_envelope = norm_coord(1625, 647, (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger, Options.typ_falling_curve,))
    release_curve_settings_envelope = norm_coord(1626, 678, (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger, Options.typ_falling_curve,))
    retrigger_settings_env = norm_coord(1653, 586, (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger,))
    chord_root = norm_coord(168, 776, (Options.primary_advanced, Options.mde_name_scale,))
    scale_mode = norm_coord(226, 771, (Options.primary_advanced, Options.mde_scale,))
    rate_lfo_shaper = norm_coord(549, 1085, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos, Options.mde_lfo_shaper_rate,))

class Clickable_Sliders(Enum):
    rise_curve_settings_run_cycenv = norm_coord(1349, 680, ("",))
    fall_curve_settings_run_cycenv = norm_coord(1348, 707, ("",))
    rise_curve_settings_loop_cycenv = norm_coord(1347, 686, ("",))
    fall_curve_settings_loop_cycenv = norm_coord(1346, 715, ("",))
    vel_vca_settings_envelope = norm_coord(1836, 620, ("",))
    vel_vcf_settings_envelope = norm_coord(1836, 650, ("",))
    vel_env_settings_envelope = norm_coord(1836, 677, ("",))
    vel_time_settings_envelope = norm_coord(1835, 708, ("",))
    vibrato_rate_settings_wheels = norm_coord(210, 1047, ("",))
    vibrato_depth_settings_wheels = norm_coord(209, 1091, ("",))
    bend_range_settings_wheels = norm_coord(209, 1134, ("",))
    uni_count_settings_uni_voice = norm_coord(476, 688, ("",))
    uni_spread_settings_uni_voice = norm_coord(479, 712, ("",))
    amount_1_macro_1 = norm_coord(549, 1032, ("",))
    amount_2_macro_1 = norm_coord(551, 1089, ("",))
    amount_3_macro_1 = norm_coord(552, 1151, ("",))
    amount_4_macro_1 = norm_coord(552, 1210, ("",))
    amount_1_macro_2 = norm_coord(843, 1031, ("",))
    amount_2_macro_2 = norm_coord(841, 1090, ("",))
    amount_3_macro_2 = norm_coord(842, 1153, ("",))
    amount_4_macro_2 = norm_coord(842, 1211, ("",))
    brightness = norm_coord(1389, 1283, ("",))
    timbre = norm_coord(1524, 1285, ("",))
    grid_length_lfo_shaper = norm_coord(556, 1042, ("",))
    amplitude_lfo_shaper = norm_coord(563, 1191, ("",))
    swing_seq = norm_coord(1782, 266, ("",))
    tempo_seq = norm_coord(1840, 192, ("",))
    mod_1_1_matrix = norm_coord(1089, 1046, ("",))
    mod_1_2_matrix = norm_coord
    mod_1_3_matrix = norm_coord
    mod_1_4_matrix = norm_coord
    mod_1_5_matrix = norm_coord
    mod_1_6_matrix = norm_coord
    mod_1_7_matrix = norm_coord
    mod_1_8_matrix = norm_coord
    mod_1_9_matrix = norm_coord
    mod_1_10_matrix = norm_coord
    mod_1_11_matrix = norm_coord
    mod_1_12_matrix = norm_coord
    mod_1_13_matrix = norm_coord(1764, 1043, ("",))
    mod_2_1_matrix = norm_coord
    mod_2_2_matrix = norm_coord
    mod_2_3_matrix = norm_coord
    mod_2_4_matrix = norm_coord
    mod_2_5_matrix = norm_coord
    mod_2_6_matrix = norm_coord
    mod_2_7_matrix = norm_coord
    mod_2_8_matrix = norm_coord
    mod_2_9_matrix = norm_coord
    mod_2_10_matrix = norm_coord
    mod_2_11_matrix = norm_coord
    mod_2_12_matrix = norm_coord
    mod_2_13_matrix = norm_coord
    mod_3_1_matrix = norm_coord
    mod_3_2_matrix = norm_coord
    mod_3_3_matrix = norm_coord
    mod_3_4_matrix = norm_coord
    mod_3_5_matrix = norm_coord
    mod_3_6_matrix = norm_coord
    mod_3_7_matrix = norm_coord
    mod_3_8_matrix = norm_coord
    mod_3_9_matrix = norm_coord
    mod_3_10_matrix = norm_coord
    mod_3_11_matrix = norm_coord
    mod_3_12_matrix = norm_coord
    mod_3_13_matrix = norm_coord
    mod_4_1_matrix = norm_coord
    mod_4_2_matrix = norm_coord
    mod_4_3_matrix = norm_coord
    mod_4_4_matrix = norm_coord
    mod_4_5_matrix = norm_coord
    mod_4_6_matrix = norm_coord
    mod_4_7_matrix = norm_coord
    mod_4_8_matrix = norm_coord
    mod_4_9_matrix = norm_coord
    mod_4_10_matrix = norm_coord
    mod_4_11_matrix = norm_coord
    mod_4_12_matrix = norm_coord
    mod_4_13_matrix = norm_coord
    mod_5_1_matrix = norm_coord
    mod_5_2_matrix = norm_coord
    mod_5_3_matrix = norm_coord
    mod_5_4_matrix = norm_coord
    mod_5_5_matrix = norm_coord
    mod_5_6_matrix = norm_coord
    mod_5_7_matrix = norm_coord
    mod_5_8_matrix = norm_coord
    mod_5_9_matrix = norm_coord
    mod_5_10_matrix = norm_coord
    mod_5_11_matrix = norm_coord
    mod_5_12_matrix = norm_coord
    mod_5_13_matrix = norm_coord
    mod_6_1_matrix = norm_coord
    mod_6_2_matrix = norm_coord
    mod_6_3_matrix = norm_coord
    mod_6_4_matrix = norm_coord
    mod_6_5_matrix = norm_coord
    mod_6_6_matrix = norm_coord
    mod_6_7_matrix = norm_coord
    mod_6_8_matrix = norm_coord
    mod_6_9_matrix = norm_coord
    mod_6_10_matrix = norm_coord
    mod_6_11_matrix = norm_coord
    mod_6_12_matrix = norm_coord
    mod_6_13_matrix = norm_coord
    mod_7_1_matrix = norm_coord(1088, 1231, ("",))
    mod_7_2_matrix = norm_coord
    mod_7_3_matrix = norm_coord
    mod_7_4_matrix = norm_coord
    mod_7_5_matrix = norm_coord
    mod_7_6_matrix = norm_coord
    mod_7_7_matrix = norm_coord
    mod_7_8_matrix = norm_coord
    mod_7_9_matrix = norm_coord
    mod_7_10_matrix = norm_coord
    mod_7_11_matrix = norm_coord
    mod_7_12_matrix = norm_coord
    mod_7_13_matrix = norm_coord(1763, 1230, ("",))
    gate_seq = norm_coord(1588, 263, ("",))
    spice_seq = norm_coord(1641, 262, ("",))


class Lfo_Shaper_Canvas(Enum):
    border_left = norm_coord(691, 1097, ("",))
    border_right = norm_coord(1796, 1092, ("",))
    border_mid_height = norm_coord(1043, 1094, ("",))
    border_erase_button_height = norm_coord(734, 969, ("",))

class Sequencer_Note_Display(Enum):
    pass

class Sequencer_Modulation_Display(Enum):
    pass




    
    


"""
BUTTON MAPPING LOG FOR MOUSE MANIPULATION:

(L4, T23, R1946, B1318)


"""
    