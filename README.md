# Faye Protocol v2.0

Faye Protocol is a terminal-based, voice-activated personal companion application. Built using python, it bridges lightweight local speech processing with cloud-hosted LLM execution via the Groq API. 

The application captures real-time verbal inputs, processes them into textual prompts, evaluates them through an emotionally tailored contextual system prompt, and synthesizes the final response back into fluent spoken audio.

---

## Tech Stack & Ecosystem

The architecture is built entirely on open-source Python modules, chosen for minimal execution overhead and low response latency:

*   **Runtime Environment:** Python 3.10+
*   **LLM Inference Core:** `groq` (Utilizing the hosted `llama-3.1-8b-instant` model architecture)
*   **Speech-to-Text (STT):** `SpeechRecognition` (Interfaced with the Google Web Speech API wrapper)
*   **Text-to-Speech (TTS):** `gTTS` (Google Text-to-Speech translation layer)
*   **Audio Playback Utilities:** `playsound3` (Cross-platform audio thread execution)
*   **Environment Configuration:** `python-dotenv` (Secure local credential separation)

---

## Key Features & Functionality

### 1. Hands-Free Conversational Loop
*   Automatic ambient noise filtering using mathematical energy threshold calibration (`adjust_for_ambient_noise`).
*   Configurable microphone timeout bounds to prevent deadlocked listening routines.

### 2. High-Speed Cloud Inference
*   Leverages Groq’s LPU (Language Processing Unit) architecture via the `llama-3.1-8b-instant` model to achieve exceptionally low Time-To-First-Token (TTFT).

### 3. Dual-Language Comprehension (Code-Switching)
*   The underlying system prompt enables full comprehension of mixed-language inputs (Hinglish/Hindi phrases) while enforcing strict, grammatically fluent, and emotionally intelligent English outputs.

### 4. Automated File Lifecycle Management
*   Saves audio responses dynamically to ephemeral `.mp3` buffers and forcefully flushes them from local storage immediately following thread playback to optimize disk space.

---

## 🧠 Architectural Design: How Faye Works

The system utilizes a structured pipelines approach across four primary operational phases:
[User Speech] ──> (SpeechRecognition STT) ──> [Text Prompt]
│
▼
[Spoken Audio] <── (gTTS Engine + Playback) <── [Groq LLM Engine]

1.  **Ingestion:** The local microphone captures audio streams. The `SpeechRecognition` module samples the frame data, normalizes background gain, and serializes it to the Google Web Speech API to get a string payload.
2.  **Contextual Processing:** The text string is packaged into a structured payload containing a comprehensive `system_prompt`. This prompt anchors Faye's personality—enforcing guidelines like long-term vision, emotional steadiness, accountability, and specific conversational bounds.
3.  **Inference:** The payload is securely delivered over HTTPS to Groq's API endpoint, returning an optimized response token stream.
4.  **Synthesis:** The text response is streamed into the `gTTS` engine, compiled into a temporary file (`faye_free_response.mp3`), loaded into system memory for playback via `playsound3`, and then safely unlinked from the host operating system.

---

## ⚙️ Installation & Workspace Setup

### 1. Clone the Repository
bash
git clone [https://github.com/Shaiq-Ahmed09/Faye-AI.git](https://github.com/Shaiq-Ahmed09/Faye-AI.git)
cd Faye-AI

**Configure the Virtual Environment**
Create and activate an isolated Python virtual environment to manage dependencies locally:
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Mac / Linux
python3 -m venv venv
source venv/bin/activate

---

**Install System Dependencies**
Install the required upstream packages listed in your project profile:
```
pip install speechrecognition groq gTTS playsound3 python-dotenv
```

**Secure Environment Settings**
The application relies on strict environment isolation to protect sensitive credentials.

1. Create a .env file in the root directory:
touch .env

2. Insert your valid Groq API key directly into the variable space (do not include quotation marks or spaces around the assignment operator):
GROQ_API_KEY=gsk_your_actual_private_key_here

**Execution**
To execute the protocol runtime loop, run the primary entry script:
python faye_voice_assistant.py

To interact: Wait for the 🎙️ Speak to Faye... terminal indicator before speaking.

To terminate safely: Explicitly speak the words "shutdown", "goodbye", or "exit" during your turn to safely close audio streams and tear down the loop interface.
