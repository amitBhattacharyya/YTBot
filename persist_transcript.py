from pathlib import Path

#!/usr/bin/env python3

def save_text_to_file(text: str, filename: str, encoding: str = "utf-8") -> None:
    path = Path(filename)
    if path.parent:
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=encoding)

def read_text_from_file(filename: str, encoding: str = "utf-8") -> str:    
    try:
        return Path(filename).read_text(encoding=encoding)
    except FileNotFoundError:
        return ""
    

