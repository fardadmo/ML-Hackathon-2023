"""
The dashboard app for our sentiment analysis pipeline
"""
import streamlit as st
import os
from pathlib import Path
from yaml import safe_load
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from typing import List, Dict
from argparse import ArgumentParser, Namespace

from main import speech_sentiment, text_sentiment


def parse_arguments() -> Namespace:
    """Parses the input arguments from the terminal
    :return: parsed arguments
    """
    parser = ArgumentParser(__name__)
    parser.add_argument('--config_path', type=Path, help='Path to streamlit app config file')

    return parser.parse_args()


def load_yaml_config(config_path: Path) -> Dict:
    """Load YAML config file and return a parsed, ready to consume, dictionary
    :param config_path: location of the config file
    :return: config dictionary
    """
    with config_path.open(mode='r') as stream:
        config = safe_load(stream)
    return config


def main(arguments_list: Namespace) -> None:
    """
    runs the dashboard app
    :param arguments_list: the list of arguments
    :return: n/a
    """
    if arguments_list.config_path is not None:
        config_path = Path(__file__).parent / arguments_list.config_path
        config = load_yaml_config(config_path=config_path)
    else:
        # Added to solve the error caused by docker
        arguments_list.config_path = "config.yaml"
        config_path = Path(__file__).parent / arguments_list.config_path
        config = load_yaml_config(config_path=config_path)
    
    dashboard_configs = config.get('DASHBOARD_CONFIG')
    upload_folder= dashboard_configs.get('UPLOADFOLDER')

    st. set_page_config(layout="wide")
    st.subheader("Linguistic Understanding and Management for Outstanding Service (LUMOS)")
    st.sidebar.image("./assets/LUMOS_logo.png", use_column_width=True)
    st.sidebar.subheader("AltaML Hackathon - 2023")
    st.sidebar.subheader("Team Scale")
    st.sidebar.write("Danhong Tang, Fardad Mokhtari, Han Wang, Sara Naseri Golestani, Shea McCormack")
    st.sidebar.write("Mentor: Colby Armstrong")
    text_to_num = {'positive': 1, 'neutral': 0, 'negative': -1}
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['#7ab089', '#e5d9b8', '#d3aeb0']

    tab_audio, tab_text = st.tabs(["Audio-based Analysis", "Text-based Analysis"])

    with tab_text:
        text = st.text_input('Text here: ')
        text_list = [text]
        # Create a button to initiate sentiment analysis
        if st.button("Analyze Sentiment", key=0):
            if not text:
                st.error("Please provide the text.")
            else:
                text_results = text_sentiment(text_list, True)
                for idx, doc in enumerate(text_results):
                    if len(doc)<=1:
                        sequence_analysis = False
                    else:
                        sequence_analysis = True

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader('Overall Sentiment Analysis')
                        Full_text_result = text_sentiment(text_list, False)
                        if Full_text_result[0].confidence_scores.negative >= 0.5:
                            st.error(":rage: The overall sentiment of text is negative.")
                        elif Full_text_result[0].sentiment == 'positive':
                            st.success(":smiley: The overall sentiment of text is positive.")
                        elif Full_text_result[0].sentiment == 'negative':
                            st.error(":rage: The overall sentiment of text is negative.")
                        else:
                            st.warning(":confused: The overall sentiment of text is neutral.")
                        fig, ax = plt.subplots()
                        sentiment_mark = [Full_text_result[0].confidence_scores.positive, Full_text_result[0].confidence_scores.neutral, Full_text_result[0].confidence_scores.negative]
                        pie = ax.pie(sentiment_mark, labels=labels, autopct='%1.1f%%', colors=colors)
                        st.pyplot(fig)

                    if sequence_analysis == True:
                        sentiment_sequence = []
                        with col2:
                            st.subheader('Sequencial Sentiment Analysis')
                            for portion_index in range(len(doc)):
                                portion_results = doc[portion_index]
                                sentiment_sequence.append(portion_results.sentiment)
                            sentiment_sequence = [val.replace("mixed", "neutral") for val in sentiment_sequence]
                            encoded_list = [text_to_num[sent] for sent in sentiment_sequence]
                            # Define colors for negative and positive values
                            colors = ['#ffeded' if val < 0 else '#ebfaee' for val in encoded_list]
                            fig, ax = plt.subplots()
                            ax.bar(range(len(encoded_list)), encoded_list, color=colors)
                            ax.set_xlabel('Text Portion')
                            ax.set_ylabel('Sentiment')
                            ax.set_yticklabels(['negative', 'neutral', 'positive'])
                            ax.set_yticks([-1, 0, 1])
                            ax.set_ylim(-1.5,1.5)
                            ax.set_xticks(range(len(encoded_list)))
                            st.pyplot(fig)
                    else:
                        with col2:
                            st.subheader('Sequencial Sentiment Analysis')
                            st.warning("The length of text is not enough for sequencial analysis.")
                    

    with tab_audio:
        # Set up a folder to save uploaded audio files
        file_paths =[]
        audiofile_names = []

        st.set_option('deprecation.showfileUploaderEncoding', False)

        # Allow the user to select multiple audio files
        audio_files = st.file_uploader("Select audio files", type=["mp3", "wav"], accept_multiple_files=True)

        # If the user has uploaded audio files, display them and save them to the uploaded_files directory
        if audio_files:
            os.makedirs(upload_folder, exist_ok=True)
            for audio_file in audio_files:
                audio_bytes = audio_file.read()
                st.write(f"Playing {audio_file.name}")
                st.audio(audio_bytes, format="audio/wav")
                
                # save the audio file to the output directory
                file_paths.append(os.path.join(upload_folder, audio_file.name))
                audiofile_names.append(audio_file.name)
                with open(os.path.join(upload_folder, audio_file.name), 'wb') as f:
                    f.write(audio_bytes)

        # Create a button to initiate sentiment analysis
        if st.button("Analyze Sentiment", key=1):

            # If no audio file is uploaded, display an error message
            if audio_file is None:
                st.error("Please upload an audio file to analyze.")
            else:
                audio_results = speech_sentiment(file_paths, True)
                for idx, doc in enumerate(audio_results):
                    st.header(f"Analyzing {audiofile_names[idx]}")
                    if len(doc)<=1:
                        sequence_analysis = False
                    else:
                        sequence_analysis = True

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader('Overall Sentiment Analysis')
                        Full_audio_result = speech_sentiment([file_paths[idx]], False)
                        if Full_audio_result[0].confidence_scores.negative >= 0.5:
                            st.error(":rage: The overall sentiment of text is negative.")
                        elif Full_audio_result[0].sentiment == 'positive':
                            st.success(":smiley: The overall sentiment of text is positive.")
                        elif Full_audio_result[0].sentiment == 'negative':
                            st.error(":rage: The overall sentiment of text is negative.")
                        else:
                            st.warning(":confused: The overall sentiment of text is neutral.")
                        fig, ax = plt.subplots()
                        sentiment_mark = [Full_audio_result[0].confidence_scores.positive, Full_audio_result[0].confidence_scores.neutral, Full_audio_result[0].confidence_scores.negative]
                        pie = ax.pie(sentiment_mark, labels=labels, autopct='%1.1f%%', colors=colors)
                        st.pyplot(fig)

                    if sequence_analysis == True:
                        sentiment_sequence = []
                        with col2:
                            st.subheader('Sequencial Sentiment Analysis')
                            for portion_index in range(len(doc)):
                                portion_results = doc[portion_index]
                                sentiment_sequence.append(portion_results.sentiment)
                            sentiment_sequence = [val.replace("mixed", "neutral") for val in sentiment_sequence]
                            encoded_list = [text_to_num[sent] for sent in sentiment_sequence]
                            fig, ax = plt.subplots()
                            ax.bar(range(len(encoded_list)), encoded_list)
                            ax.set_xlabel('Text Portion')
                            ax.set_ylabel('Sentiment')
                            ax.set_yticklabels(['negative', 'neutral', 'positive'])
                            ax.set_yticks([-1, 0, 1])
                            ax.set_ylim(-1.5,1.5)
                            ax.set_xticks(range(len(encoded_list)))
                            st.pyplot(fig)
                    else:
                        with col2:
                            st.subheader('Sequencial Sentiment Analysis')
                            st.warning("The length of audio is not enough for sequencial analysis.")


if __name__ == "__main__":
    
    load_dotenv()
    args = parse_arguments()
    main(args)
