# AIVI PRO - AI-Powered Interview Platform

AIVI PRO is a comprehensive, industry-standard interview preparation platform that uses advanced AI models to conduct, monitor, and evaluate technical interviews. It features real-time video monitoring, movement detection, and voice-driven interactions.

## 🚀 Key Features

- **User Authentication**: Secure Login and Registration system with password hashing.
- **Smart Resume Parsing**: Automatically extracts skills from PDF resumes to tailor the interview.
- **AI-Driven Interviewer**:
    - **Text Mode**: Traditional text-based interview.
    - **Live Mode**: Real-time video interview with webcam monitoring.
- **Multi-Modal AI Interaction**:
    - **Speech-to-Text (STT)**: Listen to candidate answers using Google Speech API.
    - **Text-to-Speech (TTS)**: AI speaks questions using high-fidelity `edge-tts`.
- **Intelligent Evaluation**: Strict technical scoring and qualitative feedback using Gemini/Groq.
- **Visual Proctoring**: Real-time movement detection using OpenCV to monitor candidate attention.
- **Performance Analytics**: Mission Control dashboard to track scores and history.

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | Flask (Python) |
| **Architecture** | Factory Pattern & Blueprints |
| **Database** | SQLite (via SQLAlchemy) |
| **Primary AI Model** | Google Gemini 1.5 Flash |
| **Fallback AI Model** | Groq Llama 3.3 (70B) |
| **Computer Vision** | OpenCV |
| **Speech Synthesis** | Edge-TTS (Microsoft) |
| **Speech Recognition** | SpeechRecognition (Google API) |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Jinja2 |

## 📂 Project Structure

```text
AIVI/
├── app.py              # Application Entry Point
├── app_factory.py      # Flask Factory Pattern Setup
├── models.py           # Database Schema (User, Interview, etc.)
├── routes/             # Modular Route Blueprints (Auth, Main)
├── services/           # Business Logic (AI, Voice, Video, Resume)
├── static/             # Assets (CSS, AI-generated Images, Audio)
├── templates/          # Jinja2 HTML Templates
├── requirement.txt     # Python Dependencies
└── .env                # API Keys and Environment Config
```

## 🔄 Workflow

1. **Authentication**: User logs in or registers for an account.
2. **Dashboard**: User enters "Mission Control" and selects "New Interview".
3. **Resume Upload**: User uploads a PDF. The `resume_service` extracts keywords.
4. **Question Generation**: The `ai_service` generates 5-7 technical questions based on the resume.
5. **Interview Session**:
    - AI uses `voice_service` to speak the question.
    - Candidate speaks their answer; `voice_service` converts it to text.
    - `video_service` monitors the webcam for movement/attention.
6. **AI Evaluation**: The `evaluation_service` sends all Q&A to the LLM for a strict score (0-100) and feedback.
7. **Report**: Results are stored in the SQLite database and displayed to the user.

## 🏁 How to Run

1. **Clone/Open the Project** in your workspace.
2. **Setup environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   GEMINI_API_KEY="your_key_here"
   GROQ_API_KEY="your_key_here"
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirement.txt
   ```
4. **Launch Application**:
   ```bash
   python app.py
   ```
5. **Access**: Open `http://127.0.0.1:5000` in your browser.

## 📤 Pushing to GitHub

If you have already initialized the local repository, you can push it to your GitHub using:
```bash
git remote add origin https://github.com/abdullah1208/virtual-intervie-with-AI.git
git branch -M main
git push -u origin main
```

---
Developed as a Major Project for University Submission.
