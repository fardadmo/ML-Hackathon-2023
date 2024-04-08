"""
We are using a pre-built nlp model to detect personal information in a conversation and clear them for the
purpose of privacy and security
"""

import re
import spacy
from typing import List

_nlp = spacy.load('en_core_web_sm')


def anonymize_text(results: List) -> List:
    """
    this function will filterout the personal information and outputs an anonymous conversation
    :param results: a list of text documents
    :return: a list of anonymized texts
    """
    anonymized = []
    for text in results:
        doc = _nlp(text)
        anonymized_text = []
        for token in doc:
            if token.ent_type_ == 'PERSON':
                anonymized_text.append('[PERSON]')

            elif token.ent_type_ == 'ORG':
                anonymized_text.append('[ORG]')

            elif token.ent_type_ == 'GPE':
                anonymized_text.append('[GPE]')

            elif re.match(r'\d{10}', token.text):
                anonymized_text.append('[PHONE]')

            elif re.match(r'\(\d{3}\)\s?\d{3}\-\d{4}|\d{3}\.\d{3}\.\d{4}|\d{3}\-\d{3}\-\d{4}', token.text):
                anonymized_text.append('[PHONE]')

            elif re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', token.text):
                anonymized_text.append('[EMAIL]')

            elif re.match(r'\d{2}\/\d{2}\/\d{4}', token.text):
                anonymized_text.append('[DOB]')

            elif token.text.lower() in ['male', 'female', 'non-binary']:
                anonymized_text.append('[GENDER]')

            elif re.match(r'\d{1,5}\s\w+\s\w+', token.text):
                anonymized_text.append('[ADDRESS]')

            else:
                anonymized_text.append(token.text)

        anonymized.append(' '.join(anonymized_text))

    return anonymized


if __name__ == "__main__":
    """
      This part of the function is just the local tests for each function to evaluate it's functionality
      """
    _text = ["Hello, this is Fardad. I am from Calgary, Canada and my phone number is 7807167473 my email is"
             " fardadmokhtari@gmail.com and my date of birth is 03/14/1996."]
    print(anonymize_text(_text))
