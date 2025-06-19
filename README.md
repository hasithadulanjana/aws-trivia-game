# AWS Trivia Game

A multiplayer trivia game focused on AWS (Amazon Web Services) knowledge, built with Python. Players can connect to a central server and compete in real-time trivia sessions.

## Features

- **Multiplayer Support**: Up to 10 players can join simultaneously
- **Real-time Gameplay**: Live question delivery and scoring
- **Multiple Client Options**: Terminal-based and GUI clients
- **AWS-focused Questions**: Comprehensive AWS trivia database
- **Live Leaderboard**: Real-time score tracking
- **Admin Controls**: Host can start games and manage sessions
- **Reliable Networking**: Robust connection handling for stable multiplayer experience

## Game Components

### Server (`server.py` / `server_fixed.py`)
- Handles multiple client connections
- Manages game flow and timing
- Broadcasts questions and updates
- Tracks scores and leaderboard

### Clients
- **Terminal Client** (`client.py` / `client_fixed.py`): Curses-based interface
- **GUI Client** (`gui_client.py`): Tkinter-based graphical interface

### Support Files
- `questions.py`: AWS trivia question database
- `network_utils.py`: Reliable message transmission utilities
- `test_multiplayer.py`: Automated testing for multiple connections

## Requirements

- Python 3.7+
- Standard library modules (no external dependencies)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aws-trivia-game
```

2. (Optional) Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Starting the Server

```bash
# Use the improved server version
python3 server_fixed.py
```

The server will start on `localhost:5000` by default.

### Connecting Clients

#### Terminal Client
```bash
python3 client_fixed.py --nickname YourName --host localhost --port 5000
```

#### GUI Client
```bash
python3 gui_client.py --nickname YourName --host localhost --port 5000
```

### Game Controls

#### Terminal Client
- **Arrow Keys**: Navigate answer options
- **Enter**: Submit answer
- **S**: Start game (host only)
- **Q**: Quit

#### GUI Client
- **Click**: Select answers and interact with buttons
- **Start Game**: Available to the first player (host)

## Game Flow

1. **Connection**: Players connect with unique nicknames
2. **Lobby**: First player becomes the host and can start the game
3. **Questions**: Timed multiple-choice questions (15 seconds each)
4. **Scoring**: Correct answers earn points
5. **Leaderboard**: Live updates after each question
6. **Game End**: Final scores and winner announcement

## Network Architecture

The game uses a client-server architecture with:
- **TCP Sockets**: Reliable connection-oriented communication
- **JSON Messages**: Structured data exchange
- **Message Framing**: Length-prefixed messages for reliability
- **Threading**: Concurrent handling of multiple clients

## Configuration

### Server Settings (in `server.py`/`server_fixed.py`)
```python
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000       # Server port
MAX_PLAYERS = 10  # Maximum concurrent players
QUESTION_TIMEOUT = 15  # Seconds per question
```

### Client Settings
```python
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5000
```

## Testing

### Manual Testing
Start the server and connect multiple clients from different terminals.

### Automated Testing
```bash
python3 test_multiplayer.py
```

This script simulates multiple players connecting and playing automatically.

## Troubleshooting

### Connection Issues
- Ensure the server is running before connecting clients
- Check firewall settings if connecting from different machines
- Verify port availability (default: 5000)

### Multiplayer Disconnections
- Use `server_fixed.py` and `client_fixed.py` for improved reliability
- Check network stability
- Monitor server logs for error messages

### Performance
- Limit concurrent players based on server capacity
- Monitor memory usage with many connections
- Consider network latency for remote players

## File Structure

```
aws-trivia-game/
├── server.py              # Original server
├── server_fixed.py        # Improved server with better reliability
├── client.py              # Original terminal client
├── client_fixed.py        # Improved terminal client
├── gui_client.py          # GUI client
├── questions.py           # Trivia questions database
├── network_utils.py       # Network utility functions
├── test_multiplayer.py    # Automated testing script
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── venv/                 # Virtual environment (optional)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Enhancements

- [ ] Web-based client interface
- [ ] Question categories and difficulty levels
- [ ] Player statistics and history
- [ ] Tournament mode
- [ ] Custom question sets
- [ ] Audio/visual enhancements
- [ ] Database integration
- [ ] User authentication

## License

This project is open source. Feel free to use, modify, and distribute.

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
