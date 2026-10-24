import asyncio
import json
import sys
import time

from dotenv import load_dotenv
from livekit import api

from scenarios import SCENARIOS

load_dotenv()


async def main(phone_number: str, scenario: str):
    if scenario not in SCENARIOS:
        sys.exit(f"Unknown scenario. Choose from: {', '.join(SCENARIOS)}")
    lkapi = api.LiveKitAPI()
    dispatch = await lkapi.agent_dispatch.create_dispatch(
        api.CreateAgentDispatchRequest(
            agent_name="caller",
            room=f"call-{scenario}-{int(time.time())}",
            metadata=json.dumps(
                {"phone_number": phone_number, "scenario": scenario}
            ),
        )
    )
    print("Dispatched:", dispatch.id, "scenario:", scenario)
    await lkapi.aclose()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Usage: python call.py +1XXXXXXXXXX scenario_name")
    asyncio.run(main(sys.argv[1], sys.argv[2]))