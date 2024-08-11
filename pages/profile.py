import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_extras.switch_page_button import switch_page
from streamlit_navigation_bar import st_navbar

uri = "mongodb+srv://126003302:hello123@cluster0.pbomd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["CodeCraft"]
users_collection = db["users"]
contests_collection = db["contests"]  # Contest collection

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

page = st_navbar(["Profile", "Playground", "Problems", "Contests", "About Us"], styles=styles, logo_path="C__deCraft.svg")
if page == "Playground":
    st.switch_page("pages/playground.py")
if page == "Contests":
    st.switch_page("pages/contests.py")
if page == "Profile":
    st.switch_page("pages/profile.py")
if page == "About Us":
    st.switch_page("pages/aboutus.py")

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

st.markdown("""
    <style>
    .css-1y4zwz5 {padding-top: 0;}
    .css-1l02z5j {margin-top: 0;}
    </style>
    """, unsafe_allow_html=True)

un = st.session_state["username"]
user_info = users_collection.find_one({"username": un})
if not user_info:
    st.write("User Not Found")

st.title("Welcome, " + user_info["full_name"])
st.write("Get Insights About Yourself...")
st.write('''<hr class="custom-hr">''', unsafe_allow_html=True)

a, b, c = st.columns(3)
with a:
    with st.container(border=True):
        st.header("💡" + str(user_info["problems"]) + " Problems Solved")
with b:
    with st.container(border=True):
        st.header("📈" + str(user_info["contests"]) + " Contests")
with c:
    with st.container(border=True):
        st.header("🔥" + str(user_info["streak"]) + " Days of CodeCraft")

with st.container(border=True):
    st.header("Enrolled Contests")

    registered_contests = contests_collection.find({"participants": un})
    
    for contest in registered_contests:
        with st.chat_message("user"):
            c,d = st.columns([0.5,1])
            with c:
                st.subheader(contest["contest_name"])
            with d:
                if st.button("Go to Contest", key=contest["_id"]):
                    st.session_state["current_contest_question"] = contest["question"]
                    switch_page("problems")

with st.container(border=True):
    st.header("Your Contests")
    
    created_contests = contests_collection.find({"creator": un}) 
    
    for contest in created_contests:
        with st.chat_message("user"):
            c,d = st.columns([0.5,1])
            with c:
                st.subheader(contest["contest_name"])
            with d:
                if st.button("View Contest", key=f"your_{contest['_id']}"):
                    st.session_state["current_contest_id"] = contest["_id"]
                    switch_page("yourcontest")
