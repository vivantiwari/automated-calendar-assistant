import sys
import os

# Add root directory to sys.path so Vercel can locate app, agent, calendar_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel serverless entrypoint
app = app
