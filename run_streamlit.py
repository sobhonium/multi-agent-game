#!/usr/bin/env python3
"""
Helper script to run the Streamlit app for the Werewolf game.
"""

import subprocess
import sys
import os

def main():
    print("🐺 Werewolf Game - Streamlit Interface")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your GROQ_API_KEY:")
        print("GROQ_API_KEY=your_api_key_here")
        print()
    
    print("🚀 Starting Streamlit app...")
    print("📱 The app will open in your browser automatically")
    print("🔗 If it doesn't open, go to: http://localhost:8501")
    print()
    print("💡 Tips:")
    print("   - Click 'Start New Game' to begin")
    print("   - Use 'Next Turn' to step through the game")
    print("   - Use 'Run Full Game' to watch the complete game")
    print("   - Press Ctrl+C to stop the app")
    print()
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped.")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        print("Make sure you have installed all dependencies:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main() 