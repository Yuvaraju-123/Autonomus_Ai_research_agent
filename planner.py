
import json
from google.genai import types


def create_plan(client, topic):
    prompt = f"""
    You are an expert research planner.

    Break the given research topic into
    exactly 5 smaller research tasks.

    Research topic: {topic}

    Do not answer the research questions.
    Only create the research plan.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[str]
        )
    )

    return json.loads(response.text)
