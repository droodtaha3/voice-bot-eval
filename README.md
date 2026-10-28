Voice Patient Simulator

This is a Python voice bot that phones a clinic's AI receptionist, plays a patient, and records and transcribes every call. It is built on LiveKit Agents in pipeline mode, which means listening, thinking, and talking are three separate steps. Deepgram turns the other side's speech into text, OpenAI's GPT-4o-mini decides what the patient says next, and a voice model speaks the answer. The phone call itself goes from my laptop to LiveKit Cloud and then through a Twilio SIP trunk to the phone network.

To set it up, you need Python 3.10 or newer. Make a virtual environment and install the packages with these commands, which are for Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Next, copy the file named .env.example to a new file named .env and fill in each value. You need a LiveKit URL, key, and secret from a LiveKit Cloud project, plus API keys for OpenAI, Deepgram, and Cartesia. You also need the ID of your LiveKit outbound SIP trunk, which starts with ST_. The .env file is private and is not in this repo.

For the phone side, create a Twilio Elastic SIP Trunk with a termination address and a credential list, and attach a voice-enabled phone number to it. Then create an outbound trunk in LiveKit that uses the same address, the same username and password, and your Twilio number. I also turned on dual-channel call recording on the Twilio trunk, so each call is saved with both speakers.

To make a call, you use two terminals. In the first one, start the bot and wait until it prints "registered worker":

    python agent.py dev

In the second one, start a call by giving it a phone number and a scenario name:

    python call.py +1XXXXXXXXXX refill

Run one call at a time. Wait until the first terminal prints "session closed" before you start the next one, because overlapping calls get mixed together. The scenarios are schedule, reschedule, cancel, refill, hours, insurance, sunday, vague, change_mind, and unusual. Each call saves a transcript with timestamps in a folder called transcripts, and a call stops on its own after 7 minutes.

The calls folder has the 10 calls I am submitting. Each one has a transcript and an MP3 recording with matching names, like call-05-sunday.txt and call-05-sunday.mp3. The bug report is in BUGS.md, the design choices are in ARCHITECTURE.md, and the problems I hit along the way are in ITERATION_LOG.md.

A few things to know. The transcripts come from the bot's own speech-to-text, so a word can be wrong, and I checked the bugs I report against the audio. The recordings came from Twilio and I downloaded them by hand. Calls 01 to 08 used Cartesia for the voice, and calls 09 and 10 used OpenAI's tts-1 voice because my Cartesia credits ran out. The agent.py file currently has the OpenAI line, so to match the first eight calls, swap it for cartesia.TTS().