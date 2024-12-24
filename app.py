from flask import Flask, render_template_string, jsonify, request, Response
from datasets import load_dataset
import random
import requests
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Math Learning Assistant</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 2rem auto; 
            padding: 0 1rem; 
        }
        .question, .answer, .work-area, .hint-area { 
            padding: 1rem; 
            margin: 1rem 0; 
            border-radius: 4px; 
        }
        .question { background-color: #f0f0f0; }
        .answer { background-color: #e3f2fd; display: none; }
        .hint-area { background-color: #e8f5e9; }
        .work-area { background-color: #fff3e0; }
        button { 
            padding: 0.5rem 1rem; 
            margin: 0.5rem;
            cursor: pointer;
        }
        .loading { 
            display: none; 
            color: #666;
            margin: 0.5rem 0;
            font-style: italic;
        }
        textarea {
            width: 100%;
            min-height: 100px;
            margin: 0.5rem 0;
            padding: 0.5rem;
        }
        .input-area {
            margin: 1rem 0;
        }
        .error {
            color: #d32f2f;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        .button-group {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        #checkAnswer {
            background-color: #4caf50;
            color: white;
            border: none;
        }
        .response-area {
            margin-top: 0.5rem;
            min-height: 1em;
        }
        .typing-indicator::after {
            content: '▋';
            animation: blink 1s infinite;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }
    </style>
    <script>
        async function streamResponse(url, data, responseElement, loadingElement) {
            loadingElement.style.display = 'block';
            responseElement.textContent = '';
            responseElement.classList.add('typing-indicator');
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                
                while (true) {
                    const {value, done} = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value);
                    const lines = chunk.split('\\n');
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = JSON.parse(line.slice(6));
                            responseElement.textContent += data.token;
                        }
                    }
                }
            } catch (error) {
                responseElement.textContent = 'Error: ' + error;
            } finally {
                loadingElement.style.display = 'none';
                responseElement.classList.remove('typing-indicator');
            }
        }

        async function checkAnswer() {
            const userAnswer = document.getElementById('user-answer').value;
            const questionText = document.getElementById('question').textContent;
            
            await streamResponse(
                '/check_answer',
                {
                    question: questionText,
                    answer: userAnswer
                },
                document.getElementById('feedback'),
                document.getElementById('check-loading')
            );
        }

        async function getHint() {
            const questionText = document.getElementById('question').textContent;
            
            await streamResponse(
                '/get_hint',
                {question: questionText},
                document.getElementById('hint-text'),
                document.getElementById('hint-loading')
            );
            
            document.getElementById('hint-text').style.display = 'block';
        }

        async function askQuestion() {
            const userQuestion = document.getElementById('user-question').value;
            if (!userQuestion.trim()) {
                document.getElementById('error').textContent = 'Please enter a question first';
                return;
            }
            
            const questionText = document.getElementById('question').textContent;
            
            await streamResponse(
                '/ask_question',
                {
                    context: questionText,
                    question: userQuestion
                },
                document.getElementById('llm-response'),
                document.getElementById('question-loading')
            );
        }

        async function showFullSolution() {
            const questionText = document.getElementById('question').textContent;
            const solutionArea = document.getElementById('answer');
            
            solutionArea.style.display = 'block';
            
            await streamResponse(
                '/get_solution',
                {question: questionText},
                solutionArea,
                document.getElementById('solution-loading')
            );
        }
    </script>
</head>
<body>
    <h1>Math Learning Assistant</h1>
    
    <div class="question">
        <h3>Question:</h3>
        <p id="question">{{ question }}</p>
    </div>

    <div class="input-area">
        <h3>Your Answer:</h3>
        <input type="text" id="user-answer" placeholder="Enter your answer here..." style="padding: 0.5rem; width: 200px;">
        <button onclick="checkAnswer()" id="checkAnswer">Check Answer</button>
        <div id="check-loading" class="loading">Teacher is reviewing your answer...</div>
        <div id="feedback" class="response-area"></div>
    </div>

    <div class="work-area">
        <h3>Your Work:</h3>
        <textarea placeholder="Work out your solution here..."></textarea>
    </div>

    <div class="hint-area">
        <h3>Need Help?</h3>
        <button onclick="getHint()">Get Hint</button>
        <div id="hint-loading" class="loading">Teacher is writing a hint...</div>
        <div id="hint-text" class="response-area"></div>
        
        <h4>Ask a Specific Question:</h4>
        <textarea id="user-question" placeholder="E.g., 'How do I start solving this?' or 'Can you explain the first step?'"></textarea>
        <button onclick="askQuestion()">Ask</button>
        <div id="question-loading" class="loading">Teacher is typing...</div>
        <div id="llm-response" class="response-area"></div>
    </div>

    <div id="error" class="error"></div>
    <div id="solution-loading" class="loading">Teacher is writing the complete solution...</div>
    <div class="answer" id="answer"></div>
    
    <div class="button-group">
        <button onclick="window.location.reload()">New Question</button>
        <button onclick="showFullSolution()">Show Full Solution</button>
    </div>
