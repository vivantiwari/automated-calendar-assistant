<<<<<<< HEAD
# automated-calendar-assistant
=======
# Automated Calendar Scheduling Assistant

An AI-powered Automated Calendar Scheduling Assistant built with **Python**, **Gradio**, an **LLM Agent** with Tool Calling, a self-contained **Calendar Service**, and configured for deployment on **Render**.

This project demonstrates how an LLM-based AI agent can understand natural language scheduling requests, translate relative date expressions into ISO timestamps, and interact with a calendar service to manage events and check availability.

---

## Architecture & Workflow

```
       User (Natural Language)
                 │
                 ▼
       Gradio Chat Interface
                 │
                 ▼
          LLM AI Agent
     (Tool & Function Calling)
                 │
                 ▼
          Calendar Service
 (create_event, get_events, find_free_slot)
                 │
                 ▼
         Calendar Action
                 │
                 ▼
   Natural Language User Response
```

---

## Tech Stack

* **Language**: Python 3.10+
* **Frontend**: Gradio (Minimalist Chat Interface)
* **API Framework**: FastAPI & Uvicorn
* **LLM Engine**: OpenAI API (`gpt-4o-mini`, `gpt-4o`, `gpt-5.6-luna`, or custom model) with Function Calling & Fallback Heuristics
* **Calendar Engine**: Self-contained Python Calendar Service (No external credentials required!)
* **Deployment**: Render (Web Service)

---

## Core Capabilities

1. **Create Event** (`create_event`): Schedules new meetings on specified dates and times.
2. **View Events** (`get_events`): Displays upcoming meetings and daily agendas.
3. **Check Availability** (`check_availability`): Verifies whether specific time slots are occupied.
4. **Find Free Slot** (`find_free_slot`): Automatically searches for open meeting windows during business hours (9 AM - 6 PM).
5. **Conflict Detection & Resolution**: Detects overlapping events and suggests alternative available time slots.

---

## Step-by-Step Setup and Deployment Guide (Render)

### 1. Create/Clone the Project
Navigate to the project directory:
```bash
cd automated-calendar-assistant
```

### 2. Install Dependencies Locally
Create a virtual environment and install required packages:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to create `.env`:
```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4o-mini
```

### 4. Test the Application Locally
Run the automated test suite:
```bash
python test_assistant.py
```

Run the Gradio web application locally:
```bash
python app.py
```
Open your web browser at: `http://127.0.0.1:7860`

---

## Deploying to Render & Getting Your Live Link

### Step 1: Push code to GitHub
1. Initialize git and commit files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Calendar Assistant"
   ```
2. Create a repository on [GitHub](https://github.com/new) named `automated-calendar-assistant`.
3. Push your repository:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/automated-calendar-assistant.git
   git push -u origin main
   ```

### Step 2: Create a Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com/) and log in (or sign up free).
2. Click **New +** ➔ **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your GitHub repo `automated-calendar-assistant`.
4. Configure the settings:
   * **Name**: `automated-calendar-assistant`
   * **Environment**: `Python 3`
   * **Region**: Choose any (e.g., Oregon / Frankfurt / Singapore)
   * **Branch**: `main`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   * **Instance Type**: `Free`

### Step 3: Add Environment Variables on Render
1. Scroll down to **Environment Variables** section.
2. Add:
   * Key: `OPENAI_API_KEY` | Value: `sk-proj-your_actual_key`
   * Key: `LLM_MODEL` | Value: `gpt-4o-mini`
3. Click **Create Web Service**.

### Step 4: Get Your Live Render Link
Render will automatically build and deploy your app. Once finished (1-2 minutes), you will see your live URL at the top left of the Render dashboard:
👉 **`https://automated-calendar-assistant.onrender.com`**

---

## File Structure

```
automated-calendar-assistant/
│
├── app.py                  # Gradio UI layout & FastAPI Uvicorn server
├── agent.py                # LLM agent, tool definitions, & rule fallback
├── calendar_service.py     # Self-contained Calendar Service
├── render.yaml             # Render Blueprint configuration
├── test_assistant.py       # Automated unit test suite
├── requirements.txt        # Dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## Example Requests

* *"Schedule a meeting tomorrow at 3 PM."*
* *"What meetings do I have today?"*
* *"Find a free slot tomorrow."*
* *"Schedule a 30-minute meeting at 5 PM."*
>>>>>>> 93e0058 (Initial commit of Calendar Assistant)
