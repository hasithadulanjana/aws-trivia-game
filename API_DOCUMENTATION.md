# AWS Trivia Questions API Documentation

## Overview
The AWS Trivia Questions API provides access to 10,000+ carefully curated AWS trivia questions organized by difficulty levels, categories, and game levels. This RESTful API enables developers to integrate AWS knowledge testing into their applications, training platforms, and educational tools.

## 🚀 **Quick Start**

### **Base URL**
```
https://your-domain.com/api/v1
```

### **Authentication**
No authentication required - the API is publicly accessible.

### **Response Format**
All responses are in JSON format with the following structure:
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-06-19T14:00:00.000Z"
}
```

### **Error Format**
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message",
  "timestamp": "2025-06-19T14:00:00.000Z"
}
```

## 📊 **API Statistics**
- **Total Questions**: 10,000+
- **Categories**: 15+ AWS service categories
- **Difficulty Levels**: 5 levels (beginner to master)
- **Game Levels**: 5 progressive levels
- **Rate Limit**: None
- **CORS**: Enabled for all origins

## 🔗 **Endpoints**

### **Health Check**
```http
GET /api/v1/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-06-19T14:00:00.000Z",
    "version": "v1",
    "total_questions": 10000
  }
}
```

### **API Information**
```http
GET /api/v1/info
```

**Response:**
```json
{
  "success": true,
  "data": {
    "api_version": "v1",
    "total_questions": 10000,
    "categories": ["Compute", "Storage", "Database", ...],
    "difficulties": ["beginner", "intermediate", "advanced", "expert", "master"],
    "levels": {
      "1": {
        "name": "AWS Fundamentals",
        "description": "Basic AWS services and core concepts",
        "question_count": 2000
      },
      ...
    },
    "endpoints": { ... }
  }
}
```

### **Get Questions**
```http
GET /api/v1/questions
```

**Query Parameters:**
- `limit` (integer, default: 10, max: 1000) - Number of questions to return
- `offset` (integer, default: 0) - Pagination offset
- `level` (integer, 1-5) - Filter by game level
- `category` (string) - Filter by category
- `difficulty` (string) - Filter by difficulty level
- `random` (boolean, default: false) - Randomize results

**Example:**
```http
GET /api/v1/questions?limit=5&level=1&random=true
```

**Response:**
```json
{
  "success": true,
  "data": {
    "questions": [
      {
        "id": 1,
        "question": "What does EC2 stand for?",
        "options": [
          "Elastic Compute Cloud",
          "Elastic Container Cloud",
          "Edge Control Compute",
          "Elastic Core Cluster"
        ],
        "answer": 0,
        "difficulty": "beginner",
        "category": "Compute",
        "level": 1,
        "level_name": "AWS Fundamentals"
      }
    ],
    "pagination": {
      "total": 2000,
      "limit": 5,
      "offset": 0,
      "count": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### **Get Random Questions**
```http
GET /api/v1/questions/random
```

**Query Parameters:**
- `count` (integer, default: 10, max: 1000) - Number of questions to return
- `level` (integer, 1-5) - Filter by game level
- `category` (string) - Filter by category
- `difficulty` (string) - Filter by difficulty level

**Example:**
```http
GET /api/v1/questions/random?count=3&difficulty=intermediate
```

### **Get Question by ID**
```http
GET /api/v1/questions/{id}
```

**Example:**
```http
GET /api/v1/questions/1
```

### **Get Questions by Level**
```http
GET /api/v1/questions/level/{level}
```

**Path Parameters:**
- `level` (integer, 1-5) - Game level

**Query Parameters:**
- `limit` (integer, default: 100, max: 1000)
- `offset` (integer, default: 0)
- `random` (boolean, default: false)

**Example:**
```http
GET /api/v1/questions/level/1?limit=10&random=true
```

### **Get Questions by Category**
```http
GET /api/v1/questions/category/{category}
```

**Path Parameters:**
- `category` (string) - Category name

**Available Categories:**
- Compute
- Storage
- Database
- Networking
- Security
- Management
- Analytics
- Machine Learning
- Containers
- Serverless
- Migration
- Governance
- Billing
- Emerging Tech
- Hybrid

**Example:**
```http
GET /api/v1/questions/category/Compute?limit=5
```

### **Get Questions by Difficulty**
```http
GET /api/v1/questions/difficulty/{difficulty}
```

**Path Parameters:**
- `difficulty` (string) - Difficulty level

**Available Difficulties:**
- `beginner` - Basic AWS concepts
- `intermediate` - Architecture patterns
- `advanced` - Complex scenarios
- `expert` - Specialty services
- `master` - Professional architect level

**Example:**
```http
GET /api/v1/questions/difficulty/advanced?limit=5
```

### **Get Categories**
```http
GET /api/v1/categories
```

**Response:**
```json
{
  "success": true,
  "data": {
    "categories": ["Compute", "Storage", "Database", ...],
    "count": 15
  }
}
```

### **Get Difficulties**
```http
GET /api/v1/difficulties
```

### **Get Levels**
```http
GET /api/v1/levels
```

### **Export All Questions**
```http
GET /api/v1/export/json
```

**Query Parameters:**
- `include_answers` (boolean, default: true) - Include correct answers

**⚠️ Warning:** This endpoint returns all 10,000+ questions and may be large.

## 🛠️ **SDKs and Client Libraries**

### **Python SDK**
```python
from api_client import AWSTriviaAPIClient

