# -*- coding: utf-8 -*-
"""
Studio Audio Enhancer (Cinema Quality Vocal Mastering)
Specially engineered to eliminate harsh digital bite ("कान में चुभन ख़त्म करना"):
1. High-Pass Filter (65Hz male / 80Hz female) - Cleans sub-bass rumble
2. Cinema Vocal Warmth:
   - Male: 150 Hz boost (+3.5 dB)
   - Female (Heroine): 240 Hz boost (+3.5 dB) for silky, warm, full-bodied presence
3. Anti-Harshness & Dedicated Multi-Stage De-Esser:
   - Cuts nasal harsh bite at 3400 Hz (-4.5 dB)
   - Female De-Esser: Deep notch at 4800 Hz (-8.0 dB) to permanently eliminate piercing sibilance (स, श, च)
4. Silky Cinema High-Cut:
   - Female: Low-pass filter at 5500 Hz (transforms sharp digital TTS into a smooth cinema ribbon mic tone)
   - Male: Low-pass filter at 6800 Hz
5. Smooth Optical Dynamic Compression (Clarity without ear fatigue or pumping)
6. Warm Analog Tube Saturation (Silky soft rounding of digital peaks)
7. Broadcast Loudness Normalization (-23 LUFS male, -24.5 LUFS female)
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

    smooth_gate = np.convolve(gate, np.ones(5) / 5.0, mode='same')
    gate_expanded = np.repeat(smooth_gate, hop_len)

    if len(gate_expanded) < len(audio):
        gate_expanded = np.pad(gate_expanded, (0, len(audio) - len(gate_expanded)), 'edge')
    else:
        gate_expanded = gate_expanded[:len(audio)]

    gate_expanded = np.maximum(gate_expanded, 0.1)
    return audio * gate_expanded

def _cinema_vocal_toning(audio: np.ndarray, sr: int = 24000, character: str = "NARRATOR") -> np.ndarray:
    """
    Cinema EQ & Anti-Harshness Mastering:
    Differentiates male (Narrator/Hero) and female (Heroine/Mother) to completely
    eliminate piercing sibilance ("कान में चुभन") while providing cinema warmth.
    """
    is_female = character.upper() in ("HEROINE", "FEMALE", "MOTHER", "GIRL", "WOMAN")

    if is_female:
        # --- FEMALE CINEMA MASTERING CHAIN ---
        # 1. High-Pass at 80 Hz (clean sub rumble)
        sos_hp = signal.butter(2, 80, btype='highpass', fs=sr, output='sos')
        audio = signal.sosfilt(sos_hp, audio)

        # 2. Female Chest Warmth & Intimacy: Boost +3.5 dB at 240 Hz (warm velvety body)
        audio = _peaking_filter(audio, freq=240.0, gain_db=3.5, q=1.2, sr=sr)

        # 3. Cut Nasal Honk / Upper Mid bite: Cut -4.5 dB at 3400 Hz
        audio = _peaking_filter(audio, freq=3400.0, gain_db=-4.5, q=1.4, sr=sr)

        # 4. CRITICAL DE-ESSER: Deep notch Cut -8.0 dB at 4800 Hz
        # (Permanently eliminates the piercing 's', 'sh', 'ch' bite of SwaraNeural)
        audio = _peaking_filter(audio, freq=4800.0, gain_db=-8.0, q=1.8, sr=sr)

        # 5. Silky Cinema High Roll-Off (Gentle lowpass at 5500 Hz)
        # Removes tinny digital sibilance, transforming into warm movie dialog
        sos_lp = signal.butter(2, 5500, btype='lowpass', fs=sr, output='sos')
        audio = signal.sosfilt(sos_lp, audio)

        # 6. Silky Analog Tube Saturation
        audio = np.tanh(audio * 1.10) / 1.10

    else:
        # --- MALE CINEMA MASTERING CHAIN ---
        # 1. Clean sub-bass rumble (<65Hz)
        sos_hp = signal.butter(2, 65, btype='highpass', fs=sr, output='sos')
        audio = signal.sosfilt(sos_hp, audio)

        # 2. Cinema Chest Body (150 Hz boost +3.5 dB)
        audio = _peaking_filter(audio, freq=150.0, gain_db=3.5, q=1.0, sr=sr)

        # 3. Anti-Harshness: Cut 3200 Hz by -4.5 dB
        audio = _peaking_filter(audio, freq=3200.0, gain_db=-4.5, q=1.3, sr=sr)

        # 4. De-Sibilance: Cut 5200 Hz by -4.0 dB
        audio = _peaking_filter(audio, freq=5200.0, gain_db=-4.0, q=1.5, sr=sr)

        # 5. Silky Cinema High-Cut (Gentle roll-off > 6800 Hz)
        sos_lp = signal.butter(2, 6800, btype='lowpass', fs=sr, output='sos')
        audio = signal.sosfilt(sos_lp, audio)

        # 6. Warm Vintage Analog Tube Saturation
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

    rms = np.convolve(audio**2, np.ones(window_size) / window_size, mode='same')
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

    audio, file_sr = sf.read(input_wav, dtype='float32')
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    if file_sr != sr:
        num_samples = int(len(audio) * float(sr) / file_sr)
        audio = signal.resample(audio, num_samples)

    # 1. Spectral gate (noise floor)
    if enable_gate:
        audio = _spectral_gate(audio, sr)

    # 2. Cinema Vocal Toning & Anti-Piercing De-Esser (Male vs Female)
    if enable_toning:
        audio = _cinema_vocal_toning(audio, sr, character=character)

    # 3. Dynamic compression
    if enable_compress:
        audio = _dynamic_range_compression(audio, sr=sr)

    # 4. Loudness normalization (-24.5 for female/heroine, -23.0 for male/narrator)
    if enable_loudness:
        target = -24.5 if character.upper() in ("HEROINE", "FEMALE", "MOTHER") else -23.0
        audio = _loudness_normalize(audio, target_lufs=target)

    peak = np.max(np.abs(audio))
    if peak > 0.98:
        audio = audio * (0.97 / peak)

    os.makedirs(os.path.dirname(output_wav), exist_ok=True)
    sf.write(output_wav, audio, sr, subtype='PCM_16')
    return output_wav
