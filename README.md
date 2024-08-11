# Zenovation-CodeCraft

## Project Overview

Zenovation-CodeCraft is a comprehensive online coding platform designed to enhance coding skills through a gamified approach. The platform includes features such as code editing, code execution, and contest management. It supports multiple programming languages, including Python, C, C++, and Java.

## Demo Link

[Click Here](https://drive.google.com/drive/folders/1pqMG3NFnDIMa3ZGOwfyKBuyKQLiu7_aY?usp=sharing)

## Features

- **Multi-language Code Editor**: Write and execute code in Python, C, C++, and Java.
- **Code Compilation and Execution**: Compile and run code in an isolated Docker environment.
- **Contest Management**: Participate in coding contests with problem statements and submissions.
- **User Profile**: Track progress and achievements.

## Getting Started

To get started with Zenovation-CodeCraft, follow these instructions:

### Prerequisites

- Docker
- Python
- Streamlit
- MongoDB (for backend data management)
- Additional dependencies: `streamlit_ace`, `streamlit_navigation_bar`, `pymongo`

### Setting Up the Project

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd Zenovation-CodeCraft
   ```
2. **Install Dependencies**
   
  ```bash
  pip install streamlit streamlit_ace streamlit_navigation_bar pymongo
  ```
3. **Run the Application**
   Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Docker Integration

## Overview

Docker was used in this project to create a controlled and consistent environment for code compilation. By leveraging Docker, we ensured that our code execution was isolated from the local environment, thereby avoiding dependency issues and ensuring reproducibility.

## Docker Setup

1. **Creating an Ubuntu Docker Image**
   An Ubuntu Docker image was created to serve as the base environment for compiling and running code. Here’s how it was done:
   - Dockerfile Creation: A Dockerfile was created to define the environment. This file specifies the base image (Ubuntu) and includes commands to install necessary dependencies and tools for code compilation.
   ```bash
   FROM ubuntu:latest
   ENV DEBIAN_FRONTEND=noninteractive
   RUN apt-get update && \
       apt-get install -y \
       build-essential \
       gcc \
       g++ \
       openjdk-11-jdk \
       python3 \
       python3-pip \
       && apt-get clean
   WORKDIR /app
   ```
   - Building the Docker Image: The Docker image was built using the following command:
     
   ```bash
   docker build -t ubuntu-dev-env .
   ```
   This command creates an image named ubuntu-dev-env based on the Dockerfile.

2. **Running the Docker Container**
   Once the image was built, a Docker container was created and started from this image. The container provides an isolated environment where code can be compiled and executed.
   ```bash
   docker run -it --name code-compilation-container ubuntu-dev-env
   ```

## Benefits of Using Docker
   - Isolation: Each container provides an isolated environment, preventing conflicts between different versions of dependencies.
   - Consistency: The same environment is used for every build, ensuring consistent results.
   - Reproducibility: Docker images can be versioned and shared, making it easy to reproduce the environment and compile code in the exact same setup.




