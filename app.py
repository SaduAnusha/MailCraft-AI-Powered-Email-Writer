"""MailCraft - AI-powered email writer (Flask backend).

Run:
    set GEMINI_API_KEY=your_key_here        (Windows CMD)
    $env:GEMINI_API_KEY="your_key_here"     (Windows PowerShell)
    export GEMINI_API_KEY=your_key_here     (Mac / Linux)
    python app.py
Then open http://127.0.0.1:5000
"""
import os
import time

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

EMAIL_TYPES = [
    "Leave request",
    "Job application",
    "Follow-up",
    "Complaint",
    "Thank you",
    "Meeting request",
    "Apology",
    "Other",
]
TONES = ["Formal", "Polite", "Friendly", "Persuasive"]
LENGTHS = {
    "Short": "about 60-90 words",
    "Medium": "about 120-170 words",
    "Detailed": "about 200-260 words",
}


def build_prompt(data):
    """Turn the form fields into one clear instruction for the AI model."""
    lines = [
        "You are an expert email writer. Write one complete, ready-to-send email.",
        f"Email type: {data['email_type']}",
        f"Tone: {data['tone']}",
        f"Length: {LENGTHS[data['length']]}",
        f"Situation: {data['situation']}",
    ]
    if data["recipient"]:
        lines.append(f"Recipient: {data['recipient']}")
    if data["sender"]:
        lines.append(f"Sender name (use it in the sign-off): {data['sender']}")
    lines += [
        "",
        "Rules:",
        "- Use only the facts given above. Where a detail is missing, write a clear "
        "placeholder in square brackets, for example [date].",
        "- Start the reply with exactly one line in the form: Subject: <subject line>",
        "- Then a blank line, then the email body with a greeting and a sign-off.",
        "- Output nothing else: no explanations, no markdown, no extra options.",
    ]
    return "\n".join(lines)


def split_subject(text):
    """Separate the 'Subject:' line from the email body."""
    text = text.strip()
    first, _, rest = text.partition("\n")
    if first.lower().startswith("subject:"):
        return first[len("subject:"):].strip(), rest.strip()
    return "", text


@app.route("/")
def index():
    return render_template(
        "index.html", email_types=EMAIL_TYPES, tones=TONES, lengths=list(LENGTHS)
    )


@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json(silent=True) or {}
    data = {
        "situation": str(payload.get("situation", "")).strip(),
        "email_type": payload.get("email_type", "Other"),
        "tone": payload.get("tone", "Formal"),
        "length": payload.get("length", "Medium"),
        "recipient": str(payload.get("recipient", "")).strip()[:100],
        "sender": str(payload.get("sender", "")).strip()[:100],
    }

    if not data["situation"]:
        return jsonify(error="Describe the situation first, then press Write email."), 400
    if len(data["situation"]) > 1000:
        return jsonify(error="The situation is too long. Keep it under 1000 characters."), 400
    if data["email_type"] not in EMAIL_TYPES or data["tone"] not in TONES or data["length"] not in LENGTHS:
        return jsonify(error="Please choose the email type, tone and length from the lists."), 400
    if not API_KEY:
        return jsonify(error="The server has no API key. Set GEMINI_API_KEY and restart the app."), 500

    body = {
        "contents": [{"parts": [{"text": build_prompt(data)}]}],
        # Newer models use part of this limit for internal thinking, so keep it generous.
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192},
    }

    resp = None
    for attempt in range(3):  # retry when the service is busy
        try:
            resp = requests.post(
                API_URL,
                headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"},
                json=body,
                timeout=60,
            )
        except requests.RequestException:
            return jsonify(error="Could not reach the AI service. Check your internet and try again."), 502
        if resp.status_code not in (429, 500, 503):
            break
        time.sleep(2 * (attempt + 1))

    if resp.status_code != 200:
        messages = {
            400: "The request was rejected. Check that your API key is correct.",
            403: "Your API key was not accepted. Create a new key and set it again.",
            404: "That model name is not available for your key. Set GEMINI_MODEL to a different model.",
            429: "You have reached the free usage limit for now. Wait a minute and try again.",
            500: "The AI service is having a problem. Please try again in a moment.",
            503: "The AI service is busy right now. Please press Write email again in a few seconds.",
        }
        msg = messages.get(resp.status_code, f"The AI service returned an error ({resp.status_code}).")
        return jsonify(error=msg), 502

    try:
        result = resp.json()["candidates"][0]
        text = result["content"]["parts"][0]["text"]
    except (KeyError, IndexError, ValueError):
        return jsonify(error="The AI did not return an email this time. Please try again."), 502

    if result.get("finishReason") == "MAX_TOKENS":
        return jsonify(error="The email was cut short. Please press Write email again."), 502

    subject, email_body = split_subject(text)
    return jsonify(subject=subject, body=email_body)


if __name__ == "__main__":
    app.run(debug=True)