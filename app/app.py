import streamlit as st
import time
from langchain.schema import HumanMessage
from utils import initialize_vectorstore, format_docs, llm, rag_prompt
from tavily_integration import web_response

# Set page configuration
st.set_page_config(
    page_title="Query LLM App 🤖", 
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for chat layout and hidden reasoning
st.markdown("""
    <style>
    .stApp { background-color: black; }
    
    .chat-container { display: flex; flex-direction: column; gap: 10px; }
    
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 10px;
        max-width: 75%;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-title {
        animation: fadeIn 1.5s ease-in-out;
    }
    .user { background-color: #b886e3; color:black; align-self: flex-end; text-align: right; }
    .assistant { background-color: #7bd0e3; color: black; align-self: flex-start; text-align: left; }
    
    .thinking { 
        background-color: #f0f0f0; 
        color: #333; 
        padding: 10px; 
        border-radius: 5px; 
        margin-top: 5px; 
        font-style: italic; 
    }
    
    .response { 
        background-color: #5ce1f2; 
        color: black; 
        padding: 10px; 
        border-radius: 5px; 
        margin-top: 5px; 
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🤖 Query LLM App")
# st.sidebar.markdown("### About")
st.sidebar.markdown('<h3 style="color: red;">About</h3>', unsafe_allow_html=True)
st.sidebar.write("An AI-powered chatbot for KGPians 🎓")
st.sidebar.markdown("#### Technologies:")
st.sidebar.write("- Streamlit 🌐")
st.sidebar.write("- Deepseek r1:1.5B 💬")
st.sidebar.write("- Open-Source LLM 🧠")

#Cache the vector store and retriever initialization
@st.cache_resource
def get_vectorstore():
    return initialize_vectorstore()

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

    # Display chat bubble
    st.markdown(f'<div class="chat-bubble {role_class}">{content}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask me anything about KGP! 🤔"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-bubble user">{prompt}</div>', unsafe_allow_html=True)

    # Retrieve relevant documents
    docs = retriever.invoke(prompt)
    docs_txt = format_docs(docs)
    
    web_search_results = web_response(prompt)

    docs_txt = docs_txt +"\n\n"+web_search_results
    # Format the prompt for the model
    rag_prompt_formatted = rag_prompt.format(context=docs_txt, question=prompt)

    # Get the model's response
    response = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
    response_text = response.content

    # Extract "thinking" part if present
    thinking = None
    if "<think>" in response_text and "</think>" in response_text:
        think_start = response_text.find("<think>") + 7
        think_end = response_text.find("</think>")
        thinking = response_text[think_start:think_end].strip()
        response_text = response_text[:think_start-7] + response_text[think_end+8:]  # Remove <think> section
        response_text = response_text.strip()  # Clean up remaining text

    # Initialize containers for dynamic updates
    thinking_container = st.empty()
    response_container = st.empty()

    # Function to stream thinking dynamically
    def stream_thinking():
        if thinking:
            full_thinking = ""
            words = thinking.split()
            for word in words:
                full_thinking += word + " "
                thinking_container.markdown(f'<div class="thinking">🤔 Thinking: {full_thinking}</div>', unsafe_allow_html=True)
                time.sleep(0.05)  # Adjust for streaming speed

    # Function to stream response dynamically
    def stream_response():
        full_response = ""
        words = response_text.split()
        for word in words:
            full_response += word + " "
            response_container.markdown(f'<div class="response">🤖 Response: {full_response}</div>', unsafe_allow_html=True)
            time.sleep(0.05)  # Adjust for streaming speed

    # Stream thinking first, then response
    stream_thinking()
    stream_response()

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})


# #My next task is to if user gives another question, i will also share previous conversation response etc. of the current session
