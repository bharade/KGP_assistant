import streamlit as st

def about_us():
    st.markdown("""
        <style>
            body {
                background-color: #0f0f0f;
            }
            .title {
                font-size: 48px;
                font-weight: 700;
                color: #ffffff;
                text-align: center;
                margin-bottom: 20px;
            }
            .subtitle {
                font-size: 24px;
                text-align: center;
                color: #bbbbbb;
                margin-bottom: 40px;
            }
            .section {
                background: rgba(255, 255, 255, 0.05);
                padding: 50px 30px;
                border-radius: 20px;
                margin-bottom: 40px;
                color: #e0e0e0;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(8px);
            }
            .profile-card {
                text-align: center;
                padding: 20px;
                color: #ffffff;
                background: rgba(255, 255, 255, 0.06);
                border-radius: 16px;
                backdrop-filter: blur(6px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
                margin: 20px 10px;
            }
            .profile-img {
                border-radius: 50%;
                width: 130px;
                height: 130px;
                object-fit: cover;
                border: 3px solid #00ADB5;
                margin-bottom: 10px;
            }
            .name {
                font-size: 20px;
                font-weight: 600;
                margin-top: 10px;
                color: #ffffff;
            }
            .role {
                font-size: 15px;
                color: #cccccc;
                margin-bottom: 10px;
            }
            .links a {
                text-decoration: none;
                margin: 0 8px;
                color: #00ADB5;
                font-weight: 500;
            }
            .links a:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">About Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">The minds behind ABC Chatbot ✨</div>', unsafe_allow_html=True)

    st.markdown('<div class="title">Meet the Team 👨‍🚀</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="profile-card">
            <img src="https://raw.githubusercontent.com/bharade/kgp-chatbot-assets/main/aditya.jpeg" class="profile-img" />
            <div class="name">Aditya Bharade</div>
            <div class="role">AI Engineer • SHM • RAG Wizard</div>
            <div class="links">
                <a href="https://linkedin.com/in/adityabharade" target="_blank">LinkedIn</a> |
                <a href="https://github.com/adityabharade" target="_blank">GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-card">
            <img src="https://raw.githubusercontent.com/bharade/kgp-chatbot-assets/main/ravikesh.jpeg" class="profile-img" />
            <div class="name">Ravikesh Kumar</div>
            <div class="role">NLP Specialist • Full Stack Dev</div>
            <div class="links">
                <a href="https://linkedin.com/in/ravikeshkumar" target="_blank">LinkedIn</a> |
                <a href="https://github.com/ravikeshkumar" target="_blank">GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="profile-card">
            <img src="https://raw.githubusercontent.com/bharade/kgp-chatbot-assets/main/surendra.jpeg" class="profile-img" />
            <div class="name">Surendra Kiran Kolhe</div>
            <div class="role">Infra Architect • Cloud RAG</div>
            <div class="links">
                <a href="https://linkedin.com/in/surendrakiran" target="_blank">LinkedIn</a> |
                <a href="https://github.com/surendrakiran" target="_blank">GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="section">
            <h3>🚀 Our Mission</h3>
            <p style="font-size: 18px; line-height: 1.6;">
                We’re a team of final-year Aerospace Engineering students from IIT Kharagpur, passionate about blending AI with accessibility.
                In the aftermath of the pandemic, we noticed that many KGPians were struggling to find the right guidance — whether it was for academic decisions, administrative processes like dropping additionals, or simply navigating daily campus life. With fewer in-person interactions, juniors often missed out on the informal yet invaluable support traditionally offered by seniors.
                That's where our chatbot comes in — a virtual senior, always available, bridging that gap. It’s built to empower students with instant, reliable, and contextual information so that no one feels lost or alone in their KGP journey again.
            </p>
            <p style="font-size: 18px; line-height: 1.6;">
                Built with <strong>AI, Engineering, and a whole lot of passion</strong>, our goal is to empower students and scale smart search tools to real-world platforms.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section">
        <h3>📬 Get in Touch</h3>
        <p style="font-size: 18px;">
            We’d love to hear your thoughts, ideas, or collaboration opportunities.
        </p>
        <p style="font-size: 18px;">
            📧 <a href="mailto:support@abcchatbot.com" style="color:#00ADB5;">support@abcchatbot.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    
    if st.button("🏠 Back to Home"):
        st.session_state.page = None
