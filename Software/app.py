import google.generativeai as genai
import datetime
import requests
import base64
import io
import pygame
import speech_recognition as sr
import pyttsx3
import time

Name = "Snow"

memory = []
respect = 75
speaking = False
alarm = False
timer = 0

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

GOOGLE_TTS_API = "AIzaSyDncunQw_iIj5afY5S1WYhzRkp3p3Tchzo"
GEMINI_API_KEY = "AIzaSyCA0C3jLG4xgfzcYB8JHnl1s_V052fO0ds"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def display(content):
    print(f"Emotion: {content}")

def change_respect(prompt):
    global respect
    if prompt.lower() in ["respect at 0 %", "respect at 0%"]:
        respect = 0
    elif prompt.lower() in ["respect at 25 %", "respect at 25%"]:
        respect = 25
    elif prompt.lower() in ["respect at 75 %", "respect at 75%"]:
        respect = 75
    elif prompt.lower() in ["respect at 100 %", "respect at 100%"]:
        respect = 100
    else:
        respect = 50
    response = f"Respect changed to {respect}%"
    display("Happiness")
    print(f"Chatbot: {response}")
    TTS(response)

def TTS(user_input):
    global speaking
    url = "https://texttospeech.googleapis.com/v1/text:synthesize?key=" + GOOGLE_TTS_API
    request_body = {
        "input": {"text": user_input},
        "voice": {"languageCode": "en-US", "ssmlGender": "NEUTRAL"},
        "audioConfig": {"audioEncoding": "MP3"}
    }
    response = requests.post(url, json=request_body)
    if response.status_code == 200:
        audio_content = response.json()["audioContent"]
        audio_data = base64.b64decode(audio_content)
        pygame.mixer.init()
        sound = pygame.mixer.Sound(io.BytesIO(audio_data))
        sound.play()
        while pygame.mixer.get_busy():
            speaking = True
            pygame.time.Clock().tick(10)
        speaking = False
    else:
        print("Error:", response.status_code, response.text)

def chat_with_gpt(prompt):
    global memory
    messages = [
        {
            "role": "user", 
            "parts": [{"text": 
                        f"Your name is {Name}, a virtual bot equipped with an Raspberry pi 3, 4 servo motors for hands and body movement, and an OLED display for emotions and face. You respond with a respect level of {respect}% and sarcasm level of {100 - respect}%"
                        "Include the emotion in your responses at the beginning in circular braces, such as (Happiness), (Sadness), (Anger), (Fear), (Shame), or (Love)"
                        "Additional functions you can perform are: "
                        "Set alarm by returning only 'xxSETALARM' response."
                        "Turn light on/off by returning only 'xxTGLLIGHTS' as response."
                        "Say current date/time by returning only 'xxDATETIME' as response."
                    }]
        }
    ]
    memory.extend(messages)
    chat = model.start_chat(history=memory)
    response = chat.send_message(prompt)
    memory.append({"role": "user", "parts": [{"text": response.text}]})
    gpt_response =  response.text.split(")",1)
    emotion = gpt_response[0][1:]
    response = gpt_response[1].strip()
    display(emotion)
    return response

def operation(task):
    global alarm, timer
    if task == "xxDATETIME":
        current_time = datetime.datetime.now()
        formatted_date = current_time.strftime("%d-%m-%Y")
        formatted_time = current_time.strftime("%H:%M")
        response = f"So it's {formatted_date} and the time's {formatted_time}"
        display("Happiness")
        print(f"Chatbot: {response}")
        TTS(response)
    elif task.startswith("xxSETALARM"):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M")
        alarm_time = task.replace("xxSETALARM", "")
        timer = abs(int(formatted_time.replace(":", "")) - int(alarm_time.replace(":", "")))
        alarm = True

def times_up():
    global alarm
    response = "Alarm times up"
    display("Happiness")
    print(f"Chatbot: {response}")
    TTS(response)
    alarm = False

def hearing_task():
    global respect, stop_timer, alarm, timer, speaking
    while True:
        try:
            if not speaking:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                print("You said:", user_input)
                stop_timer = 10

            if user_input.lower() in ["thank you", "that's it", "thanks", "no thanks", "nothing", "stop"]:
                response = "My pleasure" if respect > 50 else "You're welcome"
                display("Happiness")
                print(f"Chatbot: {response}")
                TTS(response)
                break
            else:
                response = chat_with_gpt(user_input)
                if response.startswith('xx'):
                    operation(response)
                else:
                    print(f"Chatbot {response}")
                    TTS(response)

        except sr.WaitTimeoutError:
            print(".")
            stop_timer -= 1
            if stop_timer == 0:
                break
            continue
        except sr.UnknownValueError:
            response = "Sorry, I couldn't understand you." if respect >= 50 else "Could you repeat that?"
            display("Confused")
            print(f"Chatbot: {response}")
            TTS(response)

        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
            break
        except KeyboardInterrupt:
            print("Stopping...")
            break

def start():
    global respect, stop_timer, speaking, Name
    response = f"Hi, I am {Name}. Nice to meet you."
    display("Happiness")
    print(f"Chatbot: {response}")
    TTS(response)
    
    while True:
        print(f"Say 'Hey {Name}!'")
        try:
            if not speaking:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio)
                print("You said:", user_input)
                stop_timer = 10

            if user_input.lower() in [f"hey {Name.lower()}", f"hi {Name.lower()}", f"{Name.lower()}"]:
                response = "Yes, how can I help you?" if respect > 50 else "Yes boss!"
                display("Happiness")
                print(f"Chatbot: {response}")
                TTS(response)
                memory.clear()
                hearing_task()
            elif user_input.lower().startswith("respect at"):
                change_respect(user_input)
            elif user_input.lower() in ["time please", "whats the time now", "time", "date"]:
                operation("xxDATETIME")
            elif user_input.lower() in ["stop", "shutdown"]:
                response = "Shutting down."
                print(response)
                TTS(response)
                break

        except sr.WaitTimeoutError:
            print(".")
            stop_timer -= 1
            if stop_timer == 0:
                break
            continue
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
            break
        except KeyboardInterrupt:
            print("Stopping...")
            break

if __name__ == "__main__":
    with sr.Microphone() as source:
        print("Initializing ambient noise cancellation...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("----- Ready to go -----")
        start()