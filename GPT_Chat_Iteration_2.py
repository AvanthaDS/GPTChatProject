# This iteration of the script connect to open AI, and Azure Cognitive Speech services APIs
# User input is taken as voice input and response is shown in as an output at the same time read aloud

import openai
import azure.cognitiveservices.speech as speechsdk
import nltk

'''
Makesure there is a text file in the same folder as this script as "Keys.txt" with the following content 
GPT_API_KEY=<your open api key>
Azure_API_KEY=<your azure cognitive speech service key>
Azure_ENDPOINT=<your azure cognitive speech service end point>
Azure_REGION=<your azure cognitive speech service region>

'''

with open('Keys.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line by the equal sign to separate the parameter name from the value
        parameter_name, parameter_value = line.strip().split('=')

        # Use an if-else statement to assign the value to the appropriate variable
        if parameter_name.strip() == 'GPT_API_KEY':
            GPT_Key = parameter_value.strip()
        elif parameter_name.strip() == 'Azure_API_KEY':
            Azure_key = parameter_value.strip()
        elif parameter_name.strip() == 'Azure_ENDPOINT':
            Azure_ENDPOINT = parameter_value.strip()
        elif parameter_name.strip() == 'Azure_REGION':
            Azure_REGION = parameter_value.strip()

# Api Key is taken from a text file.
openai.api_key = GPT_Key
model = "text-davinci-003"

#AZURE SETTING
API_KEY = Azure_key
ENDPOINT = Azure_ENDPOINT
REGION=Azure_REGION

def readNow(My_Text):
    speech_key, service_region = API_KEY, REGION
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = "en-GB-SoniaNeural"

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = synthesizer.speak_text_async(My_Text).get()
    return result

def speakNow():
    speech_key, service_region = API_KEY, REGION
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone...")
    result = speech_recognizer.recognize_once()
    result_text = "Result: {}".format(result.text)
    speech_recognizer.stop_continuous_recognition()
    return result_text

# function to send something to GPT and get a response
def getGPTresponse(my_prompt, my_max_tokens):
    maxtokens = my_max_tokens
    prompt = my_prompt
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=maxtokens
    )
    ai_response = response.choices[0].text.strip()
    return ai_response

# open and read the previous conversation context.
# This file will store the past conversation context summarized, so that the conversation can continue in a meaningful way

f = open('memory.txt', 'r')
context = f.read()
f.close()
while True:
    # user_input = input("\nYou: ")
    user_input = speakNow().lower()
    if user_input != "":
        prompt = f"{context}\n\nYou: {user_input}\nAI:"
        ai_response = getGPTresponse(prompt, 2000)

        context = f"{prompt}{ai_response}"
        print(f"AI: {ai_response}")

        voice_out=readNow(ai_response)

        tocken_Count = len(nltk.wordpunct_tokenize(context))
        #when the context is more than 900 tokens the following will summarized that and continues the conversations
        if tocken_Count > 900: # after 900 tokens the conversation will be summarized to 500 words.
            prompt = f"{context}\n\n You: This is a dialogue between you(AI) and I. Can you summarise it to 500 words.\n"
            ai_response = getGPTresponse(prompt, 2000)
            context = f"{ai_response}"
        print(f"Tocket size on conversation context:{tocken_Count}")
        f = open('memory.txt', 'w')
        # update content
        f.write(context)
        # close the file after writing
        f.close()
