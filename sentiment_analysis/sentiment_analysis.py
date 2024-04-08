"""
The purpose of this script is to analyse the sentiment of the given string
the conversation in this step is a text. it can be the outcome of the speech-to-text or a plain text of a conversation
This analysis is being done both partially and regularly.
"""

from dotenv import load_dotenv
import os
from typing import List

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def _get_client():

    """
    To get the API client for sentiment analysis
    :return: the text analysis client
    """
    endpoint = os.environ.get('SENTIMENT_ENDPOINT')
    key = os.environ.get('SENTIMENT_KEY')
    credential = AzureKeyCredential(key)
    return TextAnalyticsClient(endpoint=endpoint, credential=credential)


def sentiment_analysis(document: List) -> List:
    """
    analyse the sentiment of the given string of each conversation inside
    :param document: a list of docs
    :return: a list of doc analysis
    """

    text_analytics_client = _get_client()
    response = text_analytics_client.analyze_sentiment(documents=document)

    for idx, doc in enumerate(response):
        print("Document text: {}".format(document[idx]))
        print("Overall sentiment: {}".format(doc.sentiment))
        print("Positive score: {}".format(doc.confidence_scores.positive))
        print("Neutral score: {}".format(doc.confidence_scores.neutral))
        print("Negative score: {}".format(doc.confidence_scores.negative))

    return response


def partial_sentiment_analysis(document: List) -> List:
    """
    Partial analyse the sentiment of the given string of each conversation inside
    :param document: a list of docs
    :return: a list of doc analysis
    """

    text_analytics_client = _get_client()
    responses = []
    for doc in document:
        n = len(doc)
        if n > 250 and len(doc.split('.')) > 10:
            pointer = int(n/4)
            doc_list = [doc[:pointer], doc[pointer:pointer*2], doc[pointer*2:pointer*3], doc[pointer*3:n]]
            response = text_analytics_client.analyze_sentiment(documents=doc_list)
        else:
            response = text_analytics_client.analyze_sentiment(documents=[doc])

        for idx, doc in enumerate(response):

            print("Overall sentiment: {}".format(doc.sentiment))
            print("Positive score: {}".format(doc.confidence_scores.positive))
            print("Neutral score: {}".format(doc.confidence_scores.neutral))
            print("Negative score: {}".format(doc.confidence_scores.negative))

        responses.append(response)
    return responses


if __name__ == '__main__':
    """
     This part of the function is just the local tests for each function to evaluate it's functionality
     """
    load_dotenv()
    _documents = [
       'Document text: Hello . Thank you for calling [PERSON] [PERSON] . '
       'My name is [GPE] . How may I help you today ? No , Sir , My name is [GPE] .'
       ' That ’s quite all right , Sir . How may I assist you ? All right , '
       'Sir . Let me see if I can help you with that . May I have your telephone number ,'
       ' please ? Thank you , Sir . And may I please have your first and last name . '
       'The spelling is English . Like the language , Sir . OK . Mr. [PERSON] , '
       'could you please verify your date of birth ? Thank you , Sir . June 10th , 1998 . '
       'I am pulling up your account .', ' How may I help you today ? No , Sir , My name is [GPE] .'
       ' That ’s quite all right , Sir . How may I assist you ? All right , '
       'Sir . Let me see if I can help you with that . May I have your telephone number ,'
       ' please ?'
    ]
    # _partial_analysis = partial_sentiment_analysis(_documents)
    _output = sentiment_analysis(_documents)
