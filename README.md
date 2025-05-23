
# About me
Hello! My name is Diana, a sophomore studying EECS at MIT. I have diverse interests in both hardware and software, especially in relation to the field of AI (i.e. building hardware that can accelerate AI applications and software that can integrate or further advance these features). **Please see a demo of the functions in `demo.mp4`!**

# Project description

In this project, I wanted to explore the applications of fast inference. The project is a miniature game that simulates coaching sessions by integrating Cerebras's and Elevenlabs's text-to-speech API.

The game consists of three islands, each representing health, career, and hobbies/leisure. Leveraging fast inference, the game seeks to execute real-time-like voice responses that allow the user to experience a realistic and genuine coaching session. The coaching structure is as follows:

- Upon first starting the game, the user is prompted to answer a survey that collects information that will be used to guide the coaching session. This data is used and updated throughout the coaching session to reflect the user's progress.
- Then, the user can enter any island of their interest.
- The coach will initiate an introduction if it's the user's first session. Otherwise, it will ask follow-up questions on the prior session.
- The user can input anything they want to talk about regarding the relevant topic.

# Future Improvements:
The game lacks functionalities such as including a manual and progress view and providing the user with option to choose the coaches' voice but serves to be a proof-of-concept example that illustrates the capabilities of Cerebras' API. Although qwen3 responds really quickly, there is still a slight delay in the voice generation due to the response time of ElevensLabs's API. However, with faster text-to-speech API, such delay can be minimized. Plus, Cerebras' fast inference enables text-to-speech API to take a longer time to generate more natural, diverse voices.
