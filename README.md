# 🐺 Werewolf Game with LangGraph

A sophisticated multi-agent werewolf game implementation using LangGraph and LangChain. Watch AI agents play different roles (wolves, villagers, doctor, hunter, etc.) in a real-time interactive environment with live streaming updates.

## ✨ Features

- **🤖 AI-Powered Players**: Intelligent agents with different roles (wolves, villagers, doctor, hunter, etc.)
- **🎮 Real-Time Streaming**: Watch players think, speak, and make decisions live
- **🗳️ Interactive Voting**: Dynamic voting system with real-time results
- **📊 Live Metrics**: Real-time game state monitoring and statistics
- **🎭 Role-Based Strategy**: Each player type has unique abilities and strategies
- **🔄 Turn-Based Gameplay**: Automatic game state management with configurable flow
- **📱 Web Interface**: Beautiful Streamlit interface with chat-like experience
- **🔍 Debug Logging**: Complete visibility into player thoughts and game logic

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weaverwolf-game.git
   cd weaverwolf-game
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Run the game:**

   **🎮 Streamlit Web Interface (Recommended):**
   ```bash
   streamlit run streamlit_app.py
   ```
   
   **💻 Command Line Interface:**
   ```bash
   python main.py
   ```

The Streamlit app provides a real-time interactive interface where you can:
- **Watch players talk live** - See each player thinking, speaking, and making decisions in real-time
- **Live chat interface** - Messages appear as players speak, with color-coded chat bubbles
- **Real-time action indicators** - See what each player is doing (thinking, speaking, voting)
- **Step-by-step control** - Advance the game one turn at a time or let it run automatically
- **Live game metrics** - Watch player counts, voting status, and game state update in real-time
- **Visual feedback** - Typing indicators, thinking animations, and live status updates
- **Print statement capture** - All console print statements are captured and displayed in the Streamlit interface

## 🎯 How to Play

### Game Rules
- **🐺 Wolves**: Know each other and work together to eliminate villagers
- **👥 Villagers**: Must identify and eliminate wolves through voting
- **👨‍⚕️ Doctor**: Can save one player per round from elimination
- **🏹 Hunter**: Can eliminate a suspected wolf each round
- **🛡️ Armor**: Survives one elimination attempt
- **🔍 Detective**: Has enhanced deduction abilities

### Winning Conditions
- **Wolves Win**: When wolves equal or outnumber villagers
- **Villagers Win**: When all wolves are eliminated

### Game Flow
1. Players take turns speaking and making accusations
2. Each player votes on who they think is a wolf
3. If majority votes for a player, they are eliminated
4. Game continues until one team wins

## 📁 Project Structure

```
weaverwolf-game/
├── 🎮 streamlit_app.py     # Main Streamlit web interface
├── 💻 main.py              # Command-line interface
├── 🚀 run_streamlit.py     # Helper script for Streamlit
├── 📦 game/                # Core game package
│   ├── __init__.py         # Package initialization
│   ├── state.py            # Game state and data structures
│   ├── players.py          # Player logic and AI behavior
│   ├── game_logic.py       # Core game mechanics
│   ├── graph.py            # LangGraph configuration
│   └── streamlit_game.py   # Streamlit-compatible game runner
├── 📋 requirements.txt     # Python dependencies
├── 🔧 env.example          # Environment variables template
├── 🚫 .gitignore          # Git ignore rules
└── 📖 README.md           # This file
```

## 🎮 Usage

### Streamlit Interface (Recommended)
1. Run `streamlit run streamlit_app.py`
2. Click "Start New Game" in the sidebar
3. Use "Next Turn" to advance step-by-step or "Run Full Game" for automatic play
4. Watch the live chat and debug log for real-time updates

### Command Line Interface
1. Run `python main.py`
2. The game will run automatically and display results in the terminal

## ⚙️ Configuration

You can customize the game by modifying:
- **Player Roles**: Edit `game/state.py` to change player assignments
- **Game Rules**: Modify `game/game_logic.py` for different voting mechanics
- **AI Behavior**: Adjust prompts in `game/players.py` for different player strategies
- **Game Parameters**: Change player count and settings in `main.py`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://github.com/langchain-ai/langchain)
- Powered by [Groq](https://groq.com/) for fast AI inference
- UI built with [Streamlit](https://streamlit.io/) 