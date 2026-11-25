import requests
from bs4 import BeautifulSoup


def read_article(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        paragraphs = soup.find_all("p")

        article_text = " ".join(
            paragraph.get_text(" ", strip=True)
            for paragraph in paragraphs
        )

        return article_text[:5000]

    except requests.RequestException as e:
        print("Could not read article:", e)
        return ""
if __name__ == "__main__":

    url = "https://www.python.org/about/"

    article = read_article(url)

    print("\nExtracted Article Text:\n")
    print(article)

    print("\nTotal characters:", len(article))