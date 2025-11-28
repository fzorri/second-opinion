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
from dotenv import load_dotenv

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

load_dotenv()
#Models list: https://docs.anthropic.com/en/docs/models-overview


Anthropic_Claude_Opus_45_CFG = {
    "API_KEY": os.getenv("ANTHROPIC_API_KEY"),    "MODEL_NAME": "Claude V4.5 - Opus (Powerful)- 20251128",    "MODEL_ID": "claude-opus-4-5-20251101",    "MODEL_FOLDER": "models/anthropic-opus-45",
}

Anthropic_Claude_Sonnet_45_CFG = {
    "API_KEY": os.getenv("ANTHROPIC_API_KEY"),    "MODEL_NAME": "Claude V4.5 - Sonnet (Balanced) - 20251128",    "MODEL_ID": "claude-sonnet-4-5-20250929",    "MODEL_FOLDER": "models/anthropic-sonnet-45",
}

Anthropic_Claude_Haiku_45_CFG = {
    "API_KEY": os.getenv("ANTHROPIC_API_KEY"),    "MODEL_NAME": "Claude V4.5 - Haiku (Fast) - 20251128",    "MODEL_ID": "claude-haiku-4-5-20251001",    "MODEL_FOLDER": "models/anthropic-haiku-45",
}


Anthropic_Claude_Opus_CFG = {
    "API_KEY": os.getenv("ANTHROPIC_API_KEY"),    "MODEL_NAME": "Claude V4 - Opus (Powerful)",    "MODEL_ID": "claude-opus-4-1",    "MODEL_FOLDER": "models/anthropic",
}

Anthropic_Claude_Sonnet_CFG = {
    "API_KEY": os.getenv("ANTHROPIC_API_KEY"),    "MODEL_NAME": "Claude V4 - Sonnet (Balanced) - 20251028",    "MODEL_ID": "claude-sonnet-4-5",    "MODEL_FOLDER": "models/anthropic",
}

Anthropic_Claude_Haiku_CFG = {
    "API_KEY": os.getenv("ANTHROPIC_API_KEY"),    "MODEL_NAME": "Claude V4 - Haiku (Fast) - 20251028",    "MODEL_ID": "claude-haiku-4-5",    "MODEL_FOLDER": "models/anthropic",
}

DeepSeek_Chat_CFG ={
    "API_KEY" : os.getenv("DEEPSEEK_API_KEY"),    "MODEL_NAME": "DeepSeek (chat)",    "MODEL_ID": "deepseek-chat",        "MODEL_FOLDER": "models/deepsek-chat",    "MAX_TOKENS": 131072
}

DeepSeek_Code_CFG ={
    "API_KEY" : os.getenv("DEEPSEEK_API_KEY"),    "MODEL_NAME": "DeepSeek (reasoner)",    "MODEL_ID": "deepseek-reasoner",    "MODEL_FOLDER": "models/deepseek-reasoner",    "MAX_TOKENS": 131072
}

Fireworks_Mistral_8x22_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),    "MODEL_NAME": "Mistral 8x22 Instruct (fireworks.ai)",    "MODEL_ID": "accounts/fireworks/models/mixtral-8x22b-instruct",    "MODEL_FOLDER": "models/fireworks_mistral"
}


Fireworks_Qwen3_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),    "MODEL_NAME": "Qwen 3 Coder 480B - fireworks.ai - 20251028",    "MODEL_ID": "accounts/fireworks/models/qwen3-coder-480b-a35b-instruct",    "MODEL_FOLDER": "models/qwen3_coder-480b"
}

# accounts/fireworks/models/kimi-k2-thinking

Fireworks_KimiK2T_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),    "MODEL_NAME": "Kimi K2 Thinking - fireworks.ai - 20251113",    "MODEL_ID": "accounts/fireworks/models/kimi-k2-thinking",    "MODEL_FOLDER": "models/kimik2-thinking"
}


# Models: https://ai.google.dev/gemini-api/docs/models

Gemini_Pro_3_Preview_CFG ={
    "API_KEY" : os.getenv("GOOGLE_API_KEY"),    "MODEL_NAME": "Gemini Pro 3.0 Preview",    "MODEL_ID": "models/gemini-3-pro-preview",    "MODEL_FOLDER": "models/gemini-pro-3-preview",    "MAX_TOKENS": 256000
}


# gemini-2.5-pro & flash : 20251028
Gemini_Pro_2_5_CFG ={
    "API_KEY" : os.getenv("GOOGLE_API_KEY"),    "MODEL_NAME": "Gemini Pro 2.5",    "MODEL_ID": "models/gemini-2.5-pro",    "MODEL_FOLDER": "models/gemini-pro-2_5",    "MAX_TOKENS": 256000
}

