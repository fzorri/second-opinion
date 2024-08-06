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

"""

#Models list: https://docs.anthropic.com/en/docs/models-overview
Anthropic_Claude_Opus_CFG = {
    "API_KEY": "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Claude V3 - Opus (Powerful)",
    "MODEL_ID": "claude-3-opus-20240229",
    "MODEL_FOLDER": "models/anthropic",
}

Anthropic_Claude_Sonnet_CFG = {
    "API_KEY": "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Claude V3 - Sonnet (Balanced)",
    "MODEL_ID": "claude-3-sonnet-20240229",
    "MODEL_FOLDER": "models/anthropic",
}

Anthropic_Claude_Haiku_CFG = {
    "API_KEY": "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Claude V3 - Haiku (Fast)",
    "MODEL_ID": "claude-3-haiku-20240307",
    "MODEL_FOLDER": "models/anthropic",
}

Mistral_Largest_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Mistral Largest (Mistral)",
    "MODEL_ID": "mistral-large-latest",
    "MODEL_FOLDER": "models/mistral",
    "MODEL_ENDPOINT": "",
    "ENABLED": False,
    "ENABLED_REASON": "API has changed /proxy problems (?)"
}

#Verified I cannot access codestral with api key of mistral
Mistral_Codestral_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Mistral Codestral (Mistral)",
    "MODEL_ID": "codestral-latest",
    "MODEL_FOLDER": "models/codestral",
    "MODEL_ENDPOINT": "https://codestral.mistral.ai",
    "ENABLED": False,
    "ENABLED_REASON": "API has changed /proxy problems (?)"
}

DeepSeek_Chat_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "DeepSeek (chat)",
    "MODEL_ID": "deepseek-chat",
    "MODEL_FOLDER": "models/deepsek-chat"
}

DeepSeek_Code_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "DeepSeek (coder)",
    "MODEL_ID": "deepseek-coder",
    "MODEL_FOLDER": "models/deepseek-coder"
}

Fireworks_Mistral_8x22_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Mistral 8x22 Instruct (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/mixtral-8x22b-instruct",
    "MODEL_FOLDER": "models/fireworks_mistral"
}

Fireworks_StarCoder2_16b_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Mistral Starcode 2 15b (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/starcoder-16b",
    "MODEL_FOLDER": "accounts/fireworks/models/starcoder-7b",
    "ENABLED": False,
    "ENABLED_REASON": "In Fireworks, needs /completions mode, to investigate"
}

Fireworks_Qwen2_Instruct_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Qwen 2 Instruct 72B (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/qwen2-72b-instruct",
    "MODEL_FOLDER": "models/fireworks_qwen2_instruct"
}

Fireworks_Llama3_8b_Instruct_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Llama 3 Instruct 8B (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/llama-v3-8b-instruct",
    "MODEL_FOLDER": "models/llama_v3_8b_instruct"
}

Fireworks_Llama3_1_70b_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Llama 3.1 70B (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/llama-v3p1-70b-instruct",
    "MODEL_FOLDER": "models/llama_v3_1_70b"
}

Fireworks_Qwen2_Chat_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Qwen 2 Chat 72B (fireworks.ai)",
    "MODEL_ID": "accounts/fireworks/models/qwen-72b-chat",
    "MODEL_FOLDER": "models/fireworks_qwen2_chat",
    "ENABLED": False,
    "ENABLED_REASON": "Only by demand (GPU use == $$$)"
}

Fireworks_Yi_Large_CFG={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Yi Large (fireworks.ai)",
    "MODEL_ID": "accounts/yi-01-ai/models/yi-large",
    "MODEL_FOLDER": "models/yi_large"
}

Gemini_Pro_1_5_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Gemini Pro 1.5",
    "MODEL_ID": "gemini-1.5-pro",
    "MODEL_FOLDER": "models/gemini-pro-1_5"
}

Gemini_Flash_1_5_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Gemini Flash 1.5",
    "MODEL_ID": "gemini-1.5-flash",
    "MODEL_FOLDER": "models/gemini-flash-1_5"
}

Lepton_WizardLM_8x22_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "WizardLM 8x22 (lepton.ai)",
    "MODEL_ID": "wizardlm-2-8x22b",
    "MODEL_FOLDER": "models/lepton-wizardlm"
}

OctoAI_LLama3_70_CFG ={
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Llama 3 (70b) (octo.ai)",
    "MODEL_ID": "meta-llama-3-70b-instruct",
    "MODEL_FOLDER": "models/octoai-llama3"
}

OpenAI_35_TURBO_CFG= {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "ChatGPT 3.5 turbo (OpenAI)",
    "MODEL_ID": "gpt-3.5-turbo",
    "MODEL_FOLDER": "models/openai-chatgpt-3_5"
}

OpenAI_4TURBO_CFG= {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "ChatGPT 4 turbo (OpenAI)",
    "MODEL_ID": "gpt-4-turbo",
    "MODEL_FOLDER": "models/openai-chatgpt-4_turbo"
}

OpenAI_4OMNI_CFG= {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "ChatGPT 4 Omni (OpenAI)",
    "MODEL_ID": "gpt-4o",
    "MODEL_FOLDER": "models/openai-chatgpt-4_omni"
}

OpenAI_4O_MINI_CFG= {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "ChatGPT 4O Mini (OpenAI)",
    "MODEL_ID": "gpt-4o-mini",
    "MODEL_FOLDER": "models/openai-chatgpt-4o-mini"
}

Reka_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Reka",
    "MODEL_ID": "(no tiene)",
    "MODEL_FOLDER": "models/reka"
}

Groq_Llama3_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Llama 3 (70b) (groq.com)",
    "MODEL_ID": "llama3-70b-8192",
    "MODEL_FOLDER": "models/groq-llama3"
}

Groq_MixtralAL8x7b_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Mistral 8x7b 32kb(groq.com)",
    "MODEL_ID": "mixtral-8x7b-32768",
    "MODEL_FOLDER": "models/groq-mixtral-8x7b"
}

Groq_Gemma2_9b_CFG = {
    "API_KEY" : "YOUR-API-KEY-HERE",
    "MODEL_NAME": "Gemma 2 9B 9kb(groq.com)",
    "MODEL_ID": "gemma2-9b-it",
    "MODEL_FOLDER": "models/gemma2-9b"
}