import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_extras.switch_page_button import switch_page
from streamlit_navigation_bar import st_navbar

uri = "mongodb+srv://126003302:hello123@cluster0.pbomd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["CodeCraft"]
users_collection = db["users"]
contests_collection = db["contests"]

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

un = st.session_state.get("username")

user_info = users_collection.find_one({"username": un})

st.header("Your Contests")
st.write('''<hr class="custom-hr">''',unsafe_allow_html=True)

contests = contests_collection.find({"creator": un})

contest_list = list(contests)
if len(contest_list) > 0:
    for contest in contest_list:
        with st.container(border=True):
            st.subheader(contest["contest_name"])
            st.write(f"**Question:** {contest['question']}")
            
            if contest["participants"]:
                for participant in contest["participants"]:
                    with st.expander(f"{participant} Submission"):
                        participant_data = users_collection.find_one({"username": participant})
                        if participant_data and "submissions" in participant_data:
                            submission = participant_data["submissions"].get(str(contest["_id"]), "No submission")
                            st.code(submission, language="python")  # Adjust language if needed
                            marks = st.slider(f"Award marks to {participant}", 1, 10, 5)
                            if st.button(f"Submit marks for {participant}"):
                                contests_collection.update_one(
                                    {"_id": contest["_id"], "participants": participant},
                                    {"$set": {f"submissions.{participant}.marks": marks}}
                                )
                                st.success(f"Marks for {participant} updated to {marks}")
            else:
                st.write("No participants yet.")
else:
    st.write("You have no contests.")
