import os
import openai
import pyttsx3
import speech_recognition as sr
import tkinter as tk

# OpenAI API authentication
#openai.organization = "org-hV55Q7jK16nHIybWzSOEun90"
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up TTS engine
engine = pyttsx3.init()

# Initialize a speech recognizer object
r = sr.Recognizer()

def get_audio_response():
    # Get text from user input field
    user_input_text = user_input.get()

    audio_prompt = None
    prompt = None

    # If user has entered text, use it as prompt
    if user_input_text:
        prompt = f"{user_input_text}\nA:"
    else:
        # Otherwise, get audio prompt using speech recognizer
        try:
            with sr.Microphone() as source:
                #Listening
                r.adjust_for_ambient_noise(source)
                r.pause_threshold = 3
                print("Listening....")
                audio = r.listen(source, timeout=3)
                #Recognizing
                print("Recognizing....")
                audio_prompt = r.recognize_google(audio, language='en-in')
                print(f"user said: {audio_prompt}\n")
        #Exceptions for listening
        except sr.WaitTimeoutError:
            print(f"WaitTimeoutError - There was a wait timeout error in waiting for audio\n")
            #chat_history.insert("WaitTimeoutError - There was a wait timeout error in waiting for audio\n", "bot")
            return
        except sr.RequestError as e:
            print(f"Could not request results; {0}\n")
            #chat_history.insert("end", f"Could not request results; {0}\n", "bot")
            return
        except sr.UnknownValueError:
            print(f"Audio input device is not available or not connected.\n")
            #chat_history.insert("end", f"Audio input device is not available or not connected.\n", "bot")
            return
        #Exceptions for recognizing / translating audio to text to be used for the prompt
        except sr.UnknownValueError:
            print(f"Google Speech Recognition could not understand audio\n")
            #chat_history.insert("end", f"Google Speech Recognition could not understand audio\n", "bot")
            return
        except Exception as e:
            print(f"Unspecified error:\n {0}\n")
            return

    if audio_prompt:
        # Use audio prompt as prompt
        prompt = f"{audio_prompt}\nA"
        # May not have to use the f conversion here
        # prompt = f"{audio_prompt}\nA"

    if not prompt:
        return

    if audio_prompt == "quit":
        root.destroy()
        return

    # Generate response from OpenAI
    model_engine = "text-davinci-003"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    bot_response = completions.choices[0].text.strip()

    # Display response in chat history
    chat_history.configure(state="normal")
    chat_history.tag_config("bot", justify="center")
    chat_history.tag_config("user", justify="center", foreground="purple")
    chat_history.insert("end", f"\nYou: {prompt.split('A:')[0]}\n", "user")
    chat_history.insert("end", "\n")
    chat_history.insert("end", f"\nBot: {bot_response}\n", "bot")
    chat_history.configure(state="disabled")

    # Scroll to end of chat history
    chat_history.see(tk.END)
    root.update()

    # Speak response using TTS engine
    engine.say(bot_response)
    engine.runAndWait()

    # Clear user input field
    user_input.delete(0, tk.END)

# Set up GUI window
root = tk.Tk()
root.title("AI Chatbot")
root.geometry("1500x700")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set up chat history display
chat_history = tk.Text(root, bg="white", font=("Times", 18), wrap="word", state="disabled")
chat_history.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
chat_history.config(width=50)  # Add padding to the right

# Set up intro message
chat_history.configure(state="normal")
chat_history.insert("end", "\n")
chat_history.insert("end", "Hi, I'm an AI chatbot! \n\n Press 'Enter' to speak your question \n\n Or type it into the box \n\n And press 'Enter' to get a response. \n\n When you are finished, press 'Enter' then say 'Quit' \n\n", "bot")
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

# Set up user input field
user_input = tk.Entry(root, bg="white", font=("Helvetica", 18), fg="purple")
user_input.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
user_input.bind("<Return>", lambda event: get_audio_response())
user_input.focus()
root.update()
user_input_text = user_input.get()

# If user has entered text, use it as prompt
if user_input_text:
        prompt = f"{user_input_text}\nA:"
root.update()

# Start GUI main loop
root.mainloop()
