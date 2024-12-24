


# FineMath Learning Assistant

An **interactive math learning assistant** that uses the **FineMath** dataset and a **local LLM** (through [Ollama](https://ollama.ai/)) to provide personalized math tutoring. This application supports step-by-step learning, hints, custom questions, and a LaTeX-compatible input area.

---

## Table of Contents
1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
   - [1. Install Python Dependencies](#1-install-python-dependencies)  
   - [2. Install Ollama](#2-install-ollama)  
   - [3. Download Required LLM Model](#3-download-required-llm-model)  
4. [Running the Application](#running-the-application)  
5. [Using the App](#using-the-app)  
   - [1. Viewing and Answering Questions](#1-viewing-and-answering-questions)  
   - [2. Checking Your Answer](#2-checking-your-answer)  
   - [3. Getting Hints](#3-getting-hints)  
   - [4. Asking a Custom Question](#4-asking-a-custom-question)  
   - [5. Showing the Full Solution](#5-showing-the-full-solution)  
   - [6. Switching Dark/Light Mode](#6-switching-darklight-mode)  
6. [Troubleshooting](#troubleshooting)  
7. [Dataset Attribution](#dataset-attribution)  
8. [Model Attribution](#model-attribution)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## Features

- **Interactive math problems** from the FineMath dataset  
- **MathQuill input** for entering answers in LaTeX-like notation  
- **Real-time answer checking** with personalized feedback  
- **Step-by-step solution guidance** and hints  
- **Custom question answering** on any part of the problem  
- **Streaming responses** for immediate feedback  
- **Dark/Light mode toggle** for comfortable reading

---

## Prerequisites

1. **Python 3.8 or higher**  
2. **Ollama** (for local LLM support)  
3. **At least 8GB RAM** (16GB+ recommended for larger models)  
4. **~42GB free disk space** for the LLM model

---

## Installation

### 1. Install Python Dependencies
```bash
pip install flask datasets requests
```

### 2. Install Ollama
Follow instructions at [Ollama's installation guide](https://ollama.ai/download).

**MacOS**:
```bash
curl https://ollama.ai/install.sh | sh
```

**Linux**:
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows**:
- Use WSL2 and follow Linux instructions, **or**
- Use Docker Desktop

### 3. Download Required LLM Model
```bash
ollama pull llama3.3
```

---

## Running the Application

1. **Start Ollama server** in one terminal:
   ```bash
   ollama serve
   ```

2. **In a new terminal**, run the Flask application:
   ```bash
   python3 app.py
   ```

3. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

---

## Using the App

Below is a quick guide to the main sections you’ll see upon visiting `http://localhost:5000`:

### 1. Viewing and Answering Questions
- The app will load a **random math question** from the FineMath dataset upon page load.  
- The question appears in a gray box near the top. If you want a new question, click the **"New Question"** button.

### 2. Checking Your Answer
- **Enter your answer** in the **"Your Answer"** field. A LaTeX-compatible MathQuill editor is provided with common math symbols for convenience.  
- Click **"Check Answer"**. A loading indicator appears, and then feedback will stream in.  
- You’ll see whether you’re correct, plus some gentle guidance if not.

### 3. Getting Hints
- If you’re stuck, scroll down to the **"Need Help?"** section.  
- Click **"Get Hint"** to request a clue about how to solve the current problem **without** revealing the full solution.  
- The hint will appear beneath the loading indicator.

### 4. Asking a Custom Question
- Use the **"Ask a Specific Question"** area if you’d like to clarify a specific step or concept.  
- Type your question (e.g., “Can you explain the first step?”) in the text box and click **"Ask"**.  
- The tutor will provide a targeted response or explanation.

### 5. Showing the Full Solution
- When you’re ready to see how it’s done, click **"Show Full Solution"**.  
- A detailed, step-by-step solution will appear, including LaTeX-formatted equations.

### 6. Switching Dark/Light Mode
- By default, the page starts in **dark mode**.  
- Click the **sun/moon icon** in the top-right corner to toggle between dark and light modes.

---

## Troubleshooting

1. **"Connection refused" errors**:
   - Ensure Ollama is running:  
     ```bash
     ollama serve
     ```
   - Check it’s accessible at `http://localhost:11434`.

2. **Slow responses**:
   - Normal for the first few queries while the model loads. Subsequent queries should be faster.

3. **Memory errors**:
   - Close other applications or try a smaller model.
   - Ensure your system meets the minimum requirements.

4. **Dataset not loading**:
   - Verify your internet connection.
   - Check that Hugging Face is accessible from your environment.

---

## Dataset Attribution

This project uses the **FineMath** dataset:

- **Source:** HuggingFace Hub ([HuggingFaceTB/finemath](https://huggingface.co/datasets/HuggingFaceTB/finemath))  
- **License:** ODC-By 1.0

---

## Model Attribution

Uses **Llama 3.3** through [Ollama](https://ollama.ai/). Ensure you comply with the model’s license terms.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
