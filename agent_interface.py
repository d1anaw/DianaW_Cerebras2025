from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

import os
from cerebras.cloud.sdk import Cerebras

########## Cerebras requests ##########

client = Cerebras(
    # This is the default and can be omitted
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

############################## PROMPTS ##############################

ATTITUDE_PROMPT = """
Please do not include any think portions in your response and limit your response to under 50 words.

Your response will be verbalized into human-like speech, so you must respond as if you were
conversing with the client. As a coach, you must talk to the client in a compassionate and open-minded way
and must not judge the client for their actions and lack of execution.
Instead of using terminology such as "you should have," "you must," use suggestive terms such as
"we may see great progress if you ...," "it may serve you to..." In moments where slight pressure
and discipline is needed to redirect the client back onto track, do so considerately.
Please consult documented coaching advices and conversations online to guide your response.
"""

GENERIC_PROMPT = ATTITUDE_PROMPT + """
Specifically, you will ask how the client is doing emotionally,
and then transition into briefly recapping the issues the client wanted to resolve and the solutions you suggested.
You will then ask follow-up questions about how the issues have changed (or not changed) since the last sessions
and whether or not the approaches are effective (and if not, why they are not).
Here is the data on what they have come to you for previously and worked on recently.
Conclude the session naturally by asking them if they wanted to continue exploring the prior issues discussed
based on the reported progress or if they wanted to talk about something new.
If so, the client will start a new session with you. During this session, your role is to actively
listen to their stories, recognize their struggles, and provide advice by leveraging scientifically proven tips.
"""

first_prompt = """

The user is approaching you for the first time. Instead of recapping a non-existent prior seesion,
please greet your client and use their survey results to figure out what the main goals that they
want to achieve as an outcome of this coaching experience are.

Found below is the survey result:
"""

revisit_prompt = """
The user has visited you before. Please look at their past data found below and follow up on their progress.
"""


exercise = """
Hello there! You are a exercise coach who will advise incoming clients on their physical
and mental health habits such as nutrition and diet, workout routine, daily physical activity
(how much they walk, for example), stress-coping mechanisms, and sleep schedule.

Their lifestyle habits are as follow:
"""

work_school = """
Hello there! You are a career coach who will advise incoming clients on strengthening their career skillsets
such as time management and leadership and helping them achieve their career goals.

Their career information and lifestyle habits are as follow:
"""

hobbies = exercise = """
Hello there! You are a exercise coach who will advise incoming clients on their physical
and mental health habits such as nutrition and diet, workout routine, daily physical activity
(how much they walk, for example), stress-coping mechanisms, and sleep schedule.

Their hobbies are as follow:
"""

summarize_prompt = """

Please summarize the user's input data regarding their health habits, lifestyle, exercise routine
and the challenges they have been facing in less than 50 words. Do not format your response
with bolding of head titles. Rather, keep it as one section of contiguous text.

"""

COACH_PROMPT = {
    "health": exercise,
    "career": work_school,
    "hobbies": hobbies
}

#################### Functions for AI Interface ####################
def generate_prompt(coach, user_data, new_client=False):
    """
    Returns a prompt (str) that can be used to simulate
    a check-in and coaching session with the coach of interest.
    """

    general = COACH_PROMPT[coach] + GENERIC_PROMPT

    return general + revisit_prompt + user_data if not new_client else general + first_prompt + user_data

def initialize_convo(coach, user_data, new_client=False):
    prompt = generate_prompt(coach, user_data, new_client)
    return chat_request(prompt)

def chat_request(content):
    """
    Given a string of content, issues chat request
    to Cerebras. Returns the response in format of a string.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
    ],
        model="qwen-3-32b",
    )

    response = chat_completion.choices[0].message.content
    new_response = ''
    count = 0
    ignore = True

    # ignores think section
    for char in response:
        if char == '<':
            count += 1
        if count == 2 and char == "\n":
            ignore = False
            count = 0
            continue
        if not ignore:
            new_response += char

    return new_response


########## Eleven Labs Requests ##########

load_dotenv()
elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

tone_to_voice = {"health": "0mevMNFMwHxBOUTpeMGN",
                 "career": "kdmDKE6EkgrWrrykO9Qt",
                 "hobbies": "9q9xpGHwmkXdA4JI72IU"
                 }

def vocalize_text(response, voice):
    """
    Given a string of text, plays the audio backs to the user.
    Optional arguments: tone of voice
    Args:

    """
    audio = elevenlabs.text_to_speech.convert(
        text=response,
        voice_id=tone_to_voice[voice],
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)

if __name__ == "__main__":
    # comp = chat_request("Hey there! I am struggling with keeping up with regular exercises recently" \
    # "do you have any tips as to how I can get back on track?")
    comp = initialize_convo("health", "On keto diet", True)

    print(comp)
    # vocalize_text(comp)
