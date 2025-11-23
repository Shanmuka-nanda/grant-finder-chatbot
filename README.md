# Grant Finder Chatbot

An AI-powered grant finder chatbot built with Python (Flask backend) and vanilla HTML/CSS/JavaScript frontend.

## Features

- 🤖 Intelligent grant search with relevance scoring
- 💬 Interactive chat interface
- 🎯 Smart matching based on keywords, categories, and descriptions
- 📱 Responsive design for all devices
- 🎨 Modern, beautiful UI

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Open the Application

Open `index.html` in your web browser, or navigate to `http://localhost:5000` in your browser.

## Usage

1. Type your grant search query in the input field (e.g., "education grants for nonprofits")
2. Press Enter or click the Send button
3. The chatbot will search through the grant database and return relevant matches
4. Review the grant details including amount, deadline, category, and eligibility

## Example Queries

- "education grants"
- "small business funding"
- "research grants for universities"
- "nonprofit grants"
- "environmental conservation"
- "healthcare innovation"
- "arts and culture"

## Project Structure

```
grant-finder/
├── app.py              # Flask backend with AI search logic
├── index.html          # HTML structure
├── styles.css          # CSS styling
├── script.js           # JavaScript for chat UI and API calls
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Technologies Used

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI Logic**: Custom relevance scoring algorithm

## Grant Database

The application includes a sample database of 10 grants across various categories:
- Research
- Business
- Education
- Environment
- Arts
- Healthcare
- Community
- Technology
- Nonprofit
- Youth

You can easily extend the `GRANTS_DATABASE` in `app.py` to add more grants.

