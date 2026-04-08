import streamlit as st
from pdf_processor import process_pdf
from embeddings import create_vectorstore
from chatbot import get_answer
from datetime import datetime
import json
import os
from auth import login_user, register_user
from progress_tracker import load_progress, save_progress, add_topic, update_topic_status, delete_topic, get_stats
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="EduBot - Chat with your Notes",
    page_icon="🎓",
    layout="wide"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Custom CSS
# Dynamic theme based on dark/light mode
if st.session_state.dark_mode:
    bg_color = "#0A1628"
    sidebar_bg = "#0D1F3C"
    sidebar_border = "#1B4F8A"
    text_color = "#FFFFFF"
    h2_color = "#38BDF8"
    chat_user_bg = "#1B3A5E"
    chat_asst_bg = "#0D2137"
    chat_input_bg = "#1B3A5E"
    chat_input_border = "#1B4F8A"
    btn_bg = "#1B4F8A"
    btn_hover = "#0D9488"
    success_bg = "#0D3D2E"
    success_border = "#0D9488"
    success_color = "#6EE7B7"
    info_bg = "#0D1F3C"
    info_border = "#1B4F8A"
    info_color = "#90CDF4"
    warning_bg = "#2D1F00"
    warning_border = "#F59E0B"
    expander_bg = "#0D1F3C"
    expander_border = "#1B4F8A"
    uploader_bg = "#0D1F3C"
    uploader_border = "#1B4F8A"
    scrollbar_track = "#0A1628"
    scrollbar_thumb = "#1B4F8A"
    scrollbar_hover = "#0D9488"
    metric_bg = "#0D1F3C"
    metric_border = "#1B4F8A"
else:
    bg_color = "#F8FAFC"
    sidebar_bg = "#FFFFFF"
    sidebar_border = "#CBD5E1"
    text_color = "#1E293B"
    h2_color = "#1B4F8A"
    chat_user_bg = "#EFF6FF"
    chat_asst_bg = "#F1F5F9"
    chat_input_bg = "#FFFFFF"
    chat_input_border = "#CBD5E1"
    btn_bg = "#1B4F8A"
    btn_hover = "#0D9488"
    success_bg = "#ECFDF5"
    success_border = "#0D9488"
    success_color = "#065F46"
    info_bg = "#EFF6FF"
    info_border = "#1B4F8A"
    info_color = "#1E40AF"
    warning_bg = "#FFFBEB"
    warning_border = "#F59E0B"
    expander_bg = "#F1F5F9"
    expander_border = "#CBD5E1"
    uploader_bg = "#F1F5F9"
    uploader_border = "#94A3B8"
    scrollbar_track = "#F8FAFC"
    scrollbar_thumb = "#94A3B8"
    scrollbar_hover = "#1B4F8A"
    metric_bg = "#F1F5F9"
    metric_border = "#CBD5E1"

