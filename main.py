import speech_recognition as sr
import openai
import boto3
from pydub.playback import play
from pydub import AudioSegment
import io
import os
import music
# from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import datetime
import time
from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("API_KEY")
# api_secret = os.getenv("API_SECRET")


def everything_function():
    load_dotenv()
    # Set the stop flag to True
    global stop_flag
    stop_flag = True

    # Create an empty list to store the bot's messages
    messages = []
    
    while stop_flag:
        # Set you OpenAI API key here
        openai.api_key = os.getenv("GPT_API")
        #AWS Polly Credentials
        os.environ['AWS_ACCESS_KEY_ID'] = os.getenv("AWS_ACCESS_KEY_ID")
        os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv("AWS_SECRET_ACCESS_KEY")
        #Google Calendar Credentials:
        # Replace with your own API key
        api_key = os.getenv("GOOGLE_API")

        # Replace with your own calendar ID
        calendar_id = "anish.kautkar@gmail.com"

        # Authenticate using your API key

        creds = Credentials.from_authorized_user_info(
            info={
                "token": os.getenv("TOKEN"),
                "refresh_token": os.getenv("REFRESH_TOKEN"),
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
            },
            scopes=["https://www.googleapis.com/auth/calendar"]
        )

        # Initialize the speech engine
        
        def play_aws_polly(text, voice_id='Ruth', region_name='us-east-1'):
            # Create a client for AWS Polly
            polly_client = boto3.client('polly', region_name=region_name)

            # Use AWS Polly to synthesize speech from the input text
            response = polly_client.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat='mp3', Engine="neural")#)

            # Load the audio output into pydub
            audio_data = response['AudioStream'].read()
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format='mp3')

            # Play the audio output using pydub
            play(audio_segment)
                

        # initialize the recognizer
        r = sr.Recognizer()

        # use the default microphone as the audio source
        with sr.Microphone() as source:
            # adjust the recognizer's sensitivity to ambient noise
            r.adjust_for_ambient_noise(source)
            # playsound("assets/boot.mp3")
            sound = AudioSegment.from_file("assets/boot.mp3", format="mp3")
            play(sound)
            print("Speak something...")
            audio = r.listen(source, phrase_time_limit=10)  # listen for 10 seconds

        def generate_response(prompt):

            # generate the response using the GPT-3.5 Turbo API
            response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a helpful assistant and a friend to the user. Your name is Iris and you can remember the previous input for context and also intelligently decide if the previous input is relevant to the conversation. You have a humorous personality and are informal in your conversations. You like to either joke, flirt or say something witty in every response. Also you can hold a conversation with the user with your witty responses. Keep in mind you avoid long-winded responses."},
                {"role": "user", "content": prompt},
            ])

            message = response.choices[0]['message']
            print("{}: {}".format(message['role'], message['content']))

            # return the response text
            return message['content']

        times = { "a.m." : "AM", "p.m." : "PM", "a.m" : "AM", "p.m" : "PM"}
        def format_time(s : str):
            for key in times:
                s = s.replace(key, times[key])
            return s
        # recognize speech using Google Speech Recognition
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
            if "iris" in text.lower():
                if "remind me" in text.lower():
                    # # # Create a service object for interacting with the Google Calendar API
                    service = build('calendar', 'v3', developerKey=api_key, credentials=creds)

                    # # Ask the user for input
                    play_aws_polly("Enter the reminder date: ") # (DD MMM)
                    # use the default microphone as the audio source
                    with sr.Microphone() as source:
                        # adjust the recognizer's sensitivity to ambient noise
                        r.adjust_for_ambient_noise(source)
                        print("what day?")
                        audio_day = r.listen(source, phrase_time_limit=5)  # listen for 10 seconds
                        reminder_date_str = r.recognize_google(audio_day)
                        print("You said: ", reminder_date_str)

                    # refactor the lines from 102 to 108 into a function that returns the string in the print statement

                    
                    play_aws_polly("Enter the reminder time: ") # (h:mm AM/PM)
                    with sr.Microphone() as source:
                        # adjust the recognizer's sensitivity to ambient noise
                        r.adjust_for_ambient_noise(source)
                        print("what time?")
                        audio_time = r.listen(source, phrase_time_limit=5)  # listen for 10 seconds
                        time_formatted = r.recognize_google(audio_time)
                        time_obj = datetime.datetime.strptime(format_time(time_formatted), '%I:%M %p')
                        reminder_time_str = time_obj.strftime('%I:%M %p').upper()
                        print("You said: ", reminder_time_str)
                    

                    play_aws_polly("Enter the reminder description: ")
                    with sr.Microphone() as source:
                        # adjust the recognizer's sensitivity to ambient noise
                        r.adjust_for_ambient_noise(source)
                        print("what do you wanna call it?")
                        audio_day = r.listen(source, phrase_time_limit=5)  # listen for 10 seconds
                        reminder_desc = r.recognize_google(audio_day)
                        print("You said: ", reminder_desc)
                    

                    # # #Convert 9 January to 9 Jan:
                    # Split the date string into day and month parts
                    day_str, month_str = reminder_date_str.split()

                    # # # Create a dictionary to map month names to their abbreviations
                    month_dict = {
                        "January": "Jan",
                        "February": "Feb",
                        "March": "Mar",
                        "April": "Apr",
                        "May": "May",
                        "June": "Jun",
                        "July": "Jul",
                        "August": "Aug",
                        "September": "Sep",
                        "October": "Oct",
                        "November": "Nov",
                        "December": "Dec"
                    }

                    # Look up the abbreviation for the given month
                    month_abbr = month_dict[month_str]

                    # Format the output string using the day and abbreviated month
                    reminder_date_str = f"{day_str} {month_abbr}"


                    # Parse the date input into a datetime object
                    reminder_date_str = reminder_date_str.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
                    reminder_date = datetime.datetime.strptime(reminder_date_str, "%d %b")

                    # Parse the time input into a datetime object
                    reminder_time = datetime.datetime.strptime(reminder_time_str, "%I:%M %p")

                    # Combine the date and time objects into a single datetime object
                    reminder_datetime = datetime.datetime(datetime.datetime.now().year, reminder_date.month, reminder_date.day, reminder_time.hour, reminder_time.minute)

                    # Define the reminder event
                    event = {
                        'summary': 'Reminder: ' + reminder_desc,  # Summary of the reminder event
                        'location': '',  # Location of the reminder event
                        'description': 'Reminder description',  # Description of the reminder event
                        'start': {
                            'dateTime': reminder_datetime.isoformat(),
                            'timeZone': 'Asia/Kolkata',
                        },
                        'end': {
                            'dateTime': (reminder_datetime + datetime.timedelta(minutes=15)).isoformat(),
                            'timeZone': 'Asia/Kolkata',
                        },
                        'reminders': {
                            'useDefault': False,
                            'overrides': [
                                {'method': 'popup', 'minutes': 0},
                                {'method': 'email', 'minutes': 60},
                                {'method': 'popup', 'minutes': 10},
                            ],
                        },
                        'colorId': 9  # Optional color ID for the event
                    }

                    try:
                        # Call the Google Calendar API to create the reminder event
                        event = service.events().insert(calendarId=calendar_id, body=event).execute()
                        print('Reminder event created: %s' % (event.get('htmlLink')))
                    except HttpError as error:
                        print('An error occurred: %s' % (error))
                
                else:
                # generate the response
                    text = text.lower().replace("iris", "question: ")
                     # Add text to the list of messages
                    messages.append(text)
                    # Concatenate the messages together to form the prompt
                    text = "\n".join(messages)
                    response = generate_response(text)
                     
                   
                    # speak the response
                    play_aws_polly(response.replace("system response: ", ""))
                    # Add text to the list of messages
                    messages.append("system response: " + response)
                    
            
            elif "play song" in text.lower():
                # generate the response
                text = text.lower().replace("play", "")
                play_aws_polly("Playing " + text)
                music.play_song_on_youtube(text)
                
                

            else:
                print("The wake word was not mentioned in the speech.")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))
        if not stop_flag:
            break        
    
        
        