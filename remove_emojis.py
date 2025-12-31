#!/usr/bin/env python3
"""
Remove Emojis from All Files
Author: Victor Ibhafidon

Removes all emojis from Python, Markdown, and text files before GitHub push.
"""

import re
import os
from pathlib import Path

# Common emojis used in the codebase
EMOJI_PATTERN = re.compile(
 r'['
 r'\U0001F300-\U0001F9FF' # Miscellaneous Symbols and Pictographs
 r'\U0001F600-\U0001F64F' # Emoticons
 r'\U0001F680-\U0001F6FF' # Transport and Map Symbols
 r'\U00002600-\U000026FF' # Miscellaneous Symbols
 r'\U00002700-\U000027BF' # Dingbats
 r'\U0001F1E0-\U0001F1FF' # Flags
 r'\U0001F900-\U0001F9FF' # Supplemental Symbols and Pictographs
 r'\U0001FA00-\U0001FA6F' # Chess Symbols
 r'\U0001FA70-\U0001FAFF' # Symbols and Pictographs Extended-A
 r'\U00002648-\U00002653' # Zodiac
 r'\U000026CE' # Ophiuchus
 r'\U0001F300-\U0001F5FF' # Misc Symbols
 r'\U0001F900-\U0001F9FF' # Supplemental Symbols
 r'\U0001FA70-\U0001FAFF' # Symbols Extended-A
 r'\U00002702-\U000027B0' # Dingbats
 r'\U000024C2-\U0001F251' # Enclosed characters
 r'\U0001F004' # Mahjong
 r'\U0001F0CF' # Playing Cards
 r'\U0001F170-\U0001F251' # Enclosed
 r']+',
 flags=re.UNICODE
)

# Specific emojis we've been using
SPECIFIC_EMOJIS = ['', '', '', '', '', '', '', '', '', '', 
 '', '', '', '', '', '', '', '', '', '', 
 '', '', '', '', '', '', '', '', '', '',
 '', '', '', '', '', '', '', '', '', '']

def remove_emojis_from_text(text):
 """Remove emojis from text"""
 # Remove specific emojis
 for emoji in SPECIFIC_EMOJIS:
 text = text.replace(emoji, '')
 
 # Remove any remaining emojis using regex
 text = EMOJI_PATTERN.sub('', text)
 
 # Clean up extra spaces
 text = re.sub(r' +', ' ', text)
 text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
 
 return text

def process_file(filepath):
 """Process a single file to remove emojis"""
 try:
 with open(filepath, 'r', encoding='utf-8') as f:
 content = f.read()
 
 original_content = content
 content = remove_emojis_from_text(content)
 
 if content != original_content:
 with open(filepath, 'w', encoding='utf-8') as f:
 f.write(content)
 return True
 return False
 except Exception as e:
 print(f"Error processing {filepath}: {e}")
 return False

def main():
 """Main function to remove emojis from all files"""
 base_dir = Path('.')
 
 # File extensions to process
 extensions = {'.py', '.md', '.txt', '.sh', '.json'}
 
 # Directories to skip
 skip_dirs = {'.git', '__pycache__', 'decompiled', 'extracted', 'irobot_extract', 
 'node_modules', '.venv', 'venv', 'env'}
 
 files_processed = 0
 files_modified = 0
 
 for root, dirs, files in os.walk(base_dir):
 # Skip certain directories
 dirs[:] = [d for d in dirs if d not in skip_dirs]
 
 for file in files:
 filepath = Path(root) / file
 
 # Skip if not in our extension list
 if filepath.suffix not in extensions:
 continue
 
 # Skip if in skip directory
 if any(skip in str(filepath) for skip in skip_dirs):
 continue
 
 files_processed += 1
 if process_file(filepath):
 files_modified += 1
 print(f"Modified: {filepath}")
 
 print(f"\nProcessed: {files_processed} files")
 print(f"Modified: {files_modified} files")
 print("Done!")

if __name__ == "__main__":
 main()

