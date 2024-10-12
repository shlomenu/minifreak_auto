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

class voices_panel(Enum):
    settings = auto()
    controls = auto()

class cycenv_panel(Enum):
    settings = auto()
    controls = auto()

class env_panel(Enum):
    settings = auto()
    controls = auto()

class wheels_panel(Enum):
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

class attack_curve_types(Enum):
    Default = auto()
    Quick = auto()

class falling_curve_types(Enum):
    Default = auto()
    Percussive = auto()

class toggle(Enum):
    on = auto()
    off = auto()

class cycenv_modes(Enum):
    Env = auto()
    Run = auto()
    Loop = auto()

class voice_modes(Enum):
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

class routing_assignments(Enum):
    uni_spread = auto()
    vibrato_rate = auto()
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
    time_fx_1 = auto()
    intensity_fx_1 = auto()
    amount_fx_1 = auto()
    time_fx_2 = auto()
    intensity_fx_2 = auto()
    amount_fx_2 = auto()
    time_fx_3 = auto()
    intensity_fx_3 = auto()
    amount_fx_3 = auto()
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

class routing_slot(Enum):
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
    seq_mod_src_1 = auto()
    seq_mod_src_2 = auto()
    seq_mod_src_3 = auto()
    seq_mod_src_4 = auto()

class oscillator_modes(Enum):
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
    paraphony = auto()

class filter_types(Enum):
    LP = auto()
    BP = auto()
    HP = auto()

class fx_types(Enum):
    Chorus = auto()
    Phaser = auto()
    Flanger = auto()
    Reverb = auto()
    Delay = auto()
    Distortion = auto()
    Bit_Crusher = auto()
    _3_Bands_EQ = auto()
    Peak_EQ = auto()
    Multi_Comp = auto()
    SuperUnison = auto()

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

class lfo_retrigger_modes(Enum):
    Free = auto()
    Poly_Kbd = auto()
    Mono_Kbd = auto()
    Legato_Kbd = auto()
    One = auto()
    LFO1 = auto()
    LFO2 = auto()
    CycEnv = auto()
    Seq_Start = auto()

class env_retrigger_modes(Enum):
    Env_Reset = auto()
    Env_Continue = auto()

class glide_types(Enum):
    Time = auto()
    Time_Legato = auto()
    Rate = auto()
    Rate_Legato = auto()
    Sync = auto()
    Sync_Legato = auto()

class uni_voice_modes(Enum):
    Unison = auto()
    Uni_Poly = auto()
    Uni_Para = auto()

class stage_orders(Enum):
    Rise_Hold_Fall = auto()
    Rise_Fall_Hold = auto()
    Hold_Rise_Fall = auto()

class notes(Enum):
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

class scale_modes(Enum):
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

