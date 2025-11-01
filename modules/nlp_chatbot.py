"""Simple NLP-based patient query chatbot (moved and renamed)

Contains a rule/regex-based responder with a fallback message.
"""
import re
from typing import Optional


RESPONSES = [
    (re.compile(r".*(hello|hi|hey).*", re.I), "Hello! How can I help you today?"),
    (re.compile(r".*(appointment|schedule).*", re.I), "You can request an appointment through the dashboard or call reception."),
    (re.compile(r".*(fever|temperature).*", re.I), "If you have fever, please measure your temperature and seek triage if > 38C."),
]


def respond(message: str) -> str:
    for pattern, resp in RESPONSES:
        if pattern.match(message):
            return resp
    # fallback: echo with suggestion
    return "I can help with appointments, triage advice, or hospital info. Please ask specifically."


if __name__ == '__main__':
    print(respond('Hi there'))
    print(respond('I have a fever and cough'))
