import requests
import base64
import io
import pygame
import google.generativeai as genai
import speech_recognition as sr
import time
import geocoder

#Hardware imports
import led
import servo
import oled
import sensor
import emotions
import Head_or_Tails as HT
import wifi

Name = "Mini"

memory = []
respect = 100
speaking = False
alarm = False
timer = 0
stop_timer = 10

location = geocoder.ip("me")
lat, lon = location.latlng if location.latlng else (10.824698, 76.645973)

GOOGLE_TTS_API = "AIzaSyDncunQw_iIj5afY5S1WYhzRkp3p3Tchzo"
GEMINI_API_KEY = "AIzaSyB7v1fRBse-pzwNiSKU3oBp3hRjAharFaw"

API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

recognizer = sr.Recognizer()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def display(emotion):
    print(f"Emotion: {emotion}")
    emotions.emotions(emotion)

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

def ToggleLights():
    light = led.lights()
    if not light:
        response = "Lights turned off"
        display("Happiness")
        print(f"Chatbot: {response}")
        TTS(response)
    elif light:
        response = "Lights turned on"
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
            #print("Started speaking")
            pygame.time.Clock().tick(10)
        #print("Stoped speaking")
        display("Neutral")
        speaking = False
    else:
        print("Error:", response.status_code, response.text)

def chat_with_gpt(prompt):
    global memory
    messages = [
        {
            "role": "user",
            "parts": [{"text":
                        f"Your name is {Name}, a virtual bot equipped with an Raspberry pi 4, 4 servo motors for hands and body movement, and an OLED display for emotions and face. You respond with a respect level of {respect}% and sarcasm level of {100 - respect}%"
                        "Include the emotion in your responses at the beginning in circular braces, such as (Happiness), (Sadness), (Anger), (Neutral), (Confused), or (Love)"
                        "Additional functions you can perform are: "
                        "To set alarm include '__SET_ALARM' at the beginning of your response."
                        "To turn lights on/off include '__LIGHTS' at the beginning of your response."
                        "To say current date/time include '__DATE_OR_TIME' at the beginning of your response."
                        "To Tose a coin include '__COIN_FLIP' at the beginning of your response."
                        "For wheather information include '__WEATHER' at the beginning of your response."
                    }]
        }
    ]

    memory.extend(messages)
    chat = model.start_chat(history = memory)
    response = chat.send_message(prompt)
    gpt_response =  response.text.split(")",1)
    emotion = gpt_response[0][1:]
    response = gpt_response[1].strip()
    if not response.startswith('__'):
        print("Task not found")
        memory.append({"role": "user", "parts": [{"text": response}]})
    display(emotion)
    return response

def weather_info():
    api_response = requests.get(API_URL)

    if api_response.status_code == 200:
        data = api_response.json()
        temp = data["current_weather"]["temperature"]
        wind_speed = data["current_weather"]["windspeed"]
        weather_code = data["current_weather"]["weathercode"]

        weather_desc = {
            0: "☀️ Clear sky",
            1: "🌤️ Mostly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Foggy",
            51: "🌦️ Light drizzle",
            61: "🌧️ Light rain",
            63: "🌧️ Moderate rain",
            65: "🌧️ Heavy rain",
            71: "❄️ Light snow",
            73: "❄️ Moderate snow",
            75: "❄️ Heavy snow",
        }.get(weather_code, "🌍 Unknown weather")

        response_message = f"The temperature is at {temp}°C with a wind speed of {wind_speed}km/h. So, it's going to be a {weather_desc} condition today."
        print(response_message)
        oled.display(f"Weather: {weather_desc}\nTemperature: {temp}°C\nWind Speed: {wind_speed}km/h")
        TTS(response_message)
    else:
        response_message = "Sorry. I am unable to get any weather reports."
        print(response_message)
        oled.display("Sadness")
        TTS(response_message)

def operation(task):
    global alarm, timer
    if task.startswith("__DATE_OR_TIME"):
        current_time = datetime.datetime.now()
        formatted_date = current_time.strftime("%d-%m-%Y")
        formatted_time = current_time.strftime("%H:%M")
        oled.display(formatted_date+"\n"+formatted_time)
        response = f"So it's {formatted_date} and the time's {formatted_time}"
        print(f"Chatbot: {response}")
        TTS(response)
    elif task.startswith("__SET_ALARM"):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M")
        alarm_time = task.replace("__SET_ALARM", "")
        timer = abs(int(formatted_time.replace(":", "")) - int(alarm_time.replace(":", "")))
        alarm = True
    elif task.startswith("__LIGHTS"):
        ToggleLights()
    elif task.startswith("__COIN_FLIP"):
        if HT.coin_flip() == "Heads":
            response = f"Its a Head"
        else:
            response = f"Its a Tail"
        print(f"Chatbot: {response}")
        TTS(response)
    elif task.startswith("__WEATHER"):
        weather_info()

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
        if not wifi.connectivity():
            oled.display("Wifi connection lost!")
            print("Wifi connection lost!")
            break
        try:
            if sensor.check_temp():
                response = "Temperature too high"
                print(f"Chatbot: {response}")
                TTS(response)

            if not speaking:
                audio = recognizer.listen(source, timeout = 5)
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
                if response.startswith('__'):
                    operation(response)
                else:
                    print(f"Chatbot {response}")
                    TTS(response)

        except sr.WaitTimeoutError:
            print(".")
            oled.blink()
            emotions.emotions("idle")
            stop_timer -= 1
            if stop_timer == 0:
                break
            continue
        except sr.UnknownValueError:
            response = "Sorry, I couldn't understand you." if respect >= 50 else "Could you repeat that?"
            display("Confused")
            print(f"Chatbot: {response}")
            #TTS(response)

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
        if not wifi.connectivity():
            oled.display("Connect your wifi!")
            print("Connect your wifi!")
            continue

        print(f"Say 'Hey {Name}!'")
        try:
            if sensor.check_temp():
                response = "Temperature too high"
                print(f"Chatbot: {response}")
                TTS(response)

            if not speaking:
                audio = recognizer.listen(source, timeout = 5)
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
            #elif user_input.lower() in ["stop", "shutdown"]:
                #response = "Shutting down."
                #print(response)
                #TTS(response)
                #break

        except sr.WaitTimeoutError:
            print(".")
            oled.blink()
            emotions.emotions("idle")
            continue
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
            break
        except KeyboardInterrupt:
            print("Stopping...")
            break

def run():
    print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        print("Initializing ambient noise cancellation...")
        recognizer.adjust_for_ambient_noise(source, duration = 5)
        servo.init()
        oled.blink()
        emotions.emotions("idle")
        print("----- Ready to go -----")
        start()
        servo.init()
        display("Neutral")

if __name__ == "__main__":
    print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        print("Initializing ambient noise cancellation...")
        recognizer.adjust_for_ambient_noise(source, duration = 5)
        servo.init()
        oled.blink()
        emotions.emotions("idle")
        print("----- Ready to go -----")
        start()
        servo.init()
        display("Neutral")