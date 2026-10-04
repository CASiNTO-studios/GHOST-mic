import os
import sys
from visual_extractor import extract_audio_from_video

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/run_test.py data/<your_video.mp4>")
        return

    video_input = sys.argv[1]
    if not os.path.exists(video_input):
        print(f"Error: Target file not found: {video_input}")
        return

    os.makedirs("output", exist_ok=True)
    output_audio = os.path.join("output", "raw_recovered.wav")

    print("[*] Running Phase 1 baseline optical extraction...")
    extract_audio_from_video(video_input, output_audio)
    print(f"[✓] Phase 1 complete! Output generated at {output_audio}")

if __name__ == "__main__":
    main()