import streamlit as st
from main import generate_response, search_query
from datetime import datetime

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# JavaScript che rileva la modalità colore e permette di aggiungere una classe al body
st.markdown("""
<script>
    (function() {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        const bodyClass = prefersDark ? 'dark-mode' : 'light-mode';
        document.body.classList.add(bodyClass);
    })();
</script>
""", unsafe_allow_html=True)

# CSS per light/dark mode con box decorativi e timestamp
st.markdown("""
<style>
    .main {
        max-width: 750px;
        margin: 0 auto;
        padding: 1rem;
    }

    body.light-mode {
        background-color: #ffffff;
        color: #000000;
    }

    body.light-mode .chat-message.user-message {
        background-color: #f7f7f8;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    body.light-mode .chat-message.bot-message {
        background-color: #ececec;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    body.light-mode .chat-message .avatar {
        background-color: #ddd;
    }

    body.light-mode .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
    }

    body.light-mode .streamlit-expanderHeader {
        background-color: #f0f2f6;
        color: #000000;
    }

    body.light-mode h1 {
        color: #000000;
    }

    body.dark-mode {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }

    body.dark-mode .chat-message.user-message {
        background-color: #2a2a2a;
        border: 1px solid #333333;
        box-shadow: 0 1px 3px rgba(255,255,255,0.1);
    }

    body.dark-mode .chat-message.bot-message {
        background-color: #333333;
        border: 1px solid #444444;
        box-shadow: 0 1px 3px rgba(255,255,255,0.1);
    }

    body.dark-mode .chat-message .avatar {
        background-color: #333333;
    }

    body.dark-mode .stTextInput > div > div > input {
        background-color: #2a2a2a;
        color: #e0e0e0;
        border: 1px solid #444444;
    }

    body.dark-mode .streamlit-expanderHeader {
        background-color: #2a2a2a;
        color: #e0e0e0;
    }

    body.dark-mode h1 {
        color: #e0e0e0;
    }

    /* Stili comuni ad entrambe le modalità di illuminazione */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }

    .chat-message .avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.5rem;
        color: #fff;
        flex-shrink: 0;
    }

    .chat-message .message {
        max-width: calc(100% - 60px);
    }

    .timestamp {
        font-size: 0.8rem;
        color: #888888;
        margin-top: 0.5rem;
    }

    body.dark-mode .timestamp {
        color: #cccccc;
    }

    .stButton > button {
        background-color: #4a90e2;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        cursor: pointer;
    }

    .stButton > button:hover {
        background-color: #357ab8;
    }

    footer {visibility: hidden;}

    .source-info {
        font-size: 0.8rem;
        color: #aaa;
        margin-top: 0.5rem;
    }

    ::-webkit-scrollbar {
        width: 12px;
    }

    ::-webkit-scrollbar-track {
        background: inherit;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #444;
        border-radius: 6px;
        border: 3px solid inherit;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>Benvenuto!</h1>", unsafe_allow_html=True)

# Questo serve per ottenere la data e l'ora attuale
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if "history" not in st.session_state:
    st.session_state["history"] = []
chat_container = st.container()

# Visualizzazione dei messaggi
with chat_container:
    for message in st.session_state["history"]:
        timestamp = message.get("timestamp", "")
        if message["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-message user-message">
                    <div class="avatar">🧑</div>
                    <div class="message">
                        <div><strong>Tu</strong></div>
                        <div>{message['content']}</div>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-message bot-message">
                    <div class="avatar">🤖</div>
                    <div class="message">
                        <div><strong>Assistente</strong></div>
                        <div>{message['content']}</div>
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("Mostra fonti e chunk recuperati"):
                st.markdown("**Fonti utilizzate:**")
                for source in message.get('sources', []):
                    st.markdown(f"- {source}")

                st.markdown("\n**Chunk più rilevanti:**")
                for chunk in message.get('chunks', []):
                    st.markdown(f"```\n{chunk}\n```")

with st.form(key='chat_form', clear_on_submit=True):
    col1, col2 = st.columns([6,1])
    with col1:
        user_input = st.text_input("", placeholder="Scrivi un messaggio...", label_visibility="collapsed")
    with col2:
        submit_button = st.form_submit_button("Invia")

# Gestione dell'invio del messaggio
if submit_button and user_input:
    timestamp = get_current_timestamp()
    # Utente
    st.session_state["history"].append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })

    with st.spinner("Sto elaborando la risposta..."):
        relevant_chunks = search_query(user_input)
        response, sources, chunks_text = generate_response(user_input, relevant_chunks)
    # Chatbot
    st.session_state["history"].append({
        "role": "bot",
        "content": response,
        "sources": sources,
        "chunks": chunks_text,
        "timestamp": get_current_timestamp()
    })

    st.rerun()

# Pulsante che pulisce la chat e resetta i messaggi
with st.sidebar:
    if st.button("Pulisci Chat"):
        st.session_state["history"] = []
        st.rerun()
