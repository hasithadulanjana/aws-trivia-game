#!/usr/bin/env python3
"""
Test script to verify web setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import flask
        print("✅ Flask imported successfully")
        
        import flask_socketio
        print("✅ Flask-SocketIO imported successfully")
        
        from questions import questions
        print(f"✅ Questions loaded: {len(questions)} questions available")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_templates():
    """Test if template files exist"""
    templates = ['templates/base.html', 'templates/index.html', 'templates/game.html']
    static_files = ['static/css/style.css', 'static/js/game.js']
    
    all_exist = True
    
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            all_exist = False
    
    for static_file in static_files:
        if os.path.exists(static_file):
            print(f"✅ {static_file} exists")
        else:
            print(f"❌ {static_file} missing")
            all_exist = False
    
    return all_exist

def main():
    print("🧪 Testing AWS Trivia Game Web Setup")
    print("=" * 40)
    
    imports_ok = test_imports()
    print()
    
    files_ok = test_templates()
    print()
    
    if imports_ok and files_ok:
        print("🎉 All tests passed! Ready to start the web server.")
        print("Run: python3 start_web_server.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return imports_ok and files_ok

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
