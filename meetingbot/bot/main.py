from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyaudio
import wave
import os
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
class MyBot:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        
        # Set Chrome options for headless mode
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        print("Driver initialized")

    def take_screenshot(self, step):
        """Takes a screenshot and saves it with a step name."""
        filename = f"screenshot_{step}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")

    def open_meeting(self, link):
        """Opens Google Meet link in headless mode."""
        self.driver.get(link)
        print("Opened Google Meet link")
        self.take_screenshot("opened_meeting")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'join')]")))

    def join_now(self):
        try:
            join_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'join')]"))
            )
            join_button.click()
            print("Clicked join now")
        except Exception as e:
            print(f"Failed to join: {e}")

    def fill_name(self, name):
        try:
            name_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Your name']"))
            )
            name_input.send_keys(name)
        except Exception as e:
            print(f"Failed to fill name: {e}")

    def turn_off_mic_cam(self):
        try:
            mic_button = self.driver.find_element(By.XPATH, '//div[contains(@data-tooltip, "Turn off microphone")]')
            mic_button.click()
            cam_button = self.driver.find_element(By.XPATH, '//div[contains(@data-tooltip, "Turn off camera")]')
            cam_button.click()
            print("Turned off mic and camera")
        except Exception as e:
            print(f"Failed to turn off mic/cam: {e}")

    def send_welcome_message(self):
        try:
            message_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Chat with everyone")]'))
            )
            message_button.click()
            message_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//textarea[contains(@placeholder, "Send a message")]'))
            )
            message_input.send_keys(
                "Welcome to Google Meet chatbot! Your smart meeting assistant is here to streamline scheduling and discussions."
            )
            send_button = self.driver.find_element(By.XPATH, '//button[contains(@aria-label, "Send a message")]')
            send_button.click()
            print("Sent welcome message")
        except Exception as e:
            print(f"Failed to send welcome message: {e}")

    def leave_meeting(self):
        try:
            leave_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Leave call")]'))
            )
            leave_button.click()
            print("Left the meeting")
        except Exception as e:
            print(f"Failed to leave meeting: {e}")

    def record_and_recognize(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 48000
        RECORD_SECONDS = 20

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []

        print("Recording started")
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Recording finished")

        stream.stop_stream()
        stream.close()
        p.terminate()

        filename = "output.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(filename) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return text
        except (sr.UnknownValueError, sr.RequestError) as e:
            print(f"Speech recognition error: {e}")
        finally:
            pass
            # if os.path.exists(filename):
            #     os.remove(filename)
            
            
    def UsersAvailability(self):
        try:
            # Locate the "People" button that contains the participant count
            user_count_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div[34]/div[4]/div[10]/div/div/div[3]/div/div[2]/div/div/div'))
            )
            user_count_text = user_count_element.text.strip()
            print(f"User count: {user_count_text}",type(user_count_text))
            return int(user_count_text)

        except Exception as e:
            print(f"Error retrieving participant count: {e}")
            return 0

    def geminiOptimisation(self, data):
        prompt = '''You are an AI assistant designed to analyze meeting recordings. Given a meeting transcript, perform the following tasks:  

                    1. **Meeting Transcription**: Provide a well-structured and accurate transcription of the entire meeting.  

                    2. **Meeting Summary**: Generate a concise summary of the key topics, decisions made, and important points discussed in the meeting. Make it no longer than 100 words.  

                    3. **Highlight Extraction**: Identify and list key highlights or actionable points from the meeting. These should include important questions, decisions, tasks assigned, deadlines, or agreements made during the discussion.  

                    Input:  
                    [Insert the entire meeting transcript text here]  

                    Output Format:  
                    - **Full Transcription**: [Include the transcription here.]  
                    - **Meeting Summary**: [Include the summary here.]  
                    - **Key Highlights**:  
                    - [Point 1]  
                    - [Point 2]  
                    - [Point 3]  
'''

        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt +" and here's the meeting transcript"+ data)
        print(response.text)
        return response.text



    def join_and_record_meeting(self, link):
        """Main function to join the meeting and handle interactions."""
        try:
            self.open_meeting(link)
            self.turn_off_mic_cam()
            self.fill_name("Shubham")
            self.join_now()
            self.send_welcome_message()

            # Check if total users exceed 2, wait up to 60 seconds
            max_wait_time = 60
            check_interval = 5
            waited_time = 0

            while waited_time < max_wait_time:
                totalUsers = self.UsersAvailability()
                print(f"Total users in the meeting: {totalUsers}")
                if totalUsers > 2:
                    break
                time.sleep(check_interval)
                waited_time += check_interval

            if totalUsers <= 2:
                print("Not enough users in the meeting. Leaving now.")
                self.leave_meeting()
                data = {"transcript": "", "summary": "Not enough participants in the meeting."}
                return data

            # Proceed with recording and summarizing
            finalText = self.record_and_recognize()
            print("join_and_record_meeting text", finalText)
            if finalText:
                summary = self.geminiOptimisation(finalText)
                time.sleep(10)
                self.leave_meeting()
                data = {"transcript": finalText, "summary": summary}
                return data
            else:
                data = {"transcript": "", "summary": "No transcript available."}
                return data

        finally:
            self.driver.quit()
            print("Driver session closed")
