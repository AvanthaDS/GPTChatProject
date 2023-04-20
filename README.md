# GPT Chat Script
This scripts in this project uses Open AI language models to create a human like conversation. 

- Iteration 1: gets user input as text and returns the response in text form. like a chat window.
- Iteration 2: gets the user input via voice and reads back the response.

The script connect to the open AI API and the Azure cognitive services speach API to convert Speech to text and text to Speech. 

**Pre-requists** 
1. You need to have a open AI account created and an API Key 
2. Need to have a Azure cognitive services account to obtain a speech service API
5. Python installed in your local machine
4. following python libraries need to be installed

- azure-cognitiveservices-speech
- openai
- nltk

**Setting up**
1. Download this file GPT_chat.py file to a local folder 
2. makesure the required libraries are installed
3. Update a Keys_1.text file with your own open AI and Azure Keys, and rename the file to Keys.txt

With this you are ready to run the script. Enjoy!