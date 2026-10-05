# MailCraft: AI-Powered Email Writer

MailCraft is a Generative AI web application that writes professional emails in seconds. The user describes a situation, chooses the email type, tone and length, and the app produces a ready-to-send email with a subject line.

## Features
- Eight email types (leave request, job application, follow-up, complaint, thank you, meeting request, apology, other)
- Four tones: formal, polite, friendly, persuasive
- Three lengths: short, medium, detailed
- Optional recipient and sender name
- Copy the email with one click, or regenerate it
- Automatic retry and clear messages when the AI service is busy

## Tech stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- AI: Google Gemini API

## How it works
User input -> prompt is built on the server -> Gemini API call -> subject and body are separated -> email is shown on the page

## Run it locally
1. Install Python 3 and clone this repository.
2. Install the libraries: `pip install -r requirements.txt`
3. Get a free API key from https://aistudio.google.com
4. Set the key (Windows Command Prompt): `set GEMINI_API_KEY=your_key_here`
5. Start the app: `python app.py`
6. Open http://127.0.0.1:5000

The API key is read from an environment variable and is never stored in the code.

## Screenshots
![Home page](screenshots/1-home.png)
![Apology email example](screenshots/2-example1.png)
![Thank-you email example](screenshots/3-example2.png)

## Limitations
- AI-generated emails can include details you did not provide, so always review before sending.
- The app currently runs only on the local computer.

## Future scope
- Public deployment
- Email history and saved templates
- Support for more languages
- Direct sending through email services

## Author
Anusha Sadu
