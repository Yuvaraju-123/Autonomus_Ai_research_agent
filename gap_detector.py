
from google.genai import types


def detect_research_gaps(client, topic, analysis):
    prompt = f"""
You are a research gap detection agent.

Original research topic:
{topic}

Current research analysis:
{analysis}

Your task:
1. Identify important missing information.
2. Find unanswered questions.
3. Suggest one specific follow-up research question.
4. Do not repeat information already covered.
5. If the research is sufficiently complete,
   return an empty list.

Return at most one research question.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[str]
        )
    )

    return response.parsed or []
