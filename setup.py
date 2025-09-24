from setuptools import setup, find_packages  # type: ignore

setup(
    name="chatbot",
    version="0.0.1",
    author="AI Minds",
    author_email="SmKhizarAI025@gmail.com",
    description="This is a chatbot built on a Retrieval-Augmented Generation (RAG) system, designed to process user prompts and reference external documents for more accurate and context-aware responses.",
    packages=find_packages(),
    install_requires=[],
)
