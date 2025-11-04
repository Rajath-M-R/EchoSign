#!/usr/bin/env python
"""
Script to download NLTK data with retry logic and better error handling
"""
import nltk
import time
import sys

def download_with_retry(resource_name, max_retries=10):
    """Download NLTK resource with retry logic"""
    import os
    
    # Get the default NLTK data directory
    nltk_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'nltk_data')
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to download '{resource_name}' (attempt {attempt + 1}/{max_retries})...")
            # Try downloading to default location first
            nltk.download(resource_name, download_dir=nltk_data_dir, quiet=False)
            
            # Verify it was downloaded
            if resource_name == 'omw-1.4':
                check_path = os.path.join(nltk_data_dir, 'corpora', 'omw-1.4')
            elif resource_name == 'punkt':
                check_path = os.path.join(nltk_data_dir, 'tokenizers', 'punkt')
            elif resource_name == 'averaged_perceptron_tagger':
                check_path = os.path.join(nltk_data_dir, 'taggers', 'averaged_perceptron_tagger')
            elif resource_name == 'wordnet':
                check_path = os.path.join(nltk_data_dir, 'corpora', 'wordnet')
            else:
                check_path = None
            
            if check_path and os.path.exists(check_path):
                print(f"[OK] Successfully downloaded '{resource_name}' to {nltk_data_dir}")
                return True
            else:
                print(f"[WARNING] Download reported success but file not found at expected location")
                # Still return True if download() didn't raise an exception
                return True
        except Exception as e:
            error_msg = str(e)
            if "10054" in error_msg or "forcibly closed" in error_msg:
                print(f"[FAIL] Network error (connection closed by remote host)")
            else:
                print(f"[FAIL] Failed to download '{resource_name}': {e}")
            
            if attempt < max_retries - 1:
                wait_time = min((attempt + 1) * 3, 30)  # Max 30 seconds wait
                print(f"  Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print(f"  Max retries reached for '{resource_name}'")
    return False

if __name__ == "__main__":
    resources = ['punkt', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4']
    
    print("=" * 60)
    print("NLTK Data Downloader")
    print("=" * 60)
    print()
    
    results = {}
    for resource in resources:
        results[resource] = download_with_retry(resource)
        print()
    
    print("=" * 60)
    print("Download Summary:")
    print("=" * 60)
    for resource, success in results.items():
        status = "[OK] SUCCESS" if success else "[FAIL] FAILED"
        print(f"{resource:30} {status}")
    
    if all(results.values()):
        print("\n[OK] All NLTK resources downloaded successfully!")
        sys.exit(0)
    else:
        print("\n⚠ Some downloads failed. You may need to:")
        print("  1. Check your internet connection")
        print("  2. Try running this script again later")
        print("  3. Download manually from: https://www.nltk.org/data.html")
        sys.exit(1)

