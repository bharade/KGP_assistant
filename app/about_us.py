import streamlit as st

def about_us():
    st.title("About Us")
    st.markdown("""
    ### Welcome to ABC Chatbot! 🤖
    
    **Who We Are**
    We are a team of passionate individuals from IIT Kharagpur dedicated to making information access easier for students.
    
    **Our Mission**
    Our goal is to provide an AI-powered chatbot that helps students and faculty navigate various aspects of IIT KGP with ease.
    
    **Key Features:**
    - Instant answers to academic and campus-related queries
    - Document and web-based retrieval for enhanced responses
    - User-friendly and constantly improving!
    
    🚀 Built with AI & Love ❤️
    
    ---
    
    **Contact Us:**
    If you have any suggestions, feel free to reach out!
    
    📧 Email: support@abcchatbot.com
    """)
    
    if st.button("🏠 Back to Home"):
        st.session_state.page = None
