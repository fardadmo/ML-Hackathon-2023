"""
The purpose of this script is to convert a given audio file of a conversation to text
this conversion is being done with the help of azure cognitive services
"""
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
from typing import List
import datetime

# Load the .env file
load_dotenv()


def speech_to_text(filenames: List) -> List:
    """
    calling the speechsdk and start the conversion
    :param filenames: a list of audio file names existing under data/ directory
    :return: a list of strings of all the converted audios.
    """
    # Access your credentials from the os.environ dictionary
    service_key = os.environ.get('SPEECH_KEY')
    service_region = os.environ.get('SPEECH_REGION')
    results = []

    speech_config = speechsdk.SpeechConfig(subscription=service_key, region=service_region)
    speech_config.initial_silence_timeout = datetime.timedelta(seconds=25)
    speech_config.end_silence_timeout = datetime.timedelta(seconds=25)
    speech_config.stable_audio_duration = datetime.timedelta(seconds=70)

    # this process is done in a for loop and the converted results will be appended to the
    # results list at the end of the loop
    for file in filenames:

        audio_config = speechsdk.AudioConfig(filename=str(file))
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                       audio_config=audio_config)

        result = speech_recognizer.recognize_once()
        results.append(result.text)
        print(result.text)

    return results


if __name__ == '__main__':
    """
    This part of the function is just the local tests for each function to evaluate it's functionality
    """

    _filenames = ['GoodRepContinuous.wav', 'BadRepCont.wav', 'MockCustomer.wav',
                  'GoodRep.wav']
    _results = speech_to_text(_filenames)
    print(_results)
