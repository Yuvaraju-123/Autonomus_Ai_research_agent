
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

from planner import create_plan
from researcher import search_web
from analyzer import analyze_research
from gap_detector import detect_research_gaps
from verifier import verify_research
from report_generator import generate_report


# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found")

# Initialize Gemini client
client = genai.Client(api_key=api_key)


# STEP 1: Get research topic
topic = input("Enter your research topic: ").strip()

if not topic:
    raise ValueError("Please enter a research topic.")


# STEP 2: Create research plan
plan = create_plan(client, topic)

print("\nResearch Plan:\n")

for index, task in enumerate(plan, start=1):
    print(f"{index}. {task}")

print("\nData type:", type(plan))


# STEP 3: Collect initial research
all_results = []

for task in plan:
    print(f"\nResearching: {task}")

    results = search_web(task)

    all_results.append({
        "task": task,
        "results": results
    })


# STEP 4: Analyze collected research
print("\nAnalyzing collected research...\n")

try:
    analysis = analyze_research(
        client,
        topic,
        all_results
    )

    print("\nResearch Analysis:")
    print(analysis)

    # STEP 5: Autonomous gap detection
    MAX_FOLLOW_UP_ROUNDS = 2

    # Track already researched questions
    researched_tasks = {
        task.strip().lower()
        for task in plan
    }

    # Perform additional research when gaps are found
    for round_number in range(1, MAX_FOLLOW_UP_ROUNDS + 1):

        print(
            f"\nChecking research gaps - Round {round_number}..."
        )

        # Ask Gemini to identify missing information
        gaps = detect_research_gaps(
            client,
            topic,
            analysis
        )

        # Stop if no gaps are found
        if not gaps:
            print("\nNo further research gaps identified.")
            break

        # Avoid repeating the same research question
        new_gaps = [
            gap
            for gap in gaps
            if gap.strip().lower() not in researched_tasks
        ]

        if not new_gaps:
            print("\nNo new research questions to investigate.")
            break

        # Research newly identified questions
        for gap in new_gaps:

            print(f"\nFollow-up research: {gap}")

            researched_tasks.add(
                gap.strip().lower()
            )

            results = search_web(gap)

            all_results.append({
                "task": gap,
                "results": results
            })

        # Analyze the updated research
        print("\nRe-analyzing updated research...\n")

        analysis = analyze_research(
            client,
            topic,
            all_results
        )

        print("\nUpdated Research Analysis:")
        print(analysis)

    # STEP 6: Display final research analysis
    print("\n========== FINAL RESEARCH ANALYSIS ==========\n")
    print(analysis)

    # STEP 7: Verify research evidence
    print("\n========== VERIFYING RESEARCH EVIDENCE ==========\n")

    verification_report = verify_research(
        client,
        topic,
        analysis,
        all_results
    )

    # STEP 8: Display verification report
    print("\n========== EVIDENCE VERIFICATION REPORT ==========\n")
    print(verification_report)

    # STEP 9: Generate and save final research report
    print("\n========== GENERATING FINAL REPORT ==========\n")

    report_path = generate_report(
        topic,
        analysis,
        verification_report,
        all_results
    )

    print(
        f"\nResearch report saved successfully: {report_path}"
    )


# Handle Gemini server errors
except ServerError as e:
    print("\nResearch analysis is temporarily unavailable.")
    print("Gemini's server did not respond after multiple attempts.")
    print("Please try again later.")
    print("Error details:", e)
