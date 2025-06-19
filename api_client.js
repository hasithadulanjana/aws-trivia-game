/**
 * AWS Trivia Questions API Client - JavaScript/Node.js SDK
 * 
 * Usage:
 *   // Browser
 *   const client = new AWSTriviaAPIClient('https://your-api-domain.com');
 *   
 *   // Node.js
 *   const AWSTriviaAPIClient = require('./api_client.js');
 *   const client = new AWSTriviaAPIClient('https://your-api-domain.com');
 */

class AWSTriviaAPIClient {
    /**
     * Initialize the API client
     * @param {string} baseUrl - Base URL of the API server
     * @param {string} apiVersion - API version to use (default: v1)
     */
    constructor(baseUrl, apiVersion = 'v1') {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiVersion = apiVersion;
        this.apiBase = `${this.baseUrl}/api/${apiVersion}`;
        
        // Detect environment (Node.js vs Browser)
        this.isNode = typeof window === 'undefined';
        
        if (this.isNode) {
            // Node.js environment
            try {
                this.fetch = require('node-fetch');
            } catch (e) {
                console.warn('node-fetch not found. Please install: npm install node-fetch');
                this.fetch = null;
            }
        } else {
            // Browser environment
            this.fetch = window.fetch.bind(window);
        }
    }
    
