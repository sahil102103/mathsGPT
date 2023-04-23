import os
import openai
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/clear_history", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return redirect(url_for("index"))

@app.route("/request_help", methods=["POST"])
def request_help():
    # Get the previous math problem from session history
    math_problem, _ = session["history"][-1]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(math_problem),
        temperature=0.6,
    )
    result = response.choices[0].text.split("\n")
    # Add to session history
    session.setdefault("history", []).append((math_problem, result))
    return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        math_problem = request.form["math_problem"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(math_problem),
            temperature=0.6,
        )
        result = response.choices[0].text.split("\n")
        # Add to session history
        session.setdefault("history", []).append((math_problem, result))
        return render_template("index.html", result=result)

    return render_template("index.html")

def generate_prompt(math_problem):
    return f"""The following is a conversation with an AI assistant. The assistant is meant to guide you to solve the problem using the Socratic method.

Assistant: Can you tell me more about {math_problem}?
Human: It's a problem involving...
Assistant: What do you know about {math_problem} so far?
Human: I know that...
Assistant: What steps have you taken to solve the problem?
Human: I have tried...
Assistant: Have you considered...
Human: No, I haven't.
Assistant: How can you break down {math_problem} into smaller parts?
Human: I can break it down into...
Assistant: Great! Let's continue from there.
"""

if __name__ == "__main__":
    app.run(debug=True)

