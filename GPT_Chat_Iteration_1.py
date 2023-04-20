# This iteration of the script connect to open AI api can create a chat with open AI language model.
# No voice input or output. So Azure API's needed.


import openai
import nltk

'''
Makesure there is a text file in the same folder as this script as "Keys.txt" with the following content 
GPT_API_KEY=<your open api key>
'''

with open('Keys.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line by the equal sign to separate the parameter name from the value
        parameter_name, parameter_value = line.strip().split('=')

        # Use an if-else statement to assign the value to the appropriate variable
        if parameter_name.strip() == 'GPT_API_KEY':
            GPT_Key = parameter_value.strip()


# Api Key is taken from a text file.
openai.api_key = GPT_Key
model = "text-davinci-003"


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

# open and read the file, read past context and close.
# This file will store the past conversation context summarized, so that the conversation can continue in a meaningful way

f = open('memory.txt', 'r')
context = f.read()
f.close()


while True:
    user_input = input("\nYou: ")

    if user_input != "":
        prompt = f"{context}\n\nYou: {user_input}\nAI:"
        ai_response = getGPTresponse(prompt, 2000)

        context = f"{prompt}{ai_response}"
        print(f"AI: {ai_response}")

        tocken_Count = len(nltk.wordpunct_tokenize(context))
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