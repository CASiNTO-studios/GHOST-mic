import os
import numpy as np
import soundfile as sf
from src.visual_extractor import extract_audio_from_video

def run_pipeline(video_path, raw_audio_path, cleaned_audio_path):
    print("\n[1/2] Reconstructing optical acoustic waveform from rolling shutter...")
    extract_audio_from_video(video_path, raw_audio_path)
    
    print("\n[2/2] Applying Forensic Vocal Gain & Dynamic Expansion...")
    try:
        data, rate = sf.read(raw_audio_path)
        
        # 1. Strip the initial transient spike (first 50ms) that kills normalization
        trim_samples = int(rate * 0.05)
        if len(data) > trim_samples:
            data[:trim_samples] = 0.0
            
        # 2. Dynamic Speech AGC (Automatic Gain Control)
        # Calculate moving RMS energy to pull the quiet speech phonemes up to audible volume
        window_size = int(rate * 0.02)  # 20ms analysis window
        padded = np.pad(data ** 2, (window_size//2, window_size//2), mode='edge')
        energy = np.convolve(padded, np.ones(window_size)/window_size, mode='valid')
        rms = np.sqrt(np.maximum(energy, 1e-6))
        
        # Compress dynamic range: amplify quiet speech parts
        gain = 1.0 / (rms + 0.05)
        gain = np.clip(gain, 0.5, 8.0)  # Safe gain bounds
        amplified = data * gain
        
        # 3. Final master normalization (0.95 Full Scale)
        peak = np.max(np.abs(amplified))
        if peak > 0:
            final_audio = (amplified / peak) * 0.95
        else:
            final_audio = amplified

        sf.write(cleaned_audio_path, final_audio.astype(np.float32), rate)
        print(f"\n[✓] Speech amplified and finalized: {cleaned_audio_path}")
        
    except Exception as e:
        print(f"Error in signal enhancement: {e}")