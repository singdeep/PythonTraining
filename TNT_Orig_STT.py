import os
import openai
import pyttsx3
import speech_recognition as sr

# Set up the OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

engine = pyttsx3.init()

# Create a recognizer object
r = sr.Recognizer()

# Define the parameters for the API request
model_engine = "text-davinci-003"
temperature = 0.5
max_tokens = 1000

spokenWords = None
somethingSaid = False

print("Checking audio input")
print("If audio is detected it will appear in the prompt.")

while True:

    print("Say the the word 'quit' ")

    # use try-except to catch audio input device errors
    try:
        try:
            with sr.Microphone() as source:
                # adjust the threshold value based on your microphone's ambient noise level
                r.adjust_for_ambient_noise(source)
                print("Say something!")
                audio = r.listen(source)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Audio input device is not available or not connected.")
            
        # Use the recognizer to perform STT on the audio
        try:
            spokenWords = r.recognize_google(audio, language='en-US')
            print("Google Speech Recognition thinks you said " + spokenWords)
            somethingSaid = True
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except OSError:
        print("No audio input device was found.")
    except NameError:
        print("Audio variable not found.")

    if spokenWords is None:
        somethingSaid=False

    if somethingSaid:
        print(spokenWords)

    if somethingSaid:
        prompt = spokenWords
    else:
        prompt = input("Enter a prompt (or  type 'quit' to quit): ")

    if prompt.lower() == "quit":
        break

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    print(response.choices[0].text)
    
    #Text to speech response (TTS)
    engine.say(response.choices[0].text)
    engine.runAndWait()

exit