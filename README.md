# 🎓 EduBot - AI-Powered Study Assistant

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![LangChain](https://img.shields.io/badge/LangChain-0.1-green)
![Groq](https://img.shields.io/badge/Groq-Llama%204%20Scout-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **EduBot** is an AI-powered PDF study platform that helps students learn smarter. Upload any PDF and get instant answers, summaries, quizzes, flashcards, and much more — all powered by cutting-edge AI!

---

## 🌐 Live Demo

👉 **Render:** [https://edubot-gdys.onrender.com](https://edubot-gdys.onrender.com)

---

## ✨ Features (22+)

| Feature | Description |
|---|---|
| 🔐 Login & Register | Secure authentication with SHA-256 password hashing |
| 🌙 Dark/Light Mode | Toggle between dark and light themes |
| 📄 Single PDF Upload | Upload and study a single PDF |
| 📚 Multiple PDF Upload | Upload and query multiple PDFs at once |
| 🔍 OCR Support | Extract text from scanned PDFs using Tesseract |
| 🤖 Smart Q&A (RAG) | AI-powered answers from your PDF content |
| 🔀 Hybrid Answer Mode | Combines PDF content with LLM knowledge |
| 🌍 Multilingual Support | Supports 8 languages including Tamil, Hindi, French |
| 💾 Persistent Chat | Chat history saved per user across sessions |
| 🔄 Chat Continuation | Continue previous chats from history |
| 📌 Source References | View exact page sources for every answer |
| 📝 Summary Generator | Generate comprehensive PDF summaries |
| 🧪 Interactive Quiz | Auto-generated MCQs with difficulty levels |
| 📊 Quiz Score Tracker | Track quiz performance over time |
| 🃏 Flashcard Generator | Create study flashcards from PDF content |
| 📈 Study Progress Tracker | Track topics and study progress |
| 📉 Progress Charts | Visualize progress with Plotly charts |
| 🔎 Search Inside Chats | Search through previous conversations |
| 🔖 Bookmark Answers | Save important answers for later |
| ⬇️ Download Chat History | Export chats as text files |
| 👁️ PDF Viewer | View uploaded PDFs page by page |
| ℹ️ About/Privacy/Terms | Professional footer with legal pages |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10** | Core programming language |
| **Streamlit** | Web application framework |
| **LangChain** | LLM orchestration framework |
| **Groq (Llama 4 Scout)** | Large Language Model for AI responses |
| **FAISS** | Vector database for semantic search |
| **HuggingFace MiniLM** | Sentence embeddings (localhost) |
| **Tesseract OCR** | Optical character recognition |
| **PyMuPDF** | PDF processing and rendering |
| **Plotly** | Interactive data visualizations |
| **HuggingFace Datasets** | Persistent cloud storage |

---

## 🏗️ Project Structure

```
EDUBOT/
├── app.py                  # Main Streamlit application
├── chatbot.py              # Groq LLM integration
├── embeddings.py           # FAISS vector store & embeddings
├── pdf_processor.py        # PDF text extraction
├── auth.py                 # User authentication
├── progress_tracker.py     # Study progress tracking
├── hf_storage.py           # HuggingFace Dataset storage
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- Tesseract OCR installed
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/girishkssece/EDUBOT.git
cd EDUBOT

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo GROQ_API_KEY=your_api_key_here > .env

# Run the application
streamlit run app.py
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |
| `HF_TOKEN` | HuggingFace token (for cloud storage) |

---

## 📸 Screenshots

### Login Page
- Clean, modern login interface with dark mode
- Secure registration with password confirmation

### Chat Interface
- Upload PDFs and ask questions instantly
- Source references shown for every answer

### Quiz Generator
- Auto-generated MCQs from PDF content
- Easy, Medium, Hard, and Mixed difficulty levels

---

## 🧠 How It Works

1. **Upload PDF** → PyMuPDF extracts text (Tesseract for scanned PDFs)
2. **Text Chunking** → LangChain splits text into semantic chunks
3. **Embeddings** → MiniLM converts chunks to vector embeddings
4. **FAISS Index** → Vectors stored in FAISS for fast similarity search
5. **Query** → User question converted to vector, top-k chunks retrieved
6. **LLM Response** → Groq Llama 4 Scout generates contextual answer

---

## 👨‍💻 Developer

**Girish K S**
- 🎓 B.Tech AI-DS, Sri Eshwar College of Engineering
- 📧 girish.ks2025aids@sece.ac.in
- 📱 8248734365
- 🔗 [GitHub](https://github.com/girishkssece)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) for the blazing fast LLM API
- [LangChain](https://langchain.com) for the LLM framework
- [Streamlit](https://streamlit.io) for the amazing web framework
- [HuggingFace](https://huggingface.co) for embeddings and storage
- [Anthropic Claude](https://claude.ai) for development assistance

---

*Built with ❤️ by Girish K S | Sri Eshwar College of Engineering | 2025*
