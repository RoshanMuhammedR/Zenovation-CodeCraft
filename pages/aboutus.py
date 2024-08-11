import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_extras.switch_page_button import switch_page
import hashlib
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="CodeCraft | Learning meets Gamification",
    page_icon=":rocket:",
    layout="wide"
)

styles = {
    "nav": {
        "background-color": "#007bff",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "#007bff",
        "font-weight": "normal",
        "padding": "14px",
    }
}

page = st_navbar(["Profile","Playground","Problems","Contests","About Us"],styles=styles,logo_path="C__deCraft.svg")
if page=="Playground":
    st.switch_page("pages/playground.py")
if page=="Profile":
    st.switch_page("pages/profile.py")
if page=="Contests":
    st.switch_page("pages/contest.py")


st.markdown("""
    <style>

        .custom-hr {
            border: none;
            height: 1px;
            background: linear-gradient(to right, #00f, #00f, transparent);
            box-shadow: 0 0 10px #00f;
            margin: 20px 0;
        }

        .stButton > button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            width: 300px;
            transition: background-color 0.3s ease;
        } 

        .stButton > button:hover {
            background-color: #0056b3;
        }
    </style>
""", unsafe_allow_html=True)

st.title("About Us")
st.write('''<hr class="custom-hr">''',unsafe_allow_html=True)
st.write('''
Welcome to CodeCraft, where coding meets creativity and challenges ignite innovation. Our platform is designed to inspire and empower coders of all levels by combining the thrill of gamification with the rigors of problem-solving.

## What is CodeCraft?

CodeCraft is a unique platform that blends coding with gamification, making the learning process engaging and enjoyable. Whether you're a beginner looking to hone your skills or an experienced coder ready to tackle advanced challenges, CodeCraft offers a space where you can grow, compete, and showcase your talents.

### Key Features of CodeCraft:

- **Interactive Learning:**  
  Dive into coding with hands-on exercises and challenges that adapt to your skill level. Our interactive platform provides real-time feedback, helping you learn and improve with each attempt.

- **Gamified Experience:**  
  Compete with others, earn points, and climb the leaderboards as you solve coding problems. Our gamified approach turns learning into a fun and rewarding experience.

- **Community Engagement:**  
  Join a vibrant community of coders, share your progress, and collaborate on projects. CodeCraft is more than just a platform—it's a community where you can connect with like-minded individuals and grow together.

- **Personalized Dashboard:**  
  Track your progress, monitor your streaks, and set goals with your personalized dashboard. Stay motivated and keep pushing your limits as you see your skills evolve.

### Our Team

- **Roshan Muhammed**  
  Roshan is a visionary developer with a passion for creating impactful solutions. His technical expertise drive the innovation behind CodeCraft.

- **Yashwenth S**  
  With a deep understanding of app development, web technologies, and IoT, Yashwenth ensures that CodeCraft is both technically robust and user-friendly.

- **N P Yuvashree**  
  Yuvashree brings creativity and analytical thinking to the team. Her contributions help shape the user experience and overall design of the platform.

Together, we have built CodeCraft to be more than just a coding platform—it's a place where learning meets adventure, and challenges turn into achievements. Join us on this exciting journey and discover the coder in you!

''',unsafe_allow_html=True)
