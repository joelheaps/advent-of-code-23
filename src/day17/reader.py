from pathlib import Path

FILE = Path("input.txt")

with FILE.open("r") as f:
    input_data = f.read()
