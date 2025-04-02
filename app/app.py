import streamlit as st
import asyncio
import groq
import tempfile
import os
import time
from utils import initialize_vectorstore, format_docs, rag_prompt
from tavily_integration import web_response
from sklearn.feature_extraction.text import TfidfVectorizer

# Set page configuration
st.set_page_config(
    page_title="ABC - Chatbot",
    page_icon="🔤",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        50% { transform: translateX(5px); }
        75% { transform: translateX(-5px); }
        100% { transform: translateX(0); }
    }
    .shake {
        animation: shake 0.3s ease-in-out 2;
        background-color: #ffcccc !important;
        border: 2px solid red !important;
        border-radius: 5px;
        padding: 5px;
    }
    body { background-color: #18191A; color: white; }
    .stApp { background-color: #18191A; }
    .chat-row { display: flex; margin: 5px; width: 100%; }
    .row-reverse {flex-direction: row-reverse;}
    .chat-bubble {
    padding: 12px 18px;
    border-radius: 20px;
    max-width: 70%;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    word-wrap: break-word;
    margin-bottom: 5px; /* Added margin for padding between messages */
    }   
    .user { background-color: #0093E9; background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%); color: white; font-size: 1.25em}
    .assistant { background-color: transparent; color: white; font-size: 1.25em}
    .thinking { background-color: #3A3B3C; color: white; padding: 10px; border-radius: 10px; font-style: italic; max-width: 70%; font-size: 1.25em}
    .response { background-color: transparent; color: white; padding: 10px; border-radius: 10px; margin-top: 5px; max-width: 70%; font-size: 1.25em}
    input[type="text"] { background-color: #242526; color: white; border-radius: 10px; padding: 10px; border: none; width: 100%; font-size: 1.25em}
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🤖 Query LLM App")
st.sidebar.markdown('<h2 style="color: #54c0ff;">About</h2>', unsafe_allow_html=True)
st.sidebar.write("An AI-powered chatbot for KGPians 🎓")
st.sidebar.markdown("#### Technologies:")
st.sidebar.write("- Streamlit 🌐")
st.sidebar.write("- Open-Source LLM 🧠")
st.sidebar.write("- Groq ⚙️")
st.sidebar.write("- Tavily 🔍")

# Upload file section in sidebar
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

# Toggle button in sidebar
toggle = st.sidebar.toggle("Document-only Mode")

# Cache vector store initialization
# @st.cache_resource
# def get_vectorstore():
#     with st.spinner("Loading vector store... ⏳"):
#         return initialize_vectorstore()

@st.cache_resource
def get_vectorstore(files=None):
    with st.spinner("Loading vector store... ⏳"):
        return initialize_vectorstore(files=files)

vectorstore, retriever = get_vectorstore()

# Main app title
st.markdown('<h2 class="main-title">Hi There! 👋 How Can I Help You Today? 🚀</h2>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "assistant"
    content = message["content"]
    div = f"""
<div class="chat-row 
    {'' if role_class == 'assistant' else 'row-reverse'}">
    <div class="chat-bubble
    {'assistant' if role_class == 'assistant' else 'user'}">
        &#8203;{content}
    </div>
</div>
        """
    st.markdown(div, unsafe_allow_html=True)

# Handle toggle behavior
if toggle:
    if uploaded_file is None:
        # Apply shake effect using HTML
        st.sidebar.markdown('<div class="shake">⚠️ File required for Document-only mode!</div>', unsafe_allow_html=True)
        time.sleep(0.5)  # Brief delay for animation
    else:
        # Show success notification (pops up briefly)
        st.toast("Document-only mode activated!", icon="✅")
        time.sleep(0.5)  # Short visibility time
else:
    if "file_upload" in st.session_state:
        st.toast("⚠️ Document-only mode deactivated!", icon="⚠️")

GROQ_API_KEY = "GROQ API KEY HERE" # Replace with your actual Groq API key
# Groq client
client = groq.Groq(api_key=GROQ_API_KEY)

async def process_input(prompt):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    div = f"""
<div class="chat-row row-reverse">
    <div class="chat-bubble user">
        &#8203;{prompt}
    </div>
</div>
        """
    st.markdown(div, unsafe_allow_html=True)
    # st.markdown(f'<div class="chat-bubble user">{prompt}</div>', unsafe_allow_html=True)

    # Initialize variables for document processing
    docs_txt = ""
    temp_file_path = None
    document_vectorstore = None
    document_retriever = None
    
    # Process uploaded document if available and toggle is on
    if uploaded_file is not None and toggle:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name
        
        try:
            # Create a separate vector store for the uploaded document
            document_vectorstore, document_retriever = initialize_vectorstore(files=[temp_file_path])
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return
    
    # Decide sources based on toggle state
    if toggle and uploaded_file is not None and document_retriever:
        try:
            # Document-only mode: use only the uploaded document
            document_docs = await asyncio.to_thread(document_retriever.invoke, prompt)
            docs_txt = format_docs(document_docs)
        finally:
            # Clean up the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    else:
        # Standard mode: use only knowledge base and web search (no uploaded document)
        # Retrieve relevant documents from general knowledge base
        docs = await asyncio.to_thread(retriever.invoke, prompt)
        docs_re = format_docs(docs)

        # Perform web search
        web_search_results = await asyncio.to_thread(web_response, prompt)
        docs_txt = docs_re + "\n\n" + web_search_results
        
        # Apply TF-IDF filtering
        vectorizer = TfidfVectorizer()
        vectorizer.fit_transform([prompt, docs_txt])
        feature_names = vectorizer.get_feature_names_out()

        filtered_docs = []
        web_results_filtered = ""

        for doc in docs:
            for word in feature_names:
                if word in doc.page_content:
                    filtered_docs.append(doc)
                    break
        
        sentences = web_search_results.split(".")
        for sentence in sentences:
            for word in feature_names:
                if word in sentence:
                    web_results_filtered += sentence + "."
                    break

        docs_txt = format_docs(filtered_docs) + "\n\n" + web_results_filtered

    # Format the prompt for the model (request JSON response)
    rag_prompt_formatted = rag_prompt.format(context=docs_txt, question=prompt)
    
    # Add source indicators for clarity
    if toggle and uploaded_file is not None:
        rag_prompt_formatted += "\n\nNOTE: Please answer based ONLY on the content from the uploaded document."
    
    rag_prompt_formatted += "\n\nRespond with a JSON object containing 'thought' and 'answer' fields."

    # Groq API call
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",  # Use a supported Groq model
        messages=[
            {
                "role": "user",
                "content": rag_prompt_formatted,
            }
        ],
        response_format={"type": "json_object"}
    )

    response_content = chat_completion.choices[0].message.content

    # Parse JSON response
    try:
        import json
        response_json = json.loads(response_content)
        thinking = response_json.get("thought", "No thought provided.")
        response_text = response_json.get("answer", "No answer provided.")

    except (json.JSONDecodeError, AttributeError):
        thinking = "Error parsing response."
        response_text = response_content  # Fallback to raw response, if json fails

    # Initialize containers for dynamic updates
    thinking_container = st.empty()
    response_container = st.empty()

    # Function to stream thinking dynamically
    async def stream_thinking():
        full_thinking = ""
        words = thinking.split()
        for word in words:
            full_thinking += word + " "
            thinking_container.markdown(f'<div class="thinking">🤔 Thinking: {full_thinking}</div>', unsafe_allow_html=True)
            await asyncio.sleep(0.05)

    # Function to stream response dynamically
    async def stream_response():
        full_response = ""
        words = response_text.split()
        for word in words:
            full_response += word + " "
            response_container.markdown(f'<div class="response">{full_response}</div>', unsafe_allow_html=True)
            await asyncio.sleep(0.05)

    # Run both thinking and response streams asynchronously
    await stream_thinking()
    await stream_response()

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})


# Handle user input asynchronously
if prompt := st.chat_input("Ask me anything about KGP! 🤔"):
    asyncio.run(process_input(prompt))