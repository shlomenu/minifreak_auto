from collections import defaultdict
import copy
from enum import Enum
import itertools
from typing import List, Optional, Tuple, Union

from pywinauto import Application, mouse, keyboard
import mido
import pywinauto

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
            aff is cls.midi_disc_toggle
            or aff is cls.midi_cont_toggle
            or aff is cls.midi_slider
        )

    @classmethod
    def is_ui(cls, aff):
        return aff in cls and not cls.is_programmatic(aff)


class Toggle_State(Enum):
    On = auto()
    Off = auto()


class Hold_Toggle_State(Enum):
    Held = auto()
    Released = auto()


class MiniFreak:

    def __init__(
        self,
        executable_path="C:\\Program Files\\Arturia\\MiniFreak V\\MiniFreak V.exe",
        outport_name="loopMIDI Port 1",
        L=4,
        T=23,
        R=1946,
        B=1318,
        affordances=Def_Afford,
    ):
        self.app = Application()
        self.executable_path = executable_path
        self.outport_name = outport_name
        self.aff = affordances
        self.L = L
        self.T = T
        self.R = R
        self.B = B
        self.n_affordances = 0
        for elt in Mf_Midi_Cont_Toggle:
            self._add_programmatic_affordance(self.aff.midi_cont_toggle, elt)
        for elt in Mf_Midi_Disc_Toggle:
            self._add_programmatic_affordance(
                self.aff.midi_disc_toggle,
                elt,
                note=64,
                velocity=64,
            )
        for elt in Mf_Midi_Slider:
            self._add_programmatic_affordance(self.aff.midi_slider, elt)
        self._add_ui_affordance(
            self.aff.click_select, primary_tabs, [(1586, 102), (1716, 103)]
        )
        self._add_ui_affordance(
            self.aff.click_select,
            fx_tabs,
            [(1598, 200), (1718, 197), (1840, 198)],
            [Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            chord_scale_tabs,
            [(83, 543), (243, 541)],
            [Options.primary_advanced],
        )
        for name, points in zip(
            ("voices_panel", "cycenv_panel", "env_panel", "wheels_panel"),
            (
                [(524, 712), (523, 587)],
                [(1427, 712), (1427, 585)],
                [(1882, 713), (1882, 586)],
                [(165, 948), (163, 1241)],
            ),
        ):
            self._add_ui_affordance(
                self.aff.click_select,
                name=name,
                selections=panel,
                points=points,
                required=[Options.primary_advanced],
            )
        self._add_ui_affordance(
            self.aff.click_select,
            secondary_tabs,
            [(1103, 893), (1470, 897)],
            [Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            lfo_tabs,
            [(410, 955), (549, 953)],
            [Options.primary_advanced, Options.secondary_shaper],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            chord_octaves,
            [
                (60, 707),
                (82, 708),
                (101, 706),
                (124, 708),
                (142, 709),
                (162, 708),
                (183, 709),
                (204, 708),
                (223, 708),
                (245, 710),
                (266, 709),
            ],
            [Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            sequencer_arpeggiator_modes,
            [(99, 265), (182, 260), (265, 261)],
            [Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            arpeggiator_progression_modes,
            [
                (401, 259),
                (472, 262),
                (544, 261),
                (619, 262),
                (688, 262),
                (759, 266),
                (831, 262),
                (906, 264),
            ],
            [Options.primary_sequencer, Options.seq_arp_arp],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            arpeggiator_octave_modes,
            [(976, 263), (1044, 261), (1114, 263), (1188, 263)],
            [Options.primary_sequencer, Options.seq_arp_arp],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_slot",
            selections=routing_slot_adv,
            points=[
                (422, 1032),
                (425, 1094),
                (434, 1151),
                (439, 1212),
                (718, 1032),
                (710, 1094),
                (711, 1153),
                (715, 1215),
                (1326, 1003),
                (1386, 998),
                (1444, 998),
                (1496, 1001),
                (1556, 997),
                (1607, 1009),
                (1664, 1003),
                (1724, 1000),
                (1782, 1000),
            ],
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_slot",
            selections=routing_slot_seq,
            points=[(141, 1042), (137, 1095), (139, 1148), (138, 1206)],
            required=[Options.primary_sequencer],
        )

        def rte_asgn_req(last=None):
            return (
                [
                    (
                        [Options.primary_advanced, Options.secondary_macro_matrix],
                        [Options.mde_routing_adv],
                    ),
                    ([Options.primary_sequencer], [Options.mde_routing_seq]),
                ]
                if last is None
                else [
                    (
                        [
                            Options.primary_advanced,
                            Options.secondary_macro_matrix,
                            last,
                        ],
                        [Options.mde_routing_adv],
                    ),
                    ([Options.primary_sequencer, last], [Options.mde_routing_seq]),
                ]
            )

        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_assignments",
            selections=routing_assignments_always,
            points=[
                (468, 198),
                (97, 432),
                (195, 431),
                (292, 430),
                (380, 431),
                (474, 432),
                (1001, 197),
                (627, 432),
                (725, 431),
                (818, 433),
                (907, 428),
                (999, 433),
                (1169, 431),
                (1269, 433),
                (1374, 430),
                (1640, 428),
                (639, 773),
                (900, 774),
                (741, 776),
                (1003, 773),
                (1165, 774),
                (1272, 777),
                (1376, 777),
                (1540, 774),
                (1637, 777),
                (1735, 776),
                (1837, 776),
            ],
            required=rte_asgn_req(),
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_assignments",
            selections=routing_assignments_tab_fx1,
            points=[(1729, 432), (1827, 431), (1640, 428)],
            required=rte_asgn_req(Options.fx_1),
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_assignments",
            selections=routing_assignments_tab_fx2,
            points=[(1729, 432), (1827, 431), (1640, 428)],
            required=rte_asgn_req(Options.fx_2),
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_assignments",
            selections=routing_assignments_tab_fx3,
            points=[(1729, 432), (1827, 431), (470, 776)],
            required=rte_asgn_req(Options.fx_3),
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_assignments",
            selections=routing_assignments_stg_voices,
            points=[(479, 713)],
            required=rte_asgn_req(Options.stg_voices),
        )
        self._add_ui_affordance(
            self.aff.click_select,
            name="routing_assignments",
            selections=routing_assignments_stg_wheels,
            points=[(210, 1047)],
            required=rte_asgn_req(Options.stg_wheels),
        )
        for i in range(1, 4):
            self._add_ui_affordance(
                self.aff.click_select,
                name=f"send_insert_delay_fx_{i}",
                selections=effect_mode,
                points=[(1558, 369), (1505, 366)],
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_delay"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_select,
                name=f"send_insert_reverb_fx_{i}",
                selections=effect_mode,
                points=[(1558, 369), (1505, 366)],
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_reverb"],
                ],
            )
        self._add_ui_affordance(
            self.aff.click_select,
            lfo_shapes,
            [(401, 1162), (492, 1164), (398, 1204), (496, 1207)],
            [
                (
                    [Options.primary_advanced, Options.secondary_shaper],
                    [Options.tab_lfos],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            scroll_positions,
            [(1879, 923), (1880, 737), (1880, 605), (1880, 472)],
            [Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_select,
            n_bars,
            [(1051, 276), (1148, 259), (1231, 263), (1315, 264)],
            [Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="fx1",
            points=(1556, 199),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="fx2",
            points=(1677, 199),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="fx3",
            points=(1799, 199),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="tempo_sync_settings_run_cycenv",
            points=(1411, 617),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.run_mode],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="tempo_sync_settings_loop_cycenv",
            points=(1412, 612),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.loop_mode],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="vibrato_settings_wheels",
            points=(239, 1005),
            required=[Options.primary_advanced, Options.stg_wheels],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="legato_settings_mono_voices",
            points=(510, 689),
            required=[Options.primary_advanced, Options.stg_voices, Options.mono_mode],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="legato_settings_uni_voices",
            points=(510, 636),
            required=[Options.primary_advanced, Options.stg_voices, Options.uni_mode],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="c_chord_selection",
            points=(92, 651),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="c_shp_chord_selection",
            points=(101, 624),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="d_chord_selection",
            points=(113, 648),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="d_shp_chord_selection",
            points=(125, 623),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="e_chord_selection",
            points=(140, 649),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="f_chord_selection",
            points=(163, 648),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="f_shp_chord_selection",
            points=(173, 624),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="g_chord_selection",
            points=(186, 648),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="g_shp_chord_selection",
            points=(199, 625),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="a_chord_selection",
            points=(211, 648),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="a_shp_chord_selection",
            points=(220, 623),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="b_chord_selection",
            points=(235, 648),
            required=[Options.primary_advanced, Options.chord_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="c_scale_selection",
            points=(97, 675),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="c_shp_scale_selection",
            points=(109, 649),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="d_scale_selection",
            points=(119, 674),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="d_shp_scale_selection",
            points=(132, 646),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="e_scale_selection",
            points=(141, 673),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="f_scale_selection",
            points=(160, 675),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="f_shp_scale_selection",
            points=(174, 647),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="g_scale_selection",
            points=(183, 673),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="g_shp_scale_selection",
            points=(195, 648),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="a_scale_selection",
            points=(202, 673),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="a_shp_scale_selection",
            points=(216, 649),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="b_scale_selection",
            points=(225, 674),
            required=[Options.primary_advanced, Options.scale_tab],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="chord",
            points=(98, 773),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="rand_oct_arp",
            points=(1399, 266),
            required=[Options.primary_sequencer, Options.seq_arp_arp],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="row_1_auto_smooth_seq",
            points=(87, 1043),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="row_2_auto_smooth_seq",
            points=(88, 1097),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="row_3_auto_smooth_seq",
            points=(89, 1149),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="row_4_auto_smooth_seq",
            points=(88, 1203),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="autoplay_seq",
            points=(637, 264),
            required=[Options.primary_sequencer, Options.seq_arp_seq],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="overdub_seq",
            points=(723, 263),
            required=[Options.primary_sequencer, Options.seq_arp_seq],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="pause_play_seq",
            points=(808, 259),
            required=[Options.primary_sequencer, Options.seq_arp_seq],
        )
        self._add_ui_affordance(
            self.aff.click_toggle,
            name="record_seq",
            points=(894, 262),
            required=[Options.primary_sequencer, Options.seq_arp_seq],
        )
        self._add_ui_affordance(
            self.aff.click_hold_toggle,
            name="repeat_arp_seq",
            points=(1257, 260),
            required=[Options.primary_sequencer, Options.seq_arp_arp],
        )
        self._add_ui_affordance(
            self.aff.click_hold_toggle,
            name="ratchet_arp_seq",
            points=(1322, 261),
            required=[Options.primary_sequencer, Options.seq_arp_arp],
        )
        self._add_ui_affordance(
            self.aff.click_hold_toggle,
            name="mutate_arp_seq",
            points=(1474, 261),
            required=[Options.primary_sequencer, Options.seq_arp_arp],
        )
        self._add_ui_affordance(
            self.aff.click_refresh,
            name="roll_dice_seq",
            points=(1695, 260),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_refresh,
            name="reset_lfo_shaper",
            points=(466, 999),
            required=[
                (
                    [Options.primary_advanced, Options.secondary_shaper],
                    [Options.tab_lfos],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_refresh,
            name="incr_time_div_seq",
            points=(1830, 240),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_refresh,
            name="decr_time_div_seq",
            points=(1828, 296),
            required=[Options.primary_sequencer],
        )
        self._add_ui_affordance(
            self.aff.click_cycle,
            name="rate_type_lfo1",
            selections=lfo_rate_types,
            points=(771, 710),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_cycle,
            name="rate_type_lfo2",
            selections=lfo_rate_types,
            points=(1034, 710),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_cycle,
            name="rise_curve_settings_env_cycenv",
            selections=rising_curve_types,
            points=(1350, 665),
            required=[Options.primary_advanced, Options.stg_cycenv],
        )
        self._add_ui_affordance(
            self.aff.click_cycle,
            name="fall_curve_settings_env_cycenv",
            selections=falling_curve_type,
            points=(1353, 701),
            required=[Options.primary_advanced, Options.stg_cycenv],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown, osc_1_mode, (476, 200), [Options.primary_advanced]
        )
        self._add_ui_affordance(
            self.aff.click_dropdown, osc_2_mode, (1005, 200), [Options.primary_advanced]
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            filter_type,
            (1395, 198),
            [Options.primary_advanced],
        )
        for i in range(1, 4):
            _1, _2 = tuple(set(range(1, 4)) - set((i,)))
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"fx{i}_type",
                selections=fx_types_neither,
                points=(1524, 241),
                required=[
                    [
                        Options.primary_advanced,
                        Options[f"fx_{i}"],
                        Options[other_opt_1],
                        Options[other_opt_2],
                    ]
                    for other_opt_1, other_opt_2 in zip(
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
                        ),
                    )
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"fx{i}_type",
                selections=fx_types_delay,
                points=(1524, 241),
                required=[
                    [
                        Options.primary_advanced,
                        Options[f"fx_{i}"],
                        Options[other_opt_1],
                        Options[other_opt_2],
                    ]
                    for other_opt_1, other_opt_2 in zip(
                        (
                            f"typ_fx_{_1}_neither",
                            f"typ_fx_{_1}_reverb",
                            f"typ_fx_{_1}_neither",
                        ),
                        (
                            f"typ_fx_{_2}_reverb",
                            f"typ_fx_{_2}_neither",
                            f"typ_fx_{_2}_neither",
                        ),
                    )
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"fx{i}_type",
                selections=fx_types_reverb,
                points=(1524, 241),
                required=[
                    [
                        Options.primary_advanced,
                        Options[f"fx_{i}"],
                        Options[other_opt_1],
                        Options[other_opt_2],
                    ]
                    for other_opt_1, other_opt_2 in zip(
                        (
                            f"typ_fx_{_1}_neither",
                            f"typ_fx_{_1}_delay",
                            f"typ_fx_{_1}_neither",
                        ),
                        (
                            f"typ_fx_{_2}_delay",
                            f"typ_fx_{_2}_neither",
                            f"typ_fx_{_2}_neither",
                        ),
                    )
                ],
            )
        for i in range(1, 4):
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"chorus_preset_fx_{i}",
                selections=chorus_presets,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_chorus"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"phaser_preset_fx_{i}",
                selections=phaser_preset,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_phaser"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"flanger_preset_fx_{i}",
                selections=flanger_preset,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_flanger"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"distortion_preset_fx_{i}",
                selections=distortion_preset,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_distortion"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"_3_bands_eq_preset_fx_{i}",
                selections=options._3_bands_eq_preset,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}__3_bands_eq"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"multi_comp_preset_fx_{i}",
                selections=multi_comp_preset,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_multi_comp"],
                ],
            )
            self._add_ui_affordance(
                self.aff.click_dropdown,
                name=f"superunison_preset_fx_{i}",
                selections=superunison_preset,
                points=(1526, 429),
                required=[
                    Options.primary_advanced,
                    Options[f"fx_{i}"],
                    Options[f"typ_fx_{i}_superunison"],
                ],
            )
        self._add_ui_affordance(
            self.aff.click_dropdown, voice_mode, (421, 711), [Options.primary_advanced]
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="lfo1_retrigger_mode",
            selections=list(lfo1_retrigger_mode)
            + list(lfo_retrigger_mode)
            + list(cycenv_retrigger_mode),
            points=(689, 711),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="lfo2_retrigger_mode",
            selections=list(lfo2_retrigger_mode)
            + list(lfo_retrigger_mode)
            + list(cycenv_retrigger_mode),
            points=(943, 712),
            required=[Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            cycenv_mode,
            (1193, 712),
            [Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            env_retrigger_mode,
            (1606, 711),
            [Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="glide_mode_settings_mono_voices",
            selections=glide_type,
            points=(478, 639),
            required=[Options.primary_advanced, Options.stg_voices, Options.mono_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="glide_mode_settings_uni_voices",
            selections=glide_type,
            points=(479, 616),
            required=[Options.primary_advanced, Options.stg_voices, Options.uni_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            uni_voice_mode,
            (478, 662),
            [Options.primary_advanced, Options.stg_voices, Options.uni_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="glide_mode_settings_poly_voices",
            selections=glide_type,
            points=(481, 627),
            required=[
                (
                    [Options.primary_advanced, Options.stg_voices],
                    [Options.polypara_mode],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            voice_allocation_modes,
            (480, 664),
            [([Options.primary_advanced, Options.stg_voices], [Options.polypara_mode])],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            note_steal_modes,
            (474, 700),
            [([Options.primary_advanced, Options.stg_voices], [Options.polypara_mode])],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            voice_mode,
            (461, 586),
            [Options.primary_advanced, Options.stg_voices],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="retrigger_settings_env_cycenv",
            selections=cycenv_retrigger_mode,
            points=(1351, 626),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.env_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="stage_order_settings_run_cycenv",
            selections=stage_order,
            points=(1350, 646),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.run_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="retrigger_settings_loop_cycenv",
            selections=cycenv_retrigger_mode,
            points=(1352, 637),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.loop_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="stage_order_settings_loop_cycenv",
            selections=stage_order,
            points=(1346, 659),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.loop_mode],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            cycenv_mode,
            (1327, 586),
            [Options.primary_advanced, Options.stg_cycenv],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="attack_curve_settings_envelope",
            selections=attack_curve_type,
            points=(1631, 619),
            required=[
                (
                    [Options.primary_advanced, Options.stg_env],
                    [Options.mde_env_retrigger],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="decay_curve_settings_envelope",
            selections=falling_curve_type,
            points=(1625, 647),
            required=[
                (
                    [Options.primary_advanced, Options.stg_env],
                    [Options.mde_env_retrigger],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            name="release_curve_settings_envelope",
            selections=falling_curve_type,
            points=(1626, 678),
            required=[
                (
                    [Options.primary_advanced, Options.stg_env],
                    [Options.mde_env_retrigger],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            env_retrigger_mode,
            (1653, 586),
            [Options.primary_advanced, Options.stg_env],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            chord_root_note,
            (168, 776),
            [Options.primary_advanced],
        )
        self._add_ui_affordance(
            self.aff.click_dropdown, scale_mode, (226, 771), [Options.primary_advanced]
        )
        self._add_ui_affordance(
            self.aff.click_dropdown,
            rate_lfo_shaper,
            (549, 1085),
            [
                (
                    [Options.primary_advanced, Options.secondary_shaper],
                    [Options.tab_lfos],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="rise_curve_settings_run_cycenv",
            points=(1349, 680),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.run_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="rise_curve_settings_loop_cycenv",
            points=(1349, 680),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.loop_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="fall_curve_settings_run_cycenv",
            points=(1348, 707),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.run_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="rise_curve_settings_loop_cycenv",
            points=(1347, 686),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.loop_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="fall_curve_settings_loop_cycenv",
            points=(1346, 715),
            required=[Options.primary_advanced, Options.stg_cycenv, Options.loop_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="vel_vca_settings_envelope",
            points=(1836, 620),
            required=[Options.primary_advanced, Options.stg_env],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="vel_vcf_settings_envelope",
            points=(1836, 650),
            required=[Options.primary_advanced, Options.stg_env],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="vel_env_settings_envelope",
            points=(1836, 677),
            required=[Options.primary_advanced, Options.stg_env],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="vel_time_settings_envelope",
            points=(1835, 708),
            required=[Options.primary_advanced, Options.stg_env],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="vibrato_rate_settings_wheels",
            points=(210, 1047),
            required=[Options.primary_advanced, Options.stg_wheels],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="vibrato_depth_settings_wheels",
            points=(209, 1091),
            required=[Options.primary_advanced, Options.stg_wheels],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="bend_range_settings_wheels",
            points=(209, 1134),
            required=[Options.primary_advanced, Options.stg_wheels],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="uni_count_settings_uni_voice",
            points=(476, 688),
            required=[Options.primary_advanced, Options.stg_voices, Options.uni_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="uni_spread_settings_uni_voice",
            points=(479, 712),
            required=[Options.primary_advanced, Options.stg_voices, Options.uni_mode],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_1_macro_1",
            points=(549, 1032),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_2_macro_1",
            points=(551, 1089),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_3_macro_1",
            points=(552, 1151),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_4_macro_1",
            points=(552, 1210),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_1_macro_2",
            points=(843, 1031),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_2_macro_2",
            points=(841, 1090),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_3_macro_2",
            points=(842, 1153),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amount_4_macro_2",
            points=(842, 1211),
            required=[Options.primary_advanced, Options.secondary_macro_matrix],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider, name="brightness", points=(1389, 1283)
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider, name="timbre", points=(1524, 1285)
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="grid_length_lfo_shaper",
            points=(556, 1042),
            required=[
                (
                    [Options.primary_advanced, Options.secondary_shaper],
                    [Options.tab_lfos],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="amplitude_lfo_shaper",
            points=(563, 1191),
            required=[
                (
                    [Options.primary_advanced, Options.secondary_shaper],
                    [Options.tab_lfos],
                )
            ],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="swing_seq",
            points=(1782, 266),
            required=[Options.primary_sequencer, Options.seq_arp_not_off],
        )
        self._add_ui_affordance(
            self.aff.click_rel_slider,
            name="tempo_seq",
            points=(1840, 192),
            required=[Options.primary_sequencer, Options.seq_arp_not_off],
        )
        for i in range(13):
            x = 1088 + i * ((1764 - 1088) / 12)
            for j in range(7):
                y = 1045 + i * ((1231 - 1045) / 6)
                self._add_ui_affordance(
                    self.aff.click_rel_slider,
                    name=f"mod_{i}_{j}_matrix",
                    points=(x, y),
                    required=[Options.primary_advanced, Options.secondary_macro_matrix],
                )
        # LFO_Shaper_Canvas
        # self._add_ui_affordance(self.aff.click_rel_slider,
        #                     "border_left",
        #                     (691 , 1097),
        #                     None)
        # self._add_ui_affordance(self.aff.click_rel_slider,
        #                     "border_right",
        #                     (1796, 1092),
        #                     None)
        # self._add_ui_affordance(self.aff.click_rel_slider,
        #                     "border_mid_height",
        #                     (1043, 1094),
        #                     None)
        # self._add_ui_affordance(self.aff.click_rel_slider,
        #                     "border_erase_button_height",
        #                     (734 , 969 ),
        #                     None)

    def _add_programmatic_affordance(self, afford, cc: Enum, **kwargs):
        if not hasattr(self, f"_{afford.name}"):
            setattr(self, f"_{afford.name}", {})
        if afford is self.aff.midi_disc_toggle:
            self._midi_disc_toggle[cc.name] = kwargs
        elif afford is self.aff.midi_slider:
            kwargs.update(control=cc.value)
            self._midi_slider[cc.name] = kwargs
        elif afford is self.aff.midi_cont_toggle:
            self._midi_cont_toggle[cc] = {
                "control": cc.value,
            }

    def _norm(self, x, y):
        return (
            (x - self.L) / (self.R - self.L),
            (y - self.T) / (self.B - self.T),
        )

    def _add_ui_affordance(
        self,
        aff: Def_Afford,
        selections: Union[Enum, List[Enum], None] = None,
        points: Union[
            List[Tuple[Union[int, float], Union[int, float]]],
            Tuple[Union[int, float], Union[int, float]],
            None,
        ] = None,
        required: Union[
            Tuple[List[Options], List[Options]],
            List[Options],
            List[List[Options]],
            List[Tuple[List[Options], List[Options]]],
        ] = [],
        name: Optional[str] = None,
        _processed: bool = False,
    ):
        if selections is not None and name is None:
            name = selections.__name__
        elif selections is None and name is None:
            name = f"unnamed_{self.n_affordances}"

        if selections is not None and not isinstance(selections, list):
            selections = list(selections)
        if points is not None and not _processed:
            if isinstance(points[0], tuple):
                points = [self._norm(x, y) for (x, y) in points]
            else:
                points = [self._norm(points[0], points[1])]
        if not _processed:
            if isinstance(required, tuple) or (
                required and isinstance(required[0], Options)
            ):
                required = [required]

        if selections is None and (
            aff is self.aff.click_select
            or aff is self.aff.click_cycle
            or aff is self.aff.click_dropdown
        ):
            raise ValueError(f"_add_ui_action: {aff}: {name}: missing selections")
        if points is None:
            raise ValueError(f"_add_ui_action: {aff}: {name}: missing points")
        elif aff is not self.aff.click_select and len(points) > 1:
            raise ValueError(
                f"_add_ui_action: {aff}: multiple clickpoints not supported for this type of affordance"
            )
        if aff is self.aff.click_select and len(selections) != len(points):
            raise ValueError(
                f"_add_ui_action: {aff}: {name}: {selections}: {points}: unequal number of selections and points"
            )

        if not _processed and not hasattr(self, f"_{aff.name}"):
            setattr(self, f"_{aff.name}", defaultdict(lambda: defaultdict(dict)))

        for i, r in enumerate(required):
            if isinstance(r, tuple):
                required, branch = r
            else:
                required, branch = r, None
            if branch is not None and branch:
                sub_name, leaves = branch[0].value
                for leaf in leaves:
                    new_required = required + [(sub_name, frozenset((leaf,)))]
                    r_new = (
                        (new_required, branch[1:]) if len(branch) > 1 else new_required
                    )
                    self._add_ui_affordance(
                        aff,
                        name=f"{name}_{leaf.name}",
                        selections=selections,
                        points=points,
                        required=(required[:i] + [r_new] + required[i + 1 :]),
                        _processed=True,
                    )
                return

        records = getattr(self, f"_{aff.name}")

        if aff is self.aff.click_select:
            for selection, point in zip(selections, points):
                records[name][selection] = {"point": point, "required": required}
        elif (
            aff is self.aff.click_toggle
            or aff is self.aff.click_hold_toggle
            or aff is self.aff.click_refresh
            or aff is self.aff.click_rel_slider
        ):
            records[name][points[0]] = required
        elif aff is self.aff.click_cycle or aff is self.aff.click_dropdown:
            for selection in selections:
                records[name][selection] = {"point": points[0], "required": required}

        self.n_affordances += 1

    def _finalize_affordances(self):
        affordance_types, self._spec, self._state, self._states = {}, {}, {}, {}
        for aff in self.aff:
            affordance_type = "_".join(
                map(lambda s: s.capitalize(), aff.name.split("_"))
            )
            records = getattr(self, f"_{aff.name}")
            affordances = Enum(affordance_type, tuple(records.keys()))
            affordance_types[affordance_type] = affordances
            for afford in affordances:
                spec = records[afford.name]
                self._spec[afford] = spec
                if aff is self.aff.midi_disc_toggle or aff is self.aff.midi_cont_toggle:
                    self._state[afford] = Toggle_State.Off
                    self._states[afford] = tuple(Toggle_State)
                elif aff is self.aff.midi_slider:
                    self._state[afford] = 0
                    self._states[afford] = tuple(range(128))
                elif aff is self.aff.click_select:
                    self._states[afford] = tuple(spec.keys())
                    self._state[afford] = self._states[afford][0]
                elif aff is self.aff.click_toggle:
                    self._state[afford] = Toggle_State.Off
                    self._states[afford] = tuple(Toggle_State)
                elif aff is self.aff.click_hold_toggle:
                    self._state[afford] = Hold_Toggle_State.Released
                    self._states[afford] = tuple(Hold_Toggle_State)
                elif aff is self.aff.click_refresh:  # TODO: revisit
                    self._state[afford] = None
                    self._states[afford] = (None,)
                elif aff is self.aff.click_cycle or aff is self.aff.click_dropdown:
                    self._states[afford] = tuple(spec.keys())
                    self._state[afford] = self._states[afford][0]
                elif aff is self.aff.click_rel_slider:  # TODO: revisit
                    self._state[afford] = None
                    self._states[afford] = (None,)

        self._affordance_types = Enum(
            "Affordance_Types", {e.name: e for e in affordance_types}
        )
        self._affordances = {
            a.name: a for at in self._affordance_types for a in at.value
        }

        for afford in affordance_types[affordance_type]:
            elt = self._spec[afford]
            for afford in affordance_types[affordance_type]:
                if (
                    aff is self.aff.click_select
                    or aff is self.aff.click_cycle
                    or aff is self.aff.click_dropdown
                ):
                    for s, d in elt.items():
                        for opts in d["required"]:
                            for opt in opts:
                                assert (
                                    opt.value[0] in self._affordances
                                ), f"invalid requirement specification: {afford}: {s}: {d['required']}"
                elif (
                    aff is self.aff.click_toggle
                    or aff is self.aff.click_hold_toggle
                    or aff is self.aff.click_refresh
                    or aff is self.aff.click_rel_slider
                ):
                    for point, required in elt.items():
                        for opts in required:
                            for opt in opts:
                                assert (
                                    opt.value[0] in self._affordances
                                ), f"invalid requirement specification: {afford}: {point}: {d['required']}"

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
        states = self._states[affordance]
        spec = copy.deepcopy(self._spec[affordance])
        if state not in states:
            raise ValueError(
                f"do: {affordance}: {state}: requested state not among valid states: {states}"
            )
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
            if self._satisfied(spec[state]["required"]):
                self._click(spec[state]["point"])
        if at is self._affordance_types.Click_Toggle:
            for point, required in spec.items():
                if self._satisfied(required):
                    self._click(point)
        if at is self._affordance_types.Click_Hold_Toggle:
            for point, required in spec.items():
                if self._satisfied(required):
                    if state is Hold_Toggle_State.Released:
                        self._hold_click(point)
                    elif state is Hold_Toggle_State.Held:
                        self._release_click(point)
        if at is self._affordance_types.Click_Refresh:
            for point, required in spec.items():
                if self._satisfied(required):
                    self._click(point)
        if at is self._affordance_types.Click_Cycle:
            if self._satisfied(spec[state]["required"]):
                if choice < curr:
                    for _ in itertools.chain(states[curr:], states[:choice]):
                        self._click(spec[state]["point"])
                else:
                    for _ in states[curr:choice]:
                        self._click(spec[state]["point"])
        if at is self._affordance_types.Click_Dropdown:
            if self._satisfied(spec[state]["required"]):
                self._click(spec[state]["point"])
                for _ in range(choice + 1):
                    self._kbd_down()
                self._kbd_enter()
        if at is self._affordance_types.Click_Rel_Slider:
            pass

    def _satisfied(self, req):
        return any(
            req,
            lambda r: all(
                r,
                lambda opt: self.state[self._affordances[opt.value[0]]] in opt.value[1],
            ),
        )

    def _click(self, point):
        rect = self.app.window("MiniFreak").rectangle()
        width, height = rect.right - rect.left, rect.bottom - rect.top
        width_frac, height_frac = point
        mouse.click(
            coords=(rect.left + width * width_frac, rect.top + height * height_frac)
        )

    def _kbd_down(self):
        keyboard.send_keys("{VK_DOWN}")

    def _kbd_enter(self):
        keyboard.send_keys("{ENTER}")

    def _send(self, ty, **kwargs):
        if (
            isinstance(self._outport, mido.ports.BaseOutput)
            and not self._outport.closed
        ):
            self._outport.send(mido.Message(ty, **kwargs))
