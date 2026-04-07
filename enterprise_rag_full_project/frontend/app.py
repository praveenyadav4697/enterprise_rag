import os
import requests
import streamlit as st

st.set_page_config(page_title="Enterprise RAG Platform", page_icon="🧠", layout="wide")

api_base = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

def api_post(path, json=None, headers=None, files=None):
    return requests.post(f"{api_base}{path}", json=json, headers=headers, files=files, timeout=30)

def api_get(path, headers=None):
    return requests.get(f"{api_base}{path}", headers=headers, timeout=30)

st.title("Enterprise RAG Platform")
st.caption("Upload documents, ask questions, and save chat history in PostgreSQL.")

if "token" not in st.session_state:
    st.session_state.token = ""
if "username" not in st.session_state:
    st.session_state.username = ""

tab_login, tab_upload, tab_chat, tab_history = st.tabs(["Login", "Upload", "Chat", "History"])

with tab_login:
    st.subheader("Account")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Register"):
            try:
                r = api_post("/auth/register", json={"username": username, "password": password})
                st.success(f"Registered: {r.json()}")
            except Exception as e:
                st.error(f"Register failed: {e}")
        if st.button("Login"):
            try:
                r = api_post("/auth/login", json={"username": username, "password": password})
                data = r.json()
                if "access_token" in data:
                    st.session_state.token = data["access_token"]
                    st.session_state.username = username
                    st.success("Login successful")
                else:
                    st.error(str(data))
            except Exception as e:
                st.error(f"Login failed: {e}")
    with col2:
        st.write("Current user:")
        st.code(st.session_state.username or "not logged in")
        st.write("Token:")
        st.code(st.session_state.token[:40] + "..." if st.session_state.token else "none")

auth_headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}

with tab_upload:
    st.subheader("Upload a text file")
    st.write("Supported: .txt, .md, .csv, .log. The backend reads UTF-8 text.")
    uploaded = st.file_uploader("Choose a file", type=["txt", "md", "csv", "log"])
    if st.button("Upload document"):
        if not st.session_state.token:
            st.warning("Login first.")
        elif uploaded is None:
            st.warning("Select a file first.")
        else:
            try:
                files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "text/plain")}
                r = api_post("/documents/upload", headers=auth_headers, files=files)
                st.success(r.json())
            except Exception as e:
                st.error(f"Upload failed: {e}")

with tab_chat:
    st.subheader("Ask questions over your uploaded documents")
    query = st.text_area("Question", height=120, placeholder="Example: Summarize the main points from the uploaded documents.")
    if st.button("Ask"):
        if not st.session_state.token:
            st.warning("Login first.")
        elif not query.strip():
            st.warning("Enter a question.")
        else:
            try:
                r = api_post("/chat", headers=auth_headers, json={"query": query})
                data = r.json()
                st.markdown("### Answer")
                st.write(data.get("answer", ""))
                st.markdown("### Sources")
                for src in data.get("sources", []):
                    st.info(f"{src['filename']} | chunk {src['chunk_index']}")
                    st.write(src["content"])
            except Exception as e:
                st.error(f"Chat failed: {e}")

with tab_history:
    st.subheader("Recent chat history")
    if st.button("Refresh history"):
        pass
    if st.session_state.token:
        try:
            r = api_get("/history", headers=auth_headers)
            history = r.json()
            for item in history:
                with st.expander(f"Q: {item['query'][:80]}"):
                    st.write(item["response"])
                    st.json(item["sources"])
        except Exception as e:
            st.error(f"History fetch failed: {e}")
    else:
        st.info("Login to see chat history.")
