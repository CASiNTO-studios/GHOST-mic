# 🎙️ GhostMic: Visual Micro-Vibration Forensics

> **Recover the invisible. Verify the authentic.**

GhostMic is a computer-vision-based deepfake detection and audio forensics tool that extracts hidden audio information from the **imperceptible micro-vibrations of pixels in silent videos**.

Instead of relying solely on an existing audio track, GhostMic analyzes subtle pixel-level movements caused by physical vibrations in the scene and converts these variations into an **audio waveform**. The recovered signal can then be compared with an available audio track to help identify whether the audio is authentic or potentially tampered with.

---

## 🧠 Overview

Everyday objects can vibrate in response to nearby sound. Although these vibrations are often invisible to the human eye, they can produce extremely small variations in the pixels captured by a camera.

GhostMic uses computer vision and signal processing to capture these variations:

```text
Silent Video
     │
     ▼
🎥 Pixel-Level Motion
     │
     ▼
🔬 Micro-Vibration Extraction
     │
     ▼
📈 Signal Processing
     │
     ▼
🎵 Audio Waveform
     │
     ▼
🔍 Audio Forensic Analysis
```

The system essentially turns a camera into a **visual microphone**, allowing hidden acoustic information to be recovered from video.

---

## ✨ Key Features

### 🔬 Optical Audio Extraction

Analyzes subtle temporal pixel variations within video frames to extract signals corresponding to physical vibrations caused by sound.

### 🧹 Signal Enhancement

The extracted signal is processed to improve its quality and make the recovered waveform easier to analyze.

Processing includes:

- **Median filtering** — reduces noise and outliers.
- **Detrending** — removes slow-moving baseline variations.
- **Peak normalization** — scales the recovered signal for consistent playback.

### 🎚️ Upsampling

Typical videos have relatively low frame rates compared with standard audio sampling rates.

GhostMic converts the extracted low-FPS signal into a playable **44.1 kHz audio waveform** through signal resampling.

```text
Video Frames
   ↓
Low-FPS Signal
   ↓
Signal Processing
   ↓
Resampling / Upsampling
   ↓
44.1 kHz WAV Audio
```

### 📊 Interactive Streamlit Dashboard

A simple web interface allows users to:

- Upload an MP4 video
- Process the video
- Extract the optical audio signal
- Listen to the recovered waveform
- Inspect the generated result

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend / Dashboard | Streamlit |
| Computer Vision | OpenCV |
| Numerical Processing | NumPy |
| Signal Processing | SciPy |
| Noise Reduction | Noisereduce |
| Audio I/O | SoundFile |
| Language | Python |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/GhostMic.git
cd GhostMic
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install streamlit soundfile noisereduce scipy opencv-python numpy
```

---

## ▶️ How to Use

### 1. Start the Streamlit Application

From the project root directory:

```bash
streamlit run app.py
```

Streamlit will launch the GhostMic dashboard in your browser.

### 2. Upload a Video

Inside the dashboard:

1. Click the **Upload Video** button.
2. Select an **MP4 video** containing suitable visual material.
3. Wait for GhostMic to process the video.

### 3. Recover the Audio

The pipeline will:

```text
📹 MP4 Video
   ↓
🔬 Visual Signal Extraction
   ↓
🧹 Noise & Trend Removal
   ↓
📈 Signal Normalization
   ↓
🎚️ Upsampling
   ↓
🔊 Recovered Audio
```

Once processing is complete, use the built-in audio player to **listen to the recovered signal**.

> 💡 **For judges:** The recovered audio is generated from visual information rather than simply extracting the audio track already stored inside the video.

---

## 📁 Project Structure

```text
GhostMic/
│
├── app.py
│   └── Streamlit frontend and interactive dashboard
│
├── src/
│   ├── pipeline.py
│   │   └── Core audio-recovery and signal-processing pipeline
│   │
│   └── visual_extractor.py
│       └── Computer-vision-based micro-vibration extraction
│
├── data/
│   └── Input videos and test data
│
├── output/
│   └── Recovered audio results
│
└── README.md
    └── Project documentation
```

### Architecture

```text
                    ┌─────────────────────┐
                    │       app.py        │
                    │ Streamlit Frontend  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     pipeline.py     │
                    │    Core Engine      │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │  visual_extractor.py     │
                 │    Computer Vision       │
                 └────────────┬─────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Signal Processing   │
                    │ • Filtering         │
                    │ • Detrending        │
                    │ • Normalization     │
                    │ • Upsampling        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      output/        │
                    │   Recovered Audio   │
                    └─────────────────────┘
```

---

## 🔍 Why GhostMic?

Traditional deepfake detection often focuses on visual artifacts or inconsistencies within generated media.

GhostMic approaches the problem from a different angle:

> **Can the video itself reveal what the camera physically observed?**

If a video contains an audio track that has been replaced or manipulated, the visual micro-vibrations may provide an independent source of acoustic evidence.

This creates a potential **cross-modal forensic signal**:

```text
        Audio Track
             │
             │ Compare
             ▼
      ┌───────────────┐
      │   Authentic?  │
      └───────┬───────┘
              ▲
              │
      Visual Micro-Vibrations
              │
              ▼
       Recovered Audio
```

---

## 🧪 Testing the Project

For the best demonstration:

- Use a video with relatively stable camera framing.
- Prefer scenes containing objects that can physically respond to sound vibrations.
- Use sufficiently long video samples.
- Compare the recovered signal against the video's original audio when available.

The quality of recovery depends heavily on factors such as **video frame rate, resolution, lighting, camera characteristics, object motion, vibration strength, and environmental noise**.

---

## ⚠️ Limitations

GhostMic is a forensic research prototype rather than a guaranteed deepfake detector.

Performance can be affected by:

- Low-resolution video
- Low frame rates
- Camera movement
- Strong environmental noise
- Insufficient vibration in the scene
- Compression artifacts
- Lighting changes
- Very short video clips

The recovered signal may therefore differ significantly from the original audio depending on the recording conditions.

---

## 🏆 Hackathon Demo

**Recommended demonstration flow:**

```text
1. Launch GhostMic
       ↓
2. Upload MP4
       ↓
3. Extract visual micro-vibrations
       ↓
4. Enhance the signal
       ↓
5. Upsample to 44.1 kHz
       ↓
6. Play recovered audio
       ↓
7. Compare with original audio
```

### 🎯 Core Innovation

**GhostMic transforms a conventional camera into a potential optical microphone by exploiting microscopic visual vibrations that encode acoustic information.**

---

## 📌 Project Status

🚧 **Hackathon Prototype**

GhostMic demonstrates the feasibility of recovering acoustic information from visual micro-vibrations and using it as an additional signal for media forensics.

Future development could include:

- 🎵 Improved audio reconstruction
- 🤖 Machine-learning-based authenticity classification
- 🔊 Better source separation
- 📊 Automated similarity analysis between recovered and supplied audio
- 🎥 Support for additional video formats
- ⚡ GPU-accelerated processing

---

## 📄 License

This project is intended for **research, educational, and hackathon demonstration purposes**.
