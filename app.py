import os
import openai
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(math_problem, history):
    prompt = f"""The following is a conversation with an AI assistant. The assistant is meant to guide you to solve the problem using the Socratic method.

    """
    for name, message in history:
        prompt += f"{name}: {message}\n"
    prompt += f"""
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
    return prompt

@app.route("/clear_history", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return redirect(url_for("index"))

@app.route("/request_help", methods=["POST"])
def request_help():
    # Get the conversation history from session
    history = session.get("history", [])
    # Get the latest math problem from history
    math_problem, _ = history[-1]
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(math_problem, history),
        temperature=0.9,
    )
    result = response.choices[0].text.split("\n")
    # Add the response to history
    history.append(("Assistant", result))
    # Update the session history
    session["history"] = history
    return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        math_problem = request.form["math_problem"]
        # Get the conversation history from session
        history = session.get("history", [])
        # Add the user input to history
        history.append(("Human", math_problem))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(math_problem, history),
            temperature=0.6,
        )
        result = response.choices[0].text.split("\n")
        # Add the response to history
        history.append(("Assistant", result))
        # Update the session history
        session["history"] = history
        return render_template("index.html", result=result)

    # Clear the conversation history if requested
    if request.args.get("clear_history"):
        session.pop("history", None)
        return redirect(url_for("index"))

    return render_template("index.html", history=session.get("history", []))

if __name__ == "__main__":
    app.run(debug=False)
