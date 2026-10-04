import os
import sys
import numpy as np
import soundfile as sf
from scipy.signal import medfilt
from visual_extractor import extract_audio_from_video

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/pipeline.py data/<your_video.mp4>")
        return

    video_input = sys.argv[1]
    if not os.path.exists(video_input):
        print(f"Error: Target file not found: {video_input}")
        return

    os.makedirs("output", exist_ok=True)
    raw_audio_path = os.path.join("output", "raw_recovered.wav")
    cleaned_audio_path = os.path.join("output", "ai_cleaned.wav")
    
    # Step 1: Optical Extraction
    print("\n[1/2] Extracting optical audio from video frames...")
    try:
        extract_audio_from_video(video_input, raw_audio_path)
    except Exception as e:
        print(f"Extraction Error: {e}")
        sys.exit(1)

    # Step 2: Adaptive Signal Denoising & Normalization
    print("\n[2/2] Running signal enhancement & noise removal...")
    try:
        data, rate = sf.read(raw_audio_path)
        
        # 1. Detrend signal (remove DC drift/lighting variations)
        data_centered = data - np.mean(data)
        
        # 2. Median filter to remove visual sensor spikes/glitches
        kernel_size = 3 if len(data_centered) >= 3 else 1
        filtered = medfilt(data_centered, kernel_size=kernel_size)
        
        # 3. Peak normalization to boost signal audibility
        max_val = np.max(np.abs(filtered))
        if max_val > 0:
            cleaned = (filtered / max_val) * 0.95
        else:
            cleaned = filtered

        # Save enhanced audio
        sf.write(cleaned_audio_path, cleaned.astype(np.float32), rate)
        print(f"\n[✓] Pipeline Complete! Clean audio saved at: {cleaned_audio_path}")
        
    except Exception as e:
        print(f"\n[!] Filter bypass fallback: {e}")
        # Safe fallback: copy original raw audio
        if os.path.exists(raw_audio_path):
            data, rate = sf.read(raw_audio_path)
            sf.write(cleaned_audio_path, data, rate)

if __name__ == "__main__":
    main()