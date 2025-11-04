#!/usr/bin/env python
"""Test script to verify NLTK data is working"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

print("Testing NLTK data...")
print("=" * 50)

try:
    # Test tokenization
    words = word_tokenize('hello world')
    print(f"[OK] Tokenization works: {words}")
    
    # Test POS tagging
    tagged = nltk.pos_tag(words)
    print(f"[OK] POS tagging works: {tagged}")
    
    # Test lemmatization
    lr = WordNetLemmatizer()
    result = lr.lemmatize('running', pos='v')
    print(f"[OK] Lemmatization works: 'running' -> '{result}'")
    
    print("=" * 50)
    print("[OK] All NLTK data is working correctly!")
    print("You can now use the animation feature!")
    
except LookupError as e:
    print(f"[ERROR] NLTK data missing: {e}")
    print("Please run: python download_nltk_data.py")
except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")

