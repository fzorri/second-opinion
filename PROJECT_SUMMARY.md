# Project Summary: Second Opinion

This document provides a comprehensive overview of the "Second Opinion" CLI application, designed to facilitate rapid future reviews and development.

## 1. Project Overview

"Second Opinion" is a lightweight and efficient command-line interface for chatting with multiple Large Language Models (LLMs). Its key advantages include:

*   **Multi-LLM Support:** Easily switch between numerous LLM providers.
*   **Cost-Effective:** Operates on a pay-as-you-go basis by using individual API keys, avoiding fixed monthly subscriptions.
*   **Local History:** All conversations are saved locally, allowing users to review, resume, and manage past interactions.
*   **(Very) Low System Requirements:** Runs on minimal hardware without needing a high-end setup.
*   **Extensible:** The architecture is designed for easy addition of new LLMs.

## 2. How to Run the Application

1.  **Environment Setup:** Ensure Python (3.10+) and Git are installed. It is recommended to use a virtual environment (like `conda`).
2.  **Installation:**
    ```bash
    git clone https://github.com/fzorri/second-opinion.git
    cd second-opinion
    pip install -r requirements.txt
    ```
3.  **Configuration:**
    *   Create a `.env` file from the template: `copy .env.template .env`
    *   Edit the `.env` file to add your personal API keys for the LLMs you wish to use.
4.  **Execution:**
    *   Run the main script: `python secop.py`
    *   Select a model from the list.
    *   Optionally, press `?` to load a previous conversation for that model.
    *   Enter your prompt. To submit the prompt to the LLM, press `Ctrl+Enter` or `Ctrl+D`.
    *   To end the current chat and return to the main menu, press `Ctrl+C`.

## 3. Project Structure

The project is organized into several key files and directories:

| File / Directory      | Purpose                                                                                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `secop.py`            | Main entry point. It handles the main menu, model selection, user input loop, and calls the appropriate LLM class.                      |
| `config.py`           | Configuration file. It loads model definitions and provider settings from `models.yaml`.                                                |
| `models.yaml`         | LLMs grouped by provider, including their configuration (model ID, name, folder, max tokens, enabled status, Python class handler ).    |
| `.env`                | (User-created) Secret API keys for all LLM providers. This file is ignored by Git.                                                      |
| `requirements.txt`    | Lists all the Python dependencies for the project.                                                                                      |
| `history.py`          | Contains the `History` class, which manages loading, viewing, deleting, and merging past conversations stored as `.json` files.         |
| `tools.py`            | Static methods for tasks: printing colored text, multi-line input , saving conversations to JSON, and printing conversations to JSON.   |
| `llm_classes/`        | A directory with generalized logic for interacting with different LLMs.                                                                 |
|                       | Each file contains a single provider-specific class handling multiple models from that provider based on `models.yaml` configurations.  |
| `models/`             | Root directory where all conversation history is stored. Each model has a sub-folder defined in its `model_folder` in `models.yaml`.    |

## 4. Execution and Configuration Flow

1.  **Initialization:** When `python secop.py` is run, it first loads the `models.yaml` file via `config.py`.
2.  **Dynamic Model Loading:** `secop.py` iterates through the providers and models defined in `MODELS_CONFIGURATION` (loaded from `models.yaml`).
    *   For each provider, it dynamically imports the specified Python class (e.g., `Anthropic_LLM` from `llm_classes/llm_anthropic_base.py`).
    *   For each enabled model listed under that provider, it instantiates the corresponding provider class, passing the model's specific configuration data (model ID, name, folder, API key, etc.) to its constructor.
3.  **Menu Display:** The application then uses the `model_name` and `max_tokens` attributes of these instantiated LLM objects to build the interactive selection menu for the user. Models marked as `enabled: false` in `models.yaml` are displayed as disabled with a reason.
4.  **API Key Handling:** API keys are loaded from the `.env` file via `python-dotenv` and injected into the model configurations by `config.py` before model instantiation.

## 5. Extensibility: How to Add a New LLM

The project is now designed for much simpler extension. To add a new LLM, you primarily modify `models.yaml`:

**Step 1: Update `models.yaml`**

Add a new model entry under an existing provider, or create a new provider entry if it's a new API. For example, to add a new Grok model:

```yaml
providers:
  groq:
    api_key_env: GROQ_API_KEY
    class: Groq_LLM # Ensure this class exists in llm_classes/llm_groq_base.py
    models:
      - model_name: "Llama 3.3 70b versatile(groq)"
        model_id: "llama-3.3-70b-versatile"
        model_folder: "models/groq-llama33_70_b_versatile8b"
        max_tokens: 4096
        enabled: true
      - model_name: "Grok 4.1 Fast Reasoning (Groq)" # New model
        model_id: "grok-4-1-fast-reasoning"
        model_folder: "models/groq-grok-4-1-fr"
        max_tokens: 1000000
        enabled: true
```
*Remember to add the corresponding `API_KEY_ENV` (e.g., `GROQ_API_KEY`) to your `.env` file if it's a new provider or if the environment variable doesn't exist.*

**Step 2 (If New Provider): Create/Generalize the LLM Class in `llm_classes/`**

If you are adding a model from a **completely new provider** (one not yet in `llm_classes/`), you will need to:
1.  Create a new file, e.g., `llm_newprovider_base.py`, in `llm_classes/`.
2.  Inside this file, create a class named `NewProvider_LLM` (following the `<ProviderName>_LLM` convention). This class must inherit from `LLMBase`.
3.  Implement the `__init__`, `initialize_client`, `send_message`, and `load_conversation` methods within `NewProvider_LLM`, using `self.model_id`, `self.api_key`, etc., from the `config_data` passed to its `__init__`. Refer to existing `_base.py` files for examples.

If the model is from an **existing provider**, no code changes in `llm_classes/` are typically required, as the existing provider class (e.g., `Groq_LLM`) is designed to handle multiple models.

Once these steps are complete, running `python secop.py` will automatically include the new model(s) in the list.