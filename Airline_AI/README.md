# Airline AI

Local airline assistant powered by an Ollama-served chat model, a SQLite flight database, and a Gradio chat UI.

## What is in this folder

- `Airline_AI.ipynb` - Main notebook (DB setup, tool definitions, model calls, Gradio UI)
- `create_flight_table.py` - Script to create/populate `flight.db` from JSON
- `flights_data.json` - Seed flight data
- `chatbot/` - Additional notebooks and guide docs

## Prerequisites

- Python (project `pyproject.toml` currently specifies `>=3.14`)
- Jupyter Notebook / JupyterLab
- Ollama installed and available on PATH

Python packages used by this project code:

- `gradio`
- `openai`
- `requests`
- `ipykernel` (for notebook execution)

## Setup

From project root (`d:/Airline_AI`):

1. Install dependencies:

```bash
  pip install gradio openai requests ipykernel
```

2. Build the SQLite database from JSON:

```bash
  python create_flight_table.py
```

3. Start Ollama in a separate terminal:

```bash
  ollama serve
```

4. Pull the model referenced in the notebook (`qwen2.5:7b-instruct`):

```bash
  ollama pull qwen2.5:7b-instruct
```

## Run

Launch the notebook:

```bash
jupyter notebook Airline_AI.ipynb
```

Then run cells top-to-bottom. The final cell launches the Gradio chat app:

- Uses local OpenAI-compatible endpoint: `http://localhost:11434/v1`
- Queries `flight.db` via tool functions

## Notes

- The notebook also includes a `!ollama serve` cell. Prefer running `ollama serve` from a separate terminal to avoid blocking notebook execution.
- If you switch models, update `model_name` in the `chat_with_tools` function cell.