#gemini-2.5-flash-preview-04-17
Gemini_Flash_2_5_CFG ={
    "API_KEY" : os.getenv("GOOGLE_API_KEY"),    "MODEL_NAME": "Gemini Flash 2.5",    "MODEL_ID": "models/gemini-2.5-flash",    "MODEL_FOLDER": "models/gemini-flash-2_5",    "MAX_TOKENS": 1048576
}

OctoAI_LLama3_70_CFG ={
    "API_KEY" : os.getenv("OCTOAI_API_KEY"),    "MODEL_NAME": "Llama 3 (70b) (octo.ai)",    "MODEL_ID": "meta-llama-3-70b-instruct",    "MODEL_FOLDER": "models/octoai-llama3"
}

OpenAI_35_TURBO_CFG= {
    "API_KEY" : os.getenv("OPENAI_API_KEY"),    "MODEL_NAME": "ChatGPT 3.5 turbo (OpenAI)",    "MODEL_ID": "gpt-3.5-turbo",    "MODEL_FOLDER": "models/openai-chatgpt-3_5",    "MAX_TOKENS": 4096
}

OpenAI_4TURBO_CFG= {
    "API_KEY" : os.getenv("OPENAI_API_KEY"),    "MODEL_NAME": "ChatGPT 4 turbo (OpenAI)",    "MODEL_ID": "gpt-4-turbo",    "MODEL_FOLDER": "models/openai-chatgpt-4_turbo"
}

OpenAI_4OMNI_CFG= {"API_KEY" : os.getenv("OPENAI_API_KEY"),    "MODEL_NAME": "ChatGPT 4 Omni (OpenAI)",    "MODEL_ID": "gpt-4o",  "MODEL_FOLDER": "models/openai-chatgpt-4_omni"}

#gpt-4o-mini
OpenAI_4O_MINI_CFG= {
    "API_KEY" : os.getenv("OPENAI_API_KEY"),    "MODEL_NAME": "ChatGPT 4O Mini (OpenAI)",    "MODEL_ID": "gpt-4o-mini",    "MODEL_FOLDER": "models/openai-chatgpt-4o-mini"
}

#llama-3.1-8b-instant
Groq_Llama33_70b_CFG = {
    "API_KEY" : os.getenv("GROQ_API_KEY"),    "MODEL_NAME": "Llama 3.3 70b versatile(groq)",    "MODEL_ID": "llama-3.3-70b-versatile",    "MODEL_FOLDER": "models/groq-llama33_70_b_versatile8b",    "MAX_TOKENS": 4096
}

# qwen/qwen3-32b
Groq_Qwen3_32b_CFG = {    "API_KEY" : os.getenv("GROQ_API_KEY"),    "MODEL_NAME": "Qwen3 32b Reasoning (groq)",    "MODEL_ID": "qwen/qwen3-32b",    "MODEL_FOLDER": "models/groq-qwen3-32b",    "MAX_TOKENS": 65536
}

# moonshotai/kimi-k2-instruct
Groq_Kimi_K2_CFG = {
    "API_KEY" : os.getenv("GROQ_API_KEY"),    "MODEL_NAME": "Kimi K2 128K (groq)",    "MODEL_ID": "moonshotai/kimi-k2-instruct",    "MODEL_FOLDER": "models/kimi-k2",    "MAX_TOKENS": 128000
}


# models: https://docs.x.ai/docs/models
# grok-4-0709
# grok-4-1-fast-non-reasoning

Xai_Grok_41_fast_non_reasoning_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),      "MODEL_NAME": "Grok 4.1 Fast non-reasoning (Xai)",      "MODEL_ID": "grok-4-1-fast-non-reasoning",      "MODEL_FOLDER": "models/grok-4-fnr",      "MAX_TOKENS": 1000000
}

#grok-4-1-fast-reasoning
Xai_Grok_41_fast_reasoning_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),      "MODEL_NAME": "Grok 4.1 Fast Reasoning (Xai)",      "MODEL_ID": "grok-4-1-fast-reasoning",      "MODEL_FOLDER": "models/grok-4-fr",      "MAX_TOKENS": 1000000
}


Xai_Grok4_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),      "MODEL_NAME": "Grok 4 (Xai)",      "MODEL_ID": "grok-4-0709",      "MODEL_FOLDER": "models/grok-4",      "MAX_TOKENS": 250000
}

