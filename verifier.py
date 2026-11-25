
from google.genai import types


def verify_research(client, topic, analysis, all_results):
    """
    Compare research claims against collected source evidence.

    This is an AI-assisted evidence review, not independent
    verification of the underlying facts.
    """

    evidence = []

    # STEP 1: Collect readable article content
    for task_data in all_results:
        for result in task_data.get("results", []):

            article_text = result.get(
                "article_text", ""
            ).strip()

            # Skip sources with no extracted text
            if not article_text:
                continue

            evidence.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "content": article_text[:3000]
            })

    # STEP 2: Handle missing evidence
    if not evidence:
        return (
            "EVIDENCE VERIFICATION UNAVAILABLE\n"
            "No readable source content was collected.\n"
            "The research claims remain unverified."
        )

    # STEP 3: Prepare evidence for Gemini
    source_text = "\n\n".join(
        f"Source {index}\n"
        f"Title: {source['title']}\n"
        f"URL: {source['url']}\n"
        f"Content: {source['content']}"
        for index, source in enumerate(evidence, start=1)
    )

    # STEP 4: Create verification instructions
    prompt = f"""
You are an evidence verification agent.

Research topic:
{topic}

Research analysis:
{analysis}

Available source evidence:
{source_text}

Your task:
1. Identify important factual and numerical claims
   in the research analysis.
2. Compare each claim against the supplied source text.
3. Label each claim as:
   - SUPPORTED: The supplied evidence directly supports it.
   - PARTIALLY SUPPORTED: Only part of the claim is supported.
   - NOT VERIFIED: The supplied evidence does not establish it.
   - CONTRADICTED: The supplied evidence conflicts with it.
4. Provide supporting or conflicting source URLs.
5. Explain your reasoning briefly.
6. Never invent sources, statistics, or citations.
7. Do not treat a source's reputation as proof.
8. Do not use outside knowledge to fill evidence gaps.

Important:
A claim without matching extracted source evidence
must be labeled NOT VERIFIED.

Return a clear verification report.
"""

    # STEP 5: Ask Gemini to compare claims with evidence
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0
        )
    )

    return response.text or "Verification returned no text."
