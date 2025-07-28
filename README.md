**Adobe India Hackathon 2025 - Round 1A Solution**

Overview
This repository contains the solution for Round 1A: Understand Your Document of the Adobe India Hackathon 2025, part of the "Connecting the Dots" challenge. The goal is to extract a structured outline (Title, H1, H2, H3 headings with page numbers) from PDF files and output it as JSON, running in a Docker container on AMD64 architecture without internet access. The solution is designed to be efficient, accurate, and reusable for subsequent rounds.
Approach
The solution leverages PyMuPDF (fitz), a lightweight and efficient Python library for PDF parsing, to extract text and metadata from PDFs. The approach is modular and avoids reliance on font size alone for heading detection, ensuring robustness across diverse PDF layouts. Key components include:

Title Extraction:

Extracts the document title from PDF metadata (/Title field).
Falls back to the first prominent text (large font size, bold) on page 1 if metadata is unavailable.
Handles cases where metadata is missing or incomplete.


Heading Detection:

Uses a heuristic-based approach to classify headings (H1, H2, H3) based on:
Font size: Larger sizes indicate higher-level headings (H1 > H2 > H3).
Boldness: Headings are typically bold (detected via PyMuPDF’s text flags).
Text length: Headings are short (<100 characters) to avoid misclassifying paragraphs.
Hierarchy: Ensures H2 follows H1, and H3 follows H2, by comparing relative font sizes.


Avoids font-size-only assumptions by combining multiple properties (e.g., position, flags).
Processes text blocks page-by-page to associate headings with correct page numbers.


Multilingual Support:

Handles Unicode text to support languages like Japanese, ensuring accurate extraction of non-Latin characters.
Uses json.dump with ensure_ascii=False to preserve Unicode in the output JSON.


Output Generation:

Produces JSON files in the specified format for each input PDF:{
  "title": "Understanding AI",
  "outline": 
  [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}


Processes all PDFs in the /app/input directory and saves corresponding JSON files in /app/output.


Performance Optimization:

Optimized to process 50-page PDFs in ≤ 10 seconds on an 8-CPU, 16GB RAM system.
Uses efficient text extraction with PyMuPDF’s "dict" output to minimize processing overhead.
Keeps dependencies lightweight (PyMuPDF ~50MB, well within the 200MB limit).


Docker Compatibility:

Runs in a python:3.9-slim Docker container for AMD64 architecture.
Operates offline with --network none, as required.
Mounts /app/input and /app/output for file I/O.



Dependencies

PyMuPDF (1.23.6): A lightweight (~50MB) Python library for PDF parsing, used for text and metadata extraction.
No external models, API calls, or internet access required, ensuring compliance with hackathon constraints.

Directory Structure
BITAVENGERS-1a-adobe_hackathon/
├── Dockerfile
├── README.md
├── requirements.txt
├── process_pdfs.py


Dockerfile: Defines the Docker image for AMD64, installs dependencies, and sets up the execution environment.
README.md: This file, documenting the solution and instructions.
requirements.txt: Lists dependencies (PyMuPDF==1.23.6).
process_pdfs.py: Main script to process PDFs and generate JSON outlines.

How to Build and Run
Follow these steps to build and run the solution:
Prerequisites

Docker: Install Docker Desktop (or Docker CLI for Linux) from docker.com.
Test PDFs: Place input PDFs (e.g., sample.pdf) in an input directory for testing.

Build the Docker Image

Navigate to the project directory:cd path/to/BITAVENGERS-1a-adobe_hackathon


Build the Docker image:docker build --platform linux/amd64 -t pdf-outline-extractor:v1 .


--platform linux/amd64: Ensures compatibility with AMD64 architecture.
-t pdf-outline-extractor:v1: Names the image pdf-outline-extractor with tag v1.
.: Specifies the current directory containing the Dockerfile.



Run the Docker Container

Create input and output directories:mkdir input output


Place test PDFs in the input directory.
Run the container:docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app


