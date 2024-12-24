# FineMath Learning Assistant Demo

An interactive math learning assistant that uses the FineMath dataset and a local LLM through Ollama to provide personalized math tutoring.

## Prerequisites

1. Python 3.8 or higher
2. Ollama (for local LLM support)
3. At least 8GB RAM (recommended 16GB+ for larger models)
4. About 42GB free disk space for the LLM model

## Installation

### 1. Install Python Dependencies
```bash
pip install flask datasets requests
```

### 2. Install Ollama
Follow instructions at [Ollama's installation guide](https://ollama.ai/download):

**MacOS**:
```bash
curl https://ollama.ai/install.sh | sh
```

**Linux**:
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows**:
- Use WSL2 and follow Linux instructions, or
- Use Docker Desktop

### 3. Download Required LLM Model
```bash
ollama pull llama3.3
```

## Running the Application

1. Start Ollama server:
```bash
ollama serve
```

2. In a new terminal, run the Flask application:
```bash
python3 app.py
```

3. Open your web browser and go to:
```
http://localhost:5000
```

## Features

- Interactive math problems from the FineMath dataset
- Real-time answer checking with personalized feedback
- Step-by-step solution guidance
- Hint system
- Custom question answering
- Work area for showing your steps
- Streaming responses for immediate feedback

## Troubleshooting

1. If you get "Connection refused" errors:
   - Ensure Ollama is running (`ollama serve`)
   - Check it's accessible at `http://localhost:11434`

2. If responses are slow:
   - This is normal for the first few queries as the model loads
   - Subsequent queries should be faster

3. If you get memory errors:
   - Close other applications
   - Consider using a smaller model
   - Ensure your system meets the minimum requirements

## Dataset Attribution

This project uses the FineMath dataset:
- Source: HuggingFace Hub (HuggingFaceTB/finemath)
- License: ODC-By 1.0
- [Dataset Link](https://huggingface.co/datasets/HuggingFaceTB/finemath)

## Model Attribution

Uses Llama 3.3 through Ollama. Ensure you comply with the model's license terms.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
