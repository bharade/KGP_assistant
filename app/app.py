# import streamlit as st
# import asyncio
# import groq
# import tempfile
# import os
# from utils import initialize_vectorstore, format_docs, rag_prompt
# from tavily_integration import web_response
# from sklearn.feature_extraction.text import TfidfVectorizer

# # Set page configuration
# st.set_page_config(
#     page_title="Query LLM App 🤖",
#     page_icon="🤖",
#     layout="wide"
# )

# # Custom CSS for styling
# st.markdown("""
#     <style>
#     .stApp { background-color: black; }
#     .chat-container { display: flex; flex-direction: column; gap: 10px; }
#     .chat-bubble {
#         padding: 10px 15px;
#         border-radius: 10px;
#         max-width: 75%;
#     }
#     .user { background-color: #b886e3; color:black; align-self: flex-end; text-align: right; }
#     .assistant { background-color: #7bd0e3; color: black; align-self: flex-start; text-align: left; }
#     .thinking { background-color: #f0f0f0; color: #333; padding: 10px; border-radius: 5px; margin-top: 5px; font-style: italic; }
#     .response { background-color: #5ce1f2; color: black; padding: 10px; border-radius: 5px; margin-top: 5px; }
#     </style>
# """, unsafe_allow_html=True)

# # Sidebar
# st.sidebar.title("🤖 Query LLM App")
# st.sidebar.markdown('<h3 style="color: red;">About</h3>', unsafe_allow_html=True)
# st.sidebar.write("An AI-powered chatbot for KGPians 🎓")
# st.sidebar.markdown("#### Technologies:")
# st.sidebar.write("- Streamlit 🌐")
# st.sidebar.write("- Deepseek r1:1.5B 💬")
# st.sidebar.write("- Open-Source LLM 🧠")

# # Upload file section in sidebar
# uploaded_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

# # Toggle button in sidebar
# toggle = st.sidebar.toggle("Document-only Mode")

# # Cache vector store initialization
# @st.cache_resource
# def get_vectorstore():
#     with st.spinner("Loading vector store... ⏳"):
#         return initialize_vectorstore()

# vectorstore, retriever = get_vectorstore()

# # Main app title
# st.markdown('<h2 class="main-title">Hi There! 👋 How Can I Help You Today? 🚀</h2>', unsafe_allow_html=True)

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# for message in st.session_state.messages:
#     role_class = "user" if message["role"] == "user" else "assistant"
#     content = message["content"]
#     st.markdown(f'<div class="chat-bubble {role_class}">{content}</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# GROQ_API_KEY = "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" # Replace with your actual Groq API key
# # deepseek_api_key="sk-1a9c2c7ef24b4b4d8a8fe7a382e2cb7d"
# # Groq client
# client = groq.Groq(api_key=GROQ_API_KEY)

# async def process_input(prompt):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.markdown(f'<div class="chat-bubble user">{prompt}</div>', unsafe_allow_html=True)

#     # Retrieve relevant documents asynchronously
#     docs = await asyncio.to_thread(retriever.invoke, prompt)
#     docs_re = format_docs(docs)

#     web_search_results = await asyncio.to_thread(web_response, prompt)
#     docs_txt = docs_re + "\n\n" + web_search_results
    
#     #docs_txt = format_docs(docs)
#     vectorizer = TfidfVectorizer()
#     vectorizer.fit_transform([prompt, docs_txt])
#     feature_names = vectorizer.get_feature_names_out()

#     filtered_docs = []
#     web_results_filtered = ""

#     for doc in docs:
#         for word in feature_names:
#             if word in doc.page_content:
#                 filtered_docs.append(doc)
#                 break
    
#     sentences = web_search_results.split(".")
#     for sentence in sentences:
#         for word in feature_names:
#             if word in sentence:
#                 web_results_filtered += sentence + "." #add the sentence if a word matches.
#                 break

#     docs_txt = format_docs(filtered_docs) + "\n\n" + web_results_filtered

#     # docs_txt = format_docs(filtered_docs)
#     # print(docs_txt)


#     # docs_txt = format_docs(docs)
#     # print(len(docs_txt))

#     # max_doc_length = 8000 #add this into the process input function.
#     # truncated_docs = [doc.page_content[:max_doc_length] for doc in docs]
#     # docs_txt = "\n\n".join(truncated_docs)

