# Second Opinion is a sleek and user-friendly interface designed for chatting with multiple LLMs. Here are some
key advantages of Second Opinion:

* Lightweight and efficient - the interface is simple and works with all LLMs.
* Quick and easy switching between LLMs (currently 26, with potential for more).
* Instant responses from LLMs.
* Save conversation history locally for easy reference.
* Pay-as-you-go pricing model for cost savings. Forget about monthly payments (!!!)
* Easy setup and configuration.
* Expandable and customizable.
* Markup text for visually appealing LLM responses.
* Open Source for transparency and collaboration.
* No need for high-end hardware - works on low-spec computers.
* Perfect for on-the-go use with minimal system requirements.

## Watch the full series to install, use & understand what you can do with Second Opinion (for the moment, Spanish only, sorry!)

Installation:
 [![#1 - Second Opinion - Installation ](https://www.youtube.com/embed/vY7TTnVR-68?si=sQsjyrzEtOVLjNRJ/maxresdefault.jpg)](https://www.youtube.com/embed/vY7TTnVR-68?si=sQsjyrzEtOVLjNRJ)
 
[![#2 - Second Opinion - How to use it](https://www.youtube.com/embed/7F2RObg0Hwk?si=09K2sJ9fAr8Iydq2/maxresdefault.jpg)](https://www.youtube.com/embed/7F2RObg0Hwk?si=09K2sJ9fAr8Iydq2)

[![#3 - Second Opinion - Autocheckt](https://www.youtube.com/embed/AeP93DaDRf8?si=OZWgK5sWhnz4ndea/maxresdefault.jpg)](https://www.youtube.com/embed/AeP93DaDRf8?si=OZWgK5sWhnz4ndea)

[![#4 - Second Opinion - Conversation history](https://www.youtube.com/embed/8ZyvJ1bzolU?si=QPJ6y8A9_4o9Rdi3/maxresdefault.jpg)](https://www.youtube.com/embed/8ZyvJ1bzolU?si=QPJ6y8A9_4o9Rdi3)

[![#5 - Second Opinion - Extending secop](https://www.youtube.com/embed/5BrzWsQW2aY?si=E_ouUZpBfccQ_AlZ/maxresdefault.jpg)](https://www.youtube.com/embed/5BrzWsQW2aY?si=E_ouUZpBfccQ_AlZ)

INSTRUCTIONS:
Software to install (VERY RECOMMENDED):
- Anaconda/Miniconda
- git

STEPS: 

1- Select a folder to download the code and then
git clone https://github.com/fzorri/second-opinion.git (or use github desktop to download it)
It will create a folder called second-opinion

2- Open a terminal and navigate to the second-opinion folder
3- Create an environment to work with and select the Python version (I'm currently using 3.11.4 however Second Opinion should work with any version of Python 3.10 or higher)
    conda create --name secop python=3.11.5

4-Activate  the environment
conda activate secop

5 - Install the requirements:
pip install -r requirements.txt


6 - Copy the config template  to config.py . This file is never overwritten if you update the software.
copy config_template.py config.py (windows) | cp config_template.py config.py (linux o mac)

7 - get some api keys from the companies you want (see config_template.py info) and complete config.py. The file is self explanatory and very simple.

Running Second Opinion

How to work with Second Opinion.

1 - Run the secop.py file using 'python secop.py' (or just secop if you have the environment activated)

2 - Select Model number and Enter twice to skip history.

3 - Start the conversation

Starting conversation.
Second Opinion is very straightforward and direct to use.
After you select the model, add all the information you want to the conversation and then type 'end' to send the conversation to the LLM.
Wait few seconds and you will get the answer from the LLM. 
You can continue the conversation or press Ctl-C to end the conversation and go back to the menu.

Some tips:
- You can add text but you cannot go back to the previous lines. So be careful when you write the conversation.
- Type 'end' (case insensitive, no quotes) to end the conversation and send to the LLM.
- Press Ctl-C to abort the conversation and return to main menu.
- In windows you can copy any part of the conversation just selecting the text and pressing ENTER. The text will be in the buffer and Ctl-V or Shift-Insert to paste it.

Autocheck
The autocheck (option A) is a loop that allows you to test all configured APIs.

History Mode 
All the conversations you ever did using Second Opinion are stored locally. You can use it to browse you previous conversations, copy, delete, paste it, modify it or whatever
you like. Every LLM stores its own conversations in folders, according the configuration you'll find in config.py

All conversations are stored in JSON format, so you can use any JSON editor to modify it, also the notepad or any text editor will work fine.

The history mode has few utilities within to make your life easier:
- Select previous conversations and reload/resume it.
- Preview a conversation without continue it.
- Delete a conversation.
- Merge multiple conversations into one conversation.

Remember that you can take a conversation and extend it, and also since the conversation is stored locally, you can modify or alter
a conversation already saved and reload it into a LLM. This 2 features are very useful to improve/change/hack a conversation we had 
with a LLM, so be careful, since this is a very powerful option.








