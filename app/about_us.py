import streamlit as st

def about_us():
    st.markdown("""
        <style>
            .title {
                font-size: 48px;
                font-weight: 700;
                color: #222222;
                text-align: center;
                margin-bottom: 20px;
            }
            .subtitle {
                font-size: 24px;
                text-align: center;
                color: #666666;
                margin-bottom: 40px;
            }
            .section {
                background-color: #f9f9f9;
                padding: 50px 30px;
                border-radius: 20px;
                margin-bottom: 40px;
            }
            .profile-card {
                text-align: center;
                padding: 20px;
            }
            .profile-img {
                border-radius: 50%;
                width: 150px;
                height: 150px;
                object-fit: cover;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 10px;
            }
            .name {
                font-size: 20px;
                font-weight: 600;
                margin-top: 10px;
            }
            .role {
                font-size: 16px;
                color: #555;
                margin-bottom: 10px;
            }
            .links a {
                text-decoration: none;
                margin: 0 8px;
                color: #1f77b4;
                font-weight: 500;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">About Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">The minds behind ABC Chatbot ✨</div>', unsafe_allow_html=True)

    # Mission Section
    with st.container():
        st.markdown("""
        <div class="section">
            <h3>🚀 Our Mission</h3>
            <p style="font-size: 18px; line-height: 1.6;">
                We’re a team of final-year Aerospace Engineering students from IIT Kharagpur, passionate about blending AI with accessibility. 
                Our chatbot project simplifies access to academic and campus-related information for students, using cutting-edge RAG techniques.
            </p>
            <p style="font-size: 18px; line-height: 1.6;">
                Built with <strong>AI, Engineering, and a whole lot of passion</strong>, our goal is to empower students and scale smart search tools to real-world platforms.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Meet the Team
    st.markdown('<div class="title">Meet the Team 👨‍🚀</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="profile-card">
            <img src="images/aditya.jpg" class="profile-img" />
            <div class="name">Aditya Bharade</div>
            <div class="role">AI Engineer • ML Research • SHM Expert</div>
            <div class="links">
                <a href="https://linkedin.com/in/adityabharade" target="_blank">LinkedIn</a> |
                <a href="https://github.com/adityabharade" target="_blank">GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="profile-card">
            <img src="images/ravikesh.jpg" class="profile-img" />
            <div class="name">Ravikesh Kumar</div>
            <div class="role">NLP Specialist • Vision & Language • Backend Dev</div>
            <div class="links">
                <a href="https://linkedin.com/in/ravikeshkumar" target="_blank">LinkedIn</a> |
                <a href="https://github.com/ravikeshkumar" target="_blank">GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="profile-card">
            <img src="images/surendra.jpg" class="profile-img" />
            <div class="name">Surendra Kiran Kolhe</div>
            <div class="role">Cloud Architect • RAG Pipelines • Infra Wizard</div>
            <div class="links">
                <a href="https://linkedin.com/in/surendrakiran" target="_blank">LinkedIn</a> |
                <a href="https://github.com/surendrakiran" target="_blank">GitHub</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Contact Section
    st.markdown("""
    <div class="section">
        <h3>📬 Get in Touch</h3>
        <p style="font-size: 18px;">We’d love to hear your thoughts, collaborations, or job offers 😉</p>
        <p style="font-size: 18px;">📧 <a href="mailto:support@abcchatbot.com">support@abcchatbot.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home"):
        st.session_state.page = None
