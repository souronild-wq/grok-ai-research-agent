import os
import re
import time
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("XAI_API_KEY")
MODEL = os.getenv("XAI_MODEL", "grok-3")

if not API_KEY:
    raise ValueError(
        "XAI_API_KEY is missing. "
        "Add your xAI API key to the .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.x.ai/v1",
    timeout=60.0,
    max_retries=0
)


# ==========================================
# GENERATE RESEARCH REPORT
# ==========================================

def generate_report(topic):
    prompt = f"""
You are a professional AI research assistant.

Research topic: {topic}

Write a detailed, clear, and well-organized research report.

Use the following structure:

# Research Report

## 1. Introduction
Explain the topic and why it matters.

## 2. Background
Give the relevant context and definitions.

## 3. Key Findings
Explain the main facts, ideas, and findings.

## 4. Challenges
Discuss the problems, risks, or limitations.

## 5. Practical Solutions
Give realistic, actionable steps and examples.

## 6. Conclusion
Summarize the important points.

## 7. Further Research
Suggest useful questions for future research.

Important instructions:
- Use simple, understandable language.
- Be factual and balanced.
- Do not invent statistics, studies, or references.
- Clearly identify uncertainty.
- If you do not know something, say so.
- Do not claim to have searched the web unless
  actual search results were provided.
- This report is based on your available knowledge.
"""

    for attempt in range(3):
        try:
            print("\nConnecting to Grok...")
            print("Generating your research report...")

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful and accurate "
                            "AI research assistant."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=4000
            )

            report = response.choices[0].message.content

            if not report:
                raise ValueError(
                    "Grok returned an empty response."
                )

            return report

        except APIStatusError as error:
            status = error.status_code

            # Retry temporary server errors
            if status in (429, 500, 502, 503, 504):
                if attempt < 2:
                    wait = 10 * (attempt + 1)

                    print(
                        f"API temporarily unavailable "
                        f"(HTTP {status})."
                    )
                    print(f"Retrying in {wait} seconds...")

                    time.sleep(wait)
                    continue

            raise

        except APIConnectionError:
            if attempt < 2:
                wait = 5 * (attempt + 1)

                print("Connection problem.")
                print(f"Retrying in {wait} seconds...")

                time.sleep(wait)
            else:
                raise

    return None


# ==========================================
# SAVE REPORT
# ==========================================

def save_report(topic, report):
    folder = Path("research")
    folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    # Make a safe filename from the topic
    safe_topic = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        topic
    ).strip("_")[:50]

    filename = f"{safe_topic}_{timestamp}.md"
    filepath = folder / filename

    content = f"""# Research Report

*Topic:* {topic}

*Generated:* {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

*AI Model:* {MODEL}

---

{report}
"""

    filepath.write_text(
        content,
        encoding="utf-8"
    )

    return filepath


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    print("=" * 50)
    print("          AI RESEARCH AGENT")
    print("              Powered by Grok")
    print("=" * 50)

    print("\nModel:", MODEL)

    while True:
        topic = input(
            "\nEnter a research topic "
            "(or type 'exit' to quit): "
        ).strip()

        if topic.lower() in ("exit", "quit"):
            print("Research Agent closed.")
            break

        if not topic:
            print("Please enter a topic.")
            continue

        try:
            report = generate_report(topic)

            if report:
                print("\n" + "=" * 50)
                print("             RESEARCH REPORT")
                print("=" * 50)

                print(report)

                filepath = save_report(
                    topic,
                    report
                )

                print("\n" + "=" * 50)
                print("Research completed successfully!")
                print(f"Report saved to: {filepath}")
                print("=" * 50)

        except APIStatusError as error:
            print("\nGrok API error.")
            print("HTTP status:", error.status_code)

            if error.status_code == 401:
                print(
                    "Check your XAI_API_KEY in the .env file."
                )
            elif error.status_code == 403:
                print(
                    "Check API access, account permissions, "
                    "and billing."
                )
            elif error.status_code == 404:
                print(
                    "The model may be unavailable. "
                    "Check XAI_MODEL in your .env file."
                )
            elif error.status_code == 429:
                print(
                    "Rate limit or usage quota reached. "
                    "Check your xAI console."
                )
            else:
                print(error)

        except APIConnectionError:
            print(
                "\nCould not connect to the xAI API. "
                "Check your internet connection."
            )

        except Exception as error:
            print("\nUnexpected error:", error)


if __name__ == "__main__":   
    main()