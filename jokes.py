import random
import pyjokes


def get_joke():

    try:

        return pyjokes.get_joke(
            language="en",
            category="neutral"
        )

    except Exception:

        fallback_jokes = [

            "I would tell you a computer joke, sir, but it might need a byte.",

            "There are only 10 kinds of people, sir. Those who understand binary and those who do not.",

            "Sir, I have a joke about UDP, but you might not get it."
        ]

        return random.choice(
            fallback_jokes
        )


def should_tell_joke(
    probability
):

    return random.random() < probability