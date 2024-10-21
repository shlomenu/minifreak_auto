from enum import Enum, auto

class primary_tabs(Enum):
    Advanced = auto()
    Sequencer = auto()

class fx_tabs(Enum):
    FX_1 = auto()
    FX_2 = auto()
    FX_3 = auto()

class chord_scale_tabs(Enum):
    Chord = auto()
    Scale = auto()

class panel(Enum):
    settings = auto()
    controls = auto()

class secondary_tabs(Enum):
    Macro__slash__Matrix = auto()
    LFO_Shaper = auto()

class lfo_tabs(Enum):
    LFO_1 = auto()
    LFO_2 = auto()

class lfo_rate_types(Enum):
    Free = auto()
    All = auto()
    Straight = auto()
    Triplet = auto()
    Dotted = auto()

class rising_curve_types(Enum):
    Quick = auto()
    Linear = auto()

class attack_curve_type(Enum):
    Default = auto()
    Quick = auto()

class falling_curve_type(Enum):
    Default = auto()
    Percussive = auto()

class cycenv_mode(Enum):
    Env = auto()
    Run = auto()
    Loop = auto()

class voice_mode(Enum):
    Mono = auto()
    Unison = auto()
    Poly = auto()
    Para = auto()

class chord_octaves(Enum):
    __minus__5 = auto()
    __minus__4 = auto()
    __minus__3 = auto()
    __minus__2 = auto()
    __minus__1 = auto()
    _0 = auto()
    __plus__1 = auto()
    __plus__2 = auto()
    __plus__3 = auto()
    __plus__4 = auto()
    __plus__5 = auto()

class sequencer_arpeggiator_modes(Enum):
    Off = auto()
    Arp = auto()
    Seq = auto()

class arpeggiator_progression_modes(Enum):
    Up = auto()
    Down = auto()
    Up__slash__Down = auto()
    Random = auto()
    Order = auto()
    Poly = auto()
    Walk = auto()
    Pattern = auto()

class arpeggiator_octave_modes(Enum):
    Oct1 = auto()
    Oct2 = auto()
    Oct3 = auto()
    Oct4 = auto()

class routing_assignments_always(Enum):
    type_osc_1 = auto()
    tune_osc_1 = auto()
    wave_osc_1 = auto()
    timbre_osc_1 = auto()
    shape_osc_1 = auto()
    volume_osc_1 = auto()
    type_osc_2 = auto()
    tune_osc_2 = auto()
    wave_osc_2 = auto()
    timbre_osc_2 = auto()
    shape_osc_2 = auto()
    volume_osc_2 = auto()
    cutoff_filter = auto()
    reso_filter = auto()
    env_amt_filter = auto()
    glide = auto()
    rate_lfo1 = auto()
    rate_lfo2 = auto()
    wave_lfo1 = auto()
    wave_lfo2 = auto()
    rise_cycenv = auto()
    fall_cycenv = auto()
    hold_cycenv = auto()
    attack_env = auto()
    decay_env = auto()
    sustain_env = auto()
    release_env = auto()

class routing_assignments_tab_fx1(Enum):
    time = auto()
    intensity = auto()
    amount = auto()

class routing_assignments_tab_fx2(Enum):
    time = auto()
    intensity = auto()
    amount = auto()

class routing_assignments_tab_fx3(Enum):
    time = auto()
    intensity = auto()
    amount = auto()

class routing_assignments_stg_voices(Enum):
    uni_spread = auto()

class routing_assignments_stg_wheels(Enum):
    vibrato_rate = auto()

class routing_slot_adv(Enum):
    Macro_1_1 = auto()
    Macro_1_2 = auto()
    Macro_1_3 = auto()
    Macro_1_4 = auto()
    Macro_2_1 = auto()
    Macro_2_2 = auto()
    Macro_2_3 = auto()
    Macro_2_4 = auto()
    Matrix_5 = auto()
    Matrix_6 = auto()
    Matrix_7 = auto()
    Matrix_8 = auto()
    Matrix_9 = auto()
    Matrix_10 = auto()
    Matrix_11 = auto()
    Matrix_12 = auto()
    Matrix_13 = auto()

class routing_slot_seq(Enum):
    mod_src_1 = auto()
    mod_src_2 = auto()
    mod_src_3 = auto()
    mod_src_4 = auto()

