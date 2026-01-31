from setuptools import find_packages, setup

setup(
    name="mcqgenerator",
    version="0.0.1",
    author="Harshit Gupta",
    author_email="Harshitgupta6121@gmail.com",
    description="MCQ Generator using LLMs",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "openai>=1.0.0",
        "langchain",
        "langchain-community",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
)
