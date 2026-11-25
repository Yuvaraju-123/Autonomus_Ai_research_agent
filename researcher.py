
import time
from urllib.parse import urlparse

from ddgs import DDGS
from ddgs.exceptions import DDGSException
from article_reader import read_article


# Check whether a search result is valid
def is_valid_result(result):
    url = result.get("href", "")

    domain = urlparse(url).netloc.lower()

    # Reject Bing advertisement links
    if domain in ("www.bing.com", "bing.com") and "/aclick" in url:
        return False

    return True


# Remove duplicate website links
def remove_duplicates(results):
    seen_urls = set()
    unique_results = []

    for result in results:
        url = result.get("href", "")

        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

    return unique_results


# Calculate how relevant each result is
def relevance_score(result, query):
    title = result.get("title", "").lower()
    body = result.get("body", "").lower()

    keywords = query.lower().split()

    score = 0

    for word in keywords:
        if word in title:
            score += 2

        if word in body:
            score += 1

    return score


# NEW: Check the credibility of a website
def check_source(url):
    domain = urlparse(url).netloc.lower()

    # Government websites
    if domain.endswith((".gov", ".gov.in")):
        return "High"

    # Educational websites
    elif domain.endswith((".edu", ".ac.in")):
        return "High"

    # Recognized information sources
    elif domain in [
        "reuters.com",
        "www.reuters.com",
        "bbc.com",
        "www.bbc.com",
        "nature.com",
        "www.nature.com"
    ]:
        return "High"

    # Other websites require further verification
    else:
        return "Needs Verification"


# Search the web for a research topic
def search_web(query):

    # Retry up to 3 times if the search fails
    for attempt in range(3):

        try:
            results = DDGS().text(
                query,
                max_results=6
            )

            # Remove advertisement results
            results = [
                result
                for result in results
                if is_valid_result(result)
            ]

            # Remove duplicate results
            results = remove_duplicates(results)

            # Rank results by relevance
            results = sorted(
                results,
                key=lambda result: relevance_score(result, query),
                reverse=True
            )

            # Select the top 3 results
            results = results[:3]

            # Read full article text and check source credibility
            for result in results:
                url = result.get("href", "")

                result["article_text"] = read_article(url)

                # NEW: Add credibility label
                result["credibility"] = check_source(url)

            # Print a short summary for testing
            for result in results:
                print("\nTitle:", result.get("title"))
                print("URL:", result.get("href"))

                print(
                    "Article characters:",
                    len(result.get("article_text", ""))
                )

                # NEW: Display source credibility
                print(
                    "Source credibility:",
                    result.get("credibility")
                )

            return results

        except DDGSException as e:

            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                print("Retrying in 2 seconds...")
                time.sleep(2)

    # Return an empty list if all attempts fail
    return []


# Run this test only when researcher.py is executed directly
if __name__ == "__main__":

    results = search_web("AI impact on software developers")

    print("\nTotal valid results:", len(results))
