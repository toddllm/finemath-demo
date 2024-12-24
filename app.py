from flask import Flask, render_template, jsonify, request, Response
from datasets import load_dataset
import random
import requests
import json
import re

app = Flask(__name__)

print("Loading FineMath dataset...")
try:
    # Adjust split or dataset name as needed
    dataset = load_dataset("HuggingFaceTB/finemath", "finemath-4plus", split="train[:1000]")
    print(f"Successfully loaded {len(dataset)} samples")
    print(f"First sample: {dataset[0]}")  # Print first sample to verify content
except Exception as e:
    print(f"Error loading dataset: {e}")
    dataset = []

def extract_question(text: str) -> str:
    """Extract a question from text."""
    # Remove markdown headers and clean up
    text = re.sub(r'^#\s+', '', text)
    text = text.replace('\n', ' ').strip()
    
    # Take first substantial chunk of text
    sentences = text.split('.')
    for sentence in sentences:
        clean = sentence.strip()
        if len(clean) > 10:  # Just check it's not empty
            return clean
            
    return text  # If we can't find a good sentence, return the whole thing

def format_question(text: str) -> str:
    """Format a question, preserving any LaTeX if present."""
    # If it already has LaTeX markers, leave it alone
    if '$' in text or '\\[' in text or '\\(' in text:
        return text
    
    # Otherwise just return the text as is
    return text

def stream_ollama(prompt: str):
    """
    Query Ollama API with streaming response.
    We append instructions for Markdown + LaTeX usage to every prompt.
    """
    prompt_with_latex = (
        prompt
        + "\n\nProvide your response using **Markdown** formatting with **LaTeX** math."
        + " Use single $ for inline math and double $$ for display equations.\n"
        + "For example:\n"
        + "- Inline: $x^2$, $\\frac{a}{b}$\n"
        + "- Display: $$\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}$$\n"
        + "Make sure to:\n"
        + "1. Use proper LaTeX escaping for backslashes and special characters\n"
        + "2. Leave no space between $ and the math content\n"
        + "3. Put display equations on their own line\n"
    )

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.3',
                'prompt': prompt_with_latex,
                'stream': True
            },
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                # Each chunk of text is streamed out as JSON
                yield json_response.get('response', '')
                
    except requests.ConnectionError:
        yield "**Error:** Cannot connect to Ollama. Is it running on port 11434?"
    except requests.Timeout:
        yield "**Error:** Ollama request timed out. Try again?"
    except Exception as e:
        yield f"**Error:** {str(e)}"

def create_stream_response(tokens):
    """
    Produce SSE lines. Each line has the JSON of one token chunk:
        data: {"token": "..."}
    """
    for token in tokens:
        # Make sure the token is properly JSON-encoded
        sse_json = json.dumps({"token": token})
        yield f"data: {sse_json}\n\n"

@app.route('/get_question')
def get_question():
    if not dataset:
        return jsonify({'error': 'No dataset loaded'}), 500

    # Just take one random sample and use it
    sample = random.choice(dataset)
    question = extract_question(sample['text'])
    formatted = format_question(question)
    return jsonify({'question': formatted})

# Update home route to just return the template
@app.route('/')
def home():
    return render_template('index.html', question="Loading question...")

@app.route('/get_hint', methods=['POST'])
def get_hint():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
        
    prompt = (
        "You are a helpful math tutor. Give a small hint for solving this problem, "
        "without giving away the full solution:\n\n"
        f"{question}\n\n"
        "Provide just one helpful hint that guides the student toward the solution."
    )

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    question = request.json.get('question')
    user_answer = request.json.get('answer')
    
    if not question or not user_answer:
        return jsonify({'error': 'Missing question or answer'}), 400
        
    prompt = (
        "You are a helpful math tutor. Check if this answer is correct:\n\n"
        f"Question: {question}\n"
        f"Student's answer: {user_answer}\n\n"
        "Provide encouraging feedback, whether right or wrong. "
        "If wrong, give a gentle hint."
    )

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    context = request.json.get('context')
    user_question = request.json.get('question')
    
    if not context or not user_question:
        return jsonify({'error': 'Missing context or question'}), 400
        
    prompt = (
        "You are a helpful math tutor. Answer this specific question:\n\n"
        f"Problem: {context}\n"
        f"Student's question: {user_question}\n\n"
        "Give a clear, helpful response that guides without giving away the complete solution."
    )

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

@app.route('/get_solution', methods=['POST'])
def get_solution():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
        
    prompt = (
        "You are a helpful math tutor. Please provide a complete, detailed solution:\n\n"
        f"{question}\n\n"
        "Show all steps and explain each one clearly."
    )

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

if __name__ == '__main__':
    if not dataset:
        print("Error: Could not load dataset. Please check your internet connection and try again.")
        exit(1)
    # Run on port 5000 or whichever you prefer
    app.run(debug=True, port=5000)