#     # Perform web search asynchronously
#     # web_search_results = await asyncio.to_thread(web_response, prompt)
#     # docs_txt = docs_txt + "\n\n" + web_search_results

#     # Format the prompt for the model (request JSON response)
#     rag_prompt_formatted = rag_prompt.format(context=docs_txt, question=prompt)
#     rag_prompt_formatted += "\n\nRespond with a JSON object containing 'thought' and 'answer' fields."

#     # Groq API call
#     chat_completion = client.chat.completions.create(
#         model="llama3-70b-8192",  # Use a supported Groq model
#         messages=[
#             {
#                 "role": "user",
#                 "content": rag_prompt_formatted,
#             }
#         ],
#         response_format={"type": "json_object"}
#     )

#     response_content = chat_completion.choices[0].message.content

#     # Parse JSON response
#     try:
#         import json
#         response_json = json.loads(response_content)
#         thinking = response_json.get("thought", "No thought provided.")
#         response_text = response_json.get("answer", "No answer provided.")

#     except (json.JSONDecodeError, AttributeError):
#         thinking = "Error parsing response."
#         response_text = response_content #Fallback to raw response, if json fails

#     # Initialize containers for dynamic updates
#     thinking_container = st.empty()
#     response_container = st.empty()

#     # Function to stream thinking dynamically
#     async def stream_thinking():
#         full_thinking = ""
#         words = thinking.split()
#         for word in words:
#             full_thinking += word + " "
#             thinking_container.markdown(f'<div class="thinking">🤔 Thinking: {full_thinking}</div>', unsafe_allow_html=True)
#             await asyncio.sleep(0.05)

#     # Function to stream response dynamically
#     async def stream_response():
#         full_response = ""
#         words = response_text.split()
#         for word in words:
#             full_response += word + " "
#             response_container.markdown(f'<div class="response">🤖 Response: {full_response}</div>', unsafe_allow_html=True)
#             await asyncio.sleep(0.05)

#     # Run both thinking and response streams asynchronously
#     await stream_thinking()
#     await stream_response()

#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response_text})


# # Handle user input asynchronously
# if prompt := st.chat_input("Ask me anything about KGP! 🤔"):
#     asyncio.run(process_input(prompt))

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
    page_title="Query LLM App 🤖",
    page_icon="🤖",
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
    .stApp { background-color: black; }
    .chat-container { display: flex; flex-direction: column; gap: 10px; }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 10px;
        max-width: 75%;
    }
    .user { background-color: #b886e3; color:black; align-self: flex-end; text-align: right; }
    .assistant { background-color: #7bd0e3; color: black; align-self: flex-start; text-align: left; }
    .thinking { background-color: #f0f0f0; color: #333; padding: 10px; border-radius: 5px; margin-top: 5px; font-style: italic; }
    .response { background-color: #5ce1f2; color: black; padding: 10px; border-radius: 5px; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🤖 Query LLM App")
st.sidebar.markdown('<h3 style="color: red;">About</h3>', unsafe_allow_html=True)
st.sidebar.write("An AI-powered chatbot for KGPians 🎓")
st.sidebar.markdown("#### Technologies:")
st.sidebar.write("- Streamlit 🌐")
st.sidebar.write("- Deepseek r1:1.5B 💬")
st.sidebar.write("- Open-Source LLM 🧠")

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

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    role_class = "user" if message["role"] == "user" else "assistant"
    content = message["content"]
    st.markdown(f'<div class="chat-bubble {role_class}">{content}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


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

GROQ_API_KEY = "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" # Replace with your actual Groq API key
# deepseek_api_key="sk-1a9c2c7ef24b4b4d8a8fe7a382e2cb7d"
# Groq client
client = groq.Groq(api_key=GROQ_API_KEY)

async def process_input(prompt):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble user">{prompt}</div>', unsafe_allow_html=True)

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
            response_container.markdown(f'<div class="response">🤖 Response: {full_response}</div>', unsafe_allow_html=True)
            await asyncio.sleep(0.05)

    # Run both thinking and response streams asynchronously
    await stream_thinking()
    await stream_response()

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})


# Handle user input asynchronously
if prompt := st.chat_input("Ask me anything about KGP! 🤔"):
    asyncio.run(process_input(prompt))















