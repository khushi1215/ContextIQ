import requests
import streamlit as st
BACKEND_URL = "http://localhost:8000"
if "document_ready" not in st.session_state:
    st.session_state.document_ready = False
st.set_page_config(
    page_title="ContextIQ",
    page_icon="📄",
    layout="wide"
)

# Custom Styling
st.markdown(
    """
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-bottom:5px;
    color: var(--text-color);
}

.sub-title{
    text-align:center;
    color: var(--text-color);
    opacity: 0.7;
    margin-bottom:30px;
    font-size:17px;
}

.status-card{
    background: var(--secondary-background-color);
    color: var(--text-color);
    padding:14px;
    border-radius:12px;
    border:1px solid rgba(128,128,128,0.25);
    margin-bottom:15px;
}

.metric-card{
    background: var(--secondary-background-color);
    color: var(--text-color);
    padding:15px;
    border-radius:12px;
    border:1px solid rgba(128,128,128,0.25);
}

.answer-card{
    background: var(--secondary-background-color);
    color: var(--text-color);
    padding:24px;
    border-radius:14px;
    border-left:5px solid #00C853;
    line-height:1.8;
    font-size:16px;
}

.source-card{
    background: var(--secondary-background-color);
    color: var(--text-color);
    padding:16px;
    border-radius:14px;
    margin-bottom:12px;
    border-left:4px solid #4F8BF9;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}

.footer{
    text-align:center;
    color: var(--text-color);
    opacity:0.6;
    font-size:14px;
    margin-top:40px;
}

</style>
""",
    unsafe_allow_html=True,
)

# Title
st.markdown(
    """
<div class="main-title">
📄 ContextIQ
</div>

<div class="sub-title">
Transform documents into an intelligent, searchable knowledge base.
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:

    st.title("⚙ System")

    try:

        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=3,
        )

        if response.status_code == 200:

            st.success("Backend Connected")

        else:

            st.error("Backend Unavailable")

    except requests.exceptions.ConnectionError:

        st.error("Backend Offline")

    st.divider()

    st.subheader("Project")

    st.write("Embedding Model")

    st.caption("all-MiniLM-L6-v2")

    st.write("LLM")

    st.caption("Qwen 2.5 : 1.5B")

    st.write("Vector Database")

    st.caption("FAISS")

    st.divider()

    st.subheader("Upload Document")

    uploaded = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
    )

    if uploaded:
        st.success(f"Selected: {uploaded.name}")

    if st.button(
        "Process document",
        use_container_width=True,
    ):

        if uploaded:

            with st.spinner(
                "Processing document and preparing it for question answering..."
            ):

                ingest_response = requests.post(
                    f"{BACKEND_URL}/ingest",
                    files={
                        "file": (
                            uploaded.name,
                            uploaded.getvalue(),
                            "application/pdf",
                        )
                    },
                    timeout=300,
                )

            if ingest_response.status_code == 200:
                st.success("Document processed successfully. You can now start asking questions.")
                st.toast("Document is ready for questions.")
                st.session_state.document_ready = True
            else:
                st.error(ingest_response.text)
    st.divider()

    with st.expander("About this Project"):

        st.write("Backend : FastAPI")

        st.write("Frontend : Streamlit")

        st.write("Embeddings : Sentence Transformers")

        st.write("Vector Store : FAISS")

        st.write("LLM : Ollama")

#Tabs
chat_tab, analytics_tab = st.tabs(["Chat", "Analytics"])
#Tab 1: Chat
with chat_tab:

    st.header("Ask Questions")

    st.caption(
        "Ask questions based only on the uploaded document."
    )

    st.write("")

    query = st.text_area(
        "Question",
        placeholder="Example: What is this document about?",
        height=120,
    )

    ask_clicked = st.button(
    "Ask",
    type="primary",
    use_container_width=False,
    )

    if ask_clicked:

        if not query.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            progress = st.progress(0)

            progress.progress(20)

            status = st.empty()

            status.info(
                "Retrieving relevant document info..."
            )

            try:

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "query": query,
                    },
                    timeout=300,
                )

                progress.progress(60)

                response.raise_for_status()

                data = response.json()

                progress.progress(100)

                status.success(
                    "Response generated successfully."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Unable to connect to the backend."
                )

                st.stop()

            except requests.exceptions.HTTPError as exc:

                st.error(
                    f"Backend Error\n\n{exc}"
                )

                st.stop()

            st.write("")

            st.subheader("Answer")

            st.markdown(
                f"""
<div class="answer-card">

{data.get("answer","No answer generated.")}

</div>
""",
                unsafe_allow_html=True,
            )

            st.write("")

            st.subheader("Source Chunks")
            sources = data.get(
                    "sources",
                    [],
                )

            if sources:

                    for i, source in enumerate(
                        sources,
                        start=1,
                    ):

                        st.markdown(
                            f"""
<div class="source-card">

<b>Source {i}</b><br>

{source}

</div>
""",
                            unsafe_allow_html=True,
                        )

            else:

                    st.info(
                        "No sources available."
                    )

    else:

        st.info(
            "Upload and process a PDF to begin asking questions."
        )

#Tab 2: Analytics
with analytics_tab:

    st.header("Usage Analytics")

    st.caption(
        "Statistics collected from all document queries."
    )

    st.write("")

    refresh_col, _ = st.columns([1,4])

    with refresh_col:

        if st.button(
            "Refresh Statistics",
            use_container_width=True,
        ):
            st.rerun()

    try:

        analytics_response = requests.get(
            f"{BACKEND_URL}/analytics",
            timeout=10,
        )

        analytics_response.raise_for_status()

        stats = analytics_response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "Backend is not running."
        )

        st.stop()

    except requests.exceptions.HTTPError as exc:

        st.error(
            f"Backend Error\n\n{exc}"
        )

        st.stop()

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Questions Asked",
            stats.get(
                "total_queries",
                0,
            ),
        )

    with col2:

        st.metric(
            "Average Response Time",
            f'{stats.get("average_latency_ms",0):.0f} ms',
        )

    with col3:

        st.metric(
            "Questions Without Context",
            stats.get(
                "unanswered_queries",
                0,
            ),
        )

    st.write("")

    st.subheader(
        "Frequently Asked Questions"
    )

    frequent = stats.get(
        "most_frequent_questions",
        [],
    )

    if frequent:

        for item in frequent:

            question = item.get(
                "question",
                "",
            )

            frequency = item.get(
                "count",
                0,
            )

            st.markdown(
                f"""
<div class="source-card">

<b>{question}</b>

<br><br>

Asked <b>{frequency}</b> time(s)

</div>
""",
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "No analytics available yet."
        )

st.divider()

st.markdown(
    """
<div class="footer">

Built using

<b>FastAPI</b> •
<b>Streamlit</b> •
<b>Sentence Transformers</b> •
<b>FAISS</b> •
<b>Ollama</b>

</div>
""",
    unsafe_allow_html=True,
)