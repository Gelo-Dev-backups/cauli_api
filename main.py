from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os, re

app = Flask(__name__)
CORS(app)

# 🔒 Load .env file
load_dotenv()

# 🔑 Initialize Gemini client with API key from environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q", "").strip()
    if not question:
        return jsonify({"error": "Missing question parameter"}), 400

    try:
        # 🍀 Define system behavior — cauliflower-only and friendly
        system_prompt = (
            "You are Cauli, a friendly and cheerful AI who loves to talk only about cauliflower! 🥦\n\n"
            "Rules:\n"
            "1️⃣ Always stay positive and conversational.\n"
            "2️⃣ Only answer questions related to cauliflower — more focus on health of cauliflower, facts, farming and side category only for nutrition, cooking, recipes etc.\n"
            "3️⃣ If the user asks about anything unrelated, politely bring the conversation back to cauliflower.\n"
            "4️⃣ Use short, clear, and friendly explanations.\n"
            "5️⃣ When giving steps, format them as numbered points (1, 2, 3...) with one blank line between each and enter step.\n"
            "6️⃣ Sometimes add fun cauliflower facts or jokes to keep it light-hearted."
        )

        full_prompt = f"{system_prompt}\n\nUser: {question}\nCauli:"

        # 🧠 Generate content from Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )

        # 🧩 Clean Markdown and format steps with spacing
        formatted_answer = response.text.strip().replace("**", "").replace("*", "")

        # Add a line break *before* each step number (1., 2., etc.)
        formatted_answer = re.sub(r"(\d+\.\s)", r"\n\n\1", formatted_answer)
        # Remove excessive blank lines
        formatted_answer = re.sub(r"\n{3,}", "\n\n", formatted_answer)
        formatted_answer = formatted_answer.strip()

        return jsonify({
            "status": "success",
            "question": question,
            "answer": formatted_answer
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