client = AWSTriviaAPIClient('https://your-api-domain.com')

# Get random questions
response = client.get_random_questions(count=10, difficulty='intermediate')
questions = client.parse_questions(response)

for question in questions:
    print(f"Q: {question.question}")
    for i, option in enumerate(question.options):
        print(f"  {chr(65+i)}. {option}")
```

### **JavaScript/Node.js SDK**
```javascript
const AWSTriviaAPIClient = require('./api_client.js');
const client = new AWSTriviaAPIClient('https://your-api-domain.com');

// Get questions by level
const response = await client.getQuestionsByLevel(1, { limit: 5 });
const questions = client.parseQuestions(response);

questions.forEach(q => {
    console.log(`Q: ${q.question}`);
    q.options.forEach((option, i) => {
        console.log(`  ${String.fromCharCode(65+i)}. ${option}`);
    });
});
```

### **cURL Examples**
```bash
# Get random questions
curl "https://your-api-domain.com/api/v1/questions/random?count=5"

# Get beginner level questions
curl "https://your-api-domain.com/api/v1/questions/difficulty/beginner?limit=3"

# Get compute category questions
curl "https://your-api-domain.com/api/v1/questions/category/Compute?limit=5"

# Get API information
curl "https://your-api-domain.com/api/v1/info"
```

## 📝 **Question Format**

Each question object contains:
```json
{
  "id": 1,
  "question": "What does EC2 stand for?",
  "options": [
    "Elastic Compute Cloud",
    "Elastic Container Cloud", 
    "Edge Control Compute",
    "Elastic Core Cluster"
  ],
  "answer": 0,
  "difficulty": "beginner",
  "category": "Compute",
  "level": 1,
  "level_name": "AWS Fundamentals"
}
```

**Field Descriptions:**
- `id` - Unique question identifier
- `question` - The question text
- `options` - Array of 4 multiple choice options
- `answer` - Index of correct answer (0-3)
- `difficulty` - Difficulty level (beginner/intermediate/advanced/expert/master)
- `category` - AWS service category
- `level` - Game level (1-5)
- `level_name` - Human-readable level name

## 🎯 **Use Cases**

### **Educational Platforms**
```javascript
// Create a beginner AWS quiz
const quiz = await client.createQuiz({
    count: 10,
    difficulty: 'beginner',
    category: 'Compute'
});
```

### **Training Applications**
```python
# Progressive learning system
for level in range(1, 6):
    questions = client.get_questions_by_level(level, limit=20)
    # Present questions to user
    # Track progress and advancement
```

### **Assessment Tools**
```javascript
// Certification practice exam
const examQuestions = await client.getRandomQuestions({
    count: 50,
    difficulty: 'advanced'
});
```

### **Game Development**
```python
# Trivia game with categories
categories = client.get_categories()
for category in categories.data['categories']:
    questions = client.get_questions_by_category(category, limit=5)
    # Create category-based rounds
```

## 🔧 **Integration Examples**

### **React Component**
```jsx
import React, { useState, useEffect } from 'react';

