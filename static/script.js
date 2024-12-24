// Initialize markdown-it with KaTeX support
const md = window.markdownit()
    .use(texmath, {
        engine: katex,
        delimiters: ['dollars', 'brackets'],
        katexOptions: { macros: { "\\RR": "\\mathbb{R}" } }
    });

// Global error handler
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// Unified markdown rendering function
function renderMarkdown(text) {
    try {
        return md.render(text);
    } catch (e) {
        console.error('Error rendering markdown:', e);
        return text;
    }
}

// Unified stream handling function
function handleStream(response, outputElement, loadingElement) {
    const reader = response.body.getReader();
    let buffer = '';

    loadingElement.style.display = 'block';
    outputElement.innerHTML = '';

    reader.read().then(function processResult(result) {
        if (result.done) {
            if (buffer.trim()) {
                outputElement.innerHTML = renderMarkdown(buffer);
            }
            loadingElement.style.display = 'none';
            return;
        }

        const chunk = new TextDecoder().decode(result.value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
            if (line.startsWith('data: ')) {
                try {
                    const data = JSON.parse(line.slice(5));
                    buffer += data.token;
                    outputElement.innerHTML = renderMarkdown(buffer);
                } catch (e) {
                    console.error('Error parsing JSON:', e);
                }
            }
        }

        return reader.read().then(processResult);
    }).catch(error => {
        showError('Error reading stream: ' + error.message);
        loadingElement.style.display = 'none';
    });
}

// Unified fetch function for all endpoints
async function fetchEndpoint(endpoint, data, outputElement, loadingElement) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('Network response was not ok');
        handleStream(response, outputElement, loadingElement);

    } catch (error) {
        showError('Error: ' + error.message);
        if (loadingElement) loadingElement.style.display = 'none';
    }
}

// Handler functions for each action
async function askQuestion() {
    // Get question text without HTML tags
    const question = document.getElementById('question').innerText;
    const userQuestion = document.getElementById('user-question').value;
    
    if (!userQuestion.trim()) {
        showError('Please enter a question');
        return;
    }
    
    fetchEndpoint(
        '/ask_question',
        { context: question, question: userQuestion },
        document.getElementById('llm-response'),
        document.getElementById('question-loading')
    );
}

async function getHint() {
    const question = document.getElementById('question').textContent;
    
    fetchEndpoint(
        '/get_hint',
        { question },
        document.getElementById('hint-text'),
        document.getElementById('hint-loading')
    );
}

async function checkAnswer() {
    const question = document.getElementById('question').innerText;
    const mathField = MQ.MathField(document.querySelector('#math-input'));
    const answer = mathField.latex();
    
    if (!answer.trim()) {
        showError('Please enter an answer');
        return;
    }
    
    fetchEndpoint(
        '/check_answer',
        { question, answer },
        document.getElementById('feedback'),
        document.getElementById('check-loading')
    );
}

async function showFullSolution() {
    const question = document.getElementById('question').innerText;
    const answerDiv = document.getElementById('answer');
    
    answerDiv.style.display = 'block';
    
    fetchEndpoint(
        '/get_solution',
        { question },
        answerDiv,
        document.getElementById('solution-loading')
    );
}

// MathQuill initialization
const MQ = MathQuill.getInterface(2);
let mathField; // Global reference to the math field

document.addEventListener('DOMContentLoaded', function() {
    const mathInput = document.querySelector('#math-input');
    if (mathInput) {
        mathField = MQ.MathField(mathInput, {
            spaceBehavesLikeTab: true,
            handlers: {
                enter: () => checkAnswer()
            },
            autoCommands: 'pi theta sqrt sum int',
            autoOperatorNames: 'sin cos tan'
        });
    }
});

// Math symbol insertion
function insertSymbol(symbol) {
    if (!mathField) return;
    
    // Map of special commands that need different handling
    const symbolMap = {
        '\\sqrt{}': () => {
            mathField.cmd('\\sqrt');
            mathField.typedText(' ');
        },
        '\\frac{}{}': () => {
            mathField.cmd('\\frac');
            mathField.typedText(' ');
        },
        '^{}': () => {
            mathField.cmd('^');
            mathField.typedText(' ');
        },
        '\\sum_{}': () => {
            mathField.cmd('\\sum');
            mathField.cmd('_');
            mathField.typedText(' ');
        },
        '\\int_{}': () => {
            mathField.cmd('\\int');
            mathField.cmd('_');
            mathField.typedText(' ');
        }
    };

    if (symbolMap[symbol]) {
        symbolMap[symbol]();
    } else {
        mathField.cmd(symbol);
    }
    mathField.focus();
}

// Theme toggling
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    document.documentElement.classList.toggle('dark-mode');
    const button = document.getElementById('theme-toggle');
    button.textContent = document.body.classList.contains('dark-mode') ? '🌞' : '🌙';
}

// New question loading
async function newQuestion() {
    const questionElement = document.getElementById('question');
    const answerDiv = document.getElementById('answer');
    const feedbackDiv = document.getElementById('feedback');
    const hintDiv = document.getElementById('hint-text');
    const responseDiv = document.getElementById('llm-response');
    const mathField = MQ.MathField(document.querySelector('#math-input'));
    
    questionElement.classList.add('loading-question');
    answerDiv.style.display = 'none';
    feedbackDiv.innerHTML = '';
    hintDiv.innerHTML = '';
    responseDiv.innerHTML = '';
    mathField.latex('');
    
    try {
        const response = await fetch('/get_question');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        // Apply markdown/LaTeX rendering to the question
        questionElement.innerHTML = renderMarkdown(data.question);
        questionElement.classList.remove('loading-question');
        
    } catch (error) {
        showError('Error loading new question: ' + error.message);
        questionElement.classList.remove('loading-question');
    }
}

// Load initial question on page load
document.addEventListener('DOMContentLoaded', () => {
    newQuestion();
});