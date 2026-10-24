\# Iteration log



What broke while building the caller, and what I changed.



1\. \*\*Twilio refused the call\*\* (`403 No International Permission`). Fixed in

&#x20;  Twilio's voice geo-permissions.

2\. \*\*SIP auth error\*\* (no username or password sent). The LiveKit outbound

&#x20;  trunk needed the Twilio credential-list login added.

3\. \*\*Bot connected but said nothing.\*\* The model never spoke first and the

&#x20;  OpenAI key in `.env` was split across lines (401 error). Re-entered the key

&#x20;  on one line.

4\. \*\*Bot chatted off-topic.\*\* First prompt was a generic chat persona. Replaced

&#x20;  it with a patient persona with a goal.

5\. \*\*5 to 6 second gaps between turns\*\* with OpenAI speech-to-text and

&#x20;  text-to-speech. Switched to Deepgram `nova-3` and Cartesia, then enabled

&#x20;  preemptive generation and a 0.3 s endpointing delay. Per-turn metrics

&#x20;  afterward: about 0.6 s end-of-turn, 0.6 to 1.3 s model first token, 0.25 to

&#x20;  0.35 s first audio.

6\. \*\*Choppy audio and a dropped LiveKit connection\*\* (`ping timeout`) while

&#x20;  on a phone hotspot. Moved to a stable connection and the audio was clean.

&#x20;  Interruption-threshold tweaks made no audible difference.

7\. \*\*Launched nine calls at once.\*\* Twilio showed several calls pinned at the

&#x20;  4 minute cap and transcripts overlapped. Discarded the batch and reran

&#x20;  every call one at a time.

8\. \*\*Persona bugs found by reading early transcripts:\*\* the bot refused to

&#x20;  say its name when asked a yes/no question, invented a date correction,

&#x20;  and spoke over the recorded greeting. Rewrote the persona rules for each,

&#x20;  and raised the call cap from 4 to 7 minutes because calls were being cut off.

9\. \*\*Calls that were too short to be useful\*\* (insurance, refill ended in a

&#x20;  transfer). Rewrote those scenarios so the bot asks follow-ups and pushes

&#x20;  back politely, then reran them.

10\. \*\*Cartesia credits ran out\*\* during the last calls, so those used OpenAI

&#x20;   `tts-1`.

