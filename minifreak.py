from collections import defaultdict
from enum import Enum
import itertools
from typing import Union

from pywinauto import Application, mouse
import mido

from options import *
import options


# Midi_*: values are control numbers
class Mf_Midi_Slider(Enum):
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

class Mf_Midi_Cont_Toggle(Enum):
    hold = 64

class Mf_Midi_Disc_Toggle(Enum):
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

    @classmethod
    def is_programmatic(cls, aff):
        return (
            aff is cls.midi_disc_toggle or aff is cls.midi_cont_toggle or aff is cls.midi_slider
        )
    
    @classmethod
    def is_ui(cls, aff):
        return (
            aff in cls and not cls.is_programmatic(aff)
        ) 

class Toggle_State(Enum):
    On = auto()
    Off = auto()

class Hold_Toggle_State(Enum):
    Held = auto()
    Released = auto()

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
        self.L = L
        self.T = T 
        self.R = R
        self.B = B
        for elt in Mf_Midi_Cont_Toggle:
            self._add_programmatic_affordance(
                self.aff.midi_cont_toggle, 
                elt.name, 
                elt.value,
            )
        for elt in Mf_Midi_Disc_Toggle:
            self._add_programmatic_affordance(
                self.aff.midi_disc_toggle,
                elt.name,
                note=64,
                velocity=64,
            )
        for elt in Mf_Midi_Slider:
            self._add_programmatic_affordance(
                self.aff.midi_slider,
                elt.name,
                elt.value,
            )
        self._add_ui_affordance(self.aff.click_select, 
                            "primary_tabs", primary_tabs, 
                            ((1586, 102 ), (1716, 103 )),
                            (), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "fx_tabs", fx_tabs,
                            ((1598, 200 ), (1718, 197 ), (1840, 198 )), 
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "chord_scale_tabs", chord_scale_tabs,
                            ((83  , 543 ), (243 , 541 )),
                            (Options.primary_advanced,), ())
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
            self._add_ui_affordance(self.aff.click_select, 
                                name, panel, coords, 
                                (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "secondary_tabs", secondary_tabs, 
                            ((1103, 893 ), (1470, 897 )), 
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "lfo_tabs", lfo_tabs,
                            ((410 , 955 ), (549 , 953 )),
                            (Options.primary_advanced, Options.secondary_shaper,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "chord_octaves", chord_octaves,
                            ((60  , 707 ), (82  , 708 ), (101 , 706 ), (124 , 708 ), (142 , 709 ), 
                             (162 , 708 ),
                             (183 , 709 ), (204 , 708 ), (223 , 708 ), (245 , 710 ), (266 , 709 ), ),
                            (Options.primary_advanced, Options.chord_tab,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "sequencer_arpeggiator_modes", sequencer_arpeggiator_modes,
                            ((99  , 265 ), (182 , 260 ), (265 , 261 )), 
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "arpeggiator_progression_modes", arpeggiator_progression_modes, 
                            ((401 , 259 ), (472 , 262 ), (544 , 261 ), (619 , 262 ), (688 , 262 ), (759 , 266 ), (831 , 262 ), (906 , 264 )),
                            (Options.primary_sequencer, Options.seq_arp_arp,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "arpeggiator_octave_modes", arpeggiator_octave_modes,
                            ((976 , 263 ), (1044, 261 ), (1114, 263 ), (1188, 263 )),
                            (Options.primary_sequencer, Options.seq_arp_arp,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "routing_slot", routing_slot_adv,
                            ((422 , 1032), (425 , 1094), (434 , 1151), (439 , 1212),
                             (718 , 1032), (710 , 1094), (711 , 1153), (715 , 1215),
                             (1326, 1003), (1386, 998 ), (1444, 998 ), 
                             (1496, 1001), (1556, 997 ), (1607, 1009), 
                             (1664, 1003), (1724, 1000), (1782, 1000))
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_select,
                            "routing_slot", routing_slot_seq,
                            ((141 , 1042), (137 , 1095), (139 , 1148), (138 , 1206)),
                            (Options.primary_sequencer,), ())
        def rte_asgn_req(last=None): 
            return (
                (
                    (Options.primary_advanced, Options.secondary_macro_matrix), 
                    (Options.primary_sequencer,),
                ) if last is None else
                (
                    (Options.primary_advanced, Options.secondary_macro_matrix, last), 
                    (Options.primary_sequencer, last),
                ))
        rte_asgn_bra = (
            (Options.mde_routing_adv,), 
            (Options.mde_routing_seq,),
        ) 
        self._add_ui_affordance(self.aff.click_select, 
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
                            rte_asgn_req(), rte_asgn_bra)
        self._add_ui_affordance(self.aff.click_select,
                            "routing_assignments", routing_assignments_tab_fx1,
                            ((1729, 432 ), (1827, 431 ), (1640, 428 )),
                            rte_asgn_req(Options.fx_1), rte_asgn_bra)
        self._add_ui_affordance(self.aff.click_select,
                            "routing_assignments", routing_assignments_tab_fx2,
                            ((1729, 432 ), (1827, 431 ), (1640, 428 )),
                            rte_asgn_req(Options.fx_2), rte_asgn_bra)
        self._add_ui_affordance(self.aff.click_select,
                            "routing_assignments", routing_assignments_tab_fx3,
                            ((1729, 432 ), (1827, 431 ), (470 , 776 )),
                            rte_asgn_req(Options.fx_3), rte_asgn_bra)
        self._add_ui_affordance(self.aff.click_select,
                            "routing_assignments", routing_assignments_stg_voices,
                            ((479 , 713 ),),
                            rte_asgn_req(Options.stg_voices), rte_asgn_bra)
        self._add_ui_affordance(self.aff.click_select,
                            "routing_assignments", routing_assignments_stg_wheels,
                            ((210 , 1047),),
                            rte_asgn_req(Options.stg_wheels), rte_asgn_bra)
        for i in range(1, 4):
            self._add_ui_affordance(self.aff.click_select,
                                f"send_insert_delay_fx_{i}", effect_mode,
                                ((1558, 369 ), (1505, 366 )),
                                (
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_delay"],
                                ), ())
            self._add_ui_affordance(self.aff.click_select,
                                f"send_insert_reverb_fx_{i}", effect_mode,
                                ((1558, 369 ), (1505, 366 )),
                                (
                                    Options.primary_advanced,
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_reverb"],
                                ), ())
        self._add_ui_affordance(self.aff.click_select,
                            "lfo_shapes", lfo_shapes,
                            ((401 , 1162), (492 , 1164), (398 , 1204), (496 , 1207)),
                            (Options.primary_advanced, Options.secondary_shaper), (Options.tab_lfos,))
        self._add_ui_affordance(self.aff.click_select, 
                            "scroll_positions", scroll_positions,
                            ((1879, 923 ), (1880, 737 ), (1880, 605 ), (1880, 472 )),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_select, 
                            "n_bars", n_bars,
                            ((1051, 276 ), (1148, 259 ), (1231, 263 ), (1315, 264 )),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_toggle, 
                            "fx1", 
                            (1556, 199 ), 
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_toggle, 
                            "fx2",
                            (1677, 199 ),
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_toggle, 
                            "fx3",
                            (1799, 199 ), 
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_toggle, 
                            "tempo_sync_settings_run_cycenv",
                            (1411, 617 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.run_mode), ())
        self._add_ui_affordance(self.aff.click_toggle, 
                            "tempo_sync_settings_loop_cycenv",
                            (1412, 612 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode), ())
        self._add_ui_affordance(self.aff.click_toggle, 
                            "vibrato_settings_wheels",
                            (239 , 1005),
                            (Options.primary_advanced, Options.stg_wheels), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "legato_settings_mono_voices",
                            (510 , 689 ),
                            (Options.primary_advanced, Options.stg_voices, Options.mono_mode), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "legato_settings_uni_voices",
                            (510 , 636 ),
                            (Options.primary_advanced, Options.stg_voices, Options.uni_mode), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "c_chord_selection",
                            (92  , 651 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "c_shp_chord_selection",
                            (101 , 624 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "d_chord_selection",
                            (113 , 648 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "d_shp_chord_selection",
                            (125 , 623 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "e_chord_selection",
                            (140 , 649 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "f_chord_selection",
                            (163 , 648 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "f_shp_chord_selection",
                            (173 , 624 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "g_chord_selection",
                            (186 , 648 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "g_shp_chord_selection",
                            (199 , 625 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "a_chord_selection",
                            (211 , 648 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "a_shp_chord_selection",
                            (220 , 623 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "b_chord_selection",
                            (235 , 648 ),
                            (Options.primary_advanced, Options.chord_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "c_scale_selection",
                            (97  , 675 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "c_shp_scale_selection",
                            (109 , 649 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "d_scale_selection",
                            (119 , 674 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "d_shp_scale_selection",
                            (132 , 646 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "e_scale_selection",
                            (141 , 673 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "f_scale_selection",
                            (160 , 675 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "f_shp_scale_selection",
                            (174 , 647 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "g_scale_selection",
                            (183 , 673 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "g_shp_scale_selection",
                            (195 , 648 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "a_scale_selection",
                            (202 , 673 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "a_shp_scale_selection",
                            (216 , 649 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "b_scale_selection",
                            (225 , 674 ),
                            (Options.primary_advanced, Options.scale_tab), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "chord",
                            (98  , 773 ),
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "rand_oct_arp",
                            (1399, 266 ),
                            (Options.primary_sequencer, Options.seq_arp_arp), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "row_1_auto_smooth_seq",
                            (87  , 1043),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "row_2_auto_smooth_seq",
                            (88  , 1097),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "row_3_auto_smooth_seq",
                            (89  , 1149),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "row_4_auto_smooth_seq",
                            (88  , 1203),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "autoplay_seq",
                            (637 , 264 ),
                            (Options.primary_sequencer, Options.seq_arp_seq), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "overdub_seq",
                            (723 , 263 ),
                            (Options.primary_sequencer, Options.seq_arp_seq), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "pause_play_seq",
                            (808 , 259 ),
                            (Options.primary_sequencer, Options.seq_arp_seq), ())
        self._add_ui_affordance(self.aff.click_toggle,
                            "record_seq",
                            (894 , 262 ),
                            (Options.primary_sequencer, Options.seq_arp_seq), ())
        self._add_ui_affordance(self.aff.click_hold_toggle,
                            "repeat_arp_seq",
                            (1257, 260 ),
                            (Options.primary_sequencer, Options.seq_arp_arp), ())
        self._add_ui_affordance(self.aff.click_hold_toggle,
                            "ratchet_arp_seq",
                            (1322, 261 ),
                            (Options.primary_sequencer, Options.seq_arp_arp), ())
        self._add_ui_affordance(self.aff.click_hold_toggle,
                            "mutate_arp_seq",
                            (1474, 261 ),
                            (Options.primary_sequencer, Options.seq_arp_arp), ())
        self._add_ui_affordance(self.aff.click_refresh,
                            "roll_dice_seq",
                            (1695, 260 ),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_refresh,
                            "reset_lfo_shaper",
                            (466 , 999 ),
                            (Options.primary_advanced, Options.secondary_shaper,), (Options.tab_lfos,))
        self._add_ui_affordance(self.aff.click_refresh,
                            "incr_time_div_seq",
                            (1830, 240 ),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_refresh,
                            "decr_time_div_seq",
                            (1828, 296 ),
                            (Options.primary_sequencer,), ())
        self._add_ui_affordance(self.aff.click_cycle, 
                            "rate_type_lfo1", lfo_rate_types, 
                            (771 , 710 ), 
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_cycle, 
                            "rate_type_lfo2", lfo_rate_types,
                            (1034, 710 ), 
                            (Options.primary_advanced,), ())
        self._add_ui_affordance(self.aff.click_cycle, 
                            "rise_curve_settings_env_cycenv", falling_curve_types,
                            (1350, 665 ), 
                            (Options.primary_advanced, Options.stg_cycenv,), ())
        self._add_ui_affordance(self.aff.click_cycle,
                            "fall_curve_settings_env_cycenv", falling_curve_types,
                            (1353, 701 ), 
                            (Options.primary_advanced, Options.stg_cycenv,), ())
        self._add_ui_affordance(self.aff.click_dropdown,
                            "type_osc_1",
                            osc_1_modes,
                            (476 , 200 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "type_osc_2",
                            osc_2_modes,
                            (1005, 200 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "type_filter",
                            filter_types,
                            (1395, 198 ),
                            ((Options.primary_advanced,),), ((),))
        for i in range(1, 4):
            _1, _2 = tuple(set(range(1, 4)) - set((i,)))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"fx{i}_type",
                                fx_types_neither
                                (1524, 241 ),
                                tuple((
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
                                )), tuple([()] * 7))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"fx{i}_type",
                                fx_types_delay,
                                (1524, 241 ),
                                tuple((
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
                                )), tuple([()] * 3))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"fx{i}_type",
                                fx_types_reverb,
                                (1524, 241 ),
                                tuple((
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
                                )), tuple([()] * 3))
        for i in range(1, 4):
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"chorus_presets_fx_{i}", chorus_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_chorus"],
                                ),), ((),))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"phaser_presets_fx_{i}", phaser_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_phaser"],
                                ),), ((),))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"flanger_presets_fx_{i}", flanger_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_flanger"],
                                ),), ((),))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"distortion_presets_fx_{i}", distortion_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_distortion"],
                                ),), ((),))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"_3_bands_eq_presets_fx_{i}", options._3_bands_eq_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}__3_bands_eq"],
                                ),), ((),))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"multi_comp_presets_fx_{i}", multi_comp_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_multi_comp"],
                                ),), ((),))
            self._add_ui_affordance(self.aff.click_dropdown,
                                f"superunison_presets_fx_{i}", superunison_presets,
                                (1526, 429 ),
                                ((
                                    Options.primary_advanced, 
                                    Options[f"fx_{i}"],
                                    Options[f"typ_fx_{i}_superunison"],
                                ),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "mode_voices",
                            voice_modes,
                            (421 , 711 ),
                            ((Options.primary_advanced,),) ,((), ))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "retrigger_lfo1",
                            lfo1_retrigger_modes,
                            (689 , 711 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "retrigger_lfo2",
                            lfo2_retrigger_modes,
                            (943 , 712 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "mode_cycenv",
                            cycenv_modes,
                            (1193, 712 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "retrigger_env",
                            env_retrigger_modes,
                            (1606, 711 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "glide_mode_settings_mono_voices",
                            glide_types,
                            (478 , 639 ),
                            ((Options.primary_advanced, Options.stg_voices, Options.mono_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "glide_mode_settings_uni_voices",
                            glide_types,
                            (479 , 616 ),
                            ((Options.primary_advanced, Options.stg_voices, Options.uni_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "uni_mode_settings_uni_voices",
                            uni_voice_modes
                            (478 , 662 ),
                            ((Options.primary_advanced, Options.stg_voices, Options.uni_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "glide_mode_settings_poly_voices",
                            glide_types,
                            (481 , 627 ),
                            (Options.primary_advanced, Options.stg_voices,), (Options.polypara_mode,))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "allocation_settings_poly_voices",
                            voice_allocation_modes,
                            (480 , 664 ),
                            (Options.primary_advanced, Options.stg_voices,), (Options.polypara_mode,))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "note_steal_settings_poly_voices",
                            note_steal_modes,
                            (474 , 700 ),
                            (Options.primary_advanced, Options.stg_voices,), (Options.polypara_mode,))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "mode_settings_voices",
                            voice_modes
                            (461 , 586 ),
                            ((Options.primary_advanced, Options.stg_voices,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "retrigger_settings_env_cycenv",
                            cycenv_retrigger_modes,
                            (1351, 626 ),
                            ((Options.primary_advanced, Options.stg_cycenv, Options.env_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "stage_order_settings_run_cycenv",
                            stage_orders,
                            (1350, 646 ),
                            ((Options.primary_advanced, Options.stg_cycenv, Options.run_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "retrigger_settings_loop_cycenv",
                            cycenv_retrigger_modes,
                            (1352, 637 ),
                            ((Options.primary_advanced, Options.stg_cycenv, Options.loop_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "stage_order_settings_loop_cycenv",
                            stage_orders,
                            (1346, 659 ),
                            ((Options.primary_advanced, Options.stg_cycenv, Options.loop_mode,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "mode_settings_cycenv",
                            cycenv_modes,
                            (1327, 586 ),
                            ((Options.primary_advanced, Options.stg_cycenv,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "attack_curve_settings_envelope",
                            attack_curve_types,
                            (1631, 619 ),
                            (Options.primary_advanced, Options.stg_env,), (Options.mde_env_retrigger,))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "decay_curve_settings_envelope",
                            falling_curve_types,
                            (1625, 647 ),
                            (Options.primary_advanced, Options.stg_env,), (Options.mde_env_retrigger,))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "release_curve_settings_envelope",
                            falling_curve_types,
                            (1626, 678 ),
                            (Options.primary_advanced, Options.stg_env,), (Options.mde_env_retrigger,))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "retrigger_settings_env",
                            env_retrigger_modes,
                            (1653, 586 ),
                            ((Options.primary_advanced, Options.stg_env,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "chord_root",
                            notes,
                            (168 , 776 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "scale_mode",
                            scale_modes,
                            (226 , 771 ),
                            ((Options.primary_advanced,),), ((),))
        self._add_ui_affordance(self.aff.click_dropdown,
                            "rate_lfo_shaper",
                            rate_lfo_shaper
                            (549 , 1085),
                            (Options.primary_advanced, Options.secondary_shaper,), (Options.tab_lfos,))
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "rise_curve_settings_run_cycenv",
                            (1349, 680 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.run_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "rise_curve_settings_loop_cycenv",
                            (1349, 680 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "fall_curve_settings_run_cycenv",
                            (1348, 707 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.run_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "rise_curve_settings_loop_cycenv",
                            (1347, 686 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "fall_curve_settings_loop_cycenv",
                            (1346, 715 ),
                            (Options.primary_advanced, Options.stg_cycenv, Options.loop_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "vel_vca_settings_envelope",
                            (1836, 620 ),
                            (Options.primary_advanced, Options.stg_env), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "vel_vcf_settings_envelope",
                            (1836, 650 ),
                            (Options.primary_advanced, Options.stg_env), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "vel_env_settings_envelope",
                            (1836, 677 ),
                            (Options.primary_advanced, Options.stg_env), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "vel_time_settings_envelope",
                            (1835, 708 ),
                            (Options.primary_advanced, Options.stg_env), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "vibrato_rate_settings_wheels",
                            (210 , 1047),
                            (Options.primary_advanced, Options.stg_wheels), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "vibrato_depth_settings_wheels",
                            (209 , 1091),
                            (Options.primary_advanced, Options.stg_wheels), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "bend_range_settings_wheels",
                            (209 , 1134),
                            (Options.primary_advanced, Options.stg_wheels), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "uni_count_settings_uni_voice",
                            (476 , 688 ),
                            (Options.primary_advanced, Options.stg_voices, Options.uni_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "uni_spread_settings_uni_voice",
                            (479 , 712 ),
                            (Options.primary_advanced, Options.stg_voices, Options.uni_mode), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_1_macro_1",
                            (549 , 1032),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_2_macro_1",
                            (551 , 1089),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_3_macro_1",
                            (552 , 1151),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_4_macro_1",
                            (552 , 1210),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_1_macro_2",
                            (843 , 1031),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_2_macro_2",
                            (841 , 1090),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_3_macro_2",
                            (842 , 1153),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amount_4_macro_2",
                            (842 , 1211),
                            (Options.primary_advanced, Options.secondary_macro_matrix), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "brightness",
                            (1389, 1283),
                            (), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "timbre",
                            (1524, 1285),
                            (), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "grid_length_lfo_shaper",
                            (556 , 1042),
                            (Options.primary_advanced, Options.secondary_shaper,), (Options.tab_lfos))
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "amplitude_lfo_shaper",
                            (563 , 1191),
                            (Options.primary_advanced, Options.secondary_shaper,), (Options.tab_lfos))
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "swing_seq",
                            (1782, 266 ),
                            (Options.primary_sequencer, Options.seq_arp_not_off), ())
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "tempo_seq",
                            (1840, 192 ),
                            (Options.primary_sequencer, Options.seq_arp_not_off), ())
        for i in range(13):
            x = 1088 + i * ((1764 - 1088) / 12)
            for j in range(7):
                y = 1045  + i * ((1231 - 1045) / 6)
                self._add_ui_affordance(self.aff.click_rel_slider,
                                    f"mod_{i}_{j}_matrix",
                                    (x, y),
                                    (Options.primary_advanced, Options.secondary_macro_matrix), ())
        # LFO_Shaper_Canvas
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "border_left",
                            (691 , 1097),
                            None)
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "border_right",
                            (1796, 1092),
                            None)
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "border_mid_height",
                            (1043, 1094),
                            None)
        self._add_ui_affordance(self.aff.click_rel_slider,
                            "border_erase_button_height",
                            (734 , 969 ),
                            None)
        
    def _add_programmatic_affordance(self, afford, *conditions, **kwargs):
        if   afford is self.aff.midi_disc_toggle:
            self._midi_disc_toggle[conditions[0].name] = kwargs
        elif afford is self.aff.midi_slider:
            kwargs.update(control=conditions[0].value)
            self._midi_slider[conditions[0].name] = kwargs
        elif afford is self.aff.midi_cont_toggle:
            self._midi_cont_toggle[conditions[0].name] = {
                "control": conditions[0].value,
            }

    def _add_ui_affordance(self, aff, *conditions):
        def norm(x, y):
            return (
                (x - self.L) / (self.R - self.L),
                (y - self.T) / (self.B - self.T),
            )            
        if   aff is self.aff.click_select:
            if not hasattr(self, f"_{aff.name}"):
                setattr(self, f"_{aff.name}", defaultdict(lambda: {"selections": [], "points": [], "require": [], "branch": []}))
            name, selections, records = conditions[0], tuple(conditions[1]), getattr(self, f"_{aff.name}") 
            points = tuple(norm(x, y) for (x, y) in conditions[2])
            if len(selections) != len(points):
                raise ValueError(f"_add_ui_action: {aff}: {name}: {selections}: {points}: unequal number of selections and points")
            records[name]["selections"].extend(selections)
            records[name]["points"].extend(points)
            records[name]["require"].extend(conditions[3] for _ in range(len(points)))
            records[name]["branch"].extend(conditions[4] for _ in range(len(points)))
        elif aff is self.aff.click_toggle or aff is self.aff.click_hold_toggle or aff is self.aff.click_refresh:
            if not hasattr(self, f"_{aff.name}"):
                setattr(self, f"_{aff.name}", {})
            name, records = conditions[0], getattr(self, f"_{aff.name}")
            if name not in records:
                records[name] = {
                    "point": norm(conditions[1][0], conditions[1][1]),
                    "require": conditions[2],
                    "branch": conditions[3],
                }
            else:
                raise ValueError(f"_add_ui_action: {aff}: {name}: duplicate call")
        elif aff is self.aff.click_cycle or aff:
            if not hasattr(self, f"_{aff.name}"):
                setattr(self, f"_{aff.name}", {})
            name, records = conditions[0], getattr(self, f"_{aff.name}")
            if name not in records:
                records[name] = {
                    "selections": list(conditions[1]),
                    "point": norm(conditions[2][0], conditions[2][1]),
                    "require": conditions[3],
                    "branch": conditions[4],
                }
            else:
                raise ValueError(f"_add_ui_action: {aff}: {name}: duplicate call")
        elif aff is self.aff.click_dropdown:
            if not hasattr(self, f"_{aff.name}"):
                setattr(self, f"_{aff.name}", {})
            name, selections, records = conditions[0], list(conditions[1]), getattr(self, f"_{aff.name}")
            if name not in records:
                records[name] = {
                    "selections": selections,
                    "point": norm(conditions[2][0], conditions[2][1]),
                    "require": tuple((conditions[3] for _ in range(len(selections)))),
                    "branch": tuple((conditions[4] for _ in range(len(selections)))),
                }
            else:
                raise ValueError(f"_add_ui_action: {aff}: {name}: duplicate call")
        elif aff is self.aff.click_rel_slider:
            if not hasattr(self, f"_{aff.name}"):
                setattr(self, f"_{aff.name}", {})
            name, records = conditions[0], getattr(self, f"_{aff.name}")
            if name not in records:
                records[name] = {
                    "point": norm(conditions[1][0], conditions[1][1]),
                    "require": conditions[2],
                    "branch": conditions[3],
                }
            else:
                raise ValueError(f"_add_ui_action: {aff}: {name}: duplicate call")

    def _finalize_affordances(self):
        affordance_types, self._spec, self._state, self._states = {}, {}, {}, {}
        for aff in self.aff:
            affordance_type = "_".join(map(lambda s: s.capitalize(), aff.name.split("_")))
            records = getattr(self, f"_{aff.name}")
            affordance_types[affordance_type] = Enum(affordance_type, tuple(records.keys()))
            for afford in affordance_types[affordance_type]:
                elt = records[afford.name]
                if   aff is self.aff.midi_disc_toggle or aff is self.aff.midi_cont_toggle:
                    self._state[afford] = Toggle_State.Off
                    self._states[afford] = tuple(Toggle_State)
                elif aff is self.aff.midi_slider:
                    self._state[afford] = 0
                    self._states[afford] = tuple(range(128))
                elif aff is self.aff.click_select:
                    self._state[afford] = elt["selections"][0]
                    self._states[afford] = tuple(elt["selections"])
                    del self._spec[afford]["selections"]
                elif aff is self.aff.click_toggle:
                    self._state[afford] = Toggle_State.Off
                    self._states[afford] = tuple(Toggle_State)
                elif aff is self.aff.click_hold_toggle:
                    self._state[afford] = Hold_Toggle_State.Released
                    self._states[afford] = tuple(Hold_Toggle_State)
                elif aff is self.aff.click_refresh:
                    self._state[afford] = None
                    self._states[afford] = (None,)
                elif aff is self.aff.click_cycle or aff is self.aff.click_dropdown:
                    self._state[afford] = elt["selections"][0]
                    self._states[afford] = tuple(elt["selections"])
                    del self._spec[afford]["selections"]
                elif aff is self.aff.click_rel_slider:
                    pass

        self._affordance_types = Enum('Affordance_Types', affordance_types)
        self._affordances = tuple((a for at in self._affordance_types for a in at))
    
    @property
    def state(self):
        return self._state

    def __enter__(self):
        self.app.start(self.executable_path)
        self._outport = mido.open_output(self.outport_name)         
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.app.kill()
        self._outport.close()
        return False    

    def do(self, affordance, state, **kwargs):
        spec, states = self._spec[affordance], self._states[affordance]
        if state not in states:
            raise ValueError(f"do: {affordance}: {state}: requested state not among valid states: {states}")
        choice, curr = states.index(state), states.index(self._state[affordance])
        if choice == curr:
            return
        at = self._affordance_types[affordance.__name__]
        if at is self._affordance_types.Midi_Disc_Toggle:
            spec.update(kwargs)
            if state is Toggle_State.On:
                self._send(f"{affordance.name}_on", **spec)
            elif state is Toggle_State.Off:
                self._send(f"{affordance.name}_off", **spec)
        if at is self._affordance_types.Midi_Cont_Toggle:
            spec.update(kwargs)
            if state is Toggle_State.On:
                self._send("control_change", value=127, **spec)
            if state is Toggle_State.Off:
                self._send("control_change", value=0, **spec)
        if at is self._affordance_types.Midi_Slider:
            self._send("control_change", value=state, **spec)
        if at is self._affordance_types.Click_Select:
            if self._satisfied(spec["require"][choice]):
                self._click(spec["points"][choice])
        if at is self._affordance_types.Click_Toggle:
            if self._satisfied(spec["require"]):
                self._click(spec["point"])
        if at is self._affordance_types.Click_Hold_Toggle:
            if self._satisfied(spec["require"]):
                if state is Hold_Toggle_State.Released:
                    self._hold_click(spec["point"])
                elif state is Hold_Toggle_State.Held:
                    self._release_click(spec["point"])
        if at is self._affordance_types.Click_Refresh:
            if self._satisfied(spec["require"]):
                self._click(spec["point"])
        if at is self._affordance_types.Click_Cycle:
            if state._satisfied(spec["require"]):
                if choice < curr:
                    for _ in itertools.chain(states[curr:], states[:choice]):
                        self._click(spec["point"])
                else:
                    for _ in states[curr:choice]:
                        self._click(spec["point"])
        if at is self._affordance_types.Click_Dropdown:
            if self._satisfied(spec["require"][choice]):
                self._click(spec["point"])
                for _ in range(choice + 1):
                    self._kbd_down()
                self._kbd_enter()
        if at is self._affordance_types.Click_Rel_Slider:
            pass

    def _satisfied(self, req):
        pass

    def _click(self, point):
        pass

    def _kbd_down(self):
        pass

    def _kbd_enter(self):
        pass

    def _send(self, ty, **kwargs):
        if isinstance(self._outport, mido.ports.BaseOutput) and not self._outport.closed:
            self._outport.send(mido.Message(ty, **kwargs))
