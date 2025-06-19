#!/usr/bin/env python3
"""
AWS Trivia Questions API Server
RESTful API to serve 10,000+ AWS trivia questions
Supports filtering, pagination, random selection, and multiple formats
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import json
from datetime import datetime
import os
from questions_levels import levels, get_questions_for_level, get_level_info, get_max_level

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API Configuration
API_VERSION = "v1"
API_BASE_URL = f"/api/{API_VERSION}"
MAX_QUESTIONS_PER_REQUEST = 1000
DEFAULT_QUESTIONS_PER_REQUEST = 10

class QuestionsAPI:
    """Main API class for handling questions"""
    
    def __init__(self):
        self.all_questions = self._load_all_questions()
        self.categories = self._extract_categories()
        self.difficulties = self._extract_difficulties()
        
    def _load_all_questions(self):
        """Load all questions from all levels"""
        all_questions = []
        for level_num, level_data in levels.items():
            for question in level_data['questions']:
                question_copy = question.copy()
                question_copy['level'] = level_num
                question_copy['level_name'] = level_data['name']
                question_copy['id'] = len(all_questions) + 1
                all_questions.append(question_copy)
        return all_questions
    
    def _extract_categories(self):
        """Extract unique categories from questions"""
        categories = set()
        for question in self.all_questions:
            if 'category' in question:
                categories.add(question['category'])
        return sorted(list(categories))
    
    def _extract_difficulties(self):
        """Extract unique difficulties from questions"""
        difficulties = set()
        for question in self.all_questions:
            if 'difficulty' in question:
                difficulties.add(question['difficulty'])
        return sorted(list(difficulties))
    
    def get_questions(self, filters=None, limit=DEFAULT_QUESTIONS_PER_REQUEST, offset=0, randomize=False):
        """Get questions with optional filtering and pagination"""
        questions = self.all_questions.copy()
        
        # Apply filters
        if filters:
            if 'level' in filters:
                questions = [q for q in questions if q.get('level') == filters['level']]
            
            if 'category' in filters:
                questions = [q for q in questions if q.get('category', '').lower() == filters['category'].lower()]
            
            if 'difficulty' in filters:
                questions = [q for q in questions if q.get('difficulty', '').lower() == filters['difficulty'].lower()]
        
        # Randomize if requested
        if randomize:
            random.shuffle(questions)
        
        # Apply pagination
        total_count = len(questions)
        start_index = offset
        end_index = min(offset + limit, total_count)
        
        paginated_questions = questions[start_index:end_index]
        
        return {
            'questions': paginated_questions,
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'count': len(paginated_questions),
                'has_next': end_index < total_count,
                'has_prev': offset > 0
            }
        }
    
    def get_question_by_id(self, question_id):
        """Get a specific question by ID"""
        for question in self.all_questions:
            if question.get('id') == question_id:
                return question
        return None
    
    def get_random_questions(self, count=DEFAULT_QUESTIONS_PER_REQUEST, filters=None):
        """Get random questions with optional filtering"""
        questions = self.all_questions.copy()
        
        # Apply filters
        if filters:
            if 'level' in filters:
                questions = [q for q in questions if q.get('level') == filters['level']]
            
            if 'category' in filters:
                questions = [q for q in questions if q.get('category', '').lower() == filters['category'].lower()]
            
            if 'difficulty' in filters:
                questions = [q for q in questions if q.get('difficulty', '').lower() == filters['difficulty'].lower()]
        
        # Select random questions
        count = min(count, len(questions))
        selected_questions = random.sample(questions, count) if questions else []
        
        return {
            'questions': selected_questions,
            'count': len(selected_questions),
            'total_available': len(questions)
        }

# Initialize API
questions_api = QuestionsAPI()

# API Routes

@app.route('/')
def index():
    """API documentation homepage"""
    return render_template('api_docs.html', 
                         total_questions=len(questions_api.all_questions),
                         categories=questions_api.categories,
                         difficulties=questions_api.difficulties,
                         levels=levels)

@app.route(f'{API_BASE_URL}/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': API_VERSION,
        'total_questions': len(questions_api.all_questions)
    })

@app.route(f'{API_BASE_URL}/info')
def api_info():
    """API information and statistics"""
    return jsonify({
        'api_version': API_VERSION,
        'total_questions': len(questions_api.all_questions),
        'categories': questions_api.categories,
        'difficulties': questions_api.difficulties,
        'levels': {
            level_num: {
                'name': level_data['name'],
                'description': level_data['description'],
                'question_count': len(level_data['questions'])
            }
            for level_num, level_data in levels.items()
        },
        'endpoints': {
            'questions': f'{API_BASE_URL}/questions',
            'random': f'{API_BASE_URL}/questions/random',
            'by_level': f'{API_BASE_URL}/questions/level/{{level}}',
            'by_category': f'{API_BASE_URL}/questions/category/{{category}}',
            'by_difficulty': f'{API_BASE_URL}/questions/difficulty/{{difficulty}}',
            'single_question': f'{API_BASE_URL}/questions/{{id}}'
        }
    })

@app.route(f'{API_BASE_URL}/questions')
def get_questions():
    """Get questions with optional filtering and pagination"""
    try:
        # Parse query parameters
        limit = min(int(request.args.get('limit', DEFAULT_QUESTIONS_PER_REQUEST)), MAX_QUESTIONS_PER_REQUEST)
        offset = int(request.args.get('offset', 0))
        randomize = request.args.get('random', 'false').lower() == 'true'
        
        # Parse filters
        filters = {}
        if request.args.get('level'):
            filters['level'] = int(request.args.get('level'))
        if request.args.get('category'):
            filters['category'] = request.args.get('category')
        if request.args.get('difficulty'):
            filters['difficulty'] = request.args.get('difficulty')
        
        result = questions_api.get_questions(filters, limit, offset, randomize)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameter value',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route(f'{API_BASE_URL}/questions/random')
def get_random_questions():
    """Get random questions"""
    try:
        count = min(int(request.args.get('count', DEFAULT_QUESTIONS_PER_REQUEST)), MAX_QUESTIONS_PER_REQUEST)
        
        # Parse filters
        filters = {}
        if request.args.get('level'):
            filters['level'] = int(request.args.get('level'))
        if request.args.get('category'):
            filters['category'] = request.args.get('category')
        if request.args.get('difficulty'):
            filters['difficulty'] = request.args.get('difficulty')
        
        result = questions_api.get_random_questions(count, filters)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameter value',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route(f'{API_BASE_URL}/questions/<int:question_id>')
def get_question_by_id(question_id):
    """Get a specific question by ID"""
    try:
        question = questions_api.get_question_by_id(question_id)
        
        if question:
            return jsonify({
                'success': True,
                'data': question,
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Question not found',
                'message': f'No question found with ID {question_id}'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route(f'{API_BASE_URL}/questions/level/<int:level>')
def get_questions_by_level(level):
    """Get questions by level"""
    try:
        if level not in levels:
            return jsonify({
                'success': False,
                'error': 'Invalid level',
                'message': f'Level {level} does not exist. Available levels: {list(levels.keys())}'
            }), 400
        
        limit = min(int(request.args.get('limit', MAX_QUESTIONS_PER_REQUEST)), MAX_QUESTIONS_PER_REQUEST)
        offset = int(request.args.get('offset', 0))
        randomize = request.args.get('random', 'false').lower() == 'true'
        
        filters = {'level': level}
        result = questions_api.get_questions(filters, limit, offset, randomize)
        
        # Add level information
        level_info = get_level_info(level)
        result['level_info'] = level_info
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameter value',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route(f'{API_BASE_URL}/questions/category/<category>')
def get_questions_by_category(category):
    """Get questions by category"""
    try:
        if category not in questions_api.categories:
            return jsonify({
                'success': False,
                'error': 'Invalid category',
                'message': f'Category "{category}" does not exist. Available categories: {questions_api.categories}'
            }), 400
        
        limit = min(int(request.args.get('limit', MAX_QUESTIONS_PER_REQUEST)), MAX_QUESTIONS_PER_REQUEST)
        offset = int(request.args.get('offset', 0))
        randomize = request.args.get('random', 'false').lower() == 'true'
        
        filters = {'category': category}
        result = questions_api.get_questions(filters, limit, offset, randomize)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameter value',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route(f'{API_BASE_URL}/questions/difficulty/<difficulty>')
def get_questions_by_difficulty(difficulty):
    """Get questions by difficulty"""
    try:
        if difficulty not in questions_api.difficulties:
            return jsonify({
                'success': False,
                'error': 'Invalid difficulty',
                'message': f'Difficulty "{difficulty}" does not exist. Available difficulties: {questions_api.difficulties}'
            }), 400
        
        limit = min(int(request.args.get('limit', MAX_QUESTIONS_PER_REQUEST)), MAX_QUESTIONS_PER_REQUEST)
        offset = int(request.args.get('offset', 0))
        randomize = request.args.get('random', 'false').lower() == 'true'
        
        filters = {'difficulty': difficulty}
        result = questions_api.get_questions(filters, limit, offset, randomize)
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid parameter value',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route(f'{API_BASE_URL}/categories')
def get_categories():
    """Get all available categories"""
    return jsonify({
        'success': True,
        'data': {
            'categories': questions_api.categories,
            'count': len(questions_api.categories)
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route(f'{API_BASE_URL}/difficulties')
def get_difficulties():
    """Get all available difficulties"""
    return jsonify({
        'success': True,
        'data': {
            'difficulties': questions_api.difficulties,
            'count': len(questions_api.difficulties)
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route(f'{API_BASE_URL}/levels')
def get_levels():
    """Get all available levels"""
    levels_info = {}
    for level_num, level_data in levels.items():
        levels_info[level_num] = {
            'name': level_data['name'],
            'description': level_data['description'],
            'question_count': len(level_data['questions'])
        }
    
    return jsonify({
        'success': True,
        'data': {
            'levels': levels_info,
            'count': len(levels_info)
        },
        'timestamp': datetime.utcnow().isoformat()
    })

# Export endpoints for external use
@app.route(f'{API_BASE_URL}/export/json')
def export_json():
    """Export all questions as JSON"""
    try:
        include_answers = request.args.get('include_answers', 'true').lower() == 'true'
        
        questions = questions_api.all_questions.copy()
        
        if not include_answers:
            for question in questions:
                question.pop('answer', None)
        
        return jsonify({
            'success': True,
            'data': {
                'questions': questions,
                'metadata': {
                    'total_count': len(questions),
                    'export_timestamp': datetime.utcnow().isoformat(),
                    'includes_answers': include_answers,
                    'categories': questions_api.categories,
                    'difficulties': questions_api.difficulties,
                    'levels': list(levels.keys())
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Export failed',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed',
        'message': 'The HTTP method is not allowed for this endpoint'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting AWS Trivia Questions API Server")
    print(f"📊 Total Questions: {len(questions_api.all_questions)}")
    print(f"🏷️  Categories: {len(questions_api.categories)}")
    print(f"📈 Difficulty Levels: {len(questions_api.difficulties)}")
    print(f"🎯 Game Levels: {len(levels)}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}")
    print(f"🔗 API Base: http://localhost:{port}{API_BASE_URL}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
