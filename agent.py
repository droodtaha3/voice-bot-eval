import asyncio  # lets the bot wait (sleep) without freezing the rest of the program
import json  # used to read the phone number and scenario sent by call.py
import os  # used to read the trunk ID from the environment
import time  # used to time how far into the call each sentence happens
from datetime import datetime  # used to put a timestamp in each transcript filename
from pathlib import Path  # used to work with folder and file paths

from dotenv import load_dotenv  # reads my private keys from the .env file
from livekit import api  # LiveKit's API, used here to dial the phone and end the room
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli  # the core pieces of a LiveKit voice agent
from livekit.plugins import cartesia, deepgram, openai, silero  # provider plugins: voice, speech-to-text, language model, voice-activity detection

from scenarios import build_persona  # pulls in the patient persona for the chosen scenario

load_dotenv()  # loads the keys from .env so the plugins can find them

TRANSCRIPT_DIR = Path("transcripts")  # the folder where transcripts get saved
MAX_CALL_SECONDS = 420  # hard cap: hang up after 7 minutes so a call can't run forever


async def entrypoint(ctx: JobContext):  # runs once for every call the agent is asked to make
    await ctx.connect()  # connects this job to its LiveKit room
    meta = json.loads(ctx.job.metadata)  # reads the data call.py attached to this job
    phone_number = meta["phone_number"]  # which number to dial
    scenario = meta["scenario"]  # which patient scenario to play (refill, cancel, etc.)

    TRANSCRIPT_DIR.mkdir(exist_ok=True)  # creates the transcripts folder if it doesn't exist yet
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # current date and time, used to make the filename unique
    transcript_path = TRANSCRIPT_DIR / f"call-{stamp}-{scenario}.txt"  # e.g. call-20261023-161434-refill.txt
    call = {"start": None}  # holds the moment the call is answered, so timestamps start at 0:00

    session = AgentSession(  # the voice pipeline: ears, brain, and mouth
        vad=silero.VAD.load(),  # detects when someone is speaking versus silent
        stt=deepgram.STT(model="nova-3", language="en"),  # speech-to-text: turns the clinic agent's voice into words
        llm=openai.LLM(model="gpt-4o-mini"),  # the language model: decides what the patient says next
        tts=openai.TTS(model="tts-1", voice="alloy"),  # text-to-speech: OpenAI here; calls 01-08 used cartesia.TTS()
        preemptive_generation=True,  # starts drafting a reply before the other person has fully finished, to cut delay
        min_endpointing_delay=0.3,  # waits only 0.3 seconds of silence before deciding the other side is done
        min_interruption_duration=0.8,  # the other side must speak 0.8 seconds before it counts as an interruption
        min_interruption_words=2,  # and say at least 2 words, so a cough or "mm-hm" doesn't cut the bot off
    )

    @session.on("conversation_item_added")  # runs every time a full sentence is finished, by either side
    def on_item(ev):
        item = ev.item  # the sentence that was just completed
        text = getattr(item, "text_content", None)  # the words of that sentence
        if not text or item.role not in ("user", "assistant"):  # ignore empty items and system messages
            return
        speaker = "BOT (patient)" if item.role == "assistant" else "AGENT (other side)"  # my bot is the assistant; the clinic agent is the user
        elapsed = 0 if call["start"] is None else time.monotonic() - call["start"]  # seconds since the call was answered
        mins, secs = divmod(int(elapsed), 60)  # splits that into minutes and seconds
        with open(transcript_path, "a", encoding="utf-8") as f:  # opens the transcript file, adding to the end
            f.write(f"[{mins}:{secs:02d}] {speaker}: {text}\n")  # writes one line, like [0:17] BOT (patient): ...

    await session.start(  # starts the voice session in the room
        agent=Agent(instructions=build_persona(scenario)), room=ctx.room  # gives the bot its patient persona for this scenario
    )

    await ctx.api.sip.create_sip_participant(  # dials the real phone number
        api.CreateSIPParticipantRequest(
            room_name=ctx.room.name,  # puts the phone call into this room
            sip_trunk_id=os.environ["SIP_OUTBOUND_TRUNK_ID"],  # which outbound trunk to use (the one linked to Twilio)
            sip_call_to=phone_number,  # the number being called
            participant_identity="phone_user",  # the name given to the person on the phone line
            wait_until_answered=True,  # don't continue until someone picks up
        )
    )
    call["start"] = time.monotonic()  # the call was answered, so start the timestamp clock

    async def hang_up_after_limit():  # a small background timer
        await asyncio.sleep(MAX_CALL_SECONDS)  # waits 7 minutes
        await ctx.api.room.delete_room(api.DeleteRoomRequest(room=ctx.room.name))  # then closes the room, which ends the call

    call["timer"] = asyncio.create_task(hang_up_after_limit())  # starts that timer running in the background


if __name__ == "__main__":  # true when I run `python agent.py dev`
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name="caller"))  # starts the worker and waits for call requests named "caller"