class Options(Enum):
    tab_primary = frozenset(primary_tabs)
    primary_advanced = frozenset((primary_tabs.Advanced,))
    primary_sequencer = frozenset((primary_tabs.Sequencer,))
    tab_fx = frozenset(fx_tabs)
    fx_1 = frozenset((fx_tabs.FX_1,))
    fx_2 = frozenset((fx_tabs.FX_2,))
    fx_3 = frozenset((fx_tabs.FX_3,))
    tab_chord_scale = frozenset(chord_scale_tabs)
    chord_tab = frozenset(chord_scale_tabs.Chord)
    scale_tab = frozenset(chord_scale_tabs.Scale)
    pnl_voices = frozenset(voices_panel)
    stg_voices = frozenset((voices_panel.settings,))
    pnl_cycenv = frozenset(cycenv_panel)
    stg_cycenv = frozenset((cycenv_panel.settings,))
    pnl_env = frozenset(env_panel)
    stg_env = frozenset((env_panel.settings,))
    pnl_wheels = frozenset(wheels_panel)
    stg_wheels = frozenset((wheels_panel.settings,))
    tab_secondary = frozenset(secondary_tabs)
    secondary_macro_matrix = frozenset((secondary_tabs.Macro__slash__Matrix,))
    secondary_shaper = frozenset((secondary_tabs.LFO_Shaper,))
    tab_lfos = frozenset(lfo_tabs)
    typ_lfo_rate = frozenset(lfo_rate_types)
    typ_rise_curve = frozenset(rising_curve_types)
    typ_falling_curve = frozenset(falling_curve_types)
    mde_cycenv = frozenset(cycenv_modes)
    env_mode = frozenset((cycenv_modes.Env,))
    run_mode = frozenset((cycenv_modes.Run,))
    loop_mode = frozenset((cycenv_modes.Loop,))
    mde_voices = frozenset(voice_modes)
    mono_mode = frozenset((voice_modes.Mono,))
    uni_mode = frozenset((voice_modes.Unison,))
    polypara_mode = frozenset((voice_modes.Poly, voice_modes.Para))
    chd_octaves = frozenset(chord_octaves)
    mde_seq_arp = frozenset(sequencer_arpeggiator_modes)
    seq_arp_seq = frozenset((sequencer_arpeggiator_modes.Seq,))
    seq_arp_arp = frozenset((sequencer_arpeggiator_modes.Arp,))
    seq_arp_not_off = frozenset(set(sequencer_arpeggiator_modes) - set((sequencer_arpeggiator_modes.Off,)))
    typ_attack_curve = frozenset(attack_curve_types)
    mde_seq_prog = frozenset(arpeggiator_progression_modes)
    mde_seq_oct = frozenset(arpeggiator_octave_modes)
    asn_routing_slot_adv = frozenset(routing_assignments)
    btn_selected_unselected = Enum('button', names='selected unselected')
    mde_routing_adv = frozenset(set(routing_slot) - set((routing_slot.seq_mod_src_1, routing_slot.seq_mod_src_2, routing_slot.seq_mod_src_3, routing_slot.seq_mod_src_4)))
    mde_routing_seq = frozenset((routing_slot.seq_mod_src_1, routing_slot.seq_mod_src_2, routing_slot.seq_mod_src_3, routing_slot.seq_mod_src_4))
    typ_osc_1 = frozenset(set(oscillator_modes) - set((oscillator_modes.paraphony,)))
    typ_osc_2 = frozenset(oscillator_modes)
    typ_filter = frozenset(filter_types)
    stg_fx = frozenset(
        (t1, t2, t3) 
        for t1 in fx_types 
        for t2 in fx_types 
        for t3 in fx_types 
        if (
            [t1, t2, t3].count(fx_types.Reverb) < 2 
            and [t1, t2, t3].count(fx_types.Delay) < 2
        )
    )
    typ_lfo_shape = frozenset(lfo_shapes)
    scr_seq_note = frozenset(scroll_positions)
    btn_trigger = Enum('button', names='trigger')
    mde_n_bars = frozenset(n_bars)
    mde_lfo1_retrigger = frozenset(set(lfo_retrigger_modes) - set((lfo_retrigger_modes.LFO1,)))
    mde_lfo2_retrigger = frozenset(set(lfo_retrigger_modes) - set((lfo_retrigger_modes.LFO2,)))
    mde_env_retrigger = frozenset(env_retrigger_modes)
    mde_glide_voices = frozenset(glide_types)
    mde_uni_voices = frozenset(uni_voice_modes)
    mde_cycenv_retrigger = frozenset(set(lfo_retrigger_modes) - set((lfo_retrigger_modes.Free, lfo_retrigger_modes.One, lfo_retrigger_modes.CycEnv, lfo_retrigger_modes.Seq_Start)))
    mde_stage_order = frozenset(stage_orders)
    mde_name_scale = frozenset(notes)
    mde_scale = frozenset(scale_modes)
    mde_lfo_shaper_rate = frozenset(rate_lfo_shaper)
    mde_allocation_voices = frozenset(voice_allocation_modes)
    mde_note_steal_voices = frozenset(note_steal_modes)
    typ_fx = frozenset(fx_types)
    
    
