import cv2
import numpy as np
import soundfile as sf

def extract_audio_from_video(video_path, output_wav_path):
    """
    Visual Microphone: 1D Phase-Based Rolling Shutter Reconstruction.
    Extracts line-by-line phase displacement on high-contrast vertical features
    and applies a comb filter to remove sensor blanking harmonics.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")

    fps = 60.0  # Ground-truth rate for the Pentax rolling-shutter dataset
    ret, first_frame = cap.read()
    if not ret:
        cap.release()
        raise ValueError("Video contains no readable frames.")

    height, width = first_frame.shape[:2]
    fs = int(fps * height)  # 60 * 720 = 43,200 Hz line rate

    # Focus on the text area where vertical edge contrast is strongest
    # (Crop horizontal margins to eliminate uniform red packaging regions)
    crop_x1 = int(width * 0.10)
    crop_x2 = int(width * 0.90)

    # Reference scanlines
    ref_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    ref_roi = ref_gray[:, crop_x1:crop_x2]

    # Pre-calculate spatial derivative for the 1D phase approximation
    ref_dx = cv2.Sobel(ref_roi, cv2.CV_32F, 1, 0, ksize=3)
    ref_energy = ref_dx ** 2
    weight_per_line = np.sum(ref_energy, axis=1) + 1e-5

    signal_chunks = []
    print(f"Tracking sub-pixel scanlines: {width}x{height} @ {fps} FPS (Line rate: {fs} Hz)...")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
        roi = gray[:, crop_x1:crop_x2]

        # 1D Phase displacement: delta_x = - (I_t - I_0) / (dI / dx)
        diff = roi - ref_roi
        disp_map = - (diff * ref_dx) / (ref_energy + 1e-4)

        # Weighted spatial average along each scanline
        line_displacement = np.sum(disp_map * ref_energy, axis=1) / weight_per_line

        # Subtract baseline drift of current frame to suppress frame-boundary jump
        line_displacement = line_displacement - np.mean(line_displacement)

        # Apply a mild Tukey window to edge lines (0..15 and 705..719)
        # to smooth the discontinuity between frame boundaries
        edge_len = 16
        ramp = 0.5 * (1.0 - np.cos(np.pi * np.arange(edge_len) / edge_len))
        line_displacement[:edge_len] *= ramp
        line_displacement[-edge_len:] *= ramp[::-1]

        signal_chunks.extend(line_displacement.tolist())
        frame_count += 1

    cap.release()

    raw_audio = np.array(signal_chunks, dtype=np.float32)
    if len(raw_audio) == 0:
        raise ValueError("No frames processed.")

    # Comb notch filter for the 60 Hz frame rate and its harmonics
    # The sensor blanking gap repeats every 60 Hz (60, 120, 180, 240... Hz)
    fft_spec = np.fft.rfft(raw_audio)
    freqs = np.fft.rfftfreq(len(raw_audio), 1.0 / fs)

    # Notch width of 3 Hz around every 60 Hz harmonic up to the speech ceiling
    for h in range(60, 4000, 60):
        notch_indices = np.where(np.abs(freqs - h) <= 2.5)[0]
        fft_spec[notch_indices] *= 0.01

    # Keep speech range: suppress frequencies below 150 Hz and above 3400 Hz
    speech_mask = (freqs >= 150) & (freqs <= 3400)
    fft_spec[~speech_mask] *= 0.02

    reconstructed_audio = np.fft.irfft(fft_spec, n=len(raw_audio))

    # Resample to 44.1 kHz for standard browser audio playback
    target_sr = 44100
    duration = len(reconstructed_audio) / fs
    target_len = int(duration * target_sr)

    t_src = np.linspace(0, duration, len(reconstructed_audio), endpoint=False)
    t_dst = np.linspace(0, duration, target_len, endpoint=False)
    final_audio = np.interp(t_dst, t_src, reconstructed_audio)

    # Peak normalization
    peak = np.max(np.abs(final_audio))
    if peak > 0:
        final_audio = (final_audio / peak) * 0.95

    sf.write(output_wav_path, final_audio.astype(np.float32), target_sr)
    print(f"[✓] Extracted {frame_count} frames. Saved cleanly to {output_wav_path}.")