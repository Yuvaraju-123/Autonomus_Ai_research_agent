
import os
import streamlit as st
from google.genai.errors import ServerError

from research_pipeline import run_research


st.set_page_config(
    page_title="Autonomous AI Research Agent",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Autonomous AI Research Agent")

st.write(
    "Enter a research topic. The AI agent will plan, research, "
    "analyze, verify evidence, and generate a report."
)

topic = st.text_input(
    "Enter your research topic",
    placeholder="Example: Impact of AI on software development"
)

# Store completed research across Streamlit reruns
if "research_result" not in st.session_state:
    st.session_state.research_result = None

if st.button("🚀 Start Research", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic.")

    else:
        st.session_state.research_result = None

        progress_area = st.empty()

        def show_progress(message):
            progress_area.info(message)

        try:
            with st.spinner("AI agents are researching..."):
                result = run_research(
                    topic,
                    progress_callback=show_progress
                )

            st.session_state.research_result = result

            progress_area.empty()
            st.success("Research completed successfully!")

        except ServerError:
            progress_area.empty()
            st.error(
                "Gemini is temporarily unavailable. "
                "Please try again later."
            )

        except Exception as e:
            progress_area.empty()
            st.error(f"Research failed: {e}")


# Display results after research finishes
result = st.session_state.research_result

if result is not None:

    st.divider()

    st.subheader("📋 Research Plan")

    for index, task in enumerate(result["plan"], start=1):
        st.write(f"{index}. {task}")

    st.divider()

    st.subheader("📊 Research Analysis")
    st.markdown(result["analysis"])

    st.divider()

    st.subheader("✅ Evidence Verification")
    st.markdown(result["verification"])

    st.divider()

    st.subheader("📄 Final Research Report")

    try:
        with open(result["report_path"], "rb") as report_file:
            report_data = report_file.read()

        st.download_button(
            label="⬇️ Download Research Report",
            data=report_data,
            file_name=os.path.basename(result["report_path"]),
            mime="text/markdown"
        )

    except OSError as e:
        st.error(f"Unable to read saved report: {e}")
