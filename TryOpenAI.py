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
max_tokens = 1024

# Initialize Text to speech engine
engine = pyttsx3.init()

# Initialize a speech recognizer object
r = sr.Recognizer()

# Set up GUI window
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("1620x800")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set up chat history display
chat_history = tk.Text(root, bg="white", font=("Times", 18), wrap="word", state="disabled")
chat_history.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
chat_history.config(width=50)  # Add padding to the right

# Set up user input field
user_input = tk.Entry(root, bg="white", font=("Helvetica", 18), fg="purple")
user_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
user_input.configure(state="normal")

# Set up function to get bot response
def get_userInput():
    user_input.get()

user_input.bind("<Return>", lambda event: get_userInput())

# Set up intro message
chat_history.configure(state="normal")
chat_history.insert("end", "\n")
chat_history.insert("end", "Hi, I'm an AI chatbot! Ask me anything or type 'quit' to exit.\n\n", "bot")
chat_history.insert("end", "Checking audio input.\n\n", "bot")
chat_history.configure(state="disabled")
chat_history.tag_add("bot", "1.0", "end")
chat_history.tag_add("user", "1.0", "end")
chat_history.tag_configure("bot", justify="center", lmargin1=5, lmargin2=5)
chat_history.tag_configure("bot", font=("Helvetica", 18))
chat_history.tag_configure("bot", spacing1=10)
chat_history.tag_configure("bot", spacing2=10)
chat_history.tag_configure("bot", foreground="#009688")
chat_history.tag_configure("bot", wrap="word")
chat_history.tag_configure("bot", background="#F5F5F5")
chat_history.tag_configure("bot", relief="groove")
chat_history.tag_configure("bot", borderwidth=2)
chat_history.tag_configure("user", justify="center", foreground="purple", background="#e6eff0")
chat_history.tag_raise("bot")
chat_history.tag_raise("user")
chat_history.insert("end", "\n")
chat_history.insert("end", "Say or type quit to quit.", "bot")
chat_history.see("end")

root.update()

chat_history.configure(state="normal")
chat_history.insert("end", f"You can try speaking to me now.\n", "bot")
user_input.focus()
chat_history.see(tk.END)

def getAudioIn():
    spokenWords = None
    # use try-except to catch audio input device errors
    try:
        try:
            with sr.Microphone() as source:
                # adjust the threshold value based on your microphone's ambient noise level
                r.adjust_for_ambient_noise(source, 1)
                audio = r.listen(source)
        except sr.RequestError as e:
            chat_history.insert("end", f"Could not request results; {0}\n", "bot")
        except sr.UnknownValueError:
            chat_history.insert("end", f"Audio input device is not available or not connected.\n", "bot")
            
        # Use the recognizer to perform STT on the audio
        try:
            spokenWords = r.recognize_google(audio, language='en-US')
            chat_history.insert("end", f"Google Speech Recognition thinks you said:\n", "bot")
            chat_history.insert("end", f"You: {spokenWords}\n", "user")
        except sr.UnknownValueError:
            chat_history.insert("end", f"Google Speech Recognition could not understand audio\n", "bot")
        except sr.RequestError as e:
            chat_history.insert("end", f"Could not request results from Google Speech Recognition service; {0}\n", "bot")
    except OSError:
        chat_history.insert("end", f"No audio input device was found.\n", "bot")
    except NameError:
        chat_history.insert("end", f"Audio variable not found.\n", "user", "bot")
    return spokenWords

chat_history.see(tk.END)
root.update()

def getPrompt():
    user_message = user_input.get()
    user_input.wait_variable(user_message)
    chat_history.insert("end", f"{user_message}\n", "user")
    chat_history.see(tk.END)
    user_input.delete(0, tk.END)
    prompt = user_message
    return prompt

newPrompt = getAudioIn()
if newPrompt is None or newPrompt == "":
    newPrompt = getPrompt()

if newPrompt.lower() == "quit":
    root.destroy()
    exit

completions = openai.Completion.create(
    engine=model_engine,
    prompt=newPrompt,
    max_tokens=max_tokens,
    n=1,
    stop=None,
    temperature=temperature,
)
bot_response = completions.choices[0].text.strip()

# Display response in chat history
chat_history.insert("end", f"\nBot: {bot_response}\n", "bot")
#chat_history.configure(state="disabled")

# Scroll to end of chat history
chat_history.see(tk.END)

#Text to speech response (TTS)
engine.say(bot_response)
engine.runAndWait()

user_input.focus()

root.mainloop()
