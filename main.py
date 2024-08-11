import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from streamlit_extras.switch_page_button import switch_page

from streamlit_navigation_bar import st_navbar 
import hashlib

uri = "mongodb+srv://126003302:hello123@cluster0.pbomd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["CodeCraft"]
users_collection = db["users"]
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
            "padding": "1px",
        },
        "active": {
            "background-color": "white",
            "color": "#007bff",
            "font-weight": "normal",
            "padding": "14px",
        }
    }

page = st_navbar(["Profile","Playground","Problems","Contests","About Us"],styles=styles,logo_path="C__deCraft.svg")

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
            background-color: #007bff; /* Blue background */
            color: #ffffff; /* White text */
            border: none;
            border-radius: 12px; /* Curved borders */
            padding: 12px 24px; /* Elongated button length */
            font-size: 16px;
            cursor: pointer;
            width: 300px;
            transition: background-color 0.3s ease; /* Smooth transition for hover effect */
        }

        .stButton > button:hover {
            background-color: #0056b3; /* Darker blue on hover */
        }
    </style>
""", unsafe_allow_html=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_page():
    st.title("Sign Up")
    username = st.text_input("Username")
    full_name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if users_collection.find_one({"username": username}):
            st.error("Username already exists. Please choose another.")
        else:
            hashed_password = hash_password(password)
            user_data = {"username": username, "full_name": full_name, "password": hashed_password, "problems":0,"contests":0,"streak":0}
            users_collection.insert_one(user_data)
            st.success("Account created successfully!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            switch_page("profile")

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = users_collection.find_one({"username": username})
        if user and user["password"] == hash_password(password):
            st.success("Logged in successfully!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            switch_page("profile")
        else:
            st.error("Invalid username or password.")

def forgot_password_page():
    st.title("Forgot Password")
    username = st.text_input("Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        if users_collection.find_one({"username": username}):
            hashed_password = hash_password(new_password)
            users_collection.update_one({"username": username}, {"$set": {"password": hashed_password}})
            st.success("Password reset successfully!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            switch_page("home")
        else:
            st.error("Username not found.")

def main():
    
    st.title("CodeCraft - Coding Meets Gaming")
    st.write('''<hr class="custom-hr">''', unsafe_allow_html=True)
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
    
    if 'page' not in st.session_state:
        st.session_state['page'] = "Login"  

    if st.session_state['logged_in']:
        switch_page("playground")
    else:
        a, b = st.columns([0.3, 1], vertical_alignment="center")
        with a:
            if st.button("Login >"):
                st.session_state['page'] = "Login"
            if st.button("Sign Up >"):
                st.session_state['page'] = "Sign Up"
            if st.button("Forgot Password >"):
                st.session_state['page'] = "Forgot Password"
        with b:
            with st.container(border=True):
                if st.session_state['page'] == "Login":
                    login_page()
                elif st.session_state['page'] == "Sign Up":
                    signup_page()
                elif st.session_state['page'] == "Forgot Password":
                    forgot_password_page()

if __name__ == "__main__":
    main()
