#!/usr/bin/env python3
"""
AWS Trivia Questions API Client
Python SDK for accessing the AWS Trivia Questions API
"""

import requests
import json
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Question:
    """Question data class"""
    id: int
    question: str
    options: List[str]
    answer: int
    difficulty: str
    category: str
    level: int
    level_name: str

@dataclass
class APIResponse:
    """API response data class"""
    success: bool
    data: Dict
    timestamp: str
    error: Optional[str] = None
    message: Optional[str] = None

class AWSTrivia APIClient:
    """
    Python client for the AWS Trivia Questions API
    
    Usage:
        client = AWSTriviaAPIClient("https://your-api-domain.com")
        questions = client.get_random_questions(count=10)
    """
    
    def __init__(self, base_url: str, api_version: str = "v1"):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the API server
            api_version: API version to use (default: v1)
        """
        self.base_url = base_url.rstrip('/')
        self.api_version = api_version
        self.api_base = f"{self.base_url}/api/{api_version}"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AWS-Trivia-API-Client/1.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> APIResponse:
        """Make HTTP request to API endpoint"""
        try:
            url = f"{self.api_base}{endpoint}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return APIResponse(
                success=data.get('success', False),
                data=data.get('data', {}),
                timestamp=data.get('timestamp', ''),
                error=data.get('error'),
                message=data.get('message')
            )
            
        except requests.exceptions.RequestException as e:
            return APIResponse(
                success=False,
                data={},
                timestamp=datetime.utcnow().isoformat(),
                error='Request failed',
                message=str(e)
            )
        except json.JSONDecodeError as e:
            return APIResponse(
                success=False,
                data={},
                timestamp=datetime.utcnow().isoformat(),
                error='Invalid JSON response',
                message=str(e)
            )
    
    def health_check(self) -> APIResponse:
        """Check API health status"""
        return self._make_request('/health')
    
    def get_api_info(self) -> APIResponse:
        """Get API information and statistics"""
        return self._make_request('/info')
    
    def get_questions(self, 
                     limit: int = 10, 
                     offset: int = 0,
                     level: Optional[int] = None,
                     category: Optional[str] = None,
                     difficulty: Optional[str] = None,
                     randomize: bool = False) -> APIResponse:
        """
        Get questions with optional filtering and pagination
        
        Args:
            limit: Number of questions to return (max 1000)
            offset: Pagination offset
            level: Filter by level (1-5)
            category: Filter by category
            difficulty: Filter by difficulty
            randomize: Randomize results
        """
        params = {
            'limit': limit,
            'offset': offset,
            'random': str(randomize).lower()
        }
        
        if level is not None:
            params['level'] = level
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
        
        return self._make_request('/questions', params)
    
    def get_random_questions(self,
                           count: int = 10,
                           level: Optional[int] = None,
                           category: Optional[str] = None,
                           difficulty: Optional[str] = None) -> APIResponse:
        """
        Get random questions with optional filtering
        
        Args:
            count: Number of questions to return
            level: Filter by level
            category: Filter by category
            difficulty: Filter by difficulty
        """
        params = {'count': count}
        
        if level is not None:
            params['level'] = level
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
        
        return self._make_request('/questions/random', params)
    
    def get_question_by_id(self, question_id: int) -> APIResponse:
        """Get a specific question by ID"""
        return self._make_request(f'/questions/{question_id}')
    
    def get_questions_by_level(self, 
                              level: int,
                              limit: int = 100,
                              offset: int = 0,
                              randomize: bool = False) -> APIResponse:
        """
        Get questions from a specific level
        
        Args:
            level: Level number (1-5)
            limit: Number of questions to return
            offset: Pagination offset
            randomize: Randomize results
        """
        params = {
            'limit': limit,
            'offset': offset,
            'random': str(randomize).lower()
        }
        
        return self._make_request(f'/questions/level/{level}', params)
    
    def get_questions_by_category(self,
                                 category: str,
                                 limit: int = 100,
                                 offset: int = 0,
                                 randomize: bool = False) -> APIResponse:
        """
        Get questions from a specific category
        
        Args:
            category: Category name
            limit: Number of questions to return
            offset: Pagination offset
            randomize: Randomize results
        """
        params = {
            'limit': limit,
            'offset': offset,
            'random': str(randomize).lower()
        }
        
        return self._make_request(f'/questions/category/{category}', params)
    
    def get_questions_by_difficulty(self,
                                   difficulty: str,
                                   limit: int = 100,
                                   offset: int = 0,
                                   randomize: bool = False) -> APIResponse:
        """
        Get questions from a specific difficulty level
        
        Args:
            difficulty: Difficulty level
            limit: Number of questions to return
            offset: Pagination offset
            randomize: Randomize results
        """
        params = {
            'limit': limit,
            'offset': offset,
            'random': str(randomize).lower()
        }
        
        return self._make_request(f'/questions/difficulty/{difficulty}', params)
    
    def get_categories(self) -> APIResponse:
        """Get all available categories"""
        return self._make_request('/categories')
    
    def get_difficulties(self) -> APIResponse:
        """Get all available difficulty levels"""
        return self._make_request('/difficulties')
    
    def get_levels(self) -> APIResponse:
        """Get all available game levels"""
        return self._make_request('/levels')
    
    def export_all_questions(self, include_answers: bool = True) -> APIResponse:
        """
        Export all questions as JSON
        
        Args:
            include_answers: Whether to include correct answers
        """
        params = {'include_answers': str(include_answers).lower()}
        return self._make_request('/export/json', params)
    
    def parse_questions(self, response: APIResponse) -> List[Question]:
        """
        Parse API response into Question objects
        
        Args:
            response: API response containing questions
            
        Returns:
            List of Question objects
        """
        if not response.success:
            return []
        
        questions = response.data.get('questions', [])
        return [
            Question(
                id=q.get('id', 0),
                question=q.get('question', ''),
                options=q.get('options', []),
                answer=q.get('answer', 0),
                difficulty=q.get('difficulty', ''),
                category=q.get('category', ''),
                level=q.get('level', 1),
                level_name=q.get('level_name', '')
            )
            for q in questions
        ]

# Example usage and testing
if __name__ == '__main__':
    # Example usage
    client = AWSTriviaAPIClient('http://localhost:5001')
    
    print("🚀 AWS Trivia API Client Example")
    print("=" * 50)
    
    # Health check
    print("\n1. Health Check:")
    health = client.health_check()
    if health.success:
        print(f"✅ API is healthy - {health.data.get('total_questions', 0)} questions available")
    else:
        print(f"❌ API health check failed: {health.error}")
    
    # Get API info
    print("\n2. API Information:")
    info = client.get_api_info()
    if info.success:
        data = info.data
        print(f"📊 Total Questions: {data.get('total_questions', 0)}")
        print(f"🏷️  Categories: {len(data.get('categories', []))}")
        print(f"📈 Difficulties: {len(data.get('difficulties', []))}")
        print(f"🎯 Levels: {len(data.get('levels', {}))}")
    
    # Get random questions
    print("\n3. Random Questions (3):")
    random_response = client.get_random_questions(count=3)
    if random_response.success:
        questions = client.parse_questions(random_response)
        for i, q in enumerate(questions, 1):
            print(f"\n   Question {i}: {q.question}")
            print(f"   Category: {q.category} | Difficulty: {q.difficulty} | Level: {q.level}")
            for j, option in enumerate(q.options):
                marker = "✓" if j == q.answer else " "
                print(f"   {marker} {chr(65+j)}. {option}")
    
    # Get questions by level
    print("\n4. Level 1 Questions (2):")
    level_response = client.get_questions_by_level(level=1, limit=2)
    if level_response.success:
        questions = client.parse_questions(level_response)
        for q in questions:
            print(f"   • {q.question} ({q.category})")
    
    # Get categories
    print("\n5. Available Categories:")
    categories_response = client.get_categories()
    if categories_response.success:
        categories = categories_response.data.get('categories', [])
        print(f"   {', '.join(categories)}")
    
    print("\n" + "=" * 50)
    print("✅ API Client Example Complete!")
