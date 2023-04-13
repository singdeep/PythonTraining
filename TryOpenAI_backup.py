import os
import openai
import pyttsx3
import speech_recognition as sr
import tkinter as tk
import win32com.client as wincl

# Set up the OpenAI API credentials and parameters
openai.api_key = os.environ["OPENAI_API_KEY"]
model_engine = "text-davinci-003"
temperature = 0.5
max_tokens = 1000

# Initialize Text to speech engine
engine = pyttsx3.init()

# Initialize a speech recognizer object
r = sr.Recognizer()

# Set up GUI window
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("1920x1080")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set up chat history display
chat_history = tk.Text(root, bg="white", font=("Times", 18), wrap="word", state="disabled")
chat_history.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
chat_history.config(width=50)  # Add padding to the right

# Set up user input field
user_input = tk.Entry(root, bg="white", font=("Helvetica", 18), fg="purple")
user_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
user_input.bind("<Return>", lambda event: get_response())

# Set up intro message
chat_history.configure(state="normal")
chat_history.insert("end", "\n")
chat_history.insert("end", "Hi, I'm an AI chatbot! Ask me anything or type 'quit' to exit.\n\n", "bot")
chat_history.insert("end", "Checking audio input.\n\n", "bot")
chat_history.tag_config("bot", justify="center", lmargin1=5, lmargin2=5)
chat_history.configure(state="disabled")
chat_history.tag_add("bot", "1.0", "end")
chat_history.tag_configure("bot", justify="center")
chat_history.tag_configure("bot", font=("Helvetica", 18))
chat_history.tag_configure("bot", spacing1=10)
chat_history.tag_configure("bot", spacing2=10)
chat_history.tag_configure("bot", foreground="#009688")
chat_history.tag_configure("bot", wrap="word")
chat_history.tag_configure("bot", background="#F5F5F5")
chat_history.tag_configure("bot", relief="groove")
chat_history.tag_configure("bot", borderwidth=2)
chat_history.tag_raise("bot")
chat_history.insert("end", "\n")
chat_history.see("end")

spokenWords = None
somethingSaid = False

# Set up function to get bot response
def get_response():
    chat_history.insert("end", "Say or type quit to quit.", "bot")
    chat_history.see(tk.END)
    
    user_input.focus()

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
            chat_history.insert("end", f"\nGoogle Speech Recognition thinks you said {spokenWords}\n", "bot")
            #print("Google Speech Recognition thinks you said " + spokenWords)
            somethingSaid = True
        except sr.UnknownValueError:
            chat_history.insert("end", f"Google Speech Recognition could not understand audio\n", "bot")
            #print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            chat_history.insert("end", f"Could not request results from Google Speech Recognition service; {0}\n", "bot")
            #print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except OSError:
        chat_history.insert("end", f"No audio input device was found.\n", "bot")
        #print("No audio input device was found.")
    except NameError:
        chat_history.insert("end", f"Audio variable not found.\n", "user", "bot")
        #print("Audio variable not found.")

    chat_history.see("end")

    if spokenWords is None:
        somethingSaid=False

    if somethingSaid:
        prompt = spokenWords    
    else:
        user_message = user_input.get()
        chat_history.insert("end", f"{user_message}\n", "user")
        user_input.delete(0, tk.END)
        prompt = user_message

    if prompt.lower() == "quit":
        root.destroy()

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    bot_response = completions.choices[0].text.strip()

    # Display response in chat history
    chat_history.configure(state="normal")
    # is below line duplicate?
    chat_history.tag_config("bot", justify="center")
    chat_history.tag_config("user", justify="center", foreground="purple")
    chat_history.insert("end", f"\nYou: {user_message}\n", "user")
    chat_history.insert("end", "\n")
    chat_history.insert("end", f"\nBot: {bot_response}\n", "bot")
    chat_history.configure(state="disabled")

    # Scroll to end of chat history
    chat_history.see(tk.END)
    print(bot_response.choices[0].text)
    
    #Text to speech response (TTS)
    engine.say(bot_response.choices[0].text)
    engine.runAndWait()


