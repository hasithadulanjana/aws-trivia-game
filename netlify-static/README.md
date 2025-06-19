# AWS Trivia Game - Static Version for Netlify

## 🌐 **Netlify-Compatible Version**

This is a **static, single-player version** of the AWS Trivia Game that works perfectly on Netlify and other static hosting platforms.

## ✨ **Features**

- 🎮 **Single Player Mode**: Challenge yourself with AWS questions
- ⏱️ **Timed Questions**: 15 seconds per question
- 🏆 **Score Tracking**: Track your performance
- 📱 **Responsive Design**: Works on all devices
- 🎯 **20 AWS Questions**: Curated AWS knowledge test
- 🔄 **Randomized**: Questions shuffled each game

## 🚀 **Deploy to Netlify**

### **Method 1: Drag & Drop**
1. Zip the `netlify-static` folder
2. Go to [netlify.com](https://netlify.com)
3. Drag and drop the zip file
4. Your game is live! 🎉

### **Method 2: GitHub Integration**
1. Push this folder to a GitHub repository
2. Connect Netlify to your GitHub repo
3. Set build folder to `netlify-static`
4. Deploy automatically! ✨

## 📁 **Files Structure**

```
netlify-static/
├── index.html          # Main game interface
├── game.js            # Game logic and functionality
├── questions.js       # AWS trivia questions database
└── README.md          # This file
```

## 🎮 **How to Play**

1. **Enter your name** on the welcome screen
2. **Click "Start Game"** to begin
3. **Answer questions** within 15 seconds each
4. **Track your score** in the sidebar
5. **See final results** and play again!

## 🔧 **Customization**

### **Add More Questions**
Edit `questions.js` to add more AWS questions:

```javascript
{
    "question": "Your AWS question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0  // Index of correct answer (0-3)
}
```

### **Change Game Settings**
Edit `game.js` to modify:
- Timer duration (default: 15 seconds)
- Number of questions per game (default: 10)
- Scoring system

### **Styling**
The game uses Bootstrap 5 and custom CSS. Modify the `<style>` section in `index.html` to customize appearance.

## 🌟 **Differences from Full Version**

| Feature | Static Version | Full Version |
|---------|---------------|--------------|
| **Players** | Single player | Up to 10 multiplayer |
| **Real-time** | No | Yes (Socket.IO) |
| **Hosting** | Static (Netlify) | Server required |
| **Questions** | 20 questions | 100+ questions |
| **Leaderboard** | Personal score | Live multiplayer |

## 🔗 **Links**

- **Full Multiplayer Version**: [GitHub Repository](https://github.com/hasithadulanjana/aws-trivia-game)
- **Server Version**: Requires Flask hosting (Heroku, Railway, etc.)

## 📱 **Browser Compatibility**

- ✅ Chrome, Firefox, Safari, Edge
- ✅ Mobile browsers (iOS, Android)
- ✅ Tablet browsers
- ✅ Desktop and mobile responsive

## 🎯 **Perfect For**

- 📚 **Learning AWS**: Test your knowledge
- 🎓 **Exam Prep**: Practice for AWS certifications
- 🏢 **Team Training**: Share with colleagues
- 🌐 **Easy Sharing**: Just send the URL!

---

**🎮 Enjoy testing your AWS knowledge!**

*For the full multiplayer experience with real-time gameplay, check out the server version in the main repository.*
