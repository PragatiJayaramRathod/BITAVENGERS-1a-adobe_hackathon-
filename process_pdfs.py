import fitz  
import json
import os
from pathlib import Path

def extract_title(doc):
    metadata = doc.metadata
    title = metadata.get("title", "").strip()
    if title:
        return title
    page = doc[0]
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["size"] > 14 and "bold" in span["flags"]:  # Heuristic for title
                        return span["text"].strip()
    return "Untitled Document"

def is_heading(span, prev_size, prev_flags):
    size = span["size"]
    flags = span["flags"]
    text = span["text"].strip()
    if len(text) > 100 or not text:
        return None
    if size > 10 and (flags & 16):  
        if size >= prev_size * 1.2:  
            return "H1" if size > 14 else "H2"
        elif size >= prev_size * 0.8:
            return "H2" if size > 12 else "H3"
    return None

def extract_outline(doc):
    outline = []
    prev_size = 10  
    prev_flags = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    heading_level = is_heading(span, prev_size, prev_flags)
                    if heading_level:
                        outline.append({
                            "level": heading_level,
                            "text": span["text"].strip(),
                            "page": page_num + 1
                        })
                        prev_size = span["size"]
                        prev_flags = span["flags"]
    
    return outline

def process_pdf(input_path, output_path):
    doc = fitz.open(input_path)
    title = extract_title(doc)
    outline = extract_outline(doc)
    
    output = {
        "title": title,
        "outline": outline
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    doc.close()

def main():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(exist_ok=True)
    
    for pdf_path in input_dir.glob("*.pdf"):
        output_path = output_dir / f"{pdf_path.stem}.json"
        try:
            process_pdf(pdf_path, output_path)
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")

if __name__ == "__main__":
    main()
