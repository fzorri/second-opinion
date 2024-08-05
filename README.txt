INSTRUCTIONS:
Software to install (VERY RECOMMENDED):
- Anaconda/Miniconda
- git

Install:
-Create a folder where the code will be installed: 
mkdir secop
cd secop

-Create an envrironment to work with: 
conda create --name ai python=3.9

-Activate environment
conda activate ai

- Download the code using github
clone https://github.com/fzorri/secop.git

Install the requirements:
pip install -r requirements.txt

- Copy the initial configuration to config.py
copy config_template.py config.py (windows) | cp config_template.py config.py (linux o mac)

- get some api keys from the companies you want (see config_template.py info) and complete config.py

Running Second Opinion

How to work with Second Opinion.

2 - Run the secop.py file using python secop.py (or just secop if you have the environment activated)

3 - Select Model number and Enter.

4 - Start the conversation

Starting conversation.
When you enter the conversation you can ask the question you want to the LLM of you choice.
Just type all you need normally, you can use carriage return to write multiple lines.

- You cannot go back to previous line.
- Type 'end' (case insensitive, no quotes) to end the conversation and send to the LLM.
- Press Ctl-C to abort the conversation and return to main menu.

Autocheck
The autocheck (option A) mode allow testing all configured APIs

History Mode 
All the conversations made using Second Opinion are stored locally. 
Every conversation is stored in a folder, according the configuration made in config.py

It is possible to select previous conversations and continue the conversation.
It is also possible to preview a conversation without continue it.
It is possible to delete a conversation.
It is possible to select multiple conversations and merge the selected conversations into one single conversation.

All the conversations are stored in JSON format.

Remember that you can take a conversation and extend it, and also since the conversation is stored locally, you can modify or alter
a conversation already saved and reload it into a LLM. This 2 features are very useful to improve/change/hack a conversation we had 
with a LLM, so be careful, since this is a very powerful option.








