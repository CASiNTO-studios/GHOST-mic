import cv2
import numpy as np
import soundfile as sf
from scipy.signal import butter, filtfilt

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    """Applies a zero-phase bandpass filter to isolate acoustic vibrations."""
    nyquist = 0.5 * fs
    low = max(lowcut / nyquist, 1e-4)
    high = min(highcut / nyquist, 0.99)
    if low >= high:
        return data - np.mean(data)
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def extract_audio_from_video(video_path, output_wav_path, lowcut=20.0, highcut=None):
    """
    Extracts acoustic motion signals from pixel intensity fluctuations
    and writes them to a standardized 1D audio waveform (.wav).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0  # Fallback frame rate

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[*] Processing {video_path} | FPS: {fps:.2f} | Frames: {total_frames}")

    ret, first_frame = cap.read()
    if not ret:
        raise ValueError("Failed to read the initial frame from video.")

    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    displacement_signal = []

    frame_count = 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)

        # Track differential sub-pixel luminance changes across the spatial frame
        frame_diff = curr_gray - prev_gray
        displacement = np.mean(frame_diff)
        displacement_signal.append(displacement)

        prev_gray = curr_gray
        frame_count += 1

    cap.release()

    raw_signal = np.array(displacement_signal, dtype=np.float32)
    if len(raw_signal) == 0:
        raise ValueError("No video frames were analyzed.")

    # Highcut limit cannot exceed Nyquist frequency (FPS / 2)
    max_detectable_freq = (fps / 2.0) - 1.0
    actual_highcut = min(highcut, max_detectable_freq) if highcut else max(max_detectable_freq, lowcut + 1.0)

    # Filter out baseline lighting drift, keeping acoustic band
    filtered_signal = butter_bandpass_filter(raw_signal, lowcut, actual_highcut, fs=fps)

    # Normalize audio signal to standard [-1.0, 1.0] range
    peak = np.max(np.abs(filtered_signal))
    if peak > 0:
        normalized_signal = filtered_signal / peak
    else:
        normalized_signal = filtered_signal

    # Write normalized audio signal to disk
    sf.write(output_wav_path, normalized_signal, int(fps))
    print(f"[+] Successfully extracted raw optical audio: {output_wav_path}")
    return output_wav_path, fps