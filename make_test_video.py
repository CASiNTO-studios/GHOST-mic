import cv2
import numpy as np
import os

def create_synthetic_vibration_video(output_path="data/vibration_test.mp4", duration_sec=5, fps=30):
    os.makedirs("data", exist_ok=True)
    
    width, height = 640, 480
    total_frames = int(duration_sec * fps)
    
    # Video writer using MP4V codec
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)
    
    # Base pattern: high-contrast alternating vertical stripes
    # Visual-Mic algorithms require strong edges to track phase shifts
    stripe_width = 32
    base_pattern = np.zeros((height, width), dtype=np.uint8)
    for x in range(0, width, stripe_width * 2):
        base_pattern[:, x:x + stripe_width] = 255

    vibration_frequency_hz = 4.0  # 4 vibrations per second
    vibration_amplitude_pixels = 3.0  # Micro-displacement of 3 pixels

    print(f"Generating '{output_path}' ({duration_sec}s @ {fps} FPS)...")

    for i in range(total_frames):
        t = i / fps
        # Calculate sub-pixel horizontal shift: x(t) = A * sin(2*pi*f*t)
        shift_x = vibration_amplitude_pixels * np.sin(2 * np.pi * vibration_frequency_hz * t)
        
        # 2x3 Affine transformation matrix for horizontal translation
        M = np.float32([
            [1, 0, shift_x],
            [0, 1, 0]
        ])
        
        # Apply motion with linear sub-pixel interpolation
        shifted_frame = cv2.warpAffine(
            base_pattern, 
            M, 
            (width, height), 
            borderMode=cv2.BORDER_WRAP, 
            flags=cv2.INTER_LINEAR
        )
        
        out.write(shifted_frame)

    out.release()
    print(f"[✓] Test video successfully generated: {output_path}")

if __name__ == "__main__":
    create_synthetic_vibration_video()