# 20250923 - Grok Fast 1: grok-code-fast-1 # 2 M context(el primreo con un contexto de 2M)
Xai_Grok4_Fast_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),      "MODEL_NAME": "Grok 4 Fast - 20250923",      "MODEL_ID": "grok-code-fast-1",     "MODEL_FOLDER": "models/grok-code-fast-1",      "MAX_TOKENS": 2097152
}

##################### APIS SIN USO/DEPRECADAS/OBSOLETAS
'''20251028: Nunca se usa
Mistral_Largest_CFG ={
    "API_KEY" : os.getenv("MISTRAL_API_KEY"),
    "MODEL_NAME": "Mistral Largest (Mistral)",
    "MODEL_ID": "mistral-large-latest",
    "MODEL_FOLDER": "models/mistral",
    "MODEL_ENDPOINT": "",
    "ENABLED": False,
}

#"ENABLED_REASON": "API has changed /proxy problems (?)"

#Verified I cannot access codestral with api key of mistral

20251028: Sin uso
Mistral_Codestral_CFG ={
    "API_KEY" : os.getenv("MISTRAL_API_KEY"),
    "MODEL_NAME": "Mistral Codestral (Mistral)",
    "MODEL_ID": "codestral-latest",
    "MODEL_FOLDER": "models/codestral",
    "MODEL_ENDPOINT": "https://codestral.mistral.ai",
    "ENABLED": False,
}

#  "ENABLED_REASON": "API has changed /proxy problems (?)"
Fireworks_StarCoder2_16b_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),
    "MODEL_NAME": "Mistral Starcode 2 15b (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/starcoder-16b",
    "MODEL_FOLDER": "accounts/fireworks/models/starcoder-7b",
    "ENABLED": False,
    "ENABLED_REASON": "In Fireworks, needs /completions mode, to investigate"
}



Fireworks_Qwen3_235b_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),
    "MODEL_NAME": "Qwen 3 235b A22b - fireworks.ai - 20250501",
    "MODEL_ID": "accounts/fireworks/models/qwen3-235b-a22b",
    "MODEL_FOLDER": "models/qwen3_235b"
}


# Discarded
#Fireworks_Qwen2_Chat_CFG = {
#    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),
#    "MODEL_NAME": "Qwen 2 Chat 72B (fireworks.ai)",
#    "MODEL_ID": "accounts/fireworks/models/qwen-72b-chat",
#    "MODEL_FOLDER": "models/fireworks_qwen2_chat",
#    "ENABLED": False,
#    "ENABLED_REASON": "retired in 20240814"
#}

#accounts/fireworks/models/yi-large
#accounts/fireworks/models/yi-large

Removido 20251028
Fireworks_Yi_Large_CFG={
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),
    "MODEL_NAME": "Yi Large (fireworks.ai)",
    "MODEL_ID": "accounts/yi-01-ai/models/yi-large",
    "MODEL_FOLDER": "models/yi_large"
}

20251028: Fuera de linea
Fireworks_DeepSeekR1_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),
    "MODEL_NAME": "DeepSeek R1 (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/deepseek-r1",
    "MODEL_FOLDER": "models/deepseek_r1",
    "MAX_TOKENS": 128000
}

Gemini_Gemma2_2b_CFG ={
    "API_KEY" : os.getenv("GOOGLE_API_KEY"),
    "MODEL_NAME": "Gemma 2B experimental",
    "MODEL_ID": "gemma-2-2b-it",
    "MODEL_FOLDER": "models/gemma-2-2b-it",
    "ENABLED": False,
    "ENABLED_REASON": "It does not work"
}

20251028: lo saco porque no lo uso
Lepton_WizardLM_8x22_CFG = {
    "API_KEY" : os.getenv("LEPTON_API_KEY"),
    "MODEL_NAME": "WizardLM 8x22 (lepton.ai)",
    "MODEL_ID": "wizardlm-2-8x22b",
    "MODEL_FOLDER": "models/lepton-wizardlm"
}

#Discarded. I seldom use it and they have an issue of using max_completion_tokens instead max_tokens
OpenAI_o1_preview_CFG= {
    "API_KEY" : os.getenv("OPENAI_API_KEY"),
    "MODEL_NAME": "Orion 1 Preview (OpenAI)",
    "MODEL_ID": "o1-preview",
    "MODEL_FOLDER": "models/openai-o1-preview",
    "ENABLED": True,
    "ENABLED_REASON": "Testing",
    "TEMPERATURE" : 1
}


OpenAI_o3_mini_CFG= {
    "API_KEY" : os.getenv("OPENAI_API_KEY"),
    "MODEL_NAME": "O3 Mini (OpenAI)",
    "MODEL_ID": "o3-mini",
    "MODEL_FOLDER": "models/openai-o3-mini",
    "ENABLED": True,
    "ENABLED_REASON": "Test"
}

20251028: Dejo de usarla.
La usé poco y devolvió un error de que no tenía balance. esto es imposible porque tenía créditos
Los créditos deben vencerse por lo que es una razón adicional para dejar de usarla.
Reka_CFG = {
    "API_KEY" : os.getenv("REKA_API_KEY"),
    "MODEL_NAME": "Reka Core",
    "MODEL_ID": "reka-core",
    "MODEL_FOLDER": "models/reka-core"
}

Deprecado 20251028
Groq_Llama3_CFG = {
    "API_KEY" : os.getenv("GROQ_API_KEY"),
    "MODEL_NAME": "Llama 3 (70b) (groq.com)",
    "MODEL_ID": "llama3-70b-8192",
    "MODEL_FOLDER": "models/groq-llama3"

}

Deprecado 20251028
Groq_MixtralAL8x7b_CFG = {
    "API_KEY" : os.getenv("GROQ_API_KEY"),
    "MODEL_NAME": "Mistral Saba 24B(groq.com)",
    "MODEL_ID": "mistral-saba-24b",
    "MODEL_FOLDER": "models/mistral-saba-24b",
    "MAX_TOKENS": 4096
}

Groq_Gemma2_9b_CFG = {
    "API_KEY" : os.getenv("GROQ_API_KEY"),
    "MODEL_NAME": "Gemma 2 9B 9kb(groq.com)",
    "MODEL_ID": "gemma2-9b-it",
    "MODEL_FOLDER": "models/gemma2-9b"
}

Groq_DeepSeek_R1_Llama_70b_CFG = {
    "API_KEY" : os.getenv("GROQ_API_KEY"),
    "MODEL_NAME": "DeepSeek R1 Distill llama 70b(groq.com)",
    "MODEL_ID": "deepseek-r1-distill-llama-70b",
    "MODEL_FOLDER": "models/groq-deepseek-r1-distill-llama-70b",
    "MAX_TOKENS": 65536
}

20251028: Lo doy de baja y pasa a la carpeta unused
Esta API prácticamente no la he usado.
Minimax_Text01_CFG = {
      "API_KEY": os.getenv("MINIMAX_API_KEY"),
      "MODEL_NAME": "Minimax Text 01 (intl.minimaxi.com)",
      "MODEL_ID": "MiniMax-Text-01",
      "MODEL_FOLDER": "models/minimax-1",
      "MAX_TOKENS": 2048
}

20251028: Dió un error: NoneType is not subscriptable
Lo doy de baja porque no se usa.
Abab_Chat_CFG = {
      "API_KEY": os.getenv("MINIMAX_API_KEY"),
      "MODEL_NAME": "Abab 6.5 Chat  (intl.minimaxi.com)",
      "MODEL_ID": "abab6.5s-chat",
      "MODEL_FOLDER": "models/abab-6-5-chat",
      "MAX_TOKENS": 2048
}

Xai_Grok2_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),
      "MODEL_NAME": "Grok 2 (x.ai Elon Musk)",
      "MODEL_ID": "grok-2-1212",
      "MODEL_FOLDER": "models/grok2",
      "MAX_TOKENS": 32768
}

# grok-beta
Xai_GrokBeta_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),
      "MODEL_NAME": "Grok Beta (x.ai Elon Musk)",
      "MODEL_ID": "grok-3-beta",
      "MODEL_FOLDER": "models/grok-3-beta",
      "MAX_TOKENS": 65535
}

Xai_GrokBeta_CFG = {
      "API_KEY": os.getenv("XAI_API_KEY"),
      "MODEL_NAME": "Grok Beta (x.ai Elon Musk)",
      "MODEL_ID": "grok-3-beta",
      "MODEL_FOLDER": "models/grok-3-beta",
      "MAX_TOKENS": 65535
}


Fireworks_Llama3_1_70b_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),    "MODEL_NAME": "Llama 3.1 70B (fireworks.ai)",    "MODEL_ID": "accounts/fireworks/models/llama-v3p1-70b-instruct",    "MODEL_FOLDER": "models/llama_v3_1_70b"
}

Fireworks_Llama3_1_405b_CFG = {
    "API_KEY" : os.getenv("FIREWORKS_API_KEY"),    "MODEL_NAME": "Llama 3.1 405B (fireworks.ai)",    "MODEL_ID": "accounts/fireworks/models/llama-v3p1-405b-instruct",    "MODEL_FOLDER": "models/llama_v3_1_405b"
}

'''