st.markdown(f"""
<style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {sidebar_border};
    }}
    [data-testid="stSidebar"] .stMarkdown p {{
        color: #A0AEC0;
    }}
    h1 {{
        color: {text_color} !important;
        font-family: 'Arial', sans-serif;
        font-weight: 800;
    }}
    h2, h3 {{
        color: {h2_color} !important;
    }}
    .stCaption {{
        color: #64748B !important;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        background-color: {chat_user_bg} !important;
        border-radius: 12px;
        padding: 8px;
        margin: 4px 0;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
        background-color: {chat_asst_bg} !important;
        border-radius: 12px;
        padding: 8px;
        margin: 4px 0;
    }}
    [data-testid="stChatInput"] {{
        background-color: {chat_input_bg} !important;
        border: 1px solid {chat_input_border} !important;
        border-radius: 12px !important;
        color: {text_color} !important;
    }}
    .stButton > button {{
        background-color: {btn_bg} !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        background-color: {btn_hover} !important;
        transform: translateY(-1px);
    }}
    .stSuccess {{
        background-color: {success_bg} !important;
        border: 1px solid {success_border} !important;
        border-radius: 8px !important;
        color: {success_color} !important;
    }}
    .stInfo {{
        background-color: {info_bg} !important;
        border: 1px solid {info_border} !important;
        border-radius: 8px !important;
        color: {info_color} !important;
    }}
    .stWarning {{
        background-color: {warning_bg} !important;
        border: 1px solid {warning_border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stExpander"] {{
        background-color: {expander_bg} !important;
        border: 1px solid {expander_border} !important;
        border-radius: 8px !important;
    }}
    [data-testid="stFileUploader"] {{
        background-color: {uploader_bg} !important;
        border: 2px dashed {uploader_border} !important;
        border-radius: 12px !important;
    }}
    hr {{
        border-color: {sidebar_border} !important;
    }}
    ::-webkit-scrollbar {{
        width: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {scrollbar_track};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {scrollbar_thumb};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {scrollbar_hover};
    }}
    .stDownloadButton > button {{
        background-color: #0D9488 !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
    }}
    [data-testid="stMetric"] {{
        background-color: {metric_bg};
        border: 1px solid {metric_border};
        border-radius: 8px;
        padding: 12px;
    }}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ──
# ── CONSTANTS ──
HISTORY_FILE = "chat_sessions.json"

# ── AUTH FUNCTIONS ──
def show_login_page():
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px;">
        <div style="font-size: 70px;">🎓</div>
        <h1 style="color:#FFFFFF; font-size:42px; font-weight:800; margin:16px 0;">
            Welcome to EduBot
        </h1>
        <p style="color:#38BDF8; font-size:18px; margin-bottom:32px;">
            Your AI-Powered Study Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

        with tab_login:
            st.markdown("### Login to EduBot")
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

            if st.button("🔐 Login", use_container_width=True, key="login_btn"):
                if not username or not password:
                    st.error("❌ Please fill in all fields!")
                else:
                    success, name, message = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_name = name
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        with tab_register:
            st.markdown("### Create an Account")
            new_name = st.text_input("Full Name", key="reg_name", placeholder="Enter your full name")
            new_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
            new_password = st.text_input("Password", type="password", key="reg_password", placeholder="Choose a password")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Confirm your password")

            if st.button("📝 Create Account", use_container_width=True, key="register_btn"):
                if not new_name or not new_username or not new_password or not confirm_password:
                    st.error("❌ Please fill in all fields!")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match!")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                else:
                    success, message = register_user(new_username, new_password, new_name)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# ── HELPER FUNCTIONS ──
def load_all_sessions():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_all_sessions(sessions):
    with open(HISTORY_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

def create_new_session(pdf_name):
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    return session_id, {
        "title": f"📄 {pdf_name[:30]}",
        "pdf_name": pdf_name,
        "date": datetime.now().strftime("%d %b %Y, %H:%M"),
        "messages": []
    }

# ── SESSION STATE INIT ──

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = load_all_sessions()

if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""

if "uploaded_pdf_bytes" not in st.session_state:
    st.session_state.uploaded_pdf_bytes = None

if "uploaded_pdf_name" not in st.session_state:
    st.session_state.uploaded_pdf_name = ""

# ── SHOW LOGIN IF NOT LOGGED IN ──
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## 🎓 EduBot")
    st.markdown("---")

    # User info
    st.markdown(f"👤 **{st.session_state.user_name}**")
    st.caption(f"@{st.session_state.username}")
    # Dark/Light mode toggle
    mode_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(mode_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.user_name = ""
        st.session_state.current_session_id = None
        st.session_state.vectorstore = None
        st.session_state.pdf_name = ""
        st.rerun()

    st.markdown("---")

    # New Chat button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_session_id = None
        st.session_state.vectorstore = None
        st.session_state.pdf_name = ""
        st.rerun()

    st.markdown("---")

    # PDF Upload
    # PDF Upload
    st.markdown("### 📄 Upload PDF")

    # Toggle single/multiple
    upload_mode = st.radio(
        "Upload Mode",
        ["Single PDF", "Multiple PDFs"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if upload_mode == "Single PDF":
        uploaded_files = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            label_visibility="collapsed"
        )
        uploaded_files = [uploaded_files] if uploaded_files else []
    else:
        uploaded_files = st.file_uploader(
            "Choose multiple PDF files",
            type="pdf",
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

    if uploaded_files:
        # Get combined name
        pdf_names = [f.name for f in uploaded_files]
        combined_name = ", ".join(pdf_names[:2])
        if len(pdf_names) > 2:
            combined_name += f" +{len(pdf_names)-2} more"

        # Only process if files changed
        # Process if files changed OR vectorstore is not loaded
        if combined_name != st.session_state.pdf_name or st.session_state.vectorstore is None:
            with st.spinner(f"Processing {len(uploaded_files)} PDF(s)... ⏳"):
                from pdf_processor import process_multiple_pdfs
                chunks = process_multiple_pdfs(uploaded_files)
                if not chunks:
                    st.error("❌ No text found! Upload text-based PDFs.")
                else:
                    st.session_state.vectorstore = create_vectorstore(chunks)
                    st.session_state.pdf_name = combined_name
                    # Save PDF bytes for viewer
                    if len(uploaded_files) == 1:
                        uploaded_files[0].seek(0)
                        st.session_state.uploaded_pdf_bytes = uploaded_files[0].read()
                        st.session_state.uploaded_pdf_name = uploaded_files[0].name
                    else:
                        st.session_state.uploaded_pdf_bytes = None
                        st.session_state.uploaded_pdf_name = ""

                    # Check if ANY existing session has this PDF
                    matched_session_id = None

                    # Check all sessions for matching PDF name
                    for sid, sdata in st.session_state.all_sessions.items():
                        if sdata["pdf_name"] == combined_name:
                            matched_session_id = sid
                            break

                    if matched_session_id:
                        # Continue existing session automatically
                        st.session_state.current_session_id = matched_session_id
                        st.session_state.pdf_name = combined_name
                        save_all_sessions(st.session_state.all_sessions)
                        st.success("✅ Continuing your previous chat!")
                        st.rerun()
                    else:
                        # Create new session
                        session_id, session_data = create_new_session(combined_name)
                        st.session_state.current_session_id = session_id
                        st.session_state.all_sessions[session_id] = session_data
                        save_all_sessions(st.session_state.all_sessions)
                        st.success(f"✅ {len(uploaded_files)} PDF(s) ready!")
                        st.rerun()

                    st.info(f"📚 {len(chunks)} total chunks")

                    # Show list of uploaded PDFs
                    with st.expander("📄 Uploaded PDFs"):
                        for i, name in enumerate(pdf_names):
                            st.write(f"{i+1}. {name}")

    st.markdown("---")

    # ── CHAT HISTORY LIST (like Claude sidebar) ──
    st.markdown("### 🕐 Recent Chats")

    if st.session_state.all_sessions:
        # Sort by most recent first
        sorted_sessions = sorted(
            st.session_state.all_sessions.items(),
            key=lambda x: x[0],
            reverse=True
        )

        for session_id, session in sorted_sessions:
            is_active = session_id == st.session_state.current_session_id
            msg_count = len(session["messages"])

            # Highlight active session
            label = f"{'🟢 ' if is_active else ''}{session['title']}\n{session['date']} • {msg_count} msgs"

            if st.button(label, key=f"session_{session_id}", use_container_width=True):
                st.session_state.current_session_id = session_id
                st.session_state.vectorstore = None
                st.session_state.pdf_name = session["pdf_name"]
                st.rerun()

            # Delete session button
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("🗑️", key=f"del_{session_id}"):
                    del st.session_state.all_sessions[session_id]
                    save_all_sessions(st.session_state.all_sessions)
                    if st.session_state.current_session_id == session_id:
                        st.session_state.current_session_id = None
                    st.rerun()
    else:
        st.caption("No chats yet. Upload a PDF to start!")

# ── MAIN AREA ──
st.title("🎓 EduBot")
st.caption("Chat with your PDF Notes & Documents")

# Tabs for Chat and Summary
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["💬 Chat", "📝 Summary", "🧪 Quiz", "🃏 Flashcards", "📊 Progress", "🔍 Search & Bookmarks", "📄 View PDF"])
st.markdown("---")

# No session selected
# No session selected
with tab1:
    # No session selected
    if st.session_state.current_session_id is None:
        st.markdown("""
        <div style="text-align:center; padding: 60px 20px;">
            <div style="font-size: 80px;">🎓</div>
            <h1 style="color:#FFFFFF; font-size:48px; font-weight:800; margin:16px 0;">
                Welcome to EduBot
            </h1>
            <p style="color:#38BDF8; font-size:20px; margin-bottom:32px;">
                Your AI-Powered Study Assistant
            </p>
            <div style="
                background: linear-gradient(135deg, #0D1F3C, #1B3A5E);
                border: 1px solid #1B4F8A;
                border-radius: 16px;
                padding: 32px;
                max-width: 600px;
                margin: 0 auto;
                text-align: left;
            ">
                <p style="color:#90CDF4; font-size:16px; margin:12px 0;">
                    📄 <b style="color:white;">Upload a PDF</b> — textbook, notes, or question paper
                </p>
                <p style="color:#90CDF4; font-size:16px; margin:12px 0;">
                    💬 <b style="color:white;">Ask Questions</b> — in plain English, get instant answers
                </p>
                <p style="color:#90CDF4; font-size:16px; margin:12px 0;">
                    🕐 <b style="color:white;">Chat History</b> — all sessions saved automatically
                </p>
                <p style="color:#90CDF4; font-size:16px; margin:12px 0;">
                    📥 <b style="color:white;">Download Chats</b> — save your Q&A as TXT anytime
                </p>
            </div>
            <p style="color:#64748B; font-size:14px; margin-top:32px;">
                👈 Upload a PDF from the sidebar to get started!
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        session = st.session_state.all_sessions[st.session_state.current_session_id]

        st.markdown(f"**📄 PDF:** {session['pdf_name']}  |  **📅 Started:** {session['date']}")
        st.markdown("---")

        # Display all saved messages
        for idx, msg in enumerate(session["messages"]):
            with st.chat_message("user"):
                st.write(msg["question"])
            with st.chat_message("assistant"):
                st.write(msg["answer"])
                if "sources" in msg and msg["sources"]:
                    with st.expander("📄 View Source Pages"):
                        for i, src in enumerate(msg["sources"]):
                            st.markdown(f"**🔖 Source {i+1} — Page {src['page']}**")
                            st.info(src["content"])
                            st.markdown("---")
                # Bookmark button
                col1, col2 = st.columns([8, 1])
                with col2:
                    is_bookmarked = msg.get("bookmarked", False)
                    if st.button(
                        "⭐" if is_bookmarked else "☆",
                        key=f"bookmark_{st.session_state.current_session_id}_{idx}",
                        help="Bookmark this answer"
                    ):
                        session["messages"][idx]["bookmarked"] = not is_bookmarked
                        save_all_sessions(st.session_state.all_sessions)
                        st.rerun()

                st.caption(f"🕐 {msg['time']}  {'⭐ Bookmarked' if is_bookmarked else ''}")

        # Only allow new questions if vectorstore is loaded
        # Always show chat input if vectorstore loaded
        if st.session_state.vectorstore is not None:
            col1, col2 = st.columns([3, 1])
            with col2:
                language = st.selectbox(
                "🌍 Language",
                ["Auto Detect", "English", "Tamil", "Hindi", "Telugu", "Malayalam", "Kannada", "French", "Spanish"],
                label_visibility="collapsed"
            )
            with col1:
                question = st.chat_input("Ask a question from your notes...")

            if question:
                with st.chat_message("user"):
                    st.write(question)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking... 🤔"):
                        if language != "Auto Detect":
                            question_with_lang = f"{question}\n\n[Please respond in {language}]"
                        else:
                            question_with_lang = question
                        answer, sources = get_answer(
                            st.session_state.vectorstore,
                            question_with_lang
                        )
                    st.write(answer)

                    with st.expander("📄 View Source Pages"):
                        if sources:
                            for i, doc in enumerate(sources):
                                page_num = doc.metadata.get('page', 0) + 1
                                source_file = doc.metadata.get('source_file', 'Unknown PDF')
                                st.markdown(f"**🔖 Source {i+1} — {source_file} — Page {page_num}**")
                                st.info(doc.page_content[:300])
                                st.markdown("---")
                        else:
                            st.write("No source references found.")

                    time_now = datetime.now().strftime('%H:%M:%S')
                    st.caption(f"🕐 {time_now}")

                session["messages"].append({
                    "question": question,
                    "answer": answer,
                    "sources": [
                        {
                            "page": doc.metadata.get('page', 0) + 1,
                            "content": doc.page_content[:300]
                        } for doc in sources
                    ],
                    "time": datetime.now().strftime('%H:%M:%S')
                })
                save_all_sessions(st.session_state.all_sessions)
                st.rerun()

        else:
            # Show re-upload banner prominently
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1B3A5E, #0D2137);
                border: 1px solid #F59E0B;
                border-radius: 12px;
                padding: 16px;
                margin: 10px 0;
                text-align: center;
           ">
                <p style="color:#F59E0B; font-size:15px; font-weight:600; margin:0;">
                        ⚠️ To continue this chat, re-upload the PDF from the sidebar
                </p>
                <p style="color:#A0AEC0; font-size:13px; margin:8px 0 0 0;">
                    📄 <b style="color:white;">{session['pdf_name']}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Always show download button if messages exist
        if session["messages"]:
            st.markdown("---")
            history_text = f"EduBot Chat History\nPDF: {session['pdf_name']}\nDate: {session['date']}\n{'='*50}\n\n"
            for i, msg in enumerate(session["messages"]):
                history_text += f"Q{i+1}: {msg['question']}\nA{i+1}: {msg['answer']}\nTime: {msg['time']}\n{'-'*40}\n\n"

            st.download_button(
                label="📥 Download Chat as TXT",
                data=history_text,
                file_name=f"EduBot_{session['pdf_name'][:20]}.txt",
                mime="text/plain"
            )

# ── SUMMARY TAB ──
with tab2:
    st.markdown("## 📝 PDF Summary Generator")
    st.markdown("Get an instant AI-generated summary of your uploaded PDF!")
    st.markdown("---")

    if st.session_state.vectorstore is None:
        st.info("👈 Please upload a PDF from the sidebar first!")
    else:
        st.success(f"📄 Ready to summarize: **{st.session_state.pdf_name}**")

        # Language selector for summary
        summary_language = st.selectbox(
            "🌍 Summary Language",
            ["Auto Detect", "English", "Tamil", "Hindi", "Telugu", "Malayalam", "Kannada", "French", "Spanish"],
        )

        if st.button("⚡ Generate Summary", use_container_width=True):
            with st.spinner("Generating summary... this may take a moment ⏳"):
                from chatbot import generate_summary
                summary = generate_summary(
                    st.session_state.vectorstore,
                    pdf_name=st.session_state.pdf_name,
                    language=summary_language
                )

            st.markdown("### 📋 Summary")
            st.markdown(summary)
            st.markdown("---")

            # Download summary
            st.download_button(
                label="📥 Download Summary as TXT",
                data=summary,
                file_name=f"Summary_{st.session_state.pdf_name[:20]}.txt",
                mime="text/plain"
            )

# ── QUIZ TAB ──
# ── QUIZ TAB ──
with tab3:
    st.markdown("## 🧪 Interactive Quiz")
    st.markdown("Test your knowledge with AI-generated questions!")
    st.markdown("---")

    if st.session_state.vectorstore is None:
        st.info("👈 Please upload a PDF from the sidebar first!")
    else:
        st.success(f"📄 Ready to quiz: **{st.session_state.pdf_name}**")

        # Quiz settings
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.slider(
                "How many questions?",
                min_value=3,
                max_value=10,
                value=5
            )
        with col2:
            difficulty = st.selectbox(
                "Difficulty Level",
                ["Easy 🟢", "Medium 🟡", "Hard 🔴", "Mixed 🎯"]
            )

        # Generate quiz button
        if st.button("⚡ Generate Quiz", use_container_width=True):
            with st.spinner(f"Generating {num_questions} {difficulty} questions... ⏳"):
                from chatbot import generate_quiz
                quiz_raw = generate_quiz(
                    st.session_state.vectorstore,
                    num_questions,
                    difficulty
                )
            # Save quiz to session state
            st.session_state.quiz_raw = quiz_raw
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = {}
            st.session_state.quiz_score = 0

        # Display interactive quiz
        if "quiz_raw" in st.session_state and st.session_state.quiz_raw:
            st.markdown("---")

            # Parse quiz questions
            # Parse quiz questions
            valid_questions = []
            current_q = {"question": "", "options": {}, "correct": "", "explanation": ""}

            lines = st.session_state.quiz_raw.split("\n")

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Detect question line like Q1. or Q2.
                if line.startswith("Q") and len(line) > 2 and line[1].isdigit() and "." in line[:4]:
                    # Save previous question if valid
                    if current_q["question"] and current_q["options"] and current_q["correct"]:
                        valid_questions.append(dict(current_q))
                    # Start new question
                    current_q = {"question": "", "options": {}, "correct": "", "explanation": ""}
                    current_q["question"] = line.split(".", 1)[1].strip()

                elif line.startswith("A)") or line.startswith("A) "):
                    current_q["options"]["A"] = line[2:].strip()
                elif line.startswith("B)") or line.startswith("B) "):
                    current_q["options"]["B"] = line[2:].strip()
                elif line.startswith("C)") or line.startswith("C) "):
                    current_q["options"]["C"] = line[2:].strip()
                elif line.startswith("D)") or line.startswith("D) "):
                    current_q["options"]["D"] = line[2:].strip()
                elif "✅ Answer:" in line:
                    answer_part = line.split("✅ Answer:")[1].strip()
                    current_q["correct"] = answer_part[0].strip()
                    current_q["explanation"] = answer_part[2:].strip() if len(answer_part) > 2 else ""
                elif "Answer:" in line and not current_q["correct"]:
                    answer_part = line.split("Answer:")[1].strip()
                    current_q["correct"] = answer_part[0].strip()
                    current_q["explanation"] = answer_part[2:].strip() if len(answer_part) > 2 else ""

            # Add last question
            if current_q["question"] and current_q["options"] and current_q["correct"]:
                valid_questions.append(dict(current_q))

            # Show score if all answered
            answered_count = len(st.session_state.get("quiz_submitted", {}))
            total_count = len(valid_questions)

            if total_count > 0:
                st.markdown(f"### 📋 Quiz — {difficulty}")
                st.markdown(f"**Progress: {answered_count}/{total_count} answered**")
                st.progress(answered_count / total_count if total_count > 0 else 0)
                st.markdown("---")

            # Display each question
            for i, q_data in enumerate(valid_questions):
                q_key = f"q_{i}"
                is_submitted = q_key in st.session_state.get("quiz_submitted", {})
                user_answer = st.session_state.get("quiz_answers", {}).get(q_key)

                # Question card
                st.markdown(f"""
                <div style="
                    background: {'#0D1F3C' if st.session_state.dark_mode else '#F1F5F9'};
                    border: 1px solid {'#1B4F8A' if st.session_state.dark_mode else '#CBD5E1'};
                    border-radius: 12px;
                    padding: 16px;
                    margin-bottom: 8px;
                ">
                    <p style="color:{'#38BDF8' if st.session_state.dark_mode else '#1B4F8A'}; font-weight:700; font-size:14px; margin:0;">
                        Question {i+1} of {total_count}
                    </p>
                    <p style="color:{'#FFFFFF' if st.session_state.dark_mode else '#1E293B'}; font-size:16px; font-weight:600; margin:8px 0 0 0;">
                        {q_data['question']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Options
                if not is_submitted:
                    for opt_key, opt_val in q_data["options"].items():
                        if st.button(
                            f"{opt_key}) {opt_val}",
                            key=f"btn_{i}_{opt_key}",
                            use_container_width=True
                        ):
                            if "quiz_answers" not in st.session_state:
                                st.session_state.quiz_answers = {}
                            if "quiz_submitted" not in st.session_state:
                                st.session_state.quiz_submitted = {}

                            st.session_state.quiz_answers[q_key] = opt_key
                            st.session_state.quiz_submitted[q_key] = True
                            st.rerun()
                else:
                    # Show results after answer selected
                    user_ans = st.session_state.quiz_answers.get(q_key)
                    correct_ans = q_data["correct"]

                    for opt_key, opt_val in q_data["options"].items():
                        if opt_key == correct_ans:
                            st.markdown(f"""
                            <div style="background:#0D3D2E; border:2px solid #0D9488;
                            border-radius:8px; padding:10px; margin:4px 0;">
                                <span style="color:#6EE7B7; font-weight:700;">
                                    ✅ {opt_key}) {opt_val}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        elif opt_key == user_ans and user_ans != correct_ans:
                            st.markdown(f"""
                            <div style="background:#3D0D0D; border:2px solid #EF4444;
                            border-radius:8px; padding:10px; margin:4px 0;">
                                <span style="color:#FCA5A5; font-weight:700;">
                                    ❌ {opt_key}) {opt_val} (Your answer)
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="background:{'#0D1F3C' if st.session_state.dark_mode else '#F1F5F9'};
                            border:1px solid {'#1B4F8A' if st.session_state.dark_mode else '#CBD5E1'};
                            border-radius:8px; padding:10px; margin:4px 0;">
                                <span style="color:{'#A0AEC0' if st.session_state.dark_mode else '#64748B'};">
                                    {opt_key}) {opt_val}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)

                    # Result message
                    if user_ans == correct_ans:
                        st.markdown(f"""
                        <div style="background:#0D3D2E; border:1px solid #0D9488;
                        border-radius:8px; padding:12px; margin:8px 0;">
                            <p style="color:#6EE7B7; font-weight:700; margin:0;">
                                🎉 Correct! Well done!
                            </p>
                            <p style="color:#A7F3D0; margin:4px 0 0 0; font-size:13px;">
                                💡 {q_data['explanation']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background:#3D0D0D; border:1px solid #EF4444;
                        border-radius:8px; padding:12px; margin:8px 0;">
                            <p style="color:#FCA5A5; font-weight:700; margin:0;">
                                ❌ Wrong! The correct answer is {correct_ans})
                            </p>
                            <p style="color:#FECACA; margin:4px 0 0 0; font-size:13px;">
                                💡 {q_data['explanation']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

            # Final score
            if answered_count == total_count and total_count > 0:
                correct_count = sum(
                    1 for i, q in enumerate(valid_questions)
                    if st.session_state.quiz_answers.get(f"q_{i}") == q["correct"]
                )
                score_pct = int((correct_count / total_count) * 100)

                if score_pct >= 80:
                    emoji = "🏆"
                    msg = "Excellent! You're well prepared!"
                    color = "#6EE7B7"
                    bg = "#0D3D2E"
                    border = "#0D9488"
                elif score_pct >= 60:
                    emoji = "👍"
                    msg = "Good job! Keep practicing!"
                    color = "#FCD34D"
                    bg = "#2D1F00"
                    border = "#F59E0B"
                else:
                    emoji = "📚"
                    msg = "Keep studying! You'll do better next time!"
                    color = "#FCA5A5"
                    bg = "#3D0D0D"
                    border = "#EF4444"

                st.markdown(f"""
                <div style="background:{bg}; border:2px solid {border};
                border-radius:16px; padding:24px; text-align:center; margin:16px 0;">
                    <p style="font-size:48px; margin:0;">{emoji}</p>
                    <p style="color:{color}; font-size:28px; font-weight:800; margin:8px 0;">
                        {correct_count}/{total_count} Correct ({score_pct}%)
                    </p>
                    <p style="color:{color}; font-size:16px; margin:0;">
                        {msg}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Retry button
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.quiz_raw = ""
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = {}
                    st.rerun()
# ── FLASHCARD TAB ──
with tab4:
    st.markdown("## 🃏 Flashcard Generator")
    st.markdown("Auto-generate flashcards from your PDF for quick revision!")
    st.markdown("---")

    if st.session_state.vectorstore is None:
        st.info("👈 Please upload a PDF from the sidebar first!")
    else:
        st.success(f"📄 Ready to generate flashcards: **{st.session_state.pdf_name}**")

        # Number of flashcards slider
        num_cards = st.slider(
            "How many flashcards do you want?",
            min_value=5,
            max_value=20,
            value=10
        )

        if st.button("⚡ Generate Flashcards", use_container_width=True):
            with st.spinner(f"Generating {num_cards} flashcards... ⏳"):
                from chatbot import generate_flashcards
                flashcards_raw = generate_flashcards(
                    st.session_state.vectorstore,
                    num_cards
                )

            st.markdown("---")

            # Parse and display flashcards nicely
            cards = flashcards_raw.split("---")
            st.markdown(f"### 📚 {len(cards)} Flashcards Generated!")
            st.markdown("Click each card to reveal the answer!")
            st.markdown("---")

            for i, card in enumerate(cards):
                card = card.strip()
                if not card:
                    continue

                # Extract FRONT and BACK
                lines = card.split("\n")
                front = ""
                back = ""
                for line in lines:
                    if line.startswith("FRONT:"):
                        front = line.replace("FRONT:", "").strip()
                    elif line.startswith("BACK:"):
                        back = line.replace("BACK:", "").strip()

                if front and back:
                    # Display as expander (click to reveal)
                    with st.expander(f"🃏 Card {i+1}: {front}"):
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #0D9488, #1B4F8A);
                            border-radius: 12px;
                            padding: 20px;
                            text-align: center;
                        ">
                            <p style="color:#FFFFFF; font-size:18px; font-weight:600;">
                                {back}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")

            # Download flashcards
            st.download_button(
                label="📥 Download Flashcards as TXT",
                data=flashcards_raw,
                file_name=f"Flashcards_{st.session_state.pdf_name[:20]}.txt",
                mime="text/plain"
            )

# ── PROGRESS TRACKER TAB ──
with tab5:
    st.markdown("## 📊 Study Progress Tracker")
    st.markdown("Track your study topics and monitor your progress!")
    st.markdown("---")

    # Load progress for current user
    progress = load_progress(st.session_state.username)
    total, studying, completed, mastered = get_stats(progress)

    # ── STATS ROW ──
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="background:#0D1F3C; border:1px solid #1B4F8A;
        border-radius:10px; padding:16px; text-align:center;">
            <h2 style="color:#38BDF8; margin:0;">{total}</h2>
            <p style="color:#A0AEC0; margin:0;">Total Topics</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#0D1F3C; border:1px solid #F59E0B;
        border-radius:10px; padding:16px; text-align:center;">
            <h2 style="color:#F59E0B; margin:0;">{studying}</h2>
            <p style="color:#A0AEC0; margin:0;">Studying</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#0D1F3C; border:1px solid #0D9488;
        border-radius:10px; padding:16px; text-align:center;">
            <h2 style="color:#0D9488; margin:0;">{completed}</h2>
            <p style="color:#A0AEC0; margin:0;">Completed</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="background:#0D1F3C; border:1px solid #6EE7B7;
        border-radius:10px; padding:16px; text-align:center;">
            <h2 style="color:#6EE7B7; margin:0;">{mastered}</h2>
            <p style="color:#A0AEC0; margin:0;">Mastered</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── CHARTS ──
    if total > 0:
        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)

        # Donut Chart
        with chart_col1:
            st.markdown("#### 🍩 Study Status Overview")
            fig_donut = go.Figure(data=[go.Pie(
                labels=["Studying", "Completed", "Mastered"],
                values=[studying, completed, mastered],
                hole=0.6,
                marker=dict(colors=["#F59E0B", "#0D9488", "#38BDF8"]),
                textinfo="label+percent",
                textfont=dict(size=13),
            )])
            fig_donut.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=280,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=[dict(
                    text=f"<b>{total}</b><br>Topics",
                    x=0.5, y=0.5,
                    font_size=16,
                    font_color="#FFFFFF" if st.session_state.dark_mode else "#1E293B",
                    showarrow=False
                )]
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Bar Chart
        with chart_col2:
            st.markdown("#### 📊 Topics by Status")
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=["Studying", "Completed", "Mastered"],
                    y=[studying, completed, mastered],
                    marker_color=["#F59E0B", "#0D9488", "#38BDF8"],
                    text=[studying, completed, mastered],
                    textposition="outside",
                    textfont=dict(size=14, color="#FFFFFF" if st.session_state.dark_mode else "#1E293B"),
                )
            ])
            fig_bar.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                height=280,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    tickfont=dict(color="#FFFFFF" if st.session_state.dark_mode else "#1E293B"),
                    gridcolor="rgba(0,0,0,0)"
                ),
                yaxis=dict(
                    tickfont=dict(color="#FFFFFF" if st.session_state.dark_mode else "#1E293B"),
                    gridcolor="#1B4F8A" if st.session_state.dark_mode else "#E2E8F0"
                ),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Progress bar
        progress_pct = int((mastered / total) * 100)
        st.markdown(f"### 🎯 Overall Mastery: {progress_pct}%")
        st.progress(progress_pct / 100)
        st.markdown("---")

    # ── ADD NEW TOPIC ──
    st.markdown("### ➕ Add New Topic")
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        new_topic = st.text_input(
            "Topic Name",
            placeholder="e.g. Newton's Laws, Thermodynamics...",
            label_visibility="collapsed"
        )
    with col2:
        new_status = st.selectbox(
            "Status",
            ["Studying", "Completed", "Mastered"],
            label_visibility="collapsed"
        )
    with col3:
        if st.button("➕ Add", use_container_width=True):
            if new_topic:
                success, message = add_topic(
                    st.session_state.username,
                    new_topic,
                    new_status
                )
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.warning(message)
            else:
                st.error("❌ Please enter a topic name!")

    st.markdown("---")

    # ── TOPIC LIST ──
    st.markdown("### 📚 Your Study Topics")

    if not progress:
        st.info("No topics added yet! Add your first topic above. 👆")
    else:
        # Status filter
        filter_status = st.selectbox(
            "Filter by Status",
            ["All", "Studying", "Completed", "Mastered"]
        )

        # Status emoji mapping
        status_emoji = {
            "Studying": "📖",
            "Completed": "✅",
            "Mastered": "🌟"
        }
        status_color = {
            "Studying": "#F59E0B",
            "Completed": "#0D9488",
            "Mastered": "#6EE7B7"
        }

        for topic, data in progress.items():
            if filter_status != "All" and data["status"] != filter_status:
                continue

            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.markdown(f"""
                <div style="padding: 8px 0;">
                    <span style="color:#FFFFFF; font-size:15px; font-weight:600;">
                        {status_emoji[data['status']]} {topic}
                    </span><br>
                    <span style="color:#64748B; font-size:11px;">
                        Added: {data['date_added']} | Updated: {data['date_updated']}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style="padding: 8px 0; text-align:center;">
                    <span style="
                        background: {status_color[data['status']]}22;
                        color: {status_color[data['status']]};
                        padding: 4px 12px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 600;
                    ">{data['status']}</span>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                new_status_update = st.selectbox(
                    "Update",
                    ["Studying", "Completed", "Mastered"],
                    index=["Studying", "Completed", "Mastered"].index(data["status"]),
                    key=f"status_{topic}",
                    label_visibility="collapsed"
                )
                if new_status_update != data["status"]:
                    update_topic_status(
                        st.session_state.username,
                        topic,
                        new_status_update
                    )
                    st.rerun()

            with col4:
                if st.button("🗑️", key=f"del_topic_{topic}"):
                    delete_topic(st.session_state.username, topic)
                    st.rerun()

            st.markdown("---")

# ── SEARCH & BOOKMARKS TAB ──
with tab6:
    st.markdown("## 🔍 Search & Bookmarks")
    st.markdown("---")

    search_tab, bookmark_tab = st.tabs(["🔍 Search Chats", "⭐ Bookmarks"])

    # ── SEARCH ──
    with search_tab:
        st.markdown("### 🔍 Search Inside All Chats")
        search_query = st.text_input(
            "Search",
            placeholder="Search for any question or answer...",
            label_visibility="collapsed"
        )

        if search_query:
            st.markdown(f"**Search results for:** `{search_query}`")
            st.markdown("---")

            found = False
            for session_id, session in st.session_state.all_sessions.items():
                for msg in session["messages"]:
                    if (search_query.lower() in msg["question"].lower() or
                            search_query.lower() in msg["answer"].lower()):
                        found = True
                        st.markdown(f"""
                        <div style="
                            background: #0D1F3C;
                            border: 1px solid #1B4F8A;
                            border-radius: 10px;
                            padding: 16px;
                            margin-bottom: 12px;
                        ">
                            <p style="color:#64748B; font-size:11px; margin:0;">
                                📄 {session['pdf_name']} | 📅 {session['date']}
                            </p>
                            <p style="color:#38BDF8; font-size:14px; font-weight:600; margin:8px 0 4px 0;">
                                Q: {msg['question']}
                            </p>
                            <p style="color:#FFFFFF; font-size:13px; margin:0;">
                                A: {msg['answer'][:300]}...
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

            if not found:
                st.info("No results found! Try a different search term.")
        else:
            st.info("👆 Type something to search across all your chats!")

    # ── BOOKMARKS ──
    with bookmark_tab:
        st.markdown("### ⭐ Bookmarked Answers")
        st.markdown("---")

        bookmarks_found = False
        for session_id, session in st.session_state.all_sessions.items():
            for idx, msg in enumerate(session["messages"]):
                if msg.get("bookmarked", False):
                    bookmarks_found = True
                    st.markdown(f"""
                    <div style="
                        background: #0D1F3C;
                        border: 1px solid #F59E0B;
                        border-radius: 10px;
                        padding: 16px;
                        margin-bottom: 12px;
                    ">
                        <p style="color:#64748B; font-size:11px; margin:0;">
                            ⭐ Bookmarked | 📄 {session['pdf_name']} | 🕐 {msg['time']}
                        </p>
                        <p style="color:#38BDF8; font-size:14px; font-weight:600; margin:8px 0 4px 0;">
                            Q: {msg['question']}
                        </p>
                        <p style="color:#FFFFFF; font-size:13px; margin:4px 0;">
                            A: {msg['answer']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Remove bookmark button
                    if st.button(
                        "🗑️ Remove Bookmark",
                        key=f"remove_bm_{session_id}_{idx}"
                    ):
                        st.session_state.all_sessions[session_id]["messages"][idx]["bookmarked"] = False
                        save_all_sessions(st.session_state.all_sessions)
                        st.rerun()

        if not bookmarks_found:
            st.info("No bookmarks yet! Click ☆ on any answer in the chat to bookmark it.")

        # Download bookmarks
        if bookmarks_found:
            st.markdown("---")
            bookmark_text = "EduBot Bookmarked Answers\n" + "=" * 50 + "\n\n"
            for session_id, session in st.session_state.all_sessions.items():
                for msg in session["messages"]:
                    if msg.get("bookmarked", False):
                        bookmark_text += f"PDF: {session['pdf_name']}\n"
                        bookmark_text += f"Q: {msg['question']}\n"
                        bookmark_text += f"A: {msg['answer']}\n"
                        bookmark_text += "-" * 40 + "\n\n"

            st.download_button(
                label="📥 Download Bookmarks as TXT",
                data=bookmark_text,
                file_name="EduBot_Bookmarks.txt",
                mime="text/plain"
            )

# ── PDF VIEWER TAB ──
with tab7:
    st.markdown("## 📄 PDF Viewer")
    st.markdown("View your uploaded PDF directly inside EduBot!")
    st.markdown("---")

    if st.session_state.uploaded_pdf_bytes is None:
        st.info("👈 Upload a single PDF from the sidebar to view it here!")
        st.caption("Note: PDF viewer works with single PDF uploads only.")
    else:
        st.success(f"📄 Viewing: **{st.session_state.uploaded_pdf_name}**")

        # Display PDF using base64
        import base64
        base64_pdf = base64.b64encode(
            st.session_state.uploaded_pdf_bytes
        ).decode("utf-8")

        pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="800px"
            style="border: 2px solid {'#1B4F8A' if st.session_state.dark_mode else '#CBD5E1'};
                   border-radius: 12px;"
            type="application/pdf"
        >
        </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

        # Download button
        st.markdown("---")
        st.download_button(
            label="📥 Download PDF",
            data=st.session_state.uploaded_pdf_bytes,
            file_name=st.session_state.uploaded_pdf_name,
            mime="application/pdf"
        )