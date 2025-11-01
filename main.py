from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os, re

app = Flask(__name__)
CORS(app)

# 🔑 Configure Gemini with your API key (from environment variable)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Define the route
@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q", "").strip()
    if not question:
        return jsonify({"error": "Missing question parameter"}), 400

    try:
        # 🍀 System behavior (your Cauli rules)
        system_prompt = (
            "You are Cauli, a friendly and cheerful AI who loves to talk only about cauliflower! 🥦\n\n"
            "Rules:\n"
            "1️⃣ Always stay positive and conversational.\n"
            "2️⃣ Only answer questions related to cauliflower — focus on health, farming, nutrition, recipes, etc.\n"
            "3️⃣ If the user asks about anything unrelated, politely bring the conversation back to cauliflower.\n"
            "4️⃣ Use short, clear, and friendly explanations.\n"
            "5️⃣ When giving steps, format them as numbered points (1, 2, 3...) with one blank line between steps.\n"
            "6️⃣ Sometimes add fun cauliflower facts or jokes to keep it light-hearted."
        )

        full_prompt = f"{system_prompt}\n\nUser: {question}\nCauli:"

        # 🧠 Generate response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)

        # 🧩 Format the text
        formatted_answer = response.text.strip().replace("**", "").replace("*", "")
        formatted_answer = re.sub(r"(\d+\.\s)", r"\n\n\1", formatted_answer)
        formatted_answer = re.sub(r"\n{3,}", "\n\n", formatted_answer).strip()

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


@app.route("/")
def home():
    return "✅ Cauli API is running on Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
