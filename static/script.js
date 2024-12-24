// Initialize markdown-it and functions for LaTeX rendering
let md; // We'll initialize this after DOM loads

// Dark mode toggle function
function toggleDarkMode() {
    const body = document.body;
    const button = document.getElementById('theme-toggle');
    const isDark = body.classList.toggle('dark-mode');
    button.textContent = isDark ? '🌞' : '🌙';
    localStorage.setItem('darkMode', isDark);
}

// Generic streaming function for server-sent events
async function streamResponse(url, data, responseElement, loadingElement) {
    loadingElement.style.display = 'block';
    responseElement.textContent = '';
    responseElement.classList.add('typing-indicator');

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let accumulatedText = '';
        let leftover = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            leftover += decoder.decode(value, { stream: true });
            const lines = leftover.split('\n');
            leftover = lines.pop() || '';

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                
                let raw = line.slice(6).trim();
                if (!raw) continue;

                try {
                    const sseData = JSON.parse(raw);
                    accumulatedText += sseData.token;
                    responseElement.innerHTML = md.render(accumulatedText);
                } catch (err) {
                    console.warn('Skipping malformed SSE line:', line);
                }
            }
        }
    } catch (error) {
        responseElement.innerHTML = md.render(`**Error:** ${error}`);
    } finally {
        loadingElement.style.display = 'none';
        responseElement.classList.remove('typing-indicator');
    }
}

// UI interaction functions
async function checkAnswer() {
    const userAnswer = document.getElementById('user-answer').value;
    const questionText = document.getElementById('question').textContent;
    
    await streamResponse(
        '/check_answer',
        { question: questionText, answer: userAnswer },
        document.getElementById('feedback'),
        document.getElementById('check-loading')
    );
}

async function getHint() {
    const questionText = document.getElementById('question').textContent;
    await streamResponse(
        '/get_hint',
        { question: questionText },
        document.getElementById('hint-text'),
        document.getElementById('hint-loading')
    );
    document.getElementById('hint-text').style.display = 'block';
}

async function askQuestion() {
    const userQuestion = document.getElementById('user-question').value.trim();
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = '';

    if (!userQuestion) {
        errorDiv.textContent = 'Please enter a question first';
        return;
    }

    const questionText = document.getElementById('question').textContent;
    await streamResponse(
        '/ask_question',
        { context: questionText, question: userQuestion },
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
        { question: questionText },
        solutionArea,
        document.getElementById('solution-loading')
    );
}

// Initialize everything after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    // Set initial dark mode state
    document.body.classList.add('dark-mode');
    document.getElementById('theme-toggle').textContent = '🌞';
    localStorage.setItem('darkMode', true);

    // Initialize markdown-it with KaTeX
    const tm = texmath.use(katex);
    md = markdownit({
        html: true,
        linkify: true,
        typographer: true,
        breaks: true,
        highlight: function (str, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(str, { language: lang }).value;
                } catch (__) {}
            }
            return '';
        }
    }).use(tm, {
        engine: katex,
        delimiters: 'dollars',
        katexOptions: { 
            macros: {
                "\\RR": "\\mathbb{R}",
                "\\NN": "\\mathbb{N}",
                "\\ZZ": "\\mathbb{Z}"
            },
            throwOnError: false
        }
    });
});