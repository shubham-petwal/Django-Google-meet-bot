# Google Meet Bot

Google Meet Bot is a Django-based application designed to automate Google Meet interactions and enhance productivity with AI-powered features. The bot can automatically join meetings, send messages, record audio, transcribe the meeting, and generate insights like summaries and highlights.

---

## Features

- **Automated Meeting Participation**:
  - Joins Google Meet sessions automatically.
  - Sends a welcome message to participants.

- **Audio Recording**:
  - Records the entire meeting using the system microphone.
  - Saves audio files in `.wav` format.

- **Speech-to-Text**:
  - Transcribes recorded audio using Google Speech Recognition API.
  - Provides a full text log of the meeting.

- **AI-Powered Insights**:
  - Generates concise meeting summaries.
  - Extracts highlights or key discussion points.
  - Performs detailed text analysis.

- **Task Scheduling**:
  - Uses Celery and Redis to schedule meeting participation and processing tasks.

---

## Tech Stack

- **Python**: Core programming language.
- **Django**: Web framework for building the application.
- **Selenium WebDriver**: Automates Google Meet actions.
- **ChromeDriver**: WebDriver for Google Chrome browser.
- **PyAudio**: Records audio from the microphone.
- **Wave**: Saves audio recordings as `.wav` files.
- **SpeechRecognition**: Converts recorded audio into text.
- **Google Speech API**: Provides accurate speech-to-text transcription.
- **Celery**: Task queue for scheduling and handling asynchronous tasks.
- **Redis**: Message broker for Celery tasks.
- **Webdriver Manager**: Handles ChromeDriver setup.

---

## Use Cases

1. **Meeting Transcription**: Provides a full-text transcription of the meeting.
2. **Meeting Summary**: Generates a concise summary of discussions.
3. **Highlight Extraction**: Identifies and lists key points from the transcript.
4. **Documentation**: Useful for record-keeping and sharing meeting logs.
5. **Speech-to-Text Analysis**: Enables NLP and AI-driven insights on meeting transcripts.

---

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.8+**
2. **Google Chrome Browser**
3. **ChromeDriver** (managed automatically by Webdriver Manager)
4. **Redis** (for Celery task management)
5. Required Python libraries (install using `requirements.txt`).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/google-meet-bot.git
   cd google-meet-bot
   ```

2. **Create a Virtual Environment**:

bash
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

4. **Set Up Redis: Install and start the Redis server. Follow the instructions on Redis installation**.

Configure Environment Variables: Create a .env file in the project root and configure the following:

makefile
GOOGLE_MEET_URL=<your_google_meet_url>
Run Redis Server:

```bash

redis-server
```

5. **Start Celery Worker**:

```bash
celery -A your_project_name worker --loglevel=info
```

6. **Run the Django Server**:

```bash
python manage.py runserver
```
