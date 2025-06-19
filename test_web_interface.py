#!/usr/bin/env python3
"""
Test script for the web interface to ensure no auto-start issues
"""

import requests
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_web_interface():
    """Test the web interface for auto-start issues"""
    
    print("Testing web interface...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        print(f"✓ Server is running (status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Server is not running: {e}")
        return False
    
    # Test 2: Check if game page loads
    try:
        response = requests.get('http://localhost:5000/game', timeout=5)
        print(f"✓ Game page loads (status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Game page failed to load: {e}")
        return False
    
    print("✓ Basic web interface tests passed")
    return True

def test_browser_interaction():
    """Test browser interaction to check for auto-start"""
    
    print("\nTesting browser interaction...")
    
    # Set up Chrome options for headless testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Create webdriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Test joining the game
        driver.get("http://localhost:5000")
        
        # Fill in nickname and join
        nickname_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nickname"))
        )
        nickname_input.send_keys("TestPlayer")
        
        join_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        join_button.click()
        
        # Wait for game page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gameStatus"))
        )
        
        # Check if start button appears (should appear for host)
        start_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "startGameBtn"))
        )
        
        # Wait a few seconds to see if game auto-starts
        time.sleep(3)
        
        # Check if question area is visible (would indicate auto-start)
        question_area = driver.find_element(By.ID, "questionArea")
        if question_area.is_displayed():
            print("✗ Game auto-started! This is the issue.")
            return False
        else:
            print("✓ Game did not auto-start. Manual start required.")
            return True
            
    except Exception as e:
        print(f"✗ Browser test failed: {e}")
        return False
    finally:
        try:
            driver.quit()
        except:
            pass

def main():
    """Run all tests"""
    print("AWS Trivia Game - Web Interface Test")
    print("=" * 40)
    
    # Test basic functionality
    if not test_web_interface():
        print("\n❌ Basic tests failed. Make sure the web server is running.")
        print("Run: python3 web_server.py")
        return
    
    # Test browser interaction (requires Chrome/Chromium)
    try:
        if test_browser_interaction():
            print("\n✅ All tests passed! No auto-start issues detected.")
        else:
            print("\n❌ Auto-start issue detected!")
    except Exception as e:
        print(f"\n⚠️  Browser test skipped (Chrome not available): {e}")
        print("Manual testing recommended.")

if __name__ == "__main__":
    main()
