# 🏦 NBE AI Chatbot

An AI-powered chatbot designed to assist NBE customers by providing information about banking services, accounts, cards, and loans.

## ✨ Features

* 🤖 AI-powered conversational chatbot
* 🏦 NBE banking information and services
* 📚 PDF-based knowledge base
* 🔍 Intent classification using Machine Learning
* 💬 Natural language interaction
* ⚡ Fast responses using Groq API
* 🌐 Flask web application
* 🔐 Secure API key management using environment variables

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Groq API**
* **OpenAI Python Client**
* **Machine Learning**
* **HTML / CSS / JavaScript**
* **PDF Knowledge Base**
* **python-dotenv**

## 📂 Project Structure

```text
NBE_AI_Chatbot/
│
├── app.py
├── train_model.py
├── intent_model.pkl
├── requirements.txt
├── .gitignore
│
├── knowledge/
│   ├── accounts.pdf
│   ├── cards.pdf
│   └── loans.pdf
│
├── templates/
│   └── index.html
│
└── static/
    ├── script.js
    ├── style.css
    ├── nbe background.png
    └── nbe background2.jpg
```

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Malakelwan20/AI-NBE-chatbot.git
```

### 2. Open the project

```bash
cd AI-NBE-chatbot
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the project folder and add:

```env
GROQ_API_KEY=your_api_key_here
```

> ⚠️ Never share your API key or upload the `.env` file to GitHub.

### 5. Run the application

```bash
python app.py
```

### 6. Open the chatbot

Open your browser and go to:

```text
http://127.0.0.1:5000
```

## 🧠 How It Works

The chatbot combines **Machine Learning** and **Generative AI**.

1. The user sends a question.
2. The system identifies the user's intent.
3. Relevant information is retrieved from the banking knowledge base.
4. The retrieved information is provided to the AI model.
5. The chatbot generates a natural-language response.
6. The response is displayed to the user through the Flask web interface.

## 🔐 Security

API credentials are stored locally in environment variables and are excluded from Git using `.gitignore`.

## 🎯 Project Goal

The goal of this project is to demonstrate how **Artificial Intelligence, Machine Learning, and Generative AI** can be integrated into banking applications to provide users with fast and accessible information about banking services.

## 👩‍💻 Author

**Malak Elwan**

Computer Science Student at AAST

---

⭐ If you find this project useful, feel free to star the repository!
