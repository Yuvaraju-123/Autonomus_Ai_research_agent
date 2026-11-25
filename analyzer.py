
import json
import time
from google.genai.errors import ServerError


def analyze_research(client, topic, all_results):

    research_data = json.dumps(all_results, indent=2)

    prompt = f"""
    You are an expert research analyst.

    Research topic: {topic}

    Collected research data:
    {research_data}

    Analyze the collected information and provide:
    1. Key findings
    2. Important insights
    3. Information gaps
    4. Relevant source URLs

    Use only the provided research data.
    Do not invent facts or sources.
    Mention where evidence is insufficient.
    """

    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except ServerError as e:
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 3:
                wait_time = 2 ** (attempt + 1)

                print(f"Retrying in {wait_time} seconds...")

                time.sleep(wait_time)

            else:
                raise
