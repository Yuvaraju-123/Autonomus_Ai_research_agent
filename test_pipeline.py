
from unittest.mock import patch

from research_pipeline import run_research


def test_research_pipeline():

    fake_plan = [
        "AI developer productivity",
        "AI coding security"
    ]

    fake_analysis = "AI can improve developer productivity."

    fake_verification = "Claim: SUPPORTED"

    progress_messages = []

    with (
        patch("research_pipeline.genai.Client") as mock_client,
        patch(
            "research_pipeline.create_plan",
            return_value=fake_plan
        ) as mock_planner,
        patch(
            "research_pipeline.search_web",
            return_value=[]
        ) as mock_researcher,
        patch(
            "research_pipeline.analyze_research",
            return_value=fake_analysis
        ) as mock_analyzer,
        patch(
            "research_pipeline.detect_research_gaps",
            return_value=[]
        ) as mock_gap_detector,
        patch(
            "research_pipeline.verify_research",
            return_value=fake_verification
        ) as mock_verifier,
        patch(
            "research_pipeline.generate_report",
            return_value="reports/test_report.md"
        ) as mock_report
    ):

        result = run_research(
            "AI effect on software",
            progress_callback=progress_messages.append
        )

        # Verify returned research results
        assert result["topic"] == "AI effect on software"
        assert result["plan"] == fake_plan
        assert result["analysis"] == fake_analysis
        assert result["verification"] == fake_verification
        assert result["report_path"] == "reports/test_report.md"

        # Verify employees were called
        mock_client.assert_called_once()
        mock_planner.assert_called_once()
        assert mock_researcher.call_count == 2
        mock_analyzer.assert_called_once()
        mock_gap_detector.assert_called_once()
        mock_verifier.assert_called_once()
        mock_report.assert_called_once()

        # Verify website progress messages are produced
        assert any(
            "Researching:" in message
            for message in progress_messages
        )

    print("All pipeline tests passed!")


if __name__ == "__main__":
    test_research_pipeline()
