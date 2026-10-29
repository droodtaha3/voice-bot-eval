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


def print_usage():
    names = list(SCENARIOS)
    print("Usage: python call.py +1XXXXXXXXXX scenario_name\n")
    print("Here are the available scenarios:")
    for name in names:
        print(f"  - {name}")
    if names:
        print(f"\nExample:\n  python call.py +15551234567 {names[0]}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2]))