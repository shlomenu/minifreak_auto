from collections import defaultdict
from enum import Enum
from typing import Union

from pywinauto import Application, mouse
import mido

from options import *
import options


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
    click_dropdown = auto()
    click_rel_slider = auto()

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
        for affordance in self.aff:
            v = []
            setattr(self, f"_{affordance.name}", v)
        self.L = L
        self.T = T 
        self.R = R
        self.B = B        
        self._add_ui_action(self.aff.click_select, 
                            "primary_tabs", primary_tabs, 
                            ((1586, 102 ), (1716, 103 )))
        self._add_ui_action(self.aff.click_select, 
                            "fx_tabs", fx_tabs,
                            ((1598, 200 ), (1718, 197 ), (1840, 198 )), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, 
                            "chord_scale_tabs", chord_scale_tabs,
                            ((83  , 543 ), (243 , 541 )),
                            (Options.primary_advanced,))
        for name, coords in zip(
            (
                "voices_panel", 
                "cycenv_panel", 
                "env_panel", 
                "wheels_panel"
            ), 
            (
                ((524 , 712 ), (523 , 587 )), 
                ((1427, 712 ), (1427, 585 )), 
                ((1882, 713 ), (1882, 586 )), 
                ((165 , 948 ), (163 , 1241))
            ,)
        ):
            self._add_ui_action(self.aff.click_select, 
                                name, panel, coords, 
                                (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, 
                            "secondary_tabs", secondary_tabs, 
                            ((1103, 893 ), (1470, 897 )), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_select, 
                            "lfo_tabs", lfo_tabs,
                            ((410 , 955 ), (549 , 953 )),
                            (Options.primary_advanced, Options.secondary_shaper,))
        self._add_ui_action(self.aff.click_select, 
                            "chord_octaves", chord_octaves,
                            ((60  , 707 ), (82  , 708 ), (101 , 706 ), (124 , 708 ), (142 , 709 ), 
                             (162 , 708 ),
                             (183 , 709 ), (204 , 708 ), (223 , 708 ), (245 , 710 ), (266 , 709 ), ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_select, 
                            "sequencer_arpeggiator_modes", sequencer_arpeggiator_modes,
                            ((99  , 265 ), (182 , 260 ), (265 , 261 )), 
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_select, 
                            "arpeggiator_progression_modes", arpeggiator_progression_modes, 
                            ((401 , 259 ), (472 , 262 ), (544 , 261 ), (619 , 262 ), (688 , 262 ), (759 , 266 ), (831 , 262 ), (906 , 264 )),
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_select, 
                            "arpeggiator_octave_modes", arpeggiator_octave_modes,
                            ((976 , 263 ), (1044, 261 ), (1114, 263 ), (1188, 263 )),
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_select, 
                            "routing_slot", routing_slot_adv,
                            ((422 , 1032), (425 , 1094), (434 , 1151), (439 , 1212),
                             (718 , 1032), (710 , 1094), (711 , 1153), (715 , 1215),
                             (1326, 1003), (1386, 998 ), (1444, 998 ), 
                             (1496, 1001), (1556, 997 ), (1607, 1009), 
                             (1664, 1003), (1724, 1000), (1782, 1000))
                            (Options.primary_advanced, Options.secondary_macro_matrix))
        self._add_ui_action(self.aff.click_select,
                            "routing_slot", routing_slot_seq,
                            ((141 , 1042), (137 , 1095), (139 , 1148), (138 , 1206)),
                            (Options.primary_sequencer,))
        def rte_asgn(last=None): 
            return (
                (
                    (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv,), 
                    (Options.primary_sequencer, Options.mde_routing_seq,),
                ) if last is None else
                (
                    (Options.primary_advanced, Options.secondary_macro_matrix, Options.mde_routing_adv, last), 
                    (Options.primary_sequencer, Options.mde_routing_seq, last),
                ))
        self._add_ui_action(self.aff.click_select, 
                            "routing_assignments", routing_assignments_always,
                            ((468 , 198 ), (97  , 432 ), (195 , 431 ), 
                             (292 , 430 ), (380 , 431 ), (474 , 432 ), 
                             (1001, 197 ), (627 , 432 ), (725 , 431 ), 
                             (818 , 433 ), (907 , 428 ), (999 , 433 ),
                             (1169, 431 ), (1269, 433 ), (1374, 430 ), 
                             (1640, 428 ), (639 , 773 ), (900 , 774 ), 
                             (741 , 776 ), (1003, 773 ), (1165, 774 ),
                             (1272, 777 ), (1376, 777 ), (1540, 774 ),
                             (1637, 777 ), (1735, 776 ), (1837, 776 )),
                            rte_asgn())
        self._add_ui_action(self.aff.click_select,
                            "routing_assignments", routing_assignments_tab_fx1,
                            ((1729, 432 ), (1827, 431 ), (1640, 428 )),
                            rte_asgn(Options.fx_1))
        self._add_ui_action(self.aff.click_select,
                            "routing_assignments", routing_assignments_tab_fx2,
                            ((1729, 432 ), (1827, 431 ), (1640, 428 )),
                            rte_asgn(Options.fx_2))
        self._add_ui_action(self.aff.click_select,
                            "routing_assignments", routing_assignments_tab_fx3,
                            ((1729, 432 ), (1827, 431 ), (470 , 776 )),
                            rte_asgn(Options.fx_3))
        self._add_ui_action(self.aff.click_select,
                            "routing_assignments", routing_assignments_stg_voices,
                            ((479 , 713 ),),
                            rte_asgn(Options.stg_voices))
        self._add_ui_action(self.aff.click_select,
                            "routing_assignments", routing_assignments_stg_wheels,
                            ((210 , 1047),),
                            rte_asgn(Options.stg_wheels))
        for i in range(1, 4):
            self._add_ui_action(self.aff.click_select,
                                f"send_insert_delay_fx_{i}", effect_mode,
                                ((1558, 369 ), (1505, 366 )),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_delay"],
                                ),))
            self._add_ui_action(self.aff.click_select,
                                f"send_insert_reverb_fx_{i}", effect_mode,
                                ((1558, 369 ), (1505, 366 )),
                                ((
                                    Options.primary_advanced,
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_delay"]
                                ),))
        self._add_ui_action(self.aff.click_select, 
                            "lfo_shapes", lfo_shapes,
                            ((401 , 1162), (492 , 1164), (398 , 1204), (496 , 1207)),
                            (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
        self._add_ui_action(self.aff.click_select, 
                            "scroll_positions", scroll_positions,
                            ((1879, 923 ), (1880, 737 ), (1880, 605 ), (1880, 472 )),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_select, 
                            "n_bars", n_bars,
                            ((1051, 276 ), (1148, 259 ), (1231, 263 ), (1315, 264 )),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_toggle, 
                            "fx1", 
                            (1556, 199 ), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_toggle, 
                            "fx2",
                            (1677, 199 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_toggle, 
                            "fx3",
                            (1799, 199 ), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_toggle, 
                            "tempo_sync_settings_run_cycenv",
                            (1411, 617 ),
                            (Options.primary_advanced, Options.stg_cycenv, cycenv_modes.Run))
        self._add_ui_action(self.aff.click_toggle, 
                            "tempo_sync_settings_loop_cycenv",
                            (1412, 612 ),
                            (Options.primary_advanced, Options.stg_cycenv, cycenv_modes.Loop,))
        self._add_ui_action(self.aff.click_toggle, 
                            "vibrato_settings_wheels",
                            (239 , 1005),
                            (Options.primary_advanced, Options.stg_wheels,))
        self._add_ui_action(self.aff.click_toggle,
                            "legato_settings_mono_voices",
                            (510 , 689 ),
                            (Options.primary_advanced, Options.stg_voices, voice_modes.Mono,))
        self._add_ui_action(self.aff.click_toggle,
                            "legato_settings_uni_voices",
                            (510 , 636 ),
                            (Options.primary_advanced, Options.stg_voices, voice_modes.Unison,))
        self._add_ui_action(self.aff.click_toggle,
                            "c_chord_selection",
                            (92  , 651 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "c_shp_chord_selection",
                            (101 , 624 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "d_chord_selection",
                            (113 , 648 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "d_shp_chord_selection",
                            (125 , 623 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "e_chord_selection",
                            (140 , 649 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "f_chord_selection",
                            (163 , 648 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "f_shp_chord_selection",
                            (173 , 624 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "g_chord_selection",
                            (186 , 648 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "g_shp_chord_selection",
                            (199 , 625 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "a_chord_selection",
                            (211 , 648 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "a_shp_chord_selection",
                            (220 , 623 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "b_chord_selection",
                            (235 , 648 ),
                            (Options.primary_advanced, Options.chord_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "c_scale_selection",
                            (97  , 675 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "c_shp_scale_selection",
                            (109 , 649 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "d_scale_selection",
                            (119 , 674 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "d_shp_scale_selection",
                            (132 , 646 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "e_scale_selection",
                            (141 , 673 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "f_scale_selection",
                            (160 , 675 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "f_shp_scale_selection",
                            (174 , 647 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "g_scale_selection",
                            (183 , 673 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "g_shp_scale_selection",
                            (195 , 648 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "a_scale_selection",
                            (202 , 673 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "a_shp_scale_selection",
                            (216 , 649 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "b_scale_selection",
                            (225 , 674 ),
                            (Options.primary_advanced, Options.scale_tab,))
        self._add_ui_action(self.aff.click_toggle,
                            "chord",
                            (98  , 773 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_toggle,
                            "rand_oct_arp",
                            (1399, 266 ),
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_toggle,
                            "row_1_auto_smooth_seq",
                            (87  , 1043),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_toggle,
                            "row_2_auto_smooth_seq",
                            (88  , 1097),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_toggle,
                            "row_3_auto_smooth_seq",
                            (89  , 1149),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_toggle,
                            "row_4_auto_smooth_seq",
                            (88  , 1203),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_toggle,
                            "autoplay_seq",
                            (637 , 264 ),
                            (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(self.aff.click_toggle,
                            "overdub_seq",
                            (723 , 263 ),
                            (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(self.aff.click_toggle,
                            "pause_play_seq",
                            (808 , 259 ),
                            (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(self.aff.click_toggle,
                            "record_seq",
                            (894 , 262 ),
                            (Options.primary_sequencer, Options.seq_arp_seq,))
        self._add_ui_action(self.aff.click_hold_toggle,
                            "repeat_arp_seq",
                            (1257, 260 ),
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_hold_toggle,
                            "ratchet_arp_seq",
                            (1322, 261 ),
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_hold_toggle,
                            "mutate_arp_seq",
                            (1474, 261 ),
                            (Options.primary_sequencer, Options.seq_arp_arp,))
        self._add_ui_action(self.aff.click_refresh,
                            "roll_dice_seq",
                            (1695, 260 ),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_refresh,
                            "reset_lfo_shaper",
                            (466 , 999 ),
                            (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
        self._add_ui_action(self.aff.click_refresh,
                            "incr_time_div_seq",
                            (1830, 240 ),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_refresh,
                            "decr_time_div_seq",
                            (1828, 296 ),
                            (Options.primary_sequencer,))
        self._add_ui_action(self.aff.click_cycle, 
                            "rate_type_lfo1", Options.typ_lfo_rate, 
                            (771 , 710 ), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_cycle, 
                            "rate_type_lfo2", Options.typ_lfo_rate,
                            (1034, 710 ), 
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_cycle, 
                            "rise_curve_settings_env_cycenv", Options.typ_falling_curve,
                            (1350, 665 ), 
                            (Options.primary_advanced, Options.stg_cycenv,))
        self._add_ui_action(self.aff.click_cycle,
                            "fall_curve_settings_env_cycenv", Options.typ_falling_curve,
                            (1353, 701 ), 
                            (Options.primary_advanced, Options.stg_cycenv,))
        self._add_ui_action(self.aff.click_dropdown,
                            "type_osc_1",
                            osc_1_modes,
                            (476 , 200 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "type_osc_2",
                            osc_2_modes,
                            (1005, 200 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "type_filter",
                            filter_types,
                            (1395, 198 ),
                            (Options.primary_advanced,))
        for i, name, tab_opt, other_name_1, other_name_2 in range(1, 4):
            _1, _2 = tuple(set(range(1, 4)) - set((i,)))
            self._add_ui_action(self.aff.click_dropdown,
                                f"fx{i}_type",
                                fx_types_neither
                                (1524, 241 ),
                                tuple(
                                    (
                                        Options.primary_advanced, 
                                        Options[f"fx_{i}"], 
                                        Options[other_opt_1],
                                        Options[other_opt_2],
                                    ) for other_opt_1, other_opt_2 in zip(
                                        (
                                            f"typ_fx_{_1}_reverb", 
                                            f"typ_fx_{_1}_delay", 
                                            f"typ_fx_{_1}_neither", 
                                            f"typ_fx_{_1}_reverb", 
                                            f"typ_fx_{_1}_neither", 
                                            f"typ_fx_{_1}_delay", 
                                            f"typ_fx_{_1}_neither",
                                        ),
                                        (
                                            f"typ_fx_{_2}_delay", 
                                            f"typ_fx_{_2}_reverb", 
                                            f"typ_fx_{_2}_reverb", 
                                            f"typ_fx_{_2}_neither", 
                                            f"typ_fx_{_2}_delay", 
                                            f"typ_fx_{_2}_neither", 
                                            f"typ_fx_{_2}_neither",
                                        )
                                    )
                                ))
            self._add_ui_action(self.aff.click_dropdown,
                                f"fx{i}_type",
                                fx_types_delay,
                                (1524, 241 ),
                                tuple(
                                    (
                                        Options.primary_advanced, 
                                        Options[f"fx_{i}"],
                                        Options[other_opt_1],
                                        Options[other_opt_2], 
                                    ) for other_opt_1, other_opt_2 in zip(
                                        (
                                            f"typ_fx_{_1}_neither", 
                                            f"typ_fx_{_1}_reverb", 
                                            f"typ_fx_{_1}_neither",
                                        ),
                                        (
                                            f"typ_fx_{_2}_reverb", 
                                            f"typ_fx_{_2}_neither", 
                                            f"typ_fx_{_2}_neither",
                                        )
                                    )
                                ))
            self._add_ui_action(self.aff.click_dropdown,
                                f"fx{i}_type",
                                fx_types_reverb,
                                (1524, 241 ),
                                tuple(
                                    (
                                        Options.primary_advanced, 
                                        Options[f"fx_{i}"], 
                                        Options[other_opt_1], 
                                        Options[other_opt_2],
                                    ) for other_opt_1, other_opt_2 in zip(
                                        (
                                            f"typ_fx_{_1}_neither", 
                                            f"typ_fx_{_1}_delay", 
                                            f"typ_fx_{_1}_neither",
                                        ),
                                        (
                                            f"typ_fx_{_2}_delay", 
                                            f"typ_fx_{_2}_neither", 
                                            f"typ_fx_{_2}_neither",
                                        )
                                    )
                                ))
        for i in range(1, 4):
            self._add_ui_action(self.aff.click_dropdown,
                                f"chorus_presets_fx_{i}", chorus_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_chorus"],
                                ),))
            self._add_ui_action(self.aff.click_dropdown,
                                f"phaser_presets_fx_{i}", phaser_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_phaser"],
                                ),))
            self._add_ui_action(self.aff.click_dropdown,
                                f"flanger_presets_fx_{i}", flanger_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_flanger"],
                                ),))
            self._add_ui_action(self.aff.click_dropdown,
                                f"distortion_presets_fx_{i}", distortion_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_distortion"],
                                ),))
            self._add_ui_action(self.aff.click_dropdown,
                                f"_3_bands_eq_presets_fx_{i}", options._3_bands_eq_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}__3_bands_eq"],
                                ),))
            self._add_ui_action(self.aff.click_dropdown,
                                f"multi_comp_presets_fx_{i}", multi_comp_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_multi_comp"],
                                ),))
            self._add_ui_action(self.aff.click_dropdown,
                                f"superunison_presets_fx_{i}", superunison_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_superunison"],
                                ),))
        self._add_ui_action(self.aff.click_dropdown,
                            "mode_voices",
                            voice_modes,
                            (421 , 711 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "retrigger_lfo1",
                            lfo1_retrigger_modes,
                            (689 , 711 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "retrigger_lfo2",
                            lfo2_retrigger_modes,
                            (943 , 712 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "mode_cycenv",
                            cycenv_modes,
                            (1193, 712 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "retrigger_env",
                            env_retrigger_modes,
                            (1606, 711 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "glide_mode_settings_mono_voices",
                            glide_types,
                            (478 , 639 ),
                            (Options.primary_advanced, Options.stg_voices, Options.mono_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "glide_mode_settings_uni_voices",
                            glide_types,
                            (479 , 616 ),
                            (Options.primary_advanced, Options.stg_voices, Options.uni_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "uni_mode_settings_uni_voices",
                            uni_voice_modes
                            (478 , 662 ),
                            (Options.primary_advanced, Options.stg_voices, Options.uni_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "glide_mode_settings_poly_voices",
                            glide_types,
                            (481 , 627 ),
                            (Options.primary_advanced, Options.stg_voices, Options.polypara_mode))
        self._add_ui_action(self.aff.click_dropdown,
                            "allocation_settings_poly_voices",
                            voice_allocation_modes,
                            (480 , 664 ),
                            (Options.primary_advanced, Options.stg_voices, Options.polypara_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "note_steal_settings_poly_voices",
                            note_steal_modes,
                            (474 , 700 ),
                            (Options.primary_advanced, Options.stg_voices, Options.polypara_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "mode_settings_voices",
                            voice_modes
                            (461 , 586 ),
                            (Options.primary_advanced, Options.stg_voices,))
        self._add_ui_action(self.aff.click_dropdown,
                            "retrigger_settings_env_cycenv",
                            cycenv_retrigger_modes,
                            (1351, 626 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.env_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "stage_order_settings_run_cycenv",
                            stage_orders,
                            (1350, 646 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.run_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "retrigger_settings_loop_cycenv",
                            cycenv_retrigger_modes,
                            (1352, 637 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "stage_order_settings_loop_cycenv",
                            stage_orders,
                            (1346, 659 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode,))
        self._add_ui_action(self.aff.click_dropdown,
                            "mode_settings_cycenv",
                            cycenv_modes,
                            (1327, 586 ),
                            (Options.primary_advanced, Options.stg_cycenv,))
        self._add_ui_action(self.aff.click_dropdown,
                            "attack_curve_settings_envelope",
                            attack_curve_types,
                            (1631, 619 ),
                            (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger,))
        self._add_ui_action(self.aff.click_dropdown,
                            "decay_curve_settings_envelope",
                            falling_curve_types,
                            (1625, 647 ),
                            (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger,))
        self._add_ui_action(self.aff.click_dropdown,
                            "release_curve_settings_envelope",
                            falling_curve_types,
                            (1626, 678 ),
                            (Options.primary_advanced, Options.stg_env, Options.mde_env_retrigger,))
        self._add_ui_action(self.aff.click_dropdown,
                            "retrigger_settings_env",
                            env_retrigger_modes,
                            (1653, 586 ),
                            (Options.primary_advanced, Options.stg_env,))
        self._add_ui_action(self.aff.click_dropdown,
                            "chord_root",
                            notes,
                            (168 , 776 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "scale_mode",
                            scale_modes,
                            (226 , 771 ),
                            (Options.primary_advanced,))
        self._add_ui_action(self.aff.click_dropdown,
                            "rate_lfo_shaper",
                            rate_lfo_shaper
                            (549 , 1085),
                            (Options.primary_advanced, Options.secondary_shaper, Options.tab_lfos,))
        self._add_ui_action(self.aff.click_rel_slider,
                            "rise_curve_settings_run_cycenv",
                            None,
                            (1349, 680 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "rise_curve_settings_run_cycenv",
                            None
                            (1349, 680 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "fall_curve_settings_run_cycenv",
                            None
                            (1348, 707 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "rise_curve_settings_loop_cycenv",
                            None
                            (1347, 686 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "fall_curve_settings_loop_cycenv",
                            None
                            (1346, 715 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "vel_vca_settings_envelope",
                            None
                            (1836, 620 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "vel_vcf_settings_envelope",
                            None
                            (1836, 650 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "vel_env_settings_envelope",
                            None
                            (1836, 677 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "vel_time_settings_envelope",
                            None
                            (1835, 708 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "vibrato_rate_settings_wheels",
                            None
                            (210 , 1047),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "vibrato_depth_settings_wheels",
                            None
                            (209 , 1091),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "bend_range_settings_wheels",
                            None
                            (209 , 1134),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "uni_count_settings_uni_voice",
                            None
                            (476 , 688 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "uni_spread_settings_uni_voice",
                            None
                            (479 , 712 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_1_macro_1",
                            None
                            (549 , 1032),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_2_macro_1",
                            None
                            (551 , 1089),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_3_macro_1",
                            None
                            (552 , 1151),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_4_macro_1",
                            None
                            (552 , 1210),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_1_macro_2",
                            None
                            (843 , 1031),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_2_macro_2",
                            None
                            (841 , 1090),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_3_macro_2",
                            None
                            (842 , 1153),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amount_4_macro_2",
                            None
                            (842 , 1211),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "brightness",
                            None
                            (1389, 1283),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "timbre",
                            None
                            (1524, 1285),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "grid_length_lfo_shaper",
                            None
                            (556 , 1042),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "amplitude_lfo_shaper",
                            None
                            (563 , 1191),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "swing_seq",
                            None
                            (1782, 266 ),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "tempo_seq",
                            None
                            (1840, 192 ),
                            None)
        for i in range(13):
            x = 1088 + i * ((1764 - 1088) / 12)
            for j in range(7):
                y = 1045  + i * ((1231 - 1045) / 6)
                self._add_ui_action(self.aff.click_rel_slider,
                                    f"mod_{i}_{j}_matrix",
                                    None,
                                    (x, y),
                                    (Options.primary_advanced,))
        # LFO_Shaper_Canvas
        self._add_ui_action(self.aff.click_rel_slider,
                            "border_left",
                            None
                            (691 , 1097),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "border_right",
                            None
                            (1796, 1092),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "border_mid_height",
                            None
                            (1043, 1094),
                            None)
        self._add_ui_action(self.aff.click_rel_slider,
                            "border_erase_button_height",
                            None
                            (734 , 969 ),
                            None)
        
    def _add_programmed_action(self, afford, **kwargs):
        if   afford is self.aff.midi_disc_toggle:
            self._midi_disc_toggle.append((afford.name, kwargs))
        elif afford is self.aff.midi_slider:
            kwargs.update(channel=afford.value)
            self._midi_slider.append((afford.name, kwargs))
        elif afford is self.aff.midi_cont_toggle:
            self._midi_cont_toggle.append((afford.name, {"channel": afford.value}))

    def _add_ui_action(self, x, y, afford, *conditions):
        x_norm = (x - self.L) / (self.R - self.L)
        y_norm = (y - self.T) / (self.B - self.T)
        if   afford is self.aff.click_select:
            value, paths = conditions[0], conditions[1:]
        elif afford is self.aff.click_toggle:
            paths = conditions
        elif afford is self.aff.click_hold_toggle:
            paths = conditions
        elif afford is self.aff.click_refresh:
            paths = conditions
        elif afford is self.aff.click_cycle:
            pass
        elif afford is self.aff.click_dropdown:
            menu, paths = conditions[0], conditions[1:]
        elif afford is self.aff.click_rel_slider:
            ticks, paths = conditions[0], conditions[1:]

    def _finalize_actions(self):
        Midi_Disc_Toggle = Enum(
            'Midi_Disc_Toggle', 
            [name for name, _ in self._midi_disc_toggle]
        )
        Midi_Disc_Toggle_spec = dict(zip(
            Midi_Disc_Toggle, 
            [kwargs for _, kwargs in self._midi_disc_toggle]
        ))
        Midi_Cont_Toggle = Enum(
            'Midi_Cont_Toggle',
            [name for name, _ in self._midi_cont_toggle]
        )
        Midi_Cont_Toggle_spec = dict(zip(
            Midi_Cont_Toggle,
            [kwargs for _, kwargs in self._midi_cont_toggle]
        ))
        _Midi_Slider = Enum(
            'Midi_Slider',
            [name for name, _ in self._midi_sliders]
        )
        _Midi_Slider_spec = dict(zip(
            _Midi_Slider,
            [kwargs for _, kwargs in self._midi_sliders]
        ))




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