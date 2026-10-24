\# Architecture



The bot is a LiveKit Agents worker in pipeline mode: Deepgram `nova-3` for

speech-to-text, `gpt-4o-mini` for the language model, and Cartesia `sonic-3`

for text-to-speech, with Silero VAD and LiveKit's turn-detector model deciding

when a speaker is done. A small script (`call.py`) dispatches the agent with a

phone number and scenario; the agent starts its session first, then dials out

through a LiveKit outbound SIP trunk that points at a Twilio Elastic SIP

Trunk, so the audio path is laptop to LiveKit Cloud to Twilio to the phone

network. I chose the SIP trunk over a hosted voice platform because it keeps

the pipeline visible and swappable, and I record on the Twilio side (dual

channel) because that gives both speakers in one file without extra storage

setup. Each scenario is a short persona prompt that tells the bot to stay

silent through the greeting, answer only what is asked, and steer back to its

goal, so it behaves like a caller and not a script. A 7-minute cap hangs up

runaway calls.



Latency was the main thing I tuned. A first version using OpenAI for both

speech-to-text and text-to-speech left gaps of roughly 5 to 6 seconds

between turns. Switching to Deepgram and Cartesia, plus enabling preemptive

generation and a 0.3 second endpointing delay, brought it to roughly 1.5 to

2.5 seconds, measured from the per-turn metrics (about 0.6 s to detect end

of turn, 0.6 to 1.3 s for the model's first token, 0.25 to 0.35 s for the

first audio). The interruption-threshold settings I tried did not measurably

change the cutoffs I heard, and several early bad calls turned out to be

caused by an unstable connection (a phone hotspot dropped the LiveKit link)

and by launching many calls at once, not by the models, so the final calls

were made one at a time on a stable connection. Tradeoff to note: calls 09

and 10 use OpenAI text-to-speech because Cartesia credits ran out, which is

audibly different from the first eight.

