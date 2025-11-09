#!/usr/bin/env python3
"""
file_handling_demo.py

Demonstrates common file operations in Python with safe patterns.
Run: python file_handling_demo.py
"""

from pathlib import Path
import json
import csv
import os

BASE_DIR = Path("demo_files")  # all demo files will be created inside this folder
BASE_DIR.mkdir(exist_ok=True)

# 1) WRITE a simple text file (mode 'w' — overwrites if exists)
txt_path = BASE_DIR / "example.txt"
with txt_path.open("w", encoding="utf-8") as f:
    f.write("Line 1: Hello, file handling!\n")
    f.write("Line 2: This file demonstrates writing and reading.\n")
print(f"Wrote text file: {txt_path}")

# 2) APPEND to the same file (mode 'a')
with txt_path.open("a", encoding="utf-8") as f:
    f.write("Appended Line 3: This was appended later.\n")
print("Appended a line.")

# 3) READ the entire file at once (mode 'r')
with txt_path.open("r", encoding="utf-8") as f:
    content = f.read()
print("\n--- Full file content ---")
print(content.strip())   # .strip() to avoid extra trailing newline in display

# 4) READ LINE-BY-LINE (iterator)
print("\n--- Read line-by-line ---")
with txt_path.open("r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"Line {i}: {line.rstrip()}")

# 5) READ into a list of lines
with txt_path.open("r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"\nRead {len(lines)} lines (using readlines()).")

# 6) CREATE a file only if it doesn't exist (mode 'x')
try:
    new_path = BASE_DIR / "created_once.txt"
    with new_path.open("x", encoding="utf-8") as f:
        f.write("This file was created with mode 'x'.\n")
    print(f"Created new file: {new_path}")
except FileExistsError:
    print(f"File already exists, not overwriting: {new_path}")

# 7) BINARY I/O (write and read bytes)
bin_path = BASE_DIR / "data.bin"
data_bytes = b"\x00\x01\x02\xFFhello\n"
with bin_path.open("wb") as bf:
    bf.write(data_bytes)
print(f"Wrote binary file: {bin_path}")

with bin_path.open("rb") as bf:
    b = bf.read()
print("Read binary content:", b)

# 8) JSON example (structured data)
json_path = BASE_DIR / "data.json"
sample = {"name": "Alice", "age": 30, "skills": ["python", "file I/O", "data"]}

# Write human-readable JSON
with json_path.open("w", encoding="utf-8") as jf:
    json.dump(sample, jf, ensure_ascii=False, indent=2)

# Read JSON back
with json_path.open("r", encoding="utf-8") as jf:
    obj = json.load(jf)
print("\nJSON loaded:", obj)

# 9) CSV example (using csv module)
csv_path = BASE_DIR / "people.csv"
rows = [
    ["name", "age", "city"],
    ["Alice", "30", "Coimbatore"],
    ["Bob", "28", "Chennai"],
]

with csv_path.open("w", newline='', encoding="utf-8") as cf:
    writer = csv.writer(cf)
    writer.writerows(rows)
print(f"CSV written: {csv_path}")

with csv_path.open("r", encoding="utf-8") as cf:
    reader = csv.reader(cf)
    print("\nCSV content:")
    for r in reader:
        print(r)

# 10) SAFE rename and delete (use pathlib/os)
renamed = BASE_DIR / "people_renamed.csv"
try:
    csv_path.replace(renamed)  # atomic on many OSes
    print(f"Renamed {csv_path.name} -> {renamed.name}")
except Exception as e:
    print("Rename failed:", e)

# Delete a file
tmp_to_delete = BASE_DIR / "created_once.txt"
if tmp_to_delete.exists():
    tmp_to_delete.unlink()
    print(f"Deleted file: {tmp_to_delete}")

# 11) CHECK file properties
for p in [txt_path, bin_path, json_path, renamed]:
    print(f"{p.name}: exists={p.exists()}, size={p.stat().st_size} bytes")

# 12) EXAMPLE error handling when reading a non-existent file
missing = BASE_DIR / "does_not_exist.txt"
try:
    with missing.open("r", encoding="utf-8") as f:
        f.read()
except FileNotFoundError:
    print(f"Handled missing file error for: {missing}")

# 13) Using Path.write_text / read_text convenience helpers
quick_path = BASE_DIR / "quick.txt"
quick_path.write_text("Quick text using Path.write_text()\n", encoding="utf-8")
print("quick.txt content:", quick_path.read_text(encoding="utf-8").strip())

print("\nDemo complete. Check the 'demo_files' folder for created files.")
