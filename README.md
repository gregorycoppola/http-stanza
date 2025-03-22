# HTTP Stanza - Dependency Parser Visualization

A web application that visualizes sentence dependency parsing using spaCy and React. This tool helps users understand the grammatical structure of sentences by displaying interactive dependency parse trees.

## What This App Does

This application takes input text and generates a visual representation of its grammatical structure using dependency parsing. It shows how words in a sentence relate to each other grammatically, including:
- Subject-verb relationships
- Object-verb relationships
- Modifiers and their targets
- Other grammatical relationships between words

The visualization is rendered as an interactive SVG diagram, making it easy to understand sentence structure and grammar.

## Architecture

### Backend (FastAPI + spaCy)
- Built with FastAPI (Python web framework)
- Uses spaCy's English language model (`en_core_web_sm`) for dependency parsing
- Exposes a REST API endpoint at `http://localhost:8000/parse`
- Returns SVG visualization of the dependency parse tree

### Frontend (React)
- Built with React.js
- Provides a simple user interface for text input
- Makes API calls to the backend
- Renders the SVG visualization of the parse tree
- Runs on `http://localhost:3000`

## How to Run

### Prerequisites
- Python 3.7+
- Node.js and npm
- spaCy and its English language model

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn spacy
   ```

3. Download the spaCy English language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will run on `http://localhost:8000`

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will run on `http://localhost:3000`

### Using the Application
1. Open your browser and navigate to `http://localhost:3000`
2. Enter or modify the text in the input field
3. Click the "Parse" button
4. View the generated dependency parse tree visualization

## Example
Try the default example: "The quick brown fox jumps over the lazy dog."

This will generate a visualization showing how each word relates to others in the sentence, with arrows indicating grammatical relationships and labels showing the type of relationship.

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 