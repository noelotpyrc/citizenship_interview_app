# US Citizenship Interview Prep App

A web-based application designed to help users prepare for the US Citizenship Naturalization Test (Civics Test). It offers multiple modes for studying, practicing, and challenging yourself.

## Features

-   **Study Mode:** Browse through all 100 civics questions with flashcards. Click to reveal answers.
-   **Interview Mode:** Simulate a real interview. Listen to questions (text-to-speech) and type your answers.
-   **Challenge Mode:** A gamified experience where you try to build a streak of correct answers. Questions are weighted based on your past performance (incorrectly answered questions appear more often).
-   **Stats Tracking:** Detailed statistics for every question, including mastery status and attempts history.
    -   **Accordion View:** Click on any question in the Stats tab to inspect the answer and quickly jump to its flashcard.
-   **Dynamic Answers:** Supports variable answers for questions that change based on location or time (e.g., current President, Governor, Senators).
    -   *Note: Includes logic to validate different valid answers for officials.*
-   **Fuzzy Matching:** Smarter answer validation that handles typos and variations in user input.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd interview_app
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install flask
    ```

4.  **Run the application:**
    ```bash
    export FLASK_APP=app.py
    flask run --port=5101
    ```

5.  **Open in Browser:**
    Navigate to `http://127.0.0.1:5101`

## Tech Stack

-   **Backend:** Python (Flask)
-   **Frontend:** HTML, CSS, JavaScript (Vanilla)
-   **Data:** JSON (Questions and User Progress)

## Usage

-   **Home:** Choose a mode from the navigation bar.
-   **Study:** Use the "Next" button to go through questions.
-   **Interview:** Type your answer and press Enter or "Check Answer".
-   **Stats:** Review your progress. Click rows to see answers.

## License

[MIT License](LICENSE)
