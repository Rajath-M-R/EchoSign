#!/usr/bin/env python
"""Check where NLTK data is located"""
import nltk
import os

print("NLTK Data Paths:")
print("=" * 60)
for path in nltk.data.path:
    print(f"  {path}")
    if os.path.exists(path):
        print(f"    [EXISTS] Contents: {os.listdir(path)[:5]}...")
    else:
        print(f"    [NOT FOUND]")

print("\n" + "=" * 60)
print("Checking for omw-1.4:")
print("=" * 60)

# Check each path
found = False
for path in nltk.data.path:
    omw_path = os.path.join(path, 'corpora', 'omw-1.4')
    if os.path.exists(omw_path):
        print(f"[FOUND] {omw_path}")
        found = True
    else:
        print(f"[NOT FOUND] {omw_path}")

if not found:
    print("\nTrying to download omw-1.4 to default location...")
    try:
        nltk.download('omw-1.4', quiet=False)
        print("[OK] Download completed!")
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")

