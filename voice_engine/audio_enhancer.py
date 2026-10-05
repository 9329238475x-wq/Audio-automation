# -*- coding: utf-8 -*-
"""
Cinema-Grade Audio Enhancer & Multi-Acoustic Mastering DSP.
Provides customized Radio FM & Pocket FM acoustic mastering chains for:
1. Male Cinema (Narrator, Hero, Father, Villain, Cop, Friend, Servant)
2. Female Cinema (Heroine, Sister, Bhabhi, Vamp, Mother)
3. Child / Kid Cinema (Child Male, Child Female)
4. Elderly Cinema (Grandfather, Grandmother)
"""

import os
import numpy as np
import soundfile as sf
from scipy import signal
from pathlib import Path
from typing import Union

def _peaking_filter(audio: np.ndarray, freq: float, gain_db: float, q: float, sr: int) -> np.ndarray:
    """Peaking parametric EQ filter (Audio EQ Cookbook)."""
    w0 = 2 * np.pi * freq / sr
    alpha = np.sin(w0) / (2.0 * q)
    A = 10.0 ** (gain_db / 40.0)
    b = np.array([1.0 + alpha * A, -2.0 * np.cos(w0), 1.0 - alpha * A])
    a = np.array([1.0 + alpha / A, -2.0 * np.cos(w0), 1.0 - alpha / A])
    return signal.lfilter(b / a[0], a / a[0], audio).astype(np.float32)

def _spectral_gate(audio: np.ndarray, sr: int = 24000, threshold_db: float = -45.0) -> np.ndarray:
    """Noise reduction: gentle gating for speech pauses."""
    frame_len = int(0.02 * sr)
    hop_len = int(0.01 * sr)

    if len(audio) < frame_len:
        return audio

    num_frames = 1 + (len(audio) - frame_len) // hop_len
    energy = np.zeros(num_frames)

    for i in range(num_frames):
        frame = audio[i * hop_len : i * hop_len + frame_len]
        energy[i] = np.mean(frame**2)

    energy_db = 10 * np.log10(np.maximum(energy, 1e-10))
    gate = np.where(energy_db < threshold_db, 0.25, 1.0)

    smooth_gate = np.convolve(gate, np.ones(5) / 5.0, mode="same")
    gate_expanded = np.repeat(smooth_gate, hop_len)

    if len(gate_expanded) < len(audio):
        gate_expanded = np.pad(gate_expanded, (0, len(audio) - len(gate_expanded)), "edge")
    else:
        gate_expanded = gate_expanded[:len(audio)]

    gate_expanded = np.maximum(gate_expanded, 0.1)
    return audio * gate_expanded

