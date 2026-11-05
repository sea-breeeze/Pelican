# Pelican AI

**An AI-powered desktop assistant that helps users understand the applications they're using.**

Pelican AI is a floating Windows desktop assistant powered by **Meta Muse Spark 1.3**. It allows users to select an open application, capture its interface, and ask natural-language questions about what they see.

Instead of searching through documentation or navigating unfamiliar menus, users can ask Pelican for contextual explanations directly from their desktop.

## Features

- **Floating desktop assistant:** A draggable Pelican interface that stays on top of other windows.
- **Application selection:** Discover and select currently open Windows applications.
- **Screenshot analysis:** Capture an application's interface and preview the screenshot before sending it to AI.
- **AI-powered explanations:** Ask questions about buttons, menus, settings, and other interface elements using Meta Muse Spark 1.3.
- **Windows UI Automation:** Collect accessible control names and types to provide additional context alongside screenshots.
- **Responsive interface:** Resize the assistant window to read longer responses.
- **Follow-up questions:** Ask multiple questions about a confirmed screenshot without capturing it again.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| PySide6 | Desktop GUI |
| Meta Muse Spark 1.3 | Multimodal AI reasoning and interface explanations |
| OpenAI Python SDK | Meta API integration |
| mss and Pillow | Screenshot capture and image handling |
| PyWinCtl | Application window discovery |
| uiautomation | Windows accessibility and UI inspection |
| python-dotenv | Environment variable configuration |

## How It Works

1. Launch Pelican AI.
2. Select an open Windows application.
3. Click **Capture Screen**.
4. Review and confirm the screenshot.
5. Type a question about the application.
6. Click **Analyze with AI**.
7. Pelican sends the confirmed screenshot, question, and available UI inspection information to Meta Muse Spark 1.3.
8. The AI response appears in Pelican's chat window.

Pelican uses screenshot content and accessibility information together to better understand the selected application's interface.

## Installation

### Requirements

- Windows 10 or 11
- Python 3.10 or newer
- A Meta API key with access to Muse Spark 1.3

### 1. Clone the repository

```bash
git clone https://github.com/sea-breeeze/Pelican.git
cd Pelican
```

Replace the repository URL if your GitHub repository uses a different name.

### 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
MODEL_API_KEY=your_meta_api_key_here
```

Never commit your real API key to GitHub.

### 5. Run Pelican

```powershell
python main.py
```

## Architecture

Pelican follows a Model-View-Controller-inspired structure:

- **Model:** Maintains application state and message history.
- **View:** Displays the floating assistant, screenshot confirmation, and chat interface.
- **Controller:** Coordinates user interactions, application selection, screenshot capture, and AI requests.
- **Services:** Handle Windows integration, accessibility inspection, screenshot processing, and Meta API communication.

AI requests run in a background Qt worker to keep the interface responsive.

## Privacy and Limitations

- Screenshots are sent to Meta's API only after the user explicitly confirms them.
- UI Automation may expose control names and other application text, which can also be included in AI requests.
- API credentials are loaded from a local `.env` file.
- Pelican provides explanations rather than automatically clicking or controlling applications.
- AI responses may be incomplete or incorrect and should be verified when necessary.
- The application is currently designed for Windows.

## Hackathon

Built for the **Meta Global AI Developer Hackathon**, using **Muse Spark 1.3** to make desktop applications easier to understand through multimodal AI.

## Future Improvements

- AI-assisted identification and highlighting of relevant interface controls.
- Conversation history across multiple questions.
- More detailed application guidance.
- Improved accessibility and onboarding.

## License

No license has been specified yet.