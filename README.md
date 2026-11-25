# 🔬 Autonomous AI Research Agent

An AI-powered research application that autonomously plans research tasks, searches the web, analyzes information, detects knowledge gaps, verifies claims against collected evidence, and generates downloadable research reports.

Built using **Python, Google Gemini, Streamlit, DDGS, and BeautifulSoup**.

## 🚀 Features

- **AI Research Planning:** Breaks a research topic into smaller research tasks.
- **Web Search:** Collects relevant information from online sources.
- **Article Extraction:** Extracts readable content from webpages.
- **AI Analysis:** Uses Gemini to analyze research findings.
- **Research Gap Detection:** Identifies missing information and performs additional research.
- **Evidence Verification:** Compares claims against collected source evidence using Gemini.
- **Report Generation:** Produces downloadable Markdown research reports.
- **Streamlit Interface:** Provides a user-friendly research dashboard.
- **Error Handling:** Includes retry mechanisms for temporary API failures.

## 🧠 How It Works

```text
User enters research topic
          |
          v
      AI Planner
          |
          v
     Web Researcher
          |
          v
     AI Analyzer
          |
          v
     Gap Detector
          |
          v
  Additional Research
     (if needed)
          |
          v
    Evidence Verifier
          |
          v
    Report Generator
          |
          v
   Downloadable Report
```

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application |
| Google Gemini | AI reasoning and analysis |
| Streamlit | Web interface |
| DDGS | Web search |
| BeautifulSoup | Web content extraction |
| Requests | HTTP requests |
| python-dotenv | Environment variable management |
| unittest.mock | Automated testing |

## 📁 Project Structure

```text
AI-Research-Agent/
├── app.py
├── main.py
├── research_pipeline.py
├── planner.py
├── researcher.py
├── article_reader.py
├── analyzer.py
├── gap_detector.py
├── verifier.py
├── report_generator.py
├── test_analyzer.py
├── test_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_FOLDER
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

**3. Activate the environment (Windows PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Configure the Gemini API key**

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**6. Start the application**

```bash
python -m streamlit run app.py
```

## 🧪 Testing

Run the mocked pipeline integration test:

```bash
python test_pipeline.py
```

This checks the research workflow without making real Gemini API calls.

## ⚠️ Limitations

- Some websites may block article extraction.
- Research depends on search result quality and Gemini API availability.
- LLM-based evidence verification does not guarantee factual accuracy.
- Full Streamlit end-to-end testing is still pending successful live Gemini responses.

## 🔮 Future Improvements

- PDF report downloads
- Research history
- Better citation tracking
- Improved automated testing
- Cloud deployment

## 📌 Project Status

The research backend has generated reports successfully. The Streamlit interface launches, and the mocked research pipeline integration test passes. Live end-to-end testing of the Streamlit workflow remains pending.