    /**
     * Make HTTP request to API endpoint
     * @param {string} endpoint - API endpoint
     * @param {Object} params - Query parameters
     * @returns {Promise<Object>} API response
     */
    async _makeRequest(endpoint, params = {}) {
        try {
            if (!this.fetch) {
                throw new Error('Fetch not available. In Node.js, install node-fetch: npm install node-fetch');
            }
            
            const url = new URL(`${this.apiBase}${endpoint}`);
            
            // Add query parameters
            Object.keys(params).forEach(key => {
                if (params[key] !== null && params[key] !== undefined) {
                    url.searchParams.append(key, params[key]);
                }
            });
            
            const response = await this.fetch(url.toString(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'AWS-Trivia-API-Client-JS/1.0'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            return {
                success: false,
                error: 'Request failed',
                message: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
    
    /**
     * Check API health status
     * @returns {Promise<Object>} Health status
     */
    async healthCheck() {
        return await this._makeRequest('/health');
    }
    
    /**
     * Get API information and statistics
     * @returns {Promise<Object>} API information
     */
    async getApiInfo() {
        return await this._makeRequest('/info');
    }
    
    /**
     * Get questions with optional filtering and pagination
     * @param {Object} options - Query options
     * @param {number} options.limit - Number of questions to return (max 1000)
     * @param {number} options.offset - Pagination offset
     * @param {number} options.level - Filter by level (1-5)
     * @param {string} options.category - Filter by category
     * @param {string} options.difficulty - Filter by difficulty
     * @param {boolean} options.randomize - Randomize results
     * @returns {Promise<Object>} Questions response
     */
    async getQuestions(options = {}) {
        const {
            limit = 10,
            offset = 0,
            level,
            category,
            difficulty,
            randomize = false
        } = options;
        
        const params = {
            limit,
            offset,
            random: randomize.toString()
        };
        
        if (level !== undefined) params.level = level;
        if (category) params.category = category;
        if (difficulty) params.difficulty = difficulty;
        
        return await this._makeRequest('/questions', params);
    }
    
    /**
     * Get random questions with optional filtering
     * @param {Object} options - Query options
     * @param {number} options.count - Number of questions to return
     * @param {number} options.level - Filter by level
     * @param {string} options.category - Filter by category
     * @param {string} options.difficulty - Filter by difficulty
     * @returns {Promise<Object>} Random questions response
     */
    async getRandomQuestions(options = {}) {
        const {
            count = 10,
            level,
            category,
            difficulty
        } = options;
        
        const params = { count };
        
        if (level !== undefined) params.level = level;
        if (category) params.category = category;
        if (difficulty) params.difficulty = difficulty;
        
        return await this._makeRequest('/questions/random', params);
    }
    
    /**
     * Get a specific question by ID
     * @param {number} questionId - Question ID
     * @returns {Promise<Object>} Question response
     */
    async getQuestionById(questionId) {
        return await this._makeRequest(`/questions/${questionId}`);
    }
    
    /**
     * Get questions from a specific level
     * @param {number} level - Level number (1-5)
     * @param {Object} options - Query options
     * @param {number} options.limit - Number of questions to return
     * @param {number} options.offset - Pagination offset
     * @param {boolean} options.randomize - Randomize results
     * @returns {Promise<Object>} Level questions response
     */
    async getQuestionsByLevel(level, options = {}) {
        const {
            limit = 100,
            offset = 0,
            randomize = false
        } = options;
        
        const params = {
            limit,
            offset,
            random: randomize.toString()
        };
        
        return await this._makeRequest(`/questions/level/${level}`, params);
    }
    
    /**
     * Get questions from a specific category
     * @param {string} category - Category name
     * @param {Object} options - Query options
     * @param {number} options.limit - Number of questions to return
     * @param {number} options.offset - Pagination offset
     * @param {boolean} options.randomize - Randomize results
     * @returns {Promise<Object>} Category questions response
     */
    async getQuestionsByCategory(category, options = {}) {
        const {
            limit = 100,
            offset = 0,
            randomize = false
        } = options;
        
        const params = {
            limit,
            offset,
            random: randomize.toString()
        };
        
        return await this._makeRequest(`/questions/category/${category}`, params);
    }
    
    /**
     * Get questions from a specific difficulty level
     * @param {string} difficulty - Difficulty level
     * @param {Object} options - Query options
     * @param {number} options.limit - Number of questions to return
     * @param {number} options.offset - Pagination offset
     * @param {boolean} options.randomize - Randomize results
     * @returns {Promise<Object>} Difficulty questions response
     */
    async getQuestionsByDifficulty(difficulty, options = {}) {
        const {
            limit = 100,
            offset = 0,
            randomize = false
        } = options;
        
        const params = {
            limit,
            offset,
            random: randomize.toString()
        };
        
        return await this._makeRequest(`/questions/difficulty/${difficulty}`, params);
    }
    
    /**
     * Get all available categories
     * @returns {Promise<Object>} Categories response
     */
    async getCategories() {
        return await this._makeRequest('/categories');
    }
    
    /**
     * Get all available difficulty levels
     * @returns {Promise<Object>} Difficulties response
     */
    async getDifficulties() {
        return await this._makeRequest('/difficulties');
    }
    
    /**
     * Get all available game levels
     * @returns {Promise<Object>} Levels response
     */
    async getLevels() {
        return await this._makeRequest('/levels');
    }
    
    /**
     * Export all questions as JSON
     * @param {boolean} includeAnswers - Whether to include correct answers
     * @returns {Promise<Object>} Export response
     */
    async exportAllQuestions(includeAnswers = true) {
        const params = {
            include_answers: includeAnswers.toString()
        };
        
        return await this._makeRequest('/export/json', params);
    }
    
    /**
     * Parse questions from API response
     * @param {Object} response - API response containing questions
     * @returns {Array} Array of question objects
     */
    parseQuestions(response) {
        if (!response.success || !response.data || !response.data.questions) {
            return [];
        }
        
        return response.data.questions.map(q => ({
            id: q.id || 0,
            question: q.question || '',
            options: q.options || [],
            answer: q.answer || 0,
            difficulty: q.difficulty || '',
            category: q.category || '',
            level: q.level || 1,
            levelName: q.level_name || ''
        }));
    }
    
    /**
     * Create a quiz from random questions
     * @param {Object} options - Quiz options
     * @param {number} options.count - Number of questions
     * @param {number} options.level - Filter by level
     * @param {string} options.category - Filter by category
     * @param {string} options.difficulty - Filter by difficulty
     * @returns {Promise<Object>} Quiz object
     */
    async createQuiz(options = {}) {
        const response = await this.getRandomQuestions(options);
        
        if (!response.success) {
            return {
                success: false,
                error: response.error,
                message: response.message
            };
        }
        
        const questions = this.parseQuestions(response);
        
        return {
            success: true,
            quiz: {
                id: Date.now().toString(),
                questions: questions,
                totalQuestions: questions.length,
                createdAt: new Date().toISOString(),
                options: options
            }
        };
    }
}

// Example usage function
async function exampleUsage() {
    console.log('🚀 AWS Trivia API Client - JavaScript Example');
    console.log('='.repeat(50));
    
    const client = new AWSTriviaAPIClient('http://localhost:5001');
    
    try {
        // Health check
        console.log('\n1. Health Check:');
        const health = await client.healthCheck();
        if (health.success) {
            console.log(`✅ API is healthy - ${health.total_questions || 0} questions available`);
        } else {
            console.log(`❌ API health check failed: ${health.error}`);
        }
        
        // Get API info
        console.log('\n2. API Information:');
        const info = await client.getApiInfo();
        if (info.success) {
            console.log(`📊 Total Questions: ${info.data.total_questions || 0}`);
            console.log(`🏷️  Categories: ${info.data.categories?.length || 0}`);
            console.log(`📈 Difficulties: ${info.data.difficulties?.length || 0}`);
            console.log(`🎯 Levels: ${Object.keys(info.data.levels || {}).length}`);
        }
        
        // Get random questions
        console.log('\n3. Random Questions (3):');
        const randomResponse = await client.getRandomQuestions({ count: 3 });
        if (randomResponse.success) {
            const questions = client.parseQuestions(randomResponse);
            questions.forEach((q, i) => {
                console.log(`\n   Question ${i + 1}: ${q.question}`);
                console.log(`   Category: ${q.category} | Difficulty: ${q.difficulty} | Level: ${q.level}`);
                q.options.forEach((option, j) => {
                    const marker = j === q.answer ? '✓' : ' ';
                    console.log(`   ${marker} ${String.fromCharCode(65 + j)}. ${option}`);
                });
            });
        }
        
        // Create a quiz
        console.log('\n4. Create Quiz (Level 1, 2 questions):');
        const quiz = await client.createQuiz({ count: 2, level: 1 });
        if (quiz.success) {
            console.log(`   ✅ Quiz created with ${quiz.quiz.totalQuestions} questions`);
            quiz.quiz.questions.forEach((q, i) => {
                console.log(`   • Question ${i + 1}: ${q.question} (${q.category})`);
            });
        }
        
        // Get categories
        console.log('\n5. Available Categories:');
        const categoriesResponse = await client.getCategories();
        if (categoriesResponse.success) {
            const categories = categoriesResponse.data.categories || [];
            console.log(`   ${categories.join(', ')}`);
        }
        
        console.log('\n' + '='.repeat(50));
        console.log('✅ JavaScript API Client Example Complete!');
        
    } catch (error) {
        console.error('❌ Example failed:', error.message);
    }
}

// Export for different environments
if (typeof module !== 'undefined' && module.exports) {
    // Node.js
    module.exports = AWSTriviaAPIClient;
} else if (typeof window !== 'undefined') {
    // Browser
    window.AWSTriviaAPIClient = AWSTriviaAPIClient;
}

// Run example if this file is executed directly in Node.js
if (typeof require !== 'undefined' && require.main === module) {
    exampleUsage();
}