</body>
</html>
"""

print("Loading FineMath dataset...")
try:
    dataset = load_dataset("HuggingFaceTB/finemath", "finemath-4plus", split="train[:1000]")
    print(f"Loaded {len(dataset)} samples")
except Exception as e:
    print(f"Error loading dataset: {e}")
    dataset = []

def extract_question(text: str) -> str:
    """Extract a math question from text, looking for common patterns"""
    markers = ["Problem:", "Question:", "Find:", "Solve:", "Calculate:"]
    
    for marker in markers:
        if marker in text:
            parts = text.split(marker)
            if len(parts) > 1:
                question_part = parts[1].split("\n")[0].strip()
                if len(question_part) > 10 and len(question_part) < 500:
                    return question_part
    
    # Fallback: take first paragraph if it looks like a question
    first_para = text.split("\n")[0].strip()
    if len(first_para) > 10 and len(first_para) < 500 and ("?" in first_para or "=" in first_para):
        return first_para
        
    return None

def stream_ollama(prompt: str):
    """Query Ollama API with streaming response"""
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.3',
                'prompt': prompt,
                'stream': True
            },
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                yield json_response.get('response', '')
                
    except requests.ConnectionError:
        yield "Error: Cannot connect to Ollama. Is it running on port 11434?"
    except requests.Timeout:
        yield "Error: Ollama request timed out. Try again?"
    except Exception as e:
        yield f"Error querying Ollama: {str(e)}"

def create_stream_response(tokens):
    """Helper function to create a stream response"""
    for token in tokens:
        yield f"data: {json.dumps({'token': token})}\n\n"

@app.route('/')
def home():
    for _ in range(10):  # Try up to 10 times to get a good question
        sample = random.choice(dataset)
        question = extract_question(sample['text'])
        if question:
            return render_template_string(HTML_TEMPLATE, question=question)
    
    return render_template_string(HTML_TEMPLATE, 
                                question="Error: Could not find a suitable question")

@app.route('/get_hint', methods=['POST'])
def get_hint():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
        
    prompt = f"""You are a helpful math tutor. Give a small hint for solving this problem, 
    without giving away the full solution:

    {question}

    Provide just one helpful hint that guides the student toward the solution."""

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    question = request.json.get('question')
    user_answer = request.json.get('answer')
    
    if not question or not user_answer:
        return jsonify({'error': 'Missing question or answer'}), 400
        
    prompt = f"""You are a helpful math tutor. Check if this answer is correct:

    Question: {question}
    Student's answer: {user_answer}

    Provide encouraging feedback, whether right or wrong. If wrong, give a gentle hint."""

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    context = request.json.get('context')
    user_question = request.json.get('question')
    
    if not context or not user_question:
        return jsonify({'error': 'Missing context or question'}), 400
        
    prompt = f"""You are a helpful math tutor. Answer this specific question:

    Problem: {context}
    Student's question: {user_question}

    Give a clear, helpful response that guides without giving away the complete solution."""

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

@app.route('/get_solution', methods=['POST'])
def get_solution():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
        
    prompt = f"""You are a helpful math tutor. Please provide a complete, detailed solution:

    {question}

    Show all steps and explain each one clearly."""

    return Response(create_stream_response(stream_ollama(prompt)), mimetype='text/event-stream')

if __name__ == '__main__':
    if not dataset:
        print("Error: Could not load dataset. Please check your internet connection and try again.")
        exit(1)
        
    app.run(debug=True, port=5000)