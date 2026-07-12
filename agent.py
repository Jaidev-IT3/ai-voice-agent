from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    RoomInputOptions,
)

from livekit.plugins import (
    google,
    noise_cancellation,
)

from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION

load_dotenv()


class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=AGENT_INSTRUCTION
        )


server = AgentServer()


@server.rtc_session(agent_name="jarvis")
async def my_agent(ctx: agents.JobContext):

    await ctx.connect()

    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            voice="aoede",
            temperature=0.8,
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
       # room_input_options=RoomInputOptions(
      #      noise_cancellation=noise_cancellation.BVC(),
       # ),
    )

    await session.generate_reply(
        instructions=SESSION_INSTRUCTION
    )


if __name__ == "__main__":
    agents.cli.run_app(server)