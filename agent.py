import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from livekit import api
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import cartesia, deepgram, openai, silero

from scenarios import build_persona

load_dotenv()

TRANSCRIPT_DIR = Path("transcripts")
MAX_CALL_SECONDS = 420


async def entrypoint(ctx: JobContext):
    await ctx.connect()
    meta = json.loads(ctx.job.metadata)
    phone_number = meta["phone_number"]
    scenario = meta["scenario"]

    TRANSCRIPT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    transcript_path = TRANSCRIPT_DIR / f"call-{stamp}-{scenario}.txt"
    call = {"start": None}

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-3", language="en"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(model="tts-1", voice="alloy"),
        preemptive_generation=True,
        min_endpointing_delay=0.3,
        min_interruption_duration=0.8,
        min_interruption_words=2,
    )

    @session.on("conversation_item_added")
    def on_item(ev):
        item = ev.item
        text = getattr(item, "text_content", None)
        if not text or item.role not in ("user", "assistant"):
            return
        speaker = "BOT (patient)" if item.role == "assistant" else "AGENT (other side)"
        elapsed = 0 if call["start"] is None else time.monotonic() - call["start"]
        mins, secs = divmod(int(elapsed), 60)
        with open(transcript_path, "a", encoding="utf-8") as f:
            f.write(f"[{mins}:{secs:02d}] {speaker}: {text}\n")

    await session.start(
        agent=Agent(instructions=build_persona(scenario)), room=ctx.room
    )

    await ctx.api.sip.create_sip_participant(
        api.CreateSIPParticipantRequest(
            room_name=ctx.room.name,
            sip_trunk_id=os.environ["SIP_OUTBOUND_TRUNK_ID"],
            sip_call_to=phone_number,
            participant_identity="phone_user",
            wait_until_answered=True,
        )
    )
    call["start"] = time.monotonic()

    async def hang_up_after_limit():
        await asyncio.sleep(MAX_CALL_SECONDS)
        await ctx.api.room.delete_room(api.DeleteRoomRequest(room=ctx.room.name))

    call["timer"] = asyncio.create_task(hang_up_after_limit())


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name="caller"))