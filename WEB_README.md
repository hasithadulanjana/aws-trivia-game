# AWS Trivia Game - Web Version

A modern, responsive web-based multiplayer AWS trivia game built with Flask and Socket.IO. Play in your browser with real-time multiplayer support!

## 🌟 Features

- **Modern Web Interface**: Responsive design that works on desktop, tablet, and mobile
- **Real-time Multiplayer**: Up to 10 players can join simultaneously
- **Live Updates**: Real-time question delivery, scoring, and leaderboard updates
- **Beautiful UI**: Bootstrap-based interface with custom styling
- **Cross-platform**: Works on any device with a web browser
- **No Installation Required**: Players just need to visit the URL

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# Option 1: Use the run script
./run_web.sh

# Option 2: Direct command
source venv/bin/activate && python3 start_web_server.py

# Option 3: Using the main web server file
source venv/bin/activate && python3 web_server.py
```

### 3. Access the Game

- **Local access**: http://localhost:5000
- **Network access**: http://YOUR_IP_ADDRESS:5000

## 🎮 How to Play

1. **Join the Game**:
   - Open your web browser and navigate to the server URL
   - Enter a unique nickname
   - Click "Join Game"

2. **Game Lobby**:
   - Wait for other players to join
   - The first player becomes the host
   - Host can start the game when ready

3. **During the Game**:
   - Answer multiple-choice AWS questions
   - You have 15 seconds per question
   - Click on your answer choice
   - Watch the live leaderboard update

4. **Game End**:
   - See final scores and winner
   - Host can start a new game

## 📁 File Structure

```
aws-trivia-game/
├── web_server.py              # Main Flask application
├── start_web_server.py        # Server startup script
├── run_web.sh                 # Bash launcher script
├── test_web_setup.py          # Setup verification script
├── requirements.txt           # Python dependencies
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Landing page
│   └── game.html             # Game interface
├── static/                   # Static assets
│   ├── css/
│   │   └── style.css         # Custom styles
│   └── js/
│       └── game.js           # Client-side game logic
└── questions.py              # AWS trivia questions
```

## 🔧 Configuration

### Server Settings

Edit `web_server.py` to modify:

```python
MAX_PLAYERS = 10              # Maximum concurrent players
QUESTION_TIMEOUT = 15         # Seconds per question
WAIT_TIME_BETWEEN_QUESTIONS = 3  # Pause between questions
QUESTIONS_PER_GAME = 10       # Questions per game session
```

### Network Settings

- **Default Port**: 5000
- **Host**: 0.0.0.0 (listens on all interfaces)
- **CORS**: Enabled for all origins

## 🌐 Deployment Options

### Local Network

```bash
# Find your IP address
ifconfig | grep "inet " | grep -v 127.0.0.1

# Start server (already configured for 0.0.0.0)
./run_web.sh

# Share URL: http://YOUR_IP:5000
```

### Production Deployment

#### Using Gunicorn

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 web_server:app
```

#### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python3", "start_web_server.py"]
```

## 🧪 Testing

### Verify Setup

```bash
python3 test_web_setup.py
```

### Manual Testing

1. Start the server
2. Open multiple browser tabs/windows
3. Join with different nicknames
4. Test game functionality

### Load Testing

```bash
# Install testing tools
pip install locust

# Create locustfile.py for load testing
# Run load tests
locust -f locustfile.py --host=http://localhost:5000
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Kill existing processes
   pkill -f "python.*web_server.py"
   # Or use different port in web_server.py
   ```

2. **Module Not Found**:
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Socket.IO Connection Issues**:
   - Check firewall settings
   - Verify CORS configuration
   - Test with different browsers

4. **Mobile/Tablet Issues**:
   - Ensure responsive design is working
   - Test touch interactions
   - Check viewport settings

### Debug Mode

Enable debug mode in `web_server.py`:

```python
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

## 📱 Mobile Support

The web interface is fully responsive and supports:

- **Touch Controls**: Tap to select answers
- **Mobile Layout**: Optimized for small screens
- **Portrait/Landscape**: Works in both orientations
- **iOS/Android**: Compatible with all modern mobile browsers

## 🎨 Customization

### Styling

Edit `static/css/style.css` to customize:
- Colors and themes
- Layout and spacing
- Animations and effects
- Responsive breakpoints

### Game Logic

Modify `web_server.py` to change:
- Scoring system
- Question selection
- Game flow
- Player limits

### UI Components

Update templates in `templates/` to modify:
- Page layouts
- Component structure
- Content and text
- Interactive elements

## 🔒 Security Considerations

- **Input Validation**: All user inputs are validated
- **XSS Protection**: Templates use proper escaping
- **CORS**: Configure appropriately for production
- **Rate Limiting**: Consider adding for production use

## 📊 Performance

- **Concurrent Players**: Tested with up to 10 players
- **Response Time**: Sub-second question delivery
- **Memory Usage**: Minimal server-side state
- **Scalability**: Can be scaled with load balancers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

---

**Enjoy playing AWS Trivia Game! 🎉**
