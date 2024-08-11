import streamlit as st
from streamlit_ace import st_ace
from streamlit_navigation_bar import st_navbar
import subprocess
import tempfile
import os

# Set the Docker container ID
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

page = st_navbar(["Profile", "Playground", "Problems", "Contests", "About Us"], styles=styles,
                 logo_path="C__deCraft.svg")
if page == "Profile":
    st.switch_page("pages/profile.py")
if page == "About Us":
    st.switch_page("pages/aboutus.py")
if page == "Contests":
    st.switch_page("pages/contests.py")

st.title("CodeCraft PlayGround")
st.write("""
Intelligent and Innovative Playground to Practice your coding Skills.
""")

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
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #0056b3;
        }
    </style>
    <hr class="custom-hr">
""", unsafe_allow_html=True)

# Language selection
language = st.selectbox("Select Language", ["Python", "C", "C++", "Java"])

# Initialize the code editor with default code
default_code = {
    "Python": """summ = 0
for i in range(5):
    temp = int(input())
    summ = summ + temp

print(summ)
""",
    "C": """#include <stdio.h>

int main() {
    int n, temp, summ = 0;
    printf("Enter number of inputs: ");
    scanf("%d", &n);
    for(int i = 0; i < n; i++) {
        printf("Enter: ");
        scanf("%d", &temp);
        summ += temp;
    }
    printf("%d\\n", summ);
    return 0;
}
""",
    "C++": """#include <iostream>

int main() {
    int n, temp, summ = 0;
    std::cout << "Enter number of inputs: ";
    std::cin >> n;
    for(int i = 0; i < n; i++) {
        std::cout << "Enter: ";
        std::cin >> temp;
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

# Code and input area
a, b = st.columns(2)

with a:
    st.header("Editor")
    code = st_ace(
        value=default_code.get(language, ""),
        language=language.lower(),
        theme='chaos',
        font_size=14,
        height=300
    )

with b:
    st.header("Input")
    # Allow users to input all values in one line
    user_input = st.text_area("Enter multiple values separated by spaces")

    if st.button("Run Code"):
        st.write("Button clicked")

        # Define file extension based on selected language
        extensions = {
            "Python": ".py",
            "C": ".c",
            "C++": ".cpp",
            "Java": ".java"
        }
        file_extension = extensions.get(language, ".txt")
        filename = f"HelloWorld{file_extension}" if language == "Java" else f"code{file_extension}"

        # Create a temporary file for the code
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Prepare input file if provided
        input_file = None
        if user_input:
            # Use the same file for input in all cases
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_input:
                temp_input.write(user_input)
                temp_input_path = temp_input.name
            input_file = temp_input_path
            subprocess.run(['docker', 'cp', temp_input_path, f'{DOCKER_CONTAINER_ID}:/tmp/input.txt'])

        # Copy the code file to Docker container
        subprocess.run(['docker', 'cp', temp_file_path, f'{DOCKER_CONTAINER_ID}:/tmp/{filename}'])

        # Run the code inside the Docker container
        if language == "Python":
            command = f'python3 /tmp/{filename} < /tmp/input.txt' if user_input else f'python3 /tmp/{filename}'
        elif language == "C":
            command = f'gcc /tmp/{filename} -o /tmp/code && /tmp/code < /tmp/input.txt' if user_input else f'gcc /tmp/{filename} -o /tmp/code && /tmp/code'
        elif language == "C++":
            command = f'g++ /tmp/{filename} -o /tmp/code && /tmp/code < /tmp/input.txt' if user_input else f'g++ /tmp/{filename} -o /tmp/code && /tmp/code'
        elif language == "Java":
            command = f'javac /tmp/{filename} && java -cp /tmp HelloWorld < /tmp/input.txt' if user_input else f'javac /tmp/{filename} && java -cp /tmp HelloWorld'

        result = subprocess.run(['docker', 'exec', DOCKER_CONTAINER_ID, 'bash', '-c', command], capture_output=True,
                                text=True)

        # Delete the temporary files in Docker container
        subprocess.run(['docker', 'exec', DOCKER_CONTAINER_ID, 'rm', f'/tmp/{filename}'])
        if user_input:
            subprocess.run(['docker', 'exec', DOCKER_CONTAINER_ID, 'rm', '/tmp/input.txt'])

        # Delete the local temporary files
        os.remove(temp_file_path)
        if user_input:
            os.remove(temp_input_path)

        # Display the result
        st.text(result.stdout if result.stdout else result.stderr)
