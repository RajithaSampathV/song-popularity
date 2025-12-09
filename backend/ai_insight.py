import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
print("🔹 Loaded .env file for GEMINI_API_KEY")

# Configure API key
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
print("🔹 GEMINI_API_KEY set:", bool(API_KEY))

# Initialize model once
model = genai.GenerativeModel("gemini-2.0-flash-001")
print("🔹 Gemini model initialized.")

def generate_song_insight(features: dict, popularity: float) -> str:
    """
    Generate a natural language explanation about why the model predicted this popularity.
    """
    print("🔹 generate_song_insight called")
    try:
        prompt = f"""
        You are an expert AI music analyst.
        Here are the extracted audio features and the predicted popularity score for a song.

        Popularity Score: {popularity}/100

        Features:
        {json.dumps(features, indent=2)}

        Explain in simple terms:
        1. Why might this song have received this predicted score?
        2. Which features contribute most to this outcome?
        3. Give 2-3 tips for improving the song's potential popularity.
        Make the tone friendly and useful for a music producer.
        """

        response = model.generate_content(prompt=prompt)
        # Gemini returns `response.result` as text
        insight_text = getattr(response, "result", None) or getattr(response, "output_text", None)

        if not insight_text:
            raise RuntimeError("Gemini returned empty response")

        print("🔹 Gemini response received")
        return insight_text.strip()

    except Exception as e:
        print("❌ Insight generation failed:", e)
        return f"Insight generation failed: {e}"
