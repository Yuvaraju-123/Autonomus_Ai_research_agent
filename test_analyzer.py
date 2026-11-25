from unittest.mock import Mock
from google.genai.errors import ServerError
from analyzer import analyze_research

# Create our fake Gemini client
fake_client = Mock()

# Create a fake server error
fake_error = ServerError(
    code=503,
    response_json={"error": {"message": "Server overloaded"}}
)

# Tell fake Gemini how to behave
fake_client.models.generate_content.side_effect = [
    fake_error,
    fake_error,
    fake_error,
    fake_error
]

# Give the Analyzer some sample research data
topic = "AI effect on software"

all_results = [
    {
        "task": "AI impact on developers",
        "results": []
    }
]

# Call our real Analyzer with the fake Gemini client
try:
    result = analyze_research(fake_client, topic, all_results)
    print("Final result:", result)

except ServerError as e:
    print("\nResearch analysis is temporarily unavailable.")
    print("Gemini's server did not respond after multiple attempts.")
    print("Please try again later.")
    print("Error details:", e)

print("Total Gemini calls:", fake_client.models.generate_content.call_count)