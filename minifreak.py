from collections import defaultdict
from enum import Enum
from typing import Union

from pywinauto import Application, mouse
import mido

from options import *


# Midi_*: values are control numbers
class Midi_Slider(Enum):
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

class Midi_Cont_Toggle(Enum):
    hold = 64

class Midi_Disc_Toggle(Enum):
    note = auto()

class Def_Afford(Enum):
    midi_disc_toggle = auto()
    midi_cont_toggle = auto()
    midi_slider = auto()
    click_select = auto()
    click_toggle = auto()
    click_hold_toggle = auto()
    click_refresh = auto()
    click_cycle = auto()
    click_slider = auto()
    click_dropdown = auto()
    click_slider = auto()

class MiniFreak:

    def __init__(
            self, 
            executable_path="C:\Program Files\Arturia\MiniFreak V\MiniFreak V.exe",
            outport_name="loopMIDI Port 1",
            L=4,
            T=23,
            R=1946,
            B=1318,
            affordances=Def_Afford
    ):
        self.app = Application()
        self.executable_path = executable_path
        self.outport_name = outport_name
        self.aff = affordances
        for affordance in self.affordances:
            v = []
            setattr(self, f"_{affordance.name}_unf", v)
        self.L = L
        self.T = T 
        self.R = R
        self.B = B        
        self._add_ui_action(self.aff.click_select, primary_tabs, 
                            [(1586, 102 ), (1716, 103 )])
        self._add_ui_action(self.aff.click_select, fx_tabs,
                            [(1598, 200 ), (1718, 197 ), (1840, 198 )], 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, chord_scale_tabs,
                            [(83  , 543 ), (243 , 541 )],
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, voices_panel, 
                            [(524 , 712 ), (523 , 587 )], 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, cycenv_panel,
                            [(1427, 712 ), (1427, 585 )], 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, env_panel, 
                            [(1882, 713 ), (1882, 586 )],
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, wheels_panel,
                            [(165 , 948 ), (163 , 1241)], 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, secondary_tabs, 
                            [(1103, 893 ), (1470, 897 )], 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, lfo_tabs,
                            [(410 , 955 ), (549 , 953 )],
                            (Options.primary_advanced, Options.secondary_shaper,))
        self._add_ui_action(self.aff.click_select, chord_octaves,
                            [(60  , 707 ), (82  , 708 ), (101 , 706 ), (124 , 708 ), (142 , 709 ), 
                             (162 , 708 ),
                             (183 , 709 ), (204 , 708 ), (223 , 708 ), (245 , 710 ), (266 , 709 ), ],
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_select, sequencer_arpeggiator_modes,
                            [(99  , 265 ), (182 , 260 ), (265 , 261 )], 
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_select, arpeggiator_progression_modes, 
                            [(401 , 259 ), (472 , 262 ), (544 , 261 ), (619 , 262 ), (688 , 262 ), (759 , 266 ), (831 , 262 ), (906 , 264 )],
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_select, arpeggiator_octave_modes,
                            [(976 , 263 ), (1044, 261 ), (1114, 263 ), (1188, 263 )],
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_select, routing_slot,
                            [(422 , 1032), (425 , 1094), (434 , 1151), (439 , 1212),
                             (718 , 1032), (710 , 1094), (711 , 1153), (715 , 1215),
                             (1326, 1003), (1386, 998 ), (1444, 998 ), 
                             (1496, 1001), (1556, 997 ), (1607, 1009), 
                             (1664, 1003), (1724, 1000), (1782, 1000),
                             (141 , 1042), (137 , 1095), (139 , 1148), (138 , 1206)], 
                            (Options.primary_advanced, Options.secondary_macro_matrix,))
        constraints = defaultdict(lambda: (
            (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), 
            (Options.primary_sequencer, Options.mde_routing_seq,),
        ))
        for i in range(18, 21):
            constraints[i] = (
                (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv, Options.fx_1,), 
                (Options.primary_sequencer, Options.mde_routing_seq, Options.fx_1,),
            )
        for i in range(21, 24):
            constraints[i] = (
                (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv, Options.fx_2,), 
                (Options.primary_sequencer, Options.mde_routing_seq, Options.fx_2,),
            )
        for i in range(24, 26):
            constraints[i] = (
                (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv, Options.fx_3,), 
                (Options.primary_sequencer, Options.mde_routing_seq, Options.fx_4,),
            )
        self._add_ui_action(self.aff.click_select, routing_assignments,
                            [(479 , 713 ), (210 , 1047), (468 , 198 ),
                             (97  , 432 ), (195 , 431 ), (292 , 430 ), 
                             (380 , 431 ), (474 , 432 ), (1001, 197 ), 
                             (627 , 432 ), (725 , 431 ), (818 , 433 ), 
                             (907 , 428 ), (999 , 433 ), (1169, 431 ),
                             (1269, 433 ), (1374, 430 ), (1640, 428 ),
                             (1729, 432 ), (1827, 431 ), (1640, 428 ),
                             (1729, 432 ), (1827, 431 ), (1640, 428 ),
                             (1729, 432 ), (1827, 431 ), (470 , 776 ),
                             (639 , 773 ), (900 , 774 ), (741 , 776 ),
                             (1003, 773 ), (1165, 774 ), (1272, 777 ),
                             (1376, 777 ), (1540, 774 ), (1637, 777 ),
                             (1735, 776 ), (1837, 776 )],
                             constraints,
                            )
        send_reverb_delay = norm_coord(1558, 369 , self.aff.click_select,
                            ("",))
        insert_reverb_delay = norm_coord(1505, 366 , self.aff.click_select,
                            ("",))
        self._add_ui_action(self.aff.click_select, lfo_shapes,
                            [(401 , 1162), (492 , 1164), (398 , 1204), (496 , 1207)],
                            (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
        self._add_ui_action(self.aff.click_select, scroll_positions,
                            [(1879, 923 ), (1880, 737 ), (1880, 605 ), (1880, 472 )],
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_select, n_bars,
                            [(1051, 276 ), (1148, 259 ), (1231, 263 ), (1315, 264 )],
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_toggle, "fx1", 
                            (1556, 199 ), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_toggle, "fx2",
                            (1677, 199 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_toggle, "fx3",
                            (1799, 199 ), 
                            (Options.primary_advanced,))
        self._add_ui_action(1411, 617 , self.aff.click_toggle,
                            "tempo_sync_settings_run_cycenv", (Options.primary_advanced, Options.stg_cycenv, cycenv_modes.Run))
        self._add_ui_action(1412, 612 , self.aff.click_toggle,
                            "tempo_sync_settings_loop_cycenv", (Options.primary_advanced, Options.stg_cycenv, cycenv_modes.Loop,))
        self._add_ui_action(239 , 1005, self.aff.click_toggle,
                            "vibrato_settings_wheels", (Options.primary_advanced, Options.stg_wheels,))
        self._add_ui_action(510 , 689 , self.aff.click_toggle,
                            "legato_settings_mono_voices", (Options.primary_advanced, Options.stg_voices, voice_modes.Mono,))
        self._add_ui_action(510 , 636 , self.aff.click_toggle,
                            "legato_settings_uni_voices", (Options.primary_advanced, Options.stg_voices, voice_modes.Unison,))
        self._add_ui_action(92  , 651 , self.aff.click_toggle,
                            "c_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(101 , 624 , self.aff.click_toggle,
                            "c_shp_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(113 , 648 , self.aff.click_toggle,
                            "d_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(125 , 623 , self.aff.click_toggle,
                            "d_shp_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(140 , 649 , self.aff.click_toggle,
                            "e_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(163 , 648 , self.aff.click_toggle,
                            "f_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(173 , 624 , self.aff.click_toggle,
                            "f_shp_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(186 , 648 , self.aff.click_toggle,
                            "g_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(199 , 625 , self.aff.click_toggle,
                            "g_shp_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(211 , 648 , self.aff.click_toggle,
                            "a_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(220 , 623 , self.aff.click_toggle,
                            "a_shp_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(235 , 648 , self.aff.click_toggle,
                            "b_chord_selection", (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(97  , 675 , self.aff.click_toggle,
                            "c_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(109 , 649 , self.aff.click_toggle,
                            "c_shp_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(119 , 674 , self.aff.click_toggle,
                            "d_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(132 , 646 , self.aff.click_toggle,
                            "d_shp_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(141 , 673 , self.aff.click_toggle,
                            "e_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(160 , 675 , self.aff.click_toggle,
                            "f_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(174 , 647 , self.aff.click_toggle,
                            "f_shp_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(183 , 673 , self.aff.click_toggle,
                            "g_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(195 , 648 , self.aff.click_toggle,
                            "g_shp_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(202 , 673 , self.aff.click_toggle,
                            "a_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(216 , 649 , self.aff.click_toggle,
                            "a_shp_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(225 , 674 , self.aff.click_toggle,
                            "b_scale_selection", (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(98  , 773 , self.aff.click_toggle,
                            "chord", (Options.primary_advanced,))
        self._add_ui_action(1399, 266 , self.aff.click_toggle,
                            "rand_oct_arp", (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(87  , 1043, self.aff.click_toggle,
                            "row_1_auto_smooth_seq", (Options.primary_sequencer,))
        self._add_ui_action(88  , 1097, self.aff.click_toggle,
                            "row_2_auto_smooth_seq", (Options.primary_sequencer,))
        self._add_ui_action(89  , 1149, self.aff.click_toggle,
                            "row_3_auto_smooth_seq", (Options.primary_sequencer,))
        self._add_ui_action(88  , 1203, self.aff.click_toggle,
                            "row_4_auto_smooth_seq", (Options.primary_sequencer,))
        self._add_ui_action(637 , 264 , self.aff.click_toggle,
                            "autoplay_seq", (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(723 , 263 , self.aff.click_toggle,
                            "overdub_seq", (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(808 , 259 , self.aff.click_toggle,
                            "pause_play_seq", (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(894 , 262 , self.aff.click_toggle,
                            "record_seq", (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(1257, 260 , self.aff.click_hold_toggle,
                            "repeat_arp_seq", (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(1322, 261 , self.aff.click_hold_toggle,
                            "ratchet_arp_seq", (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(1474, 261 , self.aff.click_hold_toggle,
                            "mutate_arp_seq", (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(1695, 260 , self.aff.click_refresh, 
                            "roll_dice_seq", (Options.primary_sequencer,))
        self._add_ui_action(466 , 999 , self.aff.click_refresh, 
                            "reset_lfo_shaper", (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
        self._add_ui_action(1830, 240 , self.aff.click_refresh, 
                            "incr_time_div_seq", (Options.primary_sequencer, Options.btn_trigger,))
        self._add_ui_action(1828, 296 , self.aff.click_refresh, 
                            "decr_time_div_seq", (Options.primary_sequencer, Options.btn_trigger,))

    def _add_programmed_action(self, afford, **kwargs):
        if   afford is self.affordances.midi_disc_toggle:
            self._midi_disc_toggle_unf.append((afford.name, kwargs))
        elif afford is self.affordances.midi_slider:
            self._midi_slider_unf.append((afford.name, afford.value, kwargs))
        elif afford is self.affordances.midi_cont_toggle:
            self._midi_cont_toggle_unf.append((afford.name, afford.value))

    def _add_ui_action(self, x, y, afford, *conditions):
        x_norm = (x - self.L) / (self.R - self.L)
        y_norm = (y - self.T) / (self.B - self.T)
        if   afford is self.affordances.click_select:
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
        pass


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
            if elt in Midi_Slider:
                self._outport.send(mido.Message("control_change", control=elt.value, **kwargs))
            elif elt in Midi_Toggle:
                self._outport.send(mido.Message(elt.name, **kwargs))

    def note(self, note, velocity, release=False):
        self._send(
            Midi_Toggle.note_off if release else Midi_Toggle.note_on, 
            note=note, 
            velocity=velocity)

    def hold(self, release=False):
        self._send(Midi_Toggle.hold, value=(0 if release else 127))

    def set(self, elt: Midi_Sliders, value):
        self._send(elt, value=value)


class Clickable_Single_Select_Multi_Option_Buttons(Enum):
    rate_type_lfo1 = norm_coord(771, 710 , Options.typ_lfo_rate, (Options.primary_advanced,))
    rate_type_lfo2 = norm_coord(1034, 710 , Options.typ_lfo_rate, (Options.primary_advanced,))
    rise_curve_settings_env_cycenv = norm_coord(1350, 665 , Options.typ_falling_curve, (Options.primary_advanced, Options.stg_cycenv,))
    fall_curve_settings_env_cycenv = norm_coord(1353, 701 , Options.typ_falling_curve, (Options.primary_advanced, Options.stg_cycenv,))

class Clickable_Dropdown_Menu_Areas(Enum):
    type_osc_1 = norm_coord(476, 200 , (Options.primary_advanced, Options.typ_osc_1,))
    type_osc_2 = norm_coord(1005, 200 , (Options.primary_advanced, Options.typ_osc_2,))
    type_filter = norm_coord(1395, 198 , (Options.primary_advanced, Options.typ_filter),)
    type_fx = norm_coord(1524, 241 , (Options.primary_advanced, Options.tab_fx, Options.typ_fx),)
    presets_fx = norm_coord(1526, 429 , ("",))
    mode_voices = norm_coord(421, 711 , (Options.primary_advanced, Options.mde_voices,))
    retrigger_lfo1 = norm_coord(689, 711 , (Options.primary_advanced, Options.mde_lfo1_retrigger,))
    retrigger_lfo2 = norm_coord(943, 712 , (Options.primary_advanced, Options.mde_lfo2_retrigger,))
    mode_cycenv = norm_coord(1193, 712 , (Options.primary_advanced, Options.mde_cycenv,))
    retrigger_env = norm_coord(1606, 711 , (Options.primary_advanced, Options.mde_env_retrigger,))
    glide_mode_settings_mono_voices = norm_coord(478, 639 , (Options.primary_advanced, Options.stg_voices, Options.mono_mode, Options.mde_glide_voices,))
    glide_mode_settings_uni_voices = norm_coord(479, 616 , (Options.primary_advanced, Options.stg_voices, Options.uni_mode, Options.mde_glide_voices,))
    uni_mode_settings_uni_voices = norm_coord(478, 662 , (Options.primary_advanced, Options.stg_voices, Options.uni_mode, Options.mde_uni_voices,))
    glide_mode_settings_poly_voices = norm_coord(481, 627 , (Options.primary_advanced, Options.stg_voices, Options.polypara_mode, Options.mde_glide_voices,))
    allocation_settings_poly_voices = norm_coord(480, 664 , (Options.primary_advanced, Options.stg_voices, Options.polypara_mode, Options.mde_allocation_voices,))
    note_steal_settings_poly_voices = norm_coord(474, 700 , (Options.primary_advanced, Options.stg_voices, Options.polypara_mode, Options.mde_note_steal_voices,))
    mode_settings_voices = norm_coord(461, 586 , (Options.primary_advanced, Options.stg_voices, Options.mde_voices,))
    retrigger_settings_env_cycenv = norm_coord(1351, 626 , (Options.primary_advanced, Options.stg_cycenv, Options.env_mode, Options.mde_cycenv_retrigger,))
    stage_order_settings_run_cycenv = norm_coord(1350, 646 , (Options.primary_advanced, Options.stg_cycenv, Options.run_mode, Options.mde_stage_order,))
    retrigger_settings_loop_cycenv = norm_coord(1352, 637 , (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode, Options.mde_cycenv_retrigger,))
    stage_order_settings_loop_cycenv = norm_coord(1346, 659 , (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode, Options.mde_stage_order,))
    mode_settings_cycenv = norm_coord(1327, 586 , (Options.primary_advanced, Options.stg_cycenv, Options.mde_cycenv,))
    attack_curve_settings_envelope = norm_coord(1631, 619 , (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger, Options.typ_attack_curve,))
    decay_curve_settings_envelope = norm_coord(1625, 647 , (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger, Options.typ_falling_curve,))
    release_curve_settings_envelope = norm_coord(1626, 678 , (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger, Options.typ_falling_curve,))
    retrigger_settings_env = norm_coord(1653, 586 , (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger,))
    chord_root = norm_coord(168, 776 , (Options.primary_advanced, Options.mde_name_scale,))
    scale_mode = norm_coord(226, 771 , (Options.primary_advanced, Options.mde_scale,))
    rate_lfo_shaper = norm_coord(549, 1085, (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos, Options.mde_lfo_shaper_rate,))

class Clickable_Sliders(Enum):
    rise_curve_settings_run_cycenv = norm_coord(1349, 680 , ("",))
    fall_curve_settings_run_cycenv = norm_coord(1348, 707 , ("",))
    rise_curve_settings_loop_cycenv = norm_coord(1347, 686 , ("",))
    fall_curve_settings_loop_cycenv = norm_coord(1346, 715 , ("",))
    vel_vca_settings_envelope = norm_coord(1836, 620 , ("",))
    vel_vcf_settings_envelope = norm_coord(1836, 650 , ("",))
    vel_env_settings_envelope = norm_coord(1836, 677 , ("",))
    vel_time_settings_envelope = norm_coord(1835, 708 , ("",))
    vibrato_rate_settings_wheels = norm_coord(210, 1047, ("",))
    vibrato_depth_settings_wheels = norm_coord(209, 1091, ("",))
    bend_range_settings_wheels = norm_coord(209, 1134, ("",))
    uni_count_settings_uni_voice = norm_coord(476, 688 , ("",))
    uni_spread_settings_uni_voice = norm_coord(479, 712 , ("",))
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
    swing_seq = norm_coord(1782, 266 , ("",))
    tempo_seq = norm_coord(1840, 192 , ("",))
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
    gate_seq = norm_coord(1588, 263 , ("",))
    spice_seq = norm_coord(1641, 262 , ("",))


class Lfo_Shaper_Canvas(Enum):
    border_left = norm_coord(691, 1097, ("",))
    border_right = norm_coord(1796, 1092, ("",))
    border_mid_height = norm_coord(1043, 1094, ("",))
    border_erase_button_height = norm_coord(734, 969 , ("",))

class Sequencer_Note_Display(Enum):
    pass

class Sequencer_Modulation_Display(Enum):
    pass




    
    


"""
BUTTON MAPPING LOG FOR MOUSE MANIPULATION:

(L4, T23, R1946, B1318)


"""
    