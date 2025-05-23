Hello! My name is Diana, a sophomore studying EECS at MIT. I have diverse interests in both hardware and software, especially in relation to the field of AI (i.e. building hardware that can accelerate AI applications and software that can integrate or further advance these features).

I wanted to explore how to employ the fast feature of Cerebras.

This project is a miniature game that simulates coaching sessions by integrating Cerebras's and Elevenlabs's (text-to-speech) API.
The game consists of three islands, each representing health, career, and hobbies/leisure. Leveraging fast inference, the game is able to execute real-time-like voice responses that allow the user to experience a realistic and genuine coaching session. The coaching structure is as follows:

Upon first starting the game, the user is prompted to answer a survey that collects information that will be used to guide the coaching session.
This data is used and updated throughout the coaching session to reflect the user's progress.

Due to the limited free tokens ElevenLabs provide and the amount of words that coaching responses generate,

The game lacks functionalities such as allowing the user to choose the voice and
