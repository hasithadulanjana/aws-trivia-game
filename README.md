# AWS Trivia Game

A comprehensive multiplayer trivia game focused on AWS (Amazon Web Services) knowledge, built with Python. Features both **terminal/GUI clients** and a **modern web interface** with real-time multiplayer support.

## 🌟 **Multiple Ways to Play**

### 🌐 **Web Version (Recommended)**
- **Multiplayer**: Real-time web-based gameplay for up to 10 players
- **Static Version**: Single-player version for Netlify deployment
- **Modern UI**: Bootstrap-based responsive design
- **Cross-platform**: Works on any device with a web browser

### 💻 **Desktop Version**
- **Terminal Client**: Curses-based interface
- **GUI Client**: Tkinter-based graphical interface
- **Local Multiplayer**: Connect multiple clients to a server

## 🚀 **Quick Start Options**

### **Option 1: Web Version (Easiest)**

```bash
# Clone and start web server
git clone https://github.com/hasithadulanjana/aws-trivia-game.git
cd aws-trivia-game
source venv/bin/activate
pip install -r requirements.txt
python3 web_server.py

# Access at: http://localhost:8080
```

### **Option 2: Static Version (Netlify)**

Deploy the `netlify-static/` folder to any static hosting:
- **Netlify**: Drag & drop deployment
- **GitHub Pages**: Static hosting
- **Vercel**: Instant deployment

### **Option 3: Desktop Clients**

```bash
# Terminal version
python3 server_fixed.py  # Start server
python3 client_fixed.py --nickname YourName  # Connect client

# GUI version  
python3 gui_client.py --nickname YourName
```

## 🎮 **Game Features**

### **Core Gameplay**
- **AWS-focused Questions**: 100+ comprehensive AWS trivia questions
- **Timed Challenges**: 15 seconds per question
- **Live Scoring**: Real-time score tracking and leaderboard
- **Multiple Difficulty Levels**: From basics to advanced AWS concepts

### **Multiplayer Features**
- **Real-time Gameplay**: Simultaneous question delivery
- **Live Leaderboard**: Updated after each question
- **Host Controls**: First player manages game flow
- **Reliable Networking**: Robust connection handling

### **User Interface Options**
- **Web Interface**: Modern, responsive Bootstrap design
- **Terminal Interface**: Curses-based for command-line users
- **GUI Interface**: Tkinter-based desktop application
- **Mobile Support**: Web version works on phones/tablets

## 📁 **Project Structure**

```
aws-trivia-game/
├── 🌐 Web Interface
│   ├── web_server.py              # Flask + Socket.IO server
│   ├── templates/                 # HTML templates
│   ├── static/                    # CSS, JavaScript assets
│   └── netlify-static/            # Static version for Netlify
├── 💻 Desktop Clients
│   ├── server_fixed.py            # Improved multiplayer server
│   ├── client_fixed.py            # Enhanced terminal client
│   ├── gui_client.py              # Tkinter GUI client
│   └── network_utils.py           # Networking utilities
├── 📚 Game Content
│   ├── questions.py               # AWS trivia database
│   └── test_multiplayer.py        # Automated testing
├── 🚀 Deployment
│   ├── DEPLOYMENT.md              # Server deployment guide
│   ├── NETLIFY_DEPLOYMENT.md      # Static deployment guide
│   ├── Procfile                   # Heroku configuration
│   └── requirements.txt           # Python dependencies
└── 📖 Documentation
    ├── README.md                  # This file
    └── WEB_INTERFACE_UPDATES.md   # Web version details
```

## 🌐 **Deployment Options**

### **Static Hosting (Netlify, Vercel, GitHub Pages)**
- ✅ **Single-player version** in `netlify-static/`
- ✅ **No server required**
- ✅ **Instant deployment**
- ✅ **Free hosting available**

### **Server Hosting (Heroku, Railway, Render)**
- ✅ **Full multiplayer support**
- ✅ **Real-time Socket.IO connections**
- ✅ **Up to 10 concurrent players**
- ✅ **Production-ready configuration**

### **Local Development**
- ✅ **Virtual environment support**
- ✅ **Debug and test modes**
- ✅ **Cross-platform compatibility**

## 🔧 **Installation & Setup**

### **Prerequisites**
- Python 3.7+
- Modern web browser (for web version)
- Terminal access (for desktop clients)

