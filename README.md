# Flask Chatbot PDF Analyzer

This is a Flask-based web application that analyzes PDF documents using a language model API (Groq's LLaMA model) and provides conversational responses based on the content of the PDF.

## Features

- **PDF Upload:** Users can upload a PDF document, which is processed and analyzed by the application.
- **Conversational Interface:** Users can interact with the chatbot by asking questions related to the content of the uploaded PDF.
- **Contextual Responses:** The chatbot uses Groq's LLaMA model to generate responses based on the context provided by the PDF.

## Installation

### Prerequisites

- Docker installed on your machine.
- A Groq API key.

### Clone the Repository

```bash
git clone https://github.com/cestashish/Flask_chatbot_pdf-analyzer.git
cd Flask_chatbot_pdf-analyzer
docker build -t pdfanalyzer .
docker run -p 8000:8000 -e GROQ_API_KEY=your_groq_api_key_here pdfanalyzer


