"""
VERY IMPORTANT:
There is a name convention when creating and handling LLM classes.
The name convention is important to load and handling the classes dinamically

* All the LLM classes are in llm_classes folder
* All LLM classes name have a '_LLM' suffix
* The classes inherit from other classes (LLMBase) and others. Make sure these classes are not ending with '_LLM' suffix
* Every LLM class has its own '_CFG' variable
Example:
Anthropic_Claude_Opus_LLM (whichs inherits from Anthropic_Claude_Base) has its own Anthropic_Claude_Opus_CFG
* The configuration has some special cases
    -  Mistral Codestral has a MODEL_ENDPOINT, because its particular case 

* Where to get the respective apis for every Company.
    I usually use oauth (Google authentication) to manage the keys fr every company, but many of them offers another ways (for example using Github accounts)
    It's up to you what would be the best selection: 

    - Antrhopic(Opus,Sonnet,Haiku): https://console.anthropic.com/account/keys
    - Mistral (Largest,Codestral) : https://console.mistral.ai/api-keys/
    - DeepSeek (Chat,Code) : https://platform.deepseek.com/api_keys
    - Fireworks (Mistral,StarCode,Qwen2,Llama3, Llama3_1, Qwen2_chat, Yi_large) : https://fireworks.ai/account/api-keys
    - Gemini (1.5 Pro, Flash 1.5) : https://makersuite.google.com/app/apikey
    - Lepton.ai (WizardLM): I cannot recall (documentation is offline, can't see a way to create api keys)
    - Octo.ai(Llama 3 70B): Register in https://octoai.cloud and request a token
    - OpenAI(chat GPT 3.5, 4 turbo, 4 omni, 4 omni mini): https://platform.openai.com/account/api-keys
    - Reka(reka-edge, reka-flash, reka-core): https://platform.reka.ai/apikeys after signing up
    - Groq (llama 3, Mistral8x7b, Gemma2): https://console.groq.com/keys


    minimax-01 API_KEY: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJGZXJuYW5kbyBaIiwiVXNlck5hbWUiOiJGZXJuYW5kbyBaIiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE4ODA3MTgwNTk5MjA5NTQyODUiLCJQaG9uZSI6IiIsIkdyb3VwSUQiOiIxODgwNzE4MDU5OTE2NzU5OTgxIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiZmVybmFuZG8uem9ycmlsbGFAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDEtMjAgMDA6MjM6MTAiLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.BnOCSJ5KctMcXNzdQDEZVGCK5TAuUQm8698z1gJZEnN8s35MUXmJJiZbmaAxRlyyx0UkQ2IWnMZ1ao4B7mAUg8b_3NKFdFNsGiKlew9sV1Q7ebI16K2xXpDfVAPUAISszd962UZq78ID7HaC0ECYvjhmVIHYRm4RzE5z6v0zPmqKVisJM7-SKbjtNZJtj2HDiffTPq-Q2KGxrKe-1Fa0rkPWn4Rs_TPV3oYAe5Sffj0auFSawMR5H0SdJY6I2HDiQiGR7NRM2ksgat6hnQFfz6Sk_LnUZHTgEGXuhanh1JJOuhmoH7N6wedPJ0u87jm5jOjYHJkkLohnfH4mmnSpxw

"""

import os
import yaml
from dotenv import load_dotenv

MODELS_YAML_PATH = "models.yaml"

# File attachment threshold (bytes) - files smaller than this are embedded inline
MAX_FILE_SIZE_EMBED = int(os.getenv('MAX_FILE_SIZE_EMBED', '10240'))

# Maximum length for conversation names
MAX_CONVERSATION_NAME_LENGTH = int(os.getenv('MAX_CONVERSATION_NAME_LENGTH', '120'))

# Nvidia NIM API documentation link
NVIDIA_NIM_DOCS = "https://docs.nvidia.com/nim/large-language-models/latest/reasoning-model.html"

# Valid reasoning_effort values for Nvidia NIM API
VALID_REASONING_EFFORTS = ["low", "medium", "high", "max"]

# Valid thinking parameter names
VALID_THINKING_PARAMS = ["thinking", "enable_thinking"]

def validate_nvidia_thinking_config(model_name, model_config):
    """
    Validate Nvidia thinking configuration parameters.
    Returns list of error messages, empty if valid.
    """
    errors = []
    
    enable_thinking = model_config.get("enable_thinking", False)
    reasoning_effort = model_config.get("reasoning_effort", "high")
    thinking_param = model_config.get("thinking_param", "thinking")
    
    # Validate reasoning_effort
    if reasoning_effort not in VALID_REASONING_EFFORTS:
        errors.append(
            f"Invalid reasoning_effort '{reasoning_effort}' for model '{model_name}'. "
            f"Valid values: {VALID_REASONING_EFFORTS}. "
            f"Documentation: {NVIDIA_NIM_DOCS}"
        )
    
    # Validate thinking_param
    if thinking_param not in VALID_THINKING_PARAMS:
        errors.append(
            f"Invalid thinking_param '{thinking_param}' for model '{model_name}'. "
            f"Valid values: {VALID_THINKING_PARAMS}. "
            f"Documentation: {NVIDIA_NIM_DOCS}"
        )
    
    return errors

def load_model_configurations():
    load_dotenv()
    with open(MODELS_YAML_PATH, 'r') as file:
        config = yaml.safe_load(file)
    
    all_errors = []

    for provider_name, provider_data in config.get("providers", {}).items():
        api_key_env_var = provider_data.get("api_key_env")
        if api_key_env_var:
            provider_data["API_KEY"] = os.getenv(api_key_env_var)
        for model in provider_data.get("models", []):
            if "enabled" not in model:
                model["enabled"] = True
            if "show_reasoning" not in model:
                model["show_reasoning"] = True  # Default: show reasoning if present
            
            # Nvidia-specific thinking configuration
            if provider_name == "nvidia":
                # Set defaults for thinking parameters
                if "enable_thinking" not in model:
                    model["enable_thinking"] = False  # Default: disabled
                if "reasoning_effort" not in model:
                    model["reasoning_effort"] = "high"  # Default: high
                if "thinking_param" not in model:
                    model["thinking_param"] = "thinking"  # Default: thinking
                
                # Validate configuration
                errors = validate_nvidia_thinking_config(model.get("model_name", "unknown"), model)
                all_errors.extend(errors)
    
    # Print errors but don't stop execution - let user see all errors at once
    if all_errors:
        print("\n" + "="*80)
        print("CONFIGURATION ERRORS FOUND:")
        print("="*80)
        for error in all_errors:
            print(f"  ❌ {error}")
        print("="*80)
        print("Please fix the above errors in models.yaml and restart the application.")
        print("="*80 + "\n")
    
    return config

MODELS_CONFIGURATION = load_model_configurations()


# Load environment variables from .env file
# API_KEY: tell where get the data, usually the variable will be stored in a .env file
# MODEL_NAME: Model name, you can put the description you need it.
# MODEL_ID: this id is provided in the models documentation and should be exact the same value
# MODEL_FOLDER: this is where all the conversation will be stored.
# MODEL_ENDPOINT (optional): some models needs different endpoint in order to work
# ENABLED: You can optionally disable a model for different reason (temporarily not available, offline, etc.)
# ENABLED_REASON: If it is not enabled, the reason will be displayed.
# MAX_TOKENS: max tokens allowed in the conversation:
# Remember that a chat session is just a LLM illusion: is the overall text we are continuously feeding the AI, which is slowly growing while we are chatting.