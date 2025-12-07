A simple and interactive Python project that predicts a student’s upcoming exam score using past performance data. The tool speaks the results aloud using pyttsx3 and uses the Gemini API to give short, helpful responses that make the experience more engaging.

⭐ Overview

This project brings together basic machine learning, voice output, data handling, and AI-driven responses. It’s designed to be beginner-friendly and shows how different Python tools can work together to create a smooth CLI experience.

The program reads previous marks, trains a small prediction model, and then estimates the next score. The voice assistant speaks the result, and the Gemini API adds a conversational touch to guide the user.

📦 Features

Predicts student marks using past data

Voice output with pyttsx3

Gemini API responses for interaction

Clean CLI workflow

Simple and easy-to-understand code

🛠️ Tech Stack

Python

Pandas

Scikit-learn

pyttsx3

Gemini API

🚀 Setup and Installation

Clone the repository

git clone https://github.com/codewithazanofficial/Gradify.git cd Gradify

Install dependencies

pip install -r requirements.txt

Add your Gemini API key Create a .env file:

GEMINI_API_KEY=your_api_key_here

▶️ How It Works

Loads data from a CSV or predefined dataset

Trains a simple machine learning model

Takes user input in the CLI

Predicts the student’s next score

Speaks the output through pyttsx3

Uses Gemini API for supportive or explanatory responses

📝 Usage

Run the main script:

python main.py

Follow the instructions shown in the terminal.

🔮 Future Improvements

Add visual charts for progress

Improve model accuracy

Add user profiles

Build a GUI version
