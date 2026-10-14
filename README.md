# MailCraft: AI-Powered Email Writer

MailCraft is a Generative AI web application that writes professional emails in seconds. The user describes a situation, chooses the email type, tone and length, and the app produces a ready-to-send email with a subject line.

## Live Demo

Try it here: https://mailcraft-ai-powered-email-writer.onrender.com/

The app runs on a free hosting plan, so the first visit after a quiet period can take up to a minute to load.

## Features
- Eight email types (leave request, job application, follow-up, complaint, thank you, meeting request, apology, other)
- Four tones: formal, polite, friendly, persuasive
- Three lengths: short, medium, detailed
- Optional recipient and sender name
- Copy the email with one click, or regenerate it
- Automatic retry and clear messages when the AI service is busy

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- AI: Google Gemini API
- Hosting: Render (free plan)

## How It Works
User input -> prompt is built on the server -> Gemini API call -> subject and body are separated -> email is shown on the page

## Run It Locally
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
- The app uses a free AI quota, so it may show a usage-limit message at busy times.
- The free hosting plan goes to sleep when nobody is using it, so the first load can be slow.

## Future Scope
- Writing style levels (Human, Medium, Professional)
- Reason detail control (brief to in-depth)
- Email history and saved templates
- Support for more languages
- Direct sending through email services

## Author
Anusha Sadu