### **Web Version Setup**
```bash
# Clone repository
git clone https://github.com/hasithadulanjana/aws-trivia-game.git
cd aws-trivia-game

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start web server
python3 web_server.py

# Access game at http://localhost:8080
```

### **Desktop Version Setup**
```bash
# Start server
python3 server_fixed.py

# Connect clients (in separate terminals)
python3 client_fixed.py --nickname Player1
python3 gui_client.py --nickname Player2
```

## 🎯 **Game Configuration**

### **Server Settings**
```python
# In web_server.py or server_fixed.py
MAX_PLAYERS = 10              # Maximum concurrent players
QUESTION_TIMEOUT = 15         # Seconds per question
QUESTIONS_PER_GAME = 10       # Questions per session
```

### **Network Settings**
```python
HOST = '0.0.0.0'              # Listen on all interfaces
PORT = 8080                   # Server port (web version)
PORT = 5000                   # Server port (desktop version)
```

## 🧪 **Testing**

### **Automated Testing**
```bash
# Test multiplayer connections
python3 test_multiplayer.py

# Test web interface setup
python3 test_web_interface.py

# Validate static version
cd netlify-static && open index.html
```

### **Manual Testing**
- Start server and connect multiple clients
- Test on different devices and browsers
- Verify real-time synchronization

## 📊 **Performance & Scalability**

- **Concurrent Players**: Tested with up to 10 players
- **Response Time**: Sub-second question delivery
- **Memory Usage**: Minimal server-side state
- **Network Efficiency**: Optimized message protocols

## 🔒 **Security Features**

- **Input Validation**: All user inputs sanitized
- **XSS Protection**: Template-based rendering
- **CORS Configuration**: Secure cross-origin requests
- **Rate Limiting**: Built-in connection throttling

## 🌟 **Key Advantages**

### **Flexibility**
- Multiple client options (web, terminal, GUI)
- Various deployment methods
- Configurable game settings

### **Accessibility**
- No installation required (web version)
- Cross-platform compatibility
- Mobile-friendly responsive design

### **Educational Value**
- Comprehensive AWS question database
- Immediate feedback and explanations
- Progress tracking and scoring

## 🤝 **Contributing**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Add your improvements**:
   - New AWS questions in `questions.py`
   - UI enhancements
   - Performance optimizations
   - Bug fixes
4. **Test thoroughly**
5. **Submit a pull request**

### **Areas for Contribution**
- 📚 **More AWS Questions**: Expand the question database
- 🎨 **UI Improvements**: Enhance visual design
- 🔧 **New Features**: Tournament mode, statistics, etc.
- 🌐 **Internationalization**: Multi-language support
- 📱 **Mobile App**: Native mobile applications

## 📄 **License**

This project is open source under the MIT License. Feel free to use, modify, and distribute.

## 🆘 **Support & Documentation**

- **📖 Deployment Guides**: See `DEPLOYMENT.md` and `NETLIFY_DEPLOYMENT.md`
- **🐛 Bug Reports**: Open GitHub issues
- **💡 Feature Requests**: Submit enhancement proposals
- **❓ Questions**: Check existing issues or create new ones

## 🎯 **Roadmap**

### **Planned Features**
- [ ] **Tournament Mode**: Bracket-style competitions
- [ ] **User Accounts**: Save progress and statistics
- [ ] **Question Categories**: Filter by AWS service
- [ ] **Difficulty Levels**: Beginner to expert questions
- [ ] **Custom Question Sets**: User-generated content
- [ ] **Audio/Visual Enhancements**: Sound effects and animations
- [ ] **Mobile Apps**: Native iOS and Android applications
- [ ] **API Integration**: Real-time AWS service information

### **Technical Improvements**
- [ ] **Database Integration**: Persistent data storage
- [ ] **Caching Layer**: Improved performance
- [ ] **Load Balancing**: Support for more concurrent users
- [ ] **Analytics Dashboard**: Game statistics and insights

---

## 🎉 **Get Started Now!**

Choose your preferred way to play:

1. **🌐 Try the Web Version**: Clone and run `python3 web_server.py`
2. **📱 Deploy to Netlify**: Use the `netlify-static/` folder
3. **💻 Run Desktop Version**: Start with `python3 server_fixed.py`

**Test your AWS knowledge and challenge your friends!** 🚀

---

*Built with ❤️ for the AWS community. Happy learning!*
