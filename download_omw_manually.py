#!/usr/bin/env python
"""Manual download script for omw-1.4 with multiple attempts"""
import nltk
import time
import os

print("=" * 60)
print("Downloading omw-1.4 (Open Multilingual Wordnet)")
print("=" * 60)
print()

# Ensure we use the default NLTK data directory
nltk_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)

print(f"Target directory: {nltk_data_dir}")
print()

max_attempts = 15
for attempt in range(1, max_attempts + 1):
    try:
        print(f"Attempt {attempt}/{max_attempts}...")
        nltk.download('omw-1.4', download_dir=nltk_data_dir, quiet=False)
        
        # Verify download
        omw_path = os.path.join(nltk_data_dir, 'corpora', 'omw-1.4')
        if os.path.exists(omw_path):
            print(f"\n[SUCCESS] omw-1.4 downloaded successfully!")
            print(f"Location: {omw_path}")
            break
        else:
            print(f"[WARNING] Download reported success but file not found.")
            print(f"Expected at: {omw_path}")
            if attempt < max_attempts:
                wait = min(attempt * 5, 45)
                print(f"Waiting {wait} seconds before retry...\n")
                time.sleep(wait)
    except Exception as e:
        error_msg = str(e)
        if "10054" in error_msg:
            print(f"[NETWORK ERROR] Connection closed by remote host")
        else:
            print(f"[ERROR] {error_msg}")
        
        if attempt < max_attempts:
            wait = min(attempt * 5, 45)
            print(f"Waiting {wait} seconds before retry...\n")
            time.sleep(wait)
        else:
            print("\n[FAILED] Could not download omw-1.4 after all attempts.")
            print("\nAlternative options:")
            print("1. Try running: python -m nltk.downloader omw-1.4")
            print("2. Download manually from: https://www.nltk.org/nltk_data/")
            print("3. Check your internet connection and firewall settings")

print("\n" + "=" * 60)

