# 🌐 Netlify Deployment Guide

## ✅ **Static Version for Netlify**

Since Netlify only supports static websites, I've created a **single-player static version** that works perfectly on Netlify!

## 📁 **What's Different**

| Original Flask App | Static Netlify Version |
|-------------------|------------------------|
| ❌ Requires Python server | ✅ Pure HTML/CSS/JS |
| ❌ Multiplayer (needs Socket.IO) | ✅ Single player |
| ❌ Server-side processing | ✅ Client-side only |
| ❌ Won't work on Netlify | ✅ Perfect for Netlify |

## 🚀 **Deploy to Netlify - 3 Easy Methods**

### **Method 1: Drag & Drop (Fastest)**

1. **Download only the static files**:
   - Go to: https://github.com/hasithadulanjana/aws-trivia-game/tree/main/netlify-static
   - Download the `netlify-static` folder contents
   - Create a zip file with just these files:
     - `index.html`
     - `game.js`
     - `questions.js`
     - `_redirects`

2. **Deploy to Netlify**:
   - Go to [netlify.com](https://netlify.com)
   - Sign up/login
   - Drag and drop the zip file (or folder)
   - Your game is live! 🎉

### **Method 2: GitHub Integration (Recommended)**

1. **Connect Netlify to GitHub**:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository
   
2. **Configure Build Settings**:
   - **Repository**: `hasithadulanjana/aws-trivia-game`
   - **Branch**: `main`
   - **Base directory**: `netlify-static`
   - **Build command**: (leave empty)
   - **Publish directory**: `netlify-static`
   
3. **Deploy**:
   - Click "Deploy site"
   - Netlify will automatically use the `netlify.toml` configuration

### **Method 3: Manual Configuration**

If the automatic detection doesn't work:

1. **Site Settings** → **Build & Deploy**
2. **Build Settings**:
   - **Base directory**: `netlify-static`
   - **Build command**: (leave empty)
   - **Publish directory**: `netlify-static`
3. **Environment Variables**: None needed
4. **Deploy**

## 🎮 **What You Get**

✅ **Working AWS Trivia Game** on Netlify
✅ **Responsive design** (mobile-friendly)
✅ **20 AWS questions** with timer
✅ **Score tracking** and feedback
✅ **Professional UI** with Bootstrap
✅ **Fast loading** (static files)

## 🔧 **Customization Options**

### **Add More Questions**
Edit `netlify-static/questions.js`:
```javascript
const questions = [
    {
        "question": "Your new AWS question?",
        "options": ["A", "B", "C", "D"],
        "answer": 0
    }
    // Add more questions...
];
```

### **Change Game Settings**
Edit `netlify-static/game.js`:
```javascript
// Change timer (line ~85)
this.timeLeft = 20; // 20 seconds instead of 15

// Change number of questions (line ~35)
this.gameQuestions = this.shuffleArray([...questions]).slice(0, 15); // 15 instead of 10
```

## 🌟 **Live Demo**

Once deployed, your game will be available at:
- `https://your-site-name.netlify.app`
- Custom domain available with Netlify Pro

## 📊 **Performance**

- ⚡ **Fast Loading**: Static files load instantly
- 📱 **Mobile Optimized**: Works on all devices
- 🌐 **Global CDN**: Netlify's worldwide distribution
- 🔒 **HTTPS**: Automatic SSL certificate

## 🎯 **Perfect For**

- 📚 **Personal learning** and AWS practice
- 🎓 **Study groups** and exam preparation
- 🏢 **Team training** (share the URL)
- 🌐 **Portfolio projects** (showcase your work)

## 🔄 **Upgrade Path**

Want multiplayer later? Deploy the full Flask version to:
- **Heroku** (free tier)
- **Railway** (modern platform)
- **Render** (easy deployment)

## 🆘 **Troubleshooting**

### **Common Issues**:

1. **404 Error**: Make sure you're deploying the `netlify-static` folder
2. **Blank Page**: Check browser console for JavaScript errors
3. **Questions Not Loading**: Verify `questions.js` is included

### **Debug Steps**:
1. Test locally by opening `index.html` in browser
2. Check Netlify deploy logs
3. Verify all files are uploaded

## 📞 **Support**

- **GitHub Issues**: Report bugs in the repository
- **Netlify Docs**: [netlify.com/docs](https://docs.netlify.com)
- **Community**: Netlify Community Forum

---

**🎉 Ready to deploy your AWS Trivia Game to Netlify!**

The static version gives you a fully functional game that works perfectly on Netlify, while the full Flask version provides multiplayer capabilities on server platforms.
