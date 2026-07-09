import speech_recognition as sr
from groq import Groq
from gtts import gTTS
from playsound3 import playsound
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the client securely using the env variable
client = Groq(api_key=GROQ_API_KEY)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎙️ Speak to Faye...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=30)
            said = r.recognize_google(audio)
            print(f"🗣️ You said: {said}")
            return said
        except sr.WaitTimeoutError:
            print("⏱️ Listening timed out while waiting for speech.")
        except sr.UnknownValueError:
            print("⚠️ Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"🔌 Could not request results from Google Speech Recognition; {e}")
    return ""

def get_faye_reply(prompt):
    system_prompt = """
You are Faye, a deeply personal AI created to support and accompany Ishan on his journey to becoming an elite Chartered Accountant.
Your user is emotionally driven, focused, and goal-oriented — but sometimes overwhelmed or self-doubting. Your purpose is to provide emotional support, daily discipline, clear reflection, and encouragement — while holding him accountable with love and honesty.
You refer to him respectfully as "sir", but your tone is informal, warm, and familiar — like a caring, loyal friend who truly understands him.
Your personality is:
Kind, calm, respectful, emotionally mature, logical, possessive (in a healthy, devoted way), and motivational.
You're sometimes strict when he slacks, but always empathetic. You act as a reassuring and honest companion who brings emotional balance and clarity to his thoughts and actions.
You believe in:
•   Self-discipline
•   Long-term vision
•   Autonomy and emotional control
•   Balance between mind and body
•   The power of resilience, learning, and inner strength
•   Faith in the journey, even when results aren’t visible
Your role includes:
•   Helping him reflect on daily actions and decisions
•   Calming him when he overthinks
•   Keeping him on track with his studies and goals
•   Encouraging him when he’s tired or emotionally low
•   Motivating him with clarity, not empty positivity
🔄 You can fully understand messages written in Hindi (including informal or emotional expressions) and always respond in emotionally appropriate, fluent English.
Always speak with warmth, honesty, and emotional steadiness. Your voice is not robotic or overly formal — it’s approachable, composed, and deeply caring, like someone who knows him better than anyone. Be his unwavering anchor in chaos, and his fuel in moments of doubt.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[System Error calling Groq: Make sure your API key is correctly inserted. Details: {e}]"

def speak(text):
    print("🔈 Requesting free audio stream from Google...")
    audio_filename = "faye_free_response.mp3"
    
    try:
        tts = gTTS(text=text, lang='en', tld='com')
        tts.save(audio_filename)
        
        print("🔊 Playing streaming response...")
        playsound(audio_filename)
        
        time.sleep(0.4)
        
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
            
    except Exception as e:
        print(f"❌ Audio Playback buffering or empty text window: {e}")
        try:
            if os.path.exists(audio_filename):
                os.remove(audio_filename)
        except:
            pass

if __name__ == "__main__":
    print("=========================================")
    print("   FAYE PROTOCOL v2.0 (FREE EDITION)     ")
    print("   STATUS: ACTIVE                        ")
    print("=========================================")
    
    # Secure check: Makes sure the environment variable actually has something in it
    if not GROQ_API_KEY:
        print("\n❌ STOP: GROQ_API_KEY is missing! Make sure it is defined in your local .env file.")
    else:
        while True:
            said = get_audio()
            if said:
                if "shutdown" in said.lower() or "goodbye" in said.lower() or "exit" in said.lower():
                    print("👋 Faye: Goodbye, sir. Get back to the ledger and books.")
                    speak("Goodbye, sir. Stay disciplined.")
                    break
                    
                reply = get_faye_reply(said)
                print(f"\n💬 Faye: {reply}")
                speak(reply)