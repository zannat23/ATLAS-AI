# ATLAS-AI
AI Triage Language and Aid System
# ATLAS AI 🌍
### Offline Multilingual Crisis Assistance and Medical Aid System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0-red)
![GPU](https://img.shields.io/badge/GPU-RTX%203050-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🔥 What is ATLAS?
ATLAS is an offline AI system that helps displaced people, refugees, 
and crisis victims by breaking three critical barriers:

- 🎤 **Voice Bridge** — Real-time two-way translation in 60+ languages
- 🏥 **Medical Triage** — Wound photo classification + first aid guidance  
- 🗺️ **Resource Locator** — Find nearest hospitals, camps, water points

> No internet needed. No literacy required. Works on any Android phone.

---

## 🧠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Speech Recognition | OpenAI Whisper Small |
| Translation | Facebook NLLB-200 Distilled |
| Text to Speech | gTTS (60+ languages) |
| Wound Classification | EfficientNet-Lite (TFLite) |
| Intent Detection | DistilBERT-tiny |
| Offline Maps | OSMdroid + SQLite |
| Deep Learning | PyTorch 2.6.0 + CUDA 12.4 |
| UI | Gradio |

---

## ✅ Current Status

- ✅ Voice pipeline working (Whisper + NLLB-200)
- ✅ 60+ language translation on GPU
- ✅ Text to speech in multiple languages
- ✅ GPU accelerated (RTX 3050 6GB)
- 🔄 Medical triage module (in progress)
- 🔄 Resource locator module (coming soon)
- 🔄 Gradio UI (coming soon)

---

## 🚀 Setup & Installation

### Requirements
- Python 3.11
- NVIDIA GPU (recommended)
- 8GB RAM minimum
- FFmpeg installed

### Step 1 — Clone the repository
```bash
ATLAS/
├── src/
│   ├── voice/
│   │   └── pipeline.py      ← Voice + Translation module
│   ├── medical/             ← Wound triage (coming soon)
│   └── resource/            ← Resource locator (coming soon)
├── tests/
│   └── audio_samples/       ← Test audio files
├── outputs/                 ← Generated audio responses
├── day2_demo.py             ← Full voice pipeline demo
├── test_all_languages.py    ← 60+ language test
├── requirements.txt
└── .gitignore
---

## 🌍 Supported Languages (60+)

Hindi, Arabic, Bengali, Urdu, French, German, Spanish, Russian,
Turkish, Swahili, Tamil, Telugu, Marathi, Gujarati, Punjabi,
Chinese, Japanese, Korean, Vietnamese, Thai, Indonesian, and 40+ more.

---

## 📊 Demo Results
---

## 🎯 Use Cases

- Refugee camps (language barrier between aid workers and refugees)
- Disaster relief (flood, earthquake survivors)
- Migrant workers (interstate communication)
- Medical emergencies (first aid without a doctor)

---

## 📄 References

1. Radford et al. — Whisper (OpenAI, 2022)
2. NLLB Team — No Language Left Behind (Meta AI, 2022)
3. Tan & Le — EfficientNet (ICML, 2019)
4. UNHCR Global Trends Report 2023

---

## 👩‍💻 Team

B.Tech Final Year Project — Department of AI & ML  
Academic Year 2025-26

---

## 📜 License
MIT License — feel free to use and contribute!