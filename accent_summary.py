from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  # Replace with your real key
)

def generate_summary(accent: str, confidence: float) -> str:
    prompt = (
        f"The speaker's accent was detected as {accent} with {confidence:.2%} confidence. "
        "Provide a short 2-3 sentence summary explaining this result in simple, non-technical language."
    )

    completion = client.chat.completions.create(
        model="mistralai/mistral-small-24b-instruct-2501:free",
        messages=[{"role": "user", "content": prompt}],
        extra_headers={
            "HTTP-Referer": "https://your-site.com",  # Optional
            "X-Title": "AccentAnalyzerApp",  # Optional
        },
    )

    return completion.choices[0].message.content.strip()
