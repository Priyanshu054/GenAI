# GenAI Repository

A personal repository for experimenting with Generative AI integrations, notebooks, chatbots, and mini projects.

## Prerequisites

- Python (see `pyproject.toml` for the currently configured minimum version)
- VS Code + Jupyter extension (for notebook workflows)
- Ollama (optional, for local model inference)

## Setup (Option A: `uv`)

If you have `uv` installed, this is the quickest way to create an environment and install deps.

```powershell
uv --version
uv sync
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Setup (Option B: `venv` + `pip`)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e .
```

## Environment variables

Keep API keys in environment variables or a local `.env` file (do not commit secrets). Common examples:

```text
OPENAI_API_KEY=...
GOOGLE_API_KEY=...
DEEPSEEK_API_KEY=...
```

## Ollama Setup (Windows)

1. Install Ollama: https://ollama.com/download/windows
2. Confirm it works:

   ```powershell
   ollama --version
   ```
3. Pull a model (example):

   ```powershell
   ollama pull llama3.2
   ```
4. Run it:

   ```powershell
   ollama run llama3.2
   ```
5. Use from this repo:

   - Open `ollama.ipynb` in VS Code
   - Select the `.venv` kernel
   - Run the notebook cells

## Usage

Run an example script:

```powershell
python main.py
```

Or run another entry:

```powershell
python gemini.py
```

For notebooks, open any `.ipynb` and select the `.venv` kernel.

## Notes

- Some subfolders may include their own dependency files/README; follow local instructions when present.