def _cinema_vocal_toning(audio: np.ndarray, sr: int = 24000, character: str = "NARRATOR") -> np.ndarray:
    """
    Radio FM & Cinema Acoustic Chain tailored by Speaker Category:
    - Child: Bright, clean, highpass 120Hz, no boomy chest rumble.
    - Female: Warm, silky, deep de-esser at 4800Hz, roll-off at 5500Hz.
    - Male: Chest presence 150Hz, notch 3200Hz, de-sibilance 5200Hz.
    - Elderly: Gentle low-end warmth, mellow rolled-off highs.
    """
    char_up = character.upper()

    # 1. Child / Kid Voice DSP
    if any(k in char_up for k in ("CHILD", "KID", "BOY", "GIRL", "MUNNA", "PINKI")):
        # Highpass at 120Hz (removes low rumble, keeps child vocal light & pure)
        sos_hp = signal.butter(2, 120, btype="highpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_hp, audio)

        # Sweet articulate presence (+2.5 dB at 2800 Hz)
        audio = _peaking_filter(audio, freq=2800.0, gain_db=2.5, q=1.2, sr=sr)

        # Child sibilance control (Cut -4.0 dB at 6000 Hz)
        audio = _peaking_filter(audio, freq=6000.0, gain_db=-4.0, q=1.5, sr=sr)

        # Gentle analog saturation
        audio = np.tanh(audio * 1.05) / 1.05

    # 2. Elderly Voice DSP (Grandfather / Grandmother)
    elif any(k in char_up for k in ("GRANDFATHER", "GRANDMOTHER", "DADA", "DADI", "ELDER")):
        # Highpass at 75Hz
        sos_hp = signal.butter(2, 75, btype="highpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_hp, audio)

        # Warm mellow body (+2.5 dB at 200 Hz)
        audio = _peaking_filter(audio, freq=200.0, gain_db=2.5, q=1.1, sr=sr)

        # Smooth high roll-off (> 5200 Hz) for soft aged resonance
        sos_lp = signal.butter(2, 5200, btype="lowpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_lp, audio)

        # Warm tube warmth
        audio = np.tanh(audio * 1.12) / 1.12

    # 3. Adult Female Voice DSP (Heroine, Mother, Sister, Bhabhi, Vamp)
    elif any(k in char_up for k in ("HEROINE", "FEMALE", "MOTHER", "SISTER", "BHABHI", "VAMP", "WOMAN")):
        # Highpass at 80Hz
        sos_hp = signal.butter(2, 80, btype="highpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_hp, audio)

        # Velvety chest warmth (+3.5 dB at 240 Hz)
        audio = _peaking_filter(audio, freq=240.0, gain_db=3.5, q=1.2, sr=sr)

        # Cut nasal bite (-4.5 dB at 3400 Hz)
        audio = _peaking_filter(audio, freq=3400.0, gain_db=-4.5, q=1.4, sr=sr)

        # Radio FM De-Esser: Notch cut -8.0 dB at 4800 Hz
        audio = _peaking_filter(audio, freq=4800.0, gain_db=-8.0, q=1.8, sr=sr)

        # Silky cinema high roll-off at 5500 Hz
        sos_lp = signal.butter(2, 5500, btype="lowpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_lp, audio)

        # Silky analog tube saturation
        audio = np.tanh(audio * 1.10) / 1.10

    # 4. Adult Male Voice DSP (Narrator, Hero, Father, Villain, Cop, Friend, Servant)
    else:
        # Highpass at 65Hz (anti-rumble)
        sos_hp = signal.butter(2, 65, btype="highpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_hp, audio)

        # Deep Baritone Chest body (+3.8 dB at 150 Hz)
        audio = _peaking_filter(audio, freq=150.0, gain_db=3.8, q=1.0, sr=sr)

        # Anti-harshness (-4.5 dB at 3200 Hz)
        audio = _peaking_filter(audio, freq=3200.0, gain_db=-4.5, q=1.3, sr=sr)

        # De-sibilance (-4.0 dB at 5200 Hz)
        audio = _peaking_filter(audio, freq=5200.0, gain_db=-4.0, q=1.5, sr=sr)

        # Cinema high-cut (> 6800 Hz)
        sos_lp = signal.butter(2, 6800, btype="lowpass", fs=sr, output="sos")
        audio = signal.sosfilt(sos_lp, audio)

        # Vintage analog saturation
        audio = np.tanh(audio * 1.15) / 1.15

    return audio.astype(np.float32)

def _dynamic_range_compression(
    audio: np.ndarray,
    threshold_db: float = -20.0,
    ratio: float = 2.0,
    attack_ms: float = 8.0,
    release_ms: float = 180.0,
    sr: int = 24000
) -> np.ndarray:
    """Smooth dynamic compression: evens out volume without harshness."""
    window_size = int(0.01 * sr)
    if window_size <= 0 or len(audio) < window_size:
        return audio

    rms = np.convolve(audio**2, np.ones(window_size) / window_size, mode="same")
    rms = np.sqrt(np.maximum(rms, 1e-10))
    rms_db = 20 * np.log10(rms)

    gain_reduction_db = np.zeros_like(rms_db)
    mask = rms_db > threshold_db
    gain_reduction_db[mask] = (threshold_db - rms_db[mask]) * (1.0 - 1.0 / ratio) / ratio

    attack_samples = max(1, int(attack_ms * sr / 1000))
    release_samples = max(1, int(release_ms * sr / 1000))

    envelope = np.zeros_like(gain_reduction_db)
    envelope[0] = gain_reduction_db[0]

    for i in range(1, len(envelope)):
        if gain_reduction_db[i] < envelope[i - 1]:
            envelope[i] = envelope[i - 1] + (gain_reduction_db[i] - envelope[i - 1]) / attack_samples
        else:
            envelope[i] = envelope[i - 1] + (gain_reduction_db[i] - envelope[i - 1]) / release_samples

    gain_linear = 10.0 ** (envelope / 20.0)
    return audio * gain_linear

def _loudness_normalize(audio: np.ndarray, target_lufs: float = -23.0) -> np.ndarray:
    """Normalize loudness to standard broadcast target with gentle soft-clipping."""
    rms = np.sqrt(np.mean(audio**2))
    if rms < 1e-6:
        return audio

    rms_db = 20 * np.log10(rms)
    gain_db = target_lufs - rms_db
    gain_linear = 10.0 ** (gain_db / 20.0)

    output = audio * gain_linear

    peak = np.max(np.abs(output))
    if peak > 0.95:
        mask_pos = output > 0.95
        mask_neg = output < -0.95
        output[mask_pos] = 0.95 + 0.05 * np.tanh((output[mask_pos] - 0.95) / 0.05)
        output[mask_neg] = -0.95 + 0.05 * np.tanh((output[mask_neg] + 0.95) / 0.05)

    return output.astype(np.float32)

def enhance_audio(
    input_wav: Union[str, Path],
    output_wav: Union[str, Path],
    sr: int = 24000,
    character: str = "NARRATOR",
    enable_gate: bool = True,
    enable_toning: bool = True,
    enable_compress: bool = True,
    enable_loudness: bool = True,
) -> str:
    """
    Applies the cinema vocal mastering chain tailored for character acoustics.
    """
    input_wav = str(input_wav)
    output_wav = str(output_wav)

    if not os.path.exists(input_wav) or os.path.getsize(input_wav) < 512:
        return input_wav

    audio, file_sr = sf.read(input_wav, dtype="float32")
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    if file_sr != sr:
        num_samples = int(len(audio) * float(sr) / file_sr)
        audio = signal.resample(audio, num_samples)

    # 1. Spectral gate (noise floor)
    if enable_gate:
        audio = _spectral_gate(audio, sr)

    # 2. Cinema Vocal Toning (Tailored for Male, Female, Child, Elderly)
    if enable_toning:
        audio = _cinema_vocal_toning(audio, sr, character=character)

    # 3. Dynamic compression
    if enable_compress:
        audio = _dynamic_range_compression(audio, sr=sr)

    # 4. Radio FM Loudness normalization
    if enable_loudness:
        char_up = character.upper()
        if any(k in char_up for k in ("CHILD", "KID")):
            target = -24.0
        elif any(k in char_up for k in ("HEROINE", "FEMALE", "MOTHER", "SISTER", "BHABHI", "VAMP")):
            target = -24.5
        else:
            target = -23.0
        audio = _loudness_normalize(audio, target_lufs=target)

    peak = np.max(np.abs(audio))
    if peak > 0.98:
        audio = audio * (0.97 / peak)

    os.makedirs(os.path.dirname(output_wav), exist_ok=True)
    sf.write(output_wav, audio, sr, subtype="PCM_16")
    return output_wav
