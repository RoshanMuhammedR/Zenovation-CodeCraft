import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit_ace as ace
from streamlit_navigation_bar import st_navbar
import subprocess
import tempfile
import os

uri = "mongodb+srv://126003302:hello123@cluster0.pbomd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["CodeCraft"]
users_collection = db["users"]
contests_collection = db["contests"]

DOCKER_CONTAINER_ID = '89fe276cd8ba'

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="CodeCraft | Learning meets Gamification",
    page_icon=":rocket:",
    layout="wide"
)

styles = {
    "nav": {"background-color": "#007bff", "justify-content": "left"},
    "img": {"padding-right": "14px"},
    "span": {"color": "white", "padding": "14px"},
    "active": {"background-color": "white", "color": "#007bff", "font-weight": "normal", "padding": "14px"},
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
    <hr class="custom-hr">
""", unsafe_allow_html=True)

if "current_contest_question" not in st.session_state:
    st.error("No contest question found.")
    st.stop()

question = st.session_state["current_contest_question"]

st.title("Problem Statement")
st.header(question)

st.write('''<hr class="custom-hr">''', unsafe_allow_html=True)

language = st.selectbox("Select Language", ["Python", "C", "C++", "Java"])

default_code = {
    "Python": """summ = 0
for i in range(5):
    temp = int(input())
    summ = summ + temp

print(summ)
""",
    "C": """#include <stdio.h>

int main() {
    int temp, summ = 0;
    while (scanf("%d", &temp) != EOF) {
        summ += temp;
    }
    printf("%d\\n", summ);
    return 0;
}
""",
    "C++": """#include <iostream>

int main() {
    int temp, summ = 0;
    while (std::cin >> temp) {
        summ += temp;
    }
    std::cout << summ << std::endl;
    return 0;
}
""",
    "Java": """import java.util.Scanner;

public class HelloWorld {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int summ = 0;
        int n = scanner.nextInt();
        for (int i = 0; i < n; i++) {
            summ += scanner.nextInt();
        }
        System.out.println(summ);
    }
}
"""
}

a, b = st.columns(2)

with a:
    st.header("Code Editor")
    code = ace.st_ace(
        value=default_code.get(language, ""),
        language=language.lower(),
        theme='chaos',
        font_size=14,
        height=300
    )

with b:
    st.header("Input")
    user_input = st.text_area("Enter multiple values separated by spaces")

    if st.button("Run Code"):
        st.write("Button clicked")

        extensions = {
            "Python": ".py",
            "C": ".c",
            "C++": ".cpp",
            "Java": ".java"
        }
        file_extension = extensions.get(language, ".txt")
        filename = f"code{file_extension}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, mode='w', encoding='utf-8') as temp_code_file:
            temp_code_file.write(code)
            temp_code_path = temp_code_file.name

        if user_input:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_input_file:
                temp_input_file.write(user_input)
                temp_input_path = temp_input_file.name
            subprocess.run(['docker', 'cp', temp_input_path, f'{DOCKER_CONTAINER_ID}:/tmp/input.txt'])

        subprocess.run(['docker', 'cp', temp_code_path, f'{DOCKER_CONTAINER_ID}:/tmp/{filename}'])

        if language == "Python":
            command = f'python3 /tmp/{filename} < /tmp/input.txt' if user_input else f'python3 /tmp/{filename}'
        elif language == "C":
            command = f'gcc /tmp/{filename} -o /tmp/code && /tmp/code < /tmp/input.txt' if user_input else f'gcc /tmp/{filename} -o /tmp/code && /tmp/code'
        elif language == "C++":
            command = f'g++ /tmp/{filename} -o /tmp/code && /tmp/code < /tmp/input.txt' if user_input else f'g++ /tmp/{filename} -o /tmp/code && /tmp/code'
        elif language == "Java":
            command = f'javac /tmp/{filename} && java -cp /tmp HelloWorld < /tmp/input.txt' if user_input else f'javac /tmp/{filename} && java -cp /tmp HelloWorld'

        result = subprocess.run(['docker', 'exec', DOCKER_CONTAINER_ID, 'bash', '-c', command], capture_output=True, text=True)

        subprocess.run(['docker', 'exec', DOCKER_CONTAINER_ID, 'rm', f'/tmp/{filename}'])
        if user_input:
            subprocess.run(['docker', 'exec', DOCKER_CONTAINER_ID, 'rm', '/tmp/input.txt'])
        os.remove(temp_code_path)
        if user_input:
            os.remove(temp_input_path)

        st.text(result.stdout if result.stdout else result.stderr)

with st.sidebar:
    if st.button("Submit"):
        username = st.session_state["username"]
        contest_name = st.session_state["current_contest_name"]
        contests_collection.update_one(
            {"contest_name": contest_name},
            {"$push": {f"submissions.{username}": code}}
        )
        users_collection.update_one(
            {"username": username},
            {"$inc": {"problems": 1}}
        )
        st.success("Your solution has been submitted!")
