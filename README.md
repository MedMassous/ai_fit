# 📚 AI Fit — Chat with Multiple PDFs

> Upload your PDF documents and have a conversation with them using the power of AI. Ask questions, get answers — all sourced directly from your files.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)
![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20LLaMA%203.3-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧠 What Does This App Do?

**AI Fit** lets you upload one or more PDF files and chat with their content in natural language. Instead of manually searching through pages, you simply ask a question like:

> *"What are the key findings in chapter 3?"*
> *"Summarize the terms of the contract."*
> *"What medications are mentioned in this report?"*

The app reads your PDFs, understands them using AI, and gives you accurate, context-aware answers — all within a clean chat interface.

---

## ✨ Features

- 📂 **Upload multiple PDFs** at once
- 💬 **Conversational AI** — the app remembers your previous questions in the same session
- ⚡ **Powered by Groq + LLaMA 3.3 70B** — fast and highly capable LLM
- 🔍 **Semantic search** — finds relevant information even if you don't use the exact words
- 🧩 **Runs locally** — your documents stay on your machine
- 🎨 **Clean chat UI** built with Streamlit

---

## 🏗️ How It Works (Behind the Scenes)

Here's what happens when you upload PDFs and ask a question:

```
Your PDFs
   ↓
1. Text Extraction   → Raw text is pulled from every page
   ↓
2. Chunking          → Text is split into overlapping 1000-character chunks
   ↓
3. Embedding         → Each chunk is converted into a vector (all-MiniLM-L6-v2)
   ↓
4. Vector Store      → Vectors are stored in a FAISS index for fast search
   ↓
5. Your Question     → Your question is also embedded and matched against chunks
   ↓
6. LLM Answer        → Groq's LLaMA 3.3 70B generates an answer from the matched chunks
   ↓
7. Chat History      → Conversation memory keeps context across follow-up questions
```

---

## 🚀 Getting Started

Follow these steps to run the project on your local machine.

### ✅ Prerequisites

Before you begin, make sure you have:
- **Python 3.9 or higher** installed → [Download Python](https://www.python.org/downloads/)
- A free **Groq API key** → [Get one here](https://console.groq.com/)
- Basic comfort with running commands in a terminal

---

### 📥 Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/ai_fit.git
cd ai_fit
```

> 💡 If you downloaded a ZIP file instead, just unzip it and open a terminal inside the extracted folder.

---

### 🐍 Step 2 — Create a Virtual Environment (Recommended)

A virtual environment keeps this project's dependencies isolated from your other Python projects.

```bash
# Create the environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` appear at the start of your terminal prompt.

---

### 📦 Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required libraries including Streamlit, LangChain, FAISS, and more. It may take a few minutes the first time.

---

### 🔑 Step 4 — Set Up Your API Key

1. Duplicate the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open the `.env` file in any text editor and replace the placeholder with your actual Groq API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

> 🔒 **Never share your `.env` file or commit it to GitHub.** It contains your private API key.

---

### ▶️ Step 5 — Run the App

```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`. If it doesn't, just paste that URL into your browser manually.

---

## 📖 How to Use

1. **Upload PDFs** — Use the sidebar on the left to upload one or more PDF files.
2. **Click "Process"** — The app will read, chunk, and index your documents. Wait for the spinner to finish.
3. **Ask questions** — Type your question in the text box at the top and press Enter.
4. **Keep chatting** — The app remembers your conversation, so you can ask follow-up questions naturally.

---

## 📁 Project Structure

```
ai_fit/
├── app.py               # Main application logic
├── htmlTemplates.py     # Custom CSS and HTML chat bubble templates
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
└── .env                 # Your actual API key (create this yourself, never commit it)
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError` | Make sure your virtual environment is activated and you ran `pip install -r requirements.txt` |
| `GROQ_API_KEY` not found | Double-check your `.env` file exists and contains the correct key |
| App crashes on PDF upload | Ensure your PDF has selectable text (scanned/image PDFs are not supported without OCR) |
| Slow first run | HuggingFace downloads the embedding model on first use — this is normal |
| Port already in use | Run `streamlit run app.py --server.port 8502` to use a different port |

---

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome! Feel free to:
- Open an [issue](../../issues) to report a bug or suggest a feature
- Fork the repo and submit a pull request

Please make sure your code is clean and well-commented before submitting a PR.

---

## 📄 License

This project is licensed under the **MIT License** — you're free to use, modify, and distribute it.

---

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/) for the RAG framework
- [Groq](https://groq.com/) for the blazing-fast LLM inference
- [Streamlit](https://streamlit.io/) for making Python apps easy to build
- [HuggingFace](https://huggingface.co/) for open-source embeddings