function AWSQuiz() {
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const client = new AWSTriviaAPIClient('https://your-api-domain.com');
        
        client.getRandomQuestions({ count: 10 })
            .then(response => {
                if (response.success) {
                    setQuestions(client.parseQuestions(response));
                }
                setLoading(false);
            });
    }, []);
    
    if (loading) return <div>Loading questions...</div>;
    
    return (
        <div>
            {questions.map((q, index) => (
                <div key={q.id}>
                    <h3>Question {index + 1}: {q.question}</h3>
                    {q.options.map((option, i) => (
                        <button key={i}>{option}</button>
                    ))}
                </div>
            ))}
        </div>
    );
}
```

### **Express.js Backend**
```javascript
const express = require('express');
const AWSTriviaAPIClient = require('./api_client.js');

const app = express();
const triviaClient = new AWSTriviaAPIClient('https://your-api-domain.com');

app.get('/quiz/:difficulty', async (req, res) => {
    try {
        const response = await triviaClient.getQuestionsByDifficulty(
            req.params.difficulty,
            { limit: 10, randomize: true }
        );
        
        if (response.success) {
            res.json({
                quiz: triviaClient.parseQuestions(response),
                difficulty: req.params.difficulty
            });
        } else {
            res.status(400).json({ error: response.error });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});
```

### **Python Flask Integration**
```python
from flask import Flask, jsonify
from api_client import AWSTriviaAPIClient

app = Flask(__name__)
client = AWSTriviaAPIClient('https://your-api-domain.com')

@app.route('/api/quiz/<int:level>')
def get_level_quiz(level):
    try:
        response = client.get_questions_by_level(level, limit=10, randomize=True)
        
        if response.success:
            questions = client.parse_questions(response)
            return jsonify({
                'quiz': [q.__dict__ for q in questions],
                'level': level
            })
        else:
            return jsonify({'error': response.error}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## 📈 **Performance & Limits**

### **Rate Limiting**
- No rate limits currently implemented
- Fair use policy applies
- Consider caching responses for production use

### **Response Times**
- Health check: < 50ms
- Single question: < 100ms
- Bulk questions (100): < 500ms
- Export all: 2-5 seconds

### **Pagination**
- Maximum 1000 questions per request
- Use offset/limit for large datasets
- Consider multiple requests for > 1000 questions

### **Caching Recommendations**
```javascript
// Cache API info and metadata
const apiInfo = await client.getApiInfo();
localStorage.setItem('aws-trivia-api-info', JSON.stringify(apiInfo));

// Cache categories and difficulties
const categories = await client.getCategories();
const difficulties = await client.getDifficulties();
```

## 🛡️ **Error Handling**

### **Common Error Codes**
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (invalid endpoint or resource)
- `405` - Method Not Allowed
- `500` - Internal Server Error

### **Error Handling Examples**
```javascript
try {
    const response = await client.getQuestionById(999999);
    if (!response.success) {
        console.error(`API Error: ${response.error} - ${response.message}`);
    }
} catch (error) {
    console.error(`Network Error: ${error.message}`);
}
```

```python
response = client.get_questions_by_level(10)  # Invalid level
if not response.success:
    print(f"Error: {response.error}")
    print(f"Message: {response.message}")
```

## 🚀 **Deployment**

### **Self-Hosting**
```bash
# Clone the repository
git clone https://github.com/hasithadulanjana/aws-trivia-game.git
cd aws-trivia-game

# Install dependencies
pip install -r requirements.txt

# Start API server
python api_server.py

# API available at http://localhost:5001
```

### **Environment Variables**
```bash
export PORT=5001
export DEBUG=false
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["python", "api_server.py"]
```

### **Production Considerations**
- Use a production WSGI server (Gunicorn, uWSGI)
- Implement proper logging
- Add monitoring and health checks
- Consider Redis for caching
- Use a reverse proxy (Nginx)

## 📚 **Additional Resources**

### **Documentation**
- [API Interactive Documentation](https://your-domain.com/) - Try endpoints live
- [GitHub Repository](https://github.com/hasithadulanjana/aws-trivia-game)
- [Python SDK Documentation](./api_client.py)
- [JavaScript SDK Documentation](./api_client.js)

### **Community**
- Report issues on GitHub
- Contribute questions and improvements
- Share your implementations

### **Support**
- GitHub Issues for bug reports
- Feature requests welcome
- Community-driven development

---

## 🎉 **Get Started Today!**

The AWS Trivia Questions API makes it easy to integrate AWS knowledge testing into any application. With 10,000+ questions, comprehensive SDKs, and flexible filtering options, you can create engaging educational experiences for AWS learners at any level.

**Try it now:**
```bash
curl "https://your-api-domain.com/api/v1/questions/random?count=3"
```

**Happy coding!** 🚀
