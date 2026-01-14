from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__, static_folder="static")

# Put your API key in an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def build_prompt(code, level):
    if level == "beginner":
        return f"""
Explain the following code to a beginner programmer.
Use simple language.
Avoid jargon.
Explain what each part does and why it exists.

Code:
{code}
"""
    else:
        return f"""
Explain the following code to an experienced developer.
Focus on overall structure, patterns, and intent.
Do not explain basic syntax.

Code:
{code}
"""

@app.route("/explain", methods=["POST"])
def explain():
    data = request.json
    code = data.get("code", "")
    level = data.get("level", "beginner")

    prompt = build_prompt(code, level)

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful programming tutor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    explanation = response.choices[0].message.content

    return jsonify({"explanation": explanation})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
