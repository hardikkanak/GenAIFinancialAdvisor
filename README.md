
# AI-Based Financial Advisor

## 📈 Project Objective
This Django project delivers **AI-based financial advice** tailored to user inputs by utilizing profile embeddings, vector search, prompt engineering, and AI-generated responses.

Select Input
![alt text](<ScreenShot Tool -20250426224232.png>)

Output
![alt text](<ScreenShot Tool -20250426224416.png>)


## 🔥 Project Flow

```
(User Input)
     ↓
(Profile Embedding)
     ↓
(Vector Search - FAISS)
     ↓
(Top Similar Profiles)
     ↓
(Customized Prompt Engineering)
     ↓
(OpenAI Chat Completion)
     ↓
(Formatted Financial Advice in HTML)
     ↓
(User Output: Display or Download)
```

## 🚀 Key Components
- **User Input Interface**: Users submit financial-related queries.
- **Profile Embedding**: Converts user profiles into high-dimensional vectors.
- **Vector Search (FAISS)**: Finds similar financial profiles for context.
- **Prompt Engineering**: Creates dynamic prompts tailored to user needs.
- **OpenAI Chat Completion**: Generates personalized financial advice.
- **HTML Formatting**: Advice is formatted nicely for display or download.

## 🛠️ Tech Stack
- **Backend**: Django
- **AI Models**: OpenAI GPT (Chat Completion API)
- **Vector Database**: FAISS
- **Frontend**: Django Templates (HTML/CSS)
- **Deployment**: [You can add deployment details here later]

## 📂 Project Structure
```
ai_financial_advisor/
│
├── core/               # Main Django app
│   ├── views.py        # Main view logic
│   └── templates/      # HTML templates
│
├── static/             # Static files (CSS, JS)
├── manage.py
└── README.md
```

## ⚙️ How to Run Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai-financial-advisor.git
   cd ai-financial-advisor
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scriptsctivate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (for OpenAI API Key, etc.)

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the server:**
   ```bash
   python manage.py runserver
   ```

7. **Visit:**
   ```
   http://127.0.0.1:8000/
   ```

## ✅ Future Improvements
- Add user authentication
- Enable profile management
- Improve financial advice accuracy with RAG (Retrieval-Augmented Generation)
- Support multilingual advice
- Deploy on AWS or Azure

## 🤝 Contribution
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