class osc_1_mode(Enum):
    Basic_Waves = auto()
    SuperWave = auto()
    Harmo = auto()
    KarplusStr = auto()
    VAnalog = auto()
    Waveshaper = auto()
    Two_Op__period__FM = auto()
    Formant = auto()
    Speech = auto()
    Modal = auto()
    Noise = auto()
    Bass = auto()
    SawX = auto()
    Harm = auto()
    Audio_In = auto()
    Wavetable = auto()

class osc_2_mode(osc_1_mode):
    paraphony = auto()

class filter_type(Enum):
    LP = auto()
    BP = auto()
    HP = auto()

class fx_types_neither(Enum):
    Chorus = 1
    Phaser = 2
    Flanger = 3
    Distortion = 4
    Bit_Crusher = 5
    _3_Bands_EQ = 6
    Peak_EQ = 7
    Multi_Comp = 8
    SuperUnison = 9

class fx_types_reverb(Enum):
    Reverb = 10

class fx_types_delay(Enum):
    Delay = 11

class fx_types_if_reverb(fx_types_neither, fx_types_delay):
    pass


class fx_types_if_delay(fx_types_neither, fx_types_reverb):
    pass


class fx_types_both(fx_types_neither, fx_types_reverb, fx_types_delay):
    pass

class lfo_shapes(Enum):
    up = auto()
    down = auto()
    curve = auto()
    flat = auto()

class scroll_positions(Enum):
    highest = auto()
    higher = auto()
    lower = auto()
    lowest = auto()

class n_bars(Enum):
    _1_Bar = auto()
    _2_Bar = auto()
    _3_Bar = auto()
    _4_Bar = auto()

class cycenv_retrigger_mode(Enum):
    Poly_Kbd = auto()
    Mono_Kbd = auto()
    Legato_Kbd = auto()


class lfo_retrigger_modes(cycenv_retrigger_mode):
    Free = auto()
    One = auto()
    CycEnv = auto()
    Seq_Start = auto()

class lfo1_retrigger_mode(lfo_retrigger_modes):
    LFO2 = auto()

class lfo2_retrigger_mode(lfo_retrigger_modes):
    LFO1 = auto()

class env_retrigger_mode(Enum):
    Env_Reset = auto()
    Env_Continue = auto()

class glide_type(Enum):
    Time = auto()
    Time_Legato = auto()
    Rate = auto()
    Rate_Legato = auto()
    Sync = auto()
    Sync_Legato = auto()

class uni_voice_mode(Enum):
    Unison = auto()
    Uni_Poly = auto()
    Uni_Para = auto()

class stage_order(Enum):
    Rise_Hold_Fall = auto()
    Rise_Fall_Hold = auto()
    Hold_Rise_Fall = auto()

class chord_root_note(Enum):
    c = auto()
    c_sharp = auto()
    d = auto()
    d_sharp = auto()
    e = auto()
    f = auto()
    f_sharp = auto()
    g = auto()
    g_sharp = auto()
    a = auto()
    a_sharp = auto()
    b = auto()

class scale_mode(Enum):
    Global = auto()
    Major = auto()
    Minor = auto()
    Dorian = auto()
    Mixolydian = auto()
    Blues = auto()
    Pentatonic = auto()
    User = auto()

class rate_lfo_shaper(Enum):
    One_Step = auto()
    All_Steps = auto()

class voice_allocation_modes(Enum):
    Cycle = auto()
    Reassign = auto()
    Reset = auto()

class note_steal_modes(Enum):
    Oldest = auto()
    Lowest_Velo = auto()
    _None = auto()

class effect_mode(Enum):
    send = auto()
    insert = auto()

class chorus_presets(Enum):
    Default = auto()
    Lush = auto()
    Dark = auto()
    Shaded = auto()
    Single = auto()

class phaser_preset(Enum):
    Default = auto()
    Default_Sync = auto()
    Space = auto()
    Space_Sync = auto()
    SnH = auto()
    SnH_Sync = auto()

class flanger_preset(Enum):
    Default = auto()
    Default_Sync = auto()
    Silly = auto()
    Silly_Sync = auto()

class reverb_presets(Enum):
    Default = auto()
    Long = auto()
    Hall = auto()
    Echoes = auto()
    Room = auto()
    Dark_Room = auto()

class delay_presets(Enum):
    Digital = auto()
    Digital_Sync = auto()
    Stereo = auto()
    Stereo_Sync = auto()
    Ping__dash__Pong = auto()
    Ping__dash__Pong_Sync = auto()
    Mono = auto()
    Mono_Sync = auto()
    Filtered = auto()
    Filtered_Sync = auto()
    Filtered_Ping__dash__Pong = auto()
    Filtered_P__dash__P_Sync = auto()

