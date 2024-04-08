from sentiment_analysis.sentiment_analysis import sentiment_analysis, partial_sentiment_analysis
from speech_to_text.speech_to_text import speech_to_text
from speech_to_text.anonymizer import anonymize_text

from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os
from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    """Parse arguments list"""
    parser = ArgumentParser(__name__)
    parser.add_argument('--full_analysis', type=bool, default=True, help='whether to to speech or text '
                                                                         'sentiment analysis')
    parser.add_argument('--data_directory', type=Path, default='./data', help='the path to the audios from root dir')

    parser.add_argument('--partial', type=bool, default=True, help='the path to the audios from root dir')

    return parser.parse_args()


def speech_sentiment(file_paths: List, partial: bool):

    translations = speech_to_text(file_paths)
    anonymized = anonymize_text(translations)
    if partial:
        return partial_sentiment_analysis(anonymized)
    else:
        return sentiment_analysis(anonymized)


def text_sentiment(scripts: List, partial: bool):

    anonymized = anonymize_text(scripts)

    if partial:
        return partial_sentiment_analysis(anonymized)
    else:
        return sentiment_analysis(anonymized)


if __name__ == '__main__':
    load_dotenv()
    args = parse_arguments()
    full_analysis = args.full_analysis

    if full_analysis:
        file_paths = os.listdir(args.data_directory)
        file_paths = [Path(args.data_directory / i) for i in file_paths]
        resutls = speech_sentiment(file_paths, args.partial)
    else:
        scripts = ['', '']
        results = text_sentiment(scripts, args.partial)
