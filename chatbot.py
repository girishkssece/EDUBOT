from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

def get_answer(vectorstore, question):
    llm = get_llm()

    # Get relevant documents from PDF
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)

    # Combine context
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a helpful study assistant for students.

You have access to the student's uploaded notes as context below.
Follow these rules:
1. If the answer is clearly found in the context, answer from it directly.
2. If the context has partial information, use it along with your own knowledge.
3. If the context has no relevant information, use your own knowledge.
4. Always give a clear, detailed and student-friendly answer.
5. If it is a question from an exam or question paper, solve it step by step.
6. IMPORTANT: Always respond in the same language as the question asked.
   For example: if question is in Tamil, answer in Tamil.
   If in Hindi, answer in Hindi. If in English, answer in English.

Context from uploaded PDF:
{context}

Student's Question: {question}

Answer (in the same language as the question):"""

    response = llm.invoke(prompt)
    return response.content, docs


def generate_summary(vectorstore, pdf_name="the document", language="Auto Detect"):
    llm = get_llm()

    # Fetch more chunks to cover all uploaded PDFs
    retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
    docs = retriever.invoke("main topics overview introduction summary conclusion key concepts")

    # Group content by source file
    sources = {}
    for doc in docs:
        source = doc.metadata.get("source_file", "Document")
        if source not in sources:
            sources[source] = []
        sources[source].append(doc.page_content)

    # Build combined context with source labels
    context = ""
    for source_file, contents in sources.items():
        context += f"\n\n=== FROM: {source_file} ===\n"
        context += "\n\n".join(contents)

   # Build language instruction
    if language == "Auto Detect":
        lang_instruction = "Detect the primary language of the content and respond in that same language."
    else:
        lang_instruction = f"Always respond in {language} regardless of the content language."

    prompt = f"""You are an expert study assistant.
A student has uploaded the following PDF document(s): {pdf_name}

Based on the content below from ALL uploaded documents, provide a comprehensive summary.

For EACH document found in the content, provide:

1. 📌 **Document Overview** — What is this document about? (2-3 sentences)
2. 🎯 **Main Topics Covered** — List the key topics (as bullet points)
3. 📚 **Key Concepts** — Explain the most important concepts briefly
4. 💡 **Important Points to Remember** — List 5 key takeaways
5. 📝 **Study Tips** — Suggest how to best study this material

Content from all uploaded documents:
{context}

IMPORTANT: {lang_instruction}

Provide a well-structured, student-friendly summary for ALL documents:"""

    response = llm.invoke(prompt)
    return response.content

def generate_quiz(vectorstore, num_questions=5, difficulty="Medium 🟡"):
    llm = get_llm()

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke("key concepts important topics definitions")
    context = "\n\n".join([doc.page_content for doc in docs])

    # Difficulty instructions
    if "Easy" in difficulty:
        diff_instruction = """Easy difficulty rules:
- Ask straightforward factual questions
- Options should be clearly distinct
- Answers should be directly stated in the content
- Avoid tricky or complex questions"""
    elif "Hard" in difficulty:
        diff_instruction = """Hard difficulty rules:
- Ask complex analytical and application based questions
- Options should be very similar and require deep understanding
- Questions should require connecting multiple concepts
- Include calculation or reasoning based questions"""
    elif "Mixed" in difficulty:
        diff_instruction = """Mixed difficulty rules:
- Include a mix of Easy, Medium and Hard questions
- Label each question with its difficulty: [Easy], [Medium] or [Hard]
- Vary between factual, conceptual and analytical questions"""
    else:
        diff_instruction = """Medium difficulty rules:
- Ask conceptual understanding questions
- Options should require some thought to distinguish
- Questions should test understanding not just memory
- Include some application based questions"""

    prompt = f"""You are an expert teacher creating a {difficulty} quiz for students.

Based on the following content from the student's PDF, generate exactly {num_questions} multiple choice questions.

{diff_instruction}

Follow this EXACT format for each question:

Q1. [Question here]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
✅ Answer: [Correct option letter] - [Brief explanation]

---

Rules:
- Questions must be based ONLY on the content provided
- Make questions clear and student-friendly
- Each question must have exactly 4 options
- Only one option should be correct
- Give a brief explanation for the correct answer

Content from PDF:
{context}

Generate {num_questions} {difficulty} MCQ questions now:"""

    response = llm.invoke(prompt)
    return response.content

def generate_flashcards(vectorstore, num_cards=10):
    llm = get_llm()

    # Get chunks from PDF
    retriever = vectorstore.as_retriever(search_kwargs={"k": 15})
    docs = retriever.invoke("key concepts definitions important terms formulas")

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are an expert teacher creating flashcards for students.

Based on the following content from the student's PDF, generate exactly {num_cards} flashcards.

Follow this EXACT format for each flashcard:

🃏 Flashcard 1
FRONT: [Question or Term]
BACK: [Answer or Definition]

---

🃏 Flashcard 2
FRONT: [Question or Term]
BACK: [Answer or Definition]

---

Rules:
- Each flashcard must have a FRONT (question/term) and BACK (answer/definition)
- Keep FRONT short and clear — one question or term
- Keep BACK concise but complete — 1 to 3 sentences max
- Cover different topics from the document
- Focus on key concepts, definitions, formulas, and important facts
- Make them useful for quick revision before exams

Content from PDF:
{context}

Generate {num_cards} flashcards now:"""

    response = llm.invoke(prompt)
    return response.content