
import os
from dotenv import load_dotenv
from google import genai

from planner import create_plan
from researcher import search_web
from analyzer import analyze_research
from gap_detector import detect_research_gaps
from verifier import verify_research
from report_generator import generate_report


def run_research(topic, progress_callback=None):
    """Run the complete autonomous research pipeline."""

    def update_progress(message):
        if progress_callback is not None:
            progress_callback(message)
        else:
            print(message)

    # STEP 1: Validate input and initialize Gemini
    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a research topic.")

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key not found in .env")

    client = genai.Client(api_key=api_key)

    # STEP 2: Create research plan
    update_progress("Creating research plan...")

    plan = create_plan(client, topic)

    for index, task in enumerate(plan, start=1):
        update_progress(f"{index}. {task}")

    # STEP 3: Collect initial research
    all_results = []

    for task in plan:
        update_progress(f"Researching: {task}")

        results = search_web(task)

        all_results.append({
            "task": task,
            "results": results
        })

    # STEP 4: Analyze collected research
    update_progress("Analyzing collected research...")

    analysis = analyze_research(
        client,
        topic,
        all_results
    )

    # STEP 5: Autonomous gap detection
    MAX_FOLLOW_UP_ROUNDS = 2

    researched_tasks = {
        task.strip().lower()
        for task in plan
    }

    for round_number in range(1, MAX_FOLLOW_UP_ROUNDS + 1):

        update_progress(
            f"Checking research gaps - Round {round_number}..."
        )

        gaps = detect_research_gaps(
            client,
            topic,
            analysis
        )

        if not gaps:
            update_progress("No further research gaps identified.")
            break

        new_gaps = [
            gap
            for gap in gaps
            if gap.strip().lower() not in researched_tasks
        ]

        if not new_gaps:
            update_progress("No new research questions to investigate.")
            break

        for gap in new_gaps:
            update_progress(f"Follow-up research: {gap}")

            researched_tasks.add(gap.strip().lower())

            results = search_web(gap)

            all_results.append({
                "task": gap,
                "results": results
            })

        update_progress("Re-analyzing updated research...")

        analysis = analyze_research(
            client,
            topic,
            all_results
        )

    # STEP 6: Verify evidence
    update_progress("Verifying research evidence...")

    verification_report = verify_research(
        client,
        topic,
        analysis,
        all_results
    )

    # STEP 7: Generate final report
    update_progress("Generating final research report...")

    report_path = generate_report(
        topic,
        analysis,
        verification_report,
        all_results
    )

    update_progress("Research completed successfully!")

    return {
        "topic": topic,
        "plan": plan,
        "analysis": analysis,
        "verification": verification_report,
        "sources": all_results,
        "report_path": report_path
    }
