# FineMath Learning Assistant

An **interactive math learning assistant** that uses the **FineMath** dataset and a **local LLM** (through [Ollama](https://ollama.ai/)) to provide personalized math tutoring. This application supports step-by-step learning, hints, custom questions, and a LaTeX-compatible input area.

> **Note:** The default model has been switched to a **smaller, more performant model** ([SmolLM2-1.7B](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B)) for quicker response times on most systems. If your machine has more resources, you can still opt to use a larger LLM model by updating the `model` parameter in the code (see [Installation](#installation) section below).

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
   - [1. Install Python Dependencies](#1-install-python-dependencies)  
   - [2. Install Ollama](#2-install-ollama)  
   - [3. Download the Default Model (SmolLM2-1.7B)](#3-download-the-default-model-smollm2-17b)  
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
3. **At least 4GB+ RAM** (8GB or more recommended for best performance with SmolLM2-1.7B)  
4. **~15GB free disk space** for the default model  

> If you plan to use a larger LLM (like Llama 3.3 or others), you may need **16GB+ RAM** and **40GB+ free disk space**.

---

## Installation

### 1. Install Python Dependencies

```
pip install flask datasets requests
```

### 2. Install Ollama

Follow instructions at [Ollama's installation guide](https://ollama.ai/download).

**MacOS**:

```
curl https://ollama.ai/install.sh | sh
```

**Linux**:

```
curl https://ollama.ai/install.sh | sh
```

**Windows**:
- Use WSL2 and follow Linux instructions, **or**
- Use Docker Desktop

### 3. Download the Default Model (SmolLM2-1.7B)

Pull the smaller model from Ollama’s local registry:

```
ollama pull smollm2
```

**Optional:**

If you’d like to use a larger model (e.g., `llama3.3`), simply change the `"model": "smollm2"` line in `app.py` to `"model": "llama3.3"` (or another model name) and pull that model:

```
ollama pull llama3.3
```

Then follow the same steps below to run the application.

---

## Running the Application

1. **Start Ollama server** in one terminal:

```
ollama serve
```

2. **In a new terminal**, run the Flask application:

```
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

```
ollama serve
```

   - Check it’s accessible at `http://localhost:11434`.

2. **Slow responses**:
   - Normal for the first few queries while the model loads. Subsequent queries should be faster.
   - Try using a smaller model (like `smollm2`) if you haven't already.

3. **Memory errors**:
   - Close other applications or try a smaller model like `smollm2`.
   - Ensure your system meets the minimum requirements.

4. **Dataset not loading**:
   - Verify your internet connection.
   - Check that Hugging Face is accessible from your environment.

---

## Dataset Attribution

This project uses the **FineMath** dataset:

- **Source:** [HuggingFaceTB/finemath](https://huggingface.co/datasets/HuggingFaceTB/finemath)  
- **License:** ODC-By 1.0

---

## Model Attribution

- **Default Model:** [SmolLM2-1.7B](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B) via Ollama.  
- **Optional Larger Model:** Llama 3.3 or others from [Ollama's Registry](https://ollama.ai/).

Be sure to comply with the respective model licenses for any models you download or use.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