class distortion_preset(Enum):
    Classic = auto()
    Soft_Clip = auto()
    Germanium = auto()
    Dual_Fold = auto()
    Climb = auto()
    Tape = auto()

class _3_bands_eq_preset(Enum):
    Default = auto()
    Wide = auto()
    Mid_1k = auto()

class multi_comp_preset(Enum):
    OPP = auto()
    Bass_Ctrl = auto()
    High_Ctrl = auto()
    All_Up = auto()
    Tighter = auto()

class superunison_preset(Enum):
    Classic = auto()
    Ravey = auto()
    Soli = auto()
    Slow = auto()
    Slow_Trig = auto()
    Wide_Trig = auto()
    Mono_Trig = auto()
    Wavy = auto()

class Options(Enum):
    tab_primary = ("primary_tabs", frozenset(primary_tabs))
    primary_advanced = ("primary_tabs", frozenset((primary_tabs.Advanced,)))
    primary_sequencer = ("sequencer", frozenset((primary_tabs.Sequencer,)))
    tab_fx = ("fx_tabs", frozenset(fx_tabs))
    fx_1 = ("fx_tabs", frozenset((fx_tabs.FX_1,)))
    fx_2 = ("fx_tabs", frozenset((fx_tabs.FX_2,)))
    fx_3 = ("fx_tabs", frozenset((fx_tabs.FX_3,)))
    tab_chord_scale = ("chord_scale_tabs", frozenset(chord_scale_tabs))
    chord_tab = ("chord_scale_tabs", frozenset(chord_scale_tabs.Chord))
    scale_tab = ("chord_scale_tabs", frozenset(chord_scale_tabs.Scale))
    pnl_voices = ("voices_panel", frozenset(panel))
    stg_voices = ("voices_panel", frozenset((panel.settings,)))
    pnl_cycenv = ("cycenv_panel", frozenset(panel))
    stg_cycenv = ("cycenv_panel", frozenset((panel.settings,)))
    pnl_env = ("env_panel", frozenset(panel))
    stg_env = ("env_panel", frozenset((panel.settings,)))
    pnl_wheels = ("wheels_panel", frozenset(panel))
    stg_wheels = ("wheels_panel", frozenset((panel.settings,)))
    tab_secondary = ("secondary_tabs", frozenset(secondary_tabs))
    secondary_macro_matrix = ("secondary_tabs", frozenset((secondary_tabs.Macro__slash__Matrix,)))
    secondary_shaper = ("secondary_tabs", frozenset((secondary_tabs.LFO_Shaper,)))
    tab_lfos = ("lfo_tabs", frozenset(lfo_tabs))
    typ_rise_curve = ("rising_curve_types", frozenset(rising_curve_types))
    typ_falling_curve = ("falling_curve_types", frozenset(falling_curve_type))
    mde_cycenv = ("cycenv_modes", frozenset(cycenv_mode))
    env_mode = ("cycenv_modes", frozenset((cycenv_mode.Env,)))
    run_mode = ("cycenv_modes", frozenset((cycenv_mode.Run,)))
    loop_mode = ("cycenv_modes", frozenset((cycenv_mode.Loop,)))
    mde_voices = ("voice_modes", frozenset(voice_mode))
    mono_mode = ("voice_modes", frozenset((voice_mode.Mono,)))
    uni_mode = ("voice_modes", frozenset((voice_mode.Unison,)))
    polypara_mode = ("voice_modes", frozenset((voice_mode.Poly, voice_mode.Para)))
    mde_env_retrigger = ("retrigger_settings_env", frozenset(env_retrigger_mode))
    chd_octaves = ("chord_octaves", frozenset(chord_octaves))
    mde_seq_arp = ("sequencer_arpeggiator_modes", frozenset(sequencer_arpeggiator_modes))
    seq_arp_seq = ("sequencer_arpeggiator_modes", frozenset((sequencer_arpeggiator_modes.Seq,)))
    seq_arp_arp = ("sequencer_arpeggiator_modes", frozenset((sequencer_arpeggiator_modes.Arp,)))
    seq_arp_not_off = ("sequencer_arpeggiator_modes", frozenset(set(sequencer_arpeggiator_modes) - set((sequencer_arpeggiator_modes.Off,))))
    typ_attack_curve = ("attack_curve_types", frozenset(attack_curve_type))
    mde_seq_prog = ("arpeggiator_progression_modes", frozenset(arpeggiator_progression_modes))
    mde_seq_oct = ("arpeggiator_octave_modes", frozenset(arpeggiator_octave_modes))
    mde_routing_adv = ("routing_slot", frozenset(routing_slot_adv))
    mde_routing_seq = ("routing_slot", frozenset(routing_slot_seq))
    typ_osc_1 = ("osc_1_modes", frozenset(osc_1_mode))
    typ_osc_2 = ("osc_2_modes", frozenset(osc_2_mode))
    typ_filter = ("filter_type", frozenset(filter_type))
    typ_fx_1_chorus = ("fx1_type", frozenset((fx_types_neither.Chorus,)))
    typ_fx_1_phaser = ("fx1_type", frozenset((fx_types_neither.Phaser,)))
    typ_fx_1_flanger = ("fx1_type", frozenset((fx_types_neither.Flanger,)))
    typ_fx_1_distortion = ("fx1_type", frozenset((fx_types_neither.Distortion,)))
    typ_fx_1_bit_crusher = ("fx1_type", frozenset((fx_types_neither.Bit_Crusher,)))
    typ_fx_1__3_bands_eq = ("fx1_type", frozenset((fx_types_neither._3_Bands_EQ,)))
    typ_fx_1_peak_eq = ("fx1_type", frozenset((fx_types_neither.Peak_EQ,)))
    typ_fx_1_multi_comp = ("fx1_type", frozenset((fx_types_neither.Multi_Comp,)))
    typ_fx_1_superunison = ("fx1_type", frozenset((fx_types_neither.SuperUnison,)))
    typ_fx_1_reverb = ("fx1_type", frozenset(fx_types_reverb))
    typ_fx_1_delay = ("fx1_type", frozenset(fx_types_delay))
    typ_fx_1_neither = ("fx1_type", frozenset(fx_types_neither))
    typ_fx_2_chorus = ("fx2_type", frozenset((fx_types_neither.Chorus,)))
    typ_fx_2_phaser = ("fx2_type", frozenset((fx_types_neither.Phaser,)))
    typ_fx_2_flanger = ("fx2_type", frozenset((fx_types_neither.Flanger,)))
    typ_fx_2_distortion = ("fx2_type", frozenset((fx_types_neither.Distortion,)))
    typ_fx_2_bit_crusher = ("fx2_type", frozenset((fx_types_neither.Bit_Crusher,)))
    typ_fx_2__3_bands_eq = ("fx2_type", frozenset((fx_types_neither._3_Bands_EQ,)))
    typ_fx_2_peak_eq = ("fx2_type", frozenset((fx_types_neither.Peak_EQ,)))
    typ_fx_2_multi_comp = ("fx2_type", frozenset((fx_types_neither.Multi_Comp,)))
    typ_fx_2_superunison = ("fx2_type", frozenset((fx_types_neither.SuperUnison,)))
    typ_fx_2_reverb = ("fx2_type", frozenset(fx_types_reverb))
    typ_fx_2_delay = ("fx2_type", frozenset(fx_types_delay))
    typ_fx_2_neither = ("fx2_type", frozenset(fx_types_neither))
    typ_fx_3_chorus = ("fx3_type", frozenset((fx_types_neither.Chorus,)))
    typ_fx_3_phaser = ("fx3_type", frozenset((fx_types_neither.Phaser,)))
    typ_fx_3_flanger = ("fx3_type", frozenset((fx_types_neither.Flanger,)))
    typ_fx_3_distortion = ("fx3_type", frozenset((fx_types_neither.Distortion,)))
    typ_fx_3_bit_crusher = ("fx3_type", frozenset((fx_types_neither.Bit_Crusher,)))
    typ_fx_3__3_bands_eq = ("fx3_type", frozenset((fx_types_neither._3_Bands_EQ,)))
    typ_fx_3_peak_eq = ("fx3_type", frozenset((fx_types_neither.Peak_EQ,)))
    typ_fx_3_multi_comp = ("fx3_type", frozenset((fx_types_neither.Multi_Comp,)))
    typ_fx_3_superunison = ("fx3_type", frozenset((fx_types_neither.SuperUnison,)))
    typ_fx_3_reverb = ("fx3_type", frozenset(fx_types_reverb))
    typ_fx_3_delay = ("fx3_type", frozenset(fx_types_delay))
    typ_fx_3_neither = ("fx3_type", frozenset(fx_types_neither))
    typ_lfo_shape = ("lfo_shapes", frozenset(lfo_shapes))
    
    
