import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from htmlTemplates import css, bot_template, user_template


# ── ONLY CHANGE: prompt now uses the user profile ──────────────────────────
def build_prompt(name="User", level="beginner", goal="lose weight"):
    template = f"""
Tu es AI Fit, un coach personnel virtuel spécialisé en fitness, nutrition et bien-être.
Tu dois répondre uniquement à partir du contexte fourni (documents PDF uploadés par l'utilisateur).

Profil de l'utilisateur :
- Nom : {name}
- Niveau de fitness : {level}
- Objectif : {goal}

Consignes importantes :
- Réponds en français ou englais.
- Adapte tes conseils au niveau et à l'objectif de l'utilisateur.
- Si l'information n'est pas présente dans le contexte, dis clairement :
  "Je ne trouve pas cette information dans les documents fournis."
- Donne des conseils clairs, structurés et adaptés à la condition physique de l'utilisateur.
- Pour les exercices, précise les séries, répétitions et temps de repos si disponibles.
- Pour la nutrition, précise les macros et calories si disponibles.
- Termine par une ligne "Sources :" avec les fichiers utilisés.

Historique de la conversation :
{{chat_history}}

Contexte extrait des documents fitness :
{{context}}

Question de l'utilisateur :
{{question}}
"""
    return PromptTemplate(
        input_variables=["chat_history", "context", "question"],
        template=template
    )


# ── ALL FUNCTIONS BELOW ARE UNCHANGED ──────────────────────────────────────

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore, name, level, goal):
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer')

    prompt = build_prompt(name, level, goal)  # pass profile here

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="AI Fit — Your Fitness Assistant", page_icon="💪")
    st.write(css, unsafe_allow_html=True)
    st.markdown("**Try asking:** *How many calories should I eat to lose weight? / What's my weekly workout schedule? / What does this supplement do?*")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("💪 Ask Your Fitness Coach")
    user_question = st.text_input("Ask about your workout plan, diet, or progress:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:

        # ── NEW: User Profile section ───────────────────────────────────────
        st.subheader("👤 Your Profile")

        name = st.text_input("Your name", placeholder="e.g. Alex")

        level = st.selectbox(
            "Fitness level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        goal = st.selectbox(
            "Your goal",
            ["Lose Weight", "Build Muscle", "Endurance"]
        )

        st.divider()  # just a line to separate profile from PDF upload
        # ───────────────────────────────────────────────────────────────────

        st.subheader("📄 Upload your fitness docs")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                # pass profile into the chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore,
                    name=name or "User",
                    level=level.lower(),
                    goal=goal.lower()
                )


if __name__ == '__main__':
    main()
