import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_extras.switch_page_button import switch_page
from streamlit_navigation_bar import st_navbar

# MongoDB connection setup
uri = "mongodb+srv://126003302:hello123@cluster0.pbomd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["CodeCraft"]
users_collection = db["users"]
contests_collection = db["contests"]

# Set Streamlit page configuration
st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="CodeCraft | Learning meets Gamification",
    page_icon=":rocket:",
    layout="wide"
)

# Custom CSS for the navbar and page elements
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

st.title("Contests")
st.write('''<hr class="custom-hr">''', unsafe_allow_html=True)

a, b = st.columns(2)

# Left Column - Create Contest
with a:
    with st.container(border=True):
        st.header("Create Contest")
        st.write("---")
        cn = st.text_input("Enter Contest Name")
        mc = st.select_slider("Number of contestants", [1, 2, 3, 4, 5, 6])
        q = st.text_input("Question")

        if st.button("Create!"):
            un = st.session_state.get("username")  # Get the current user's username
            contest_data = {
                "contest_name": cn,
                "max_contestants": mc,
                "question": q,
                "participants": [],
                "slots_left": mc,  # Initialize with max contestants
                "creator": un  # Add creator information
            }
            contests_collection.insert_one(contest_data)

            # Update the user's document with the created contest
            users_collection.update_one(
                {"username": un},
                {"$push": {"created_contests": contest_data["_id"]}}  # Assuming created_contests field
            )
            st.success(f"Contest '{cn}' created successfully!")

# Right Column - Display Contests
with b:
    st.header("Available Contests")
    st.write("---")
    
    # Fetch all contests from MongoDB
    contests = contests_collection.find()
    
    for contest in contests:
        with st.chat_message("user"):
            st.subheader(contest["contest_name"])
            st.write(f"Slots left: {contest['slots_left']}")
            
            if contest['slots_left'] > 0:
                if st.button(f"Join {contest['contest_name']}", key=contest["_id"]):
                    un = st.session_state.get("username")  # Get the current user's username
                    
                    if un not in contest["participants"]:
                        # Update the contest document
                        contests_collection.update_one(
                            {"_id": contest["_id"]},
                            {
                                "$push": {"participants": un},
                                "$inc": {"slots_left": -1}
                            }
                        )
                        
                        # Increment the contests field in the user's document
                        users_collection.update_one(
                            {"username": un},
                            {"$inc": {"contests": 1}}
                        )
                        
                        st.success(f"You have joined the contest '{contest['contest_name']}'!")
                    else:
                        st.warning(f"You are already registered for '{contest['contest_name']}'")
            else:
                st.write("Contest Full!")
