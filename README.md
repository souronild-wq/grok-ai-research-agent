# AI Research Agent

An AI-powered research assistant built with Python and Grok by xAI.

## Features

- Generate structured research reports
- Accept any research topic
- Retry temporary API errors
- Save reports as Markdown files
- Use a configurable Grok model

## Requirements

- Python 3.10 or newer
- An xAI API key
- Internet connection

## Setup

1. Create a virtual environment:

   bash
   python -m venv .venv
   

2. Install dependencies:

   bash
   python -m pip install -r requirements.txt
   

3. Create a .env file:

   env
   XAI_API_KEY=your_actual_api_key
   XAI_MODEL=grok-3
   

4. Run the application:

   bash
   python main.py
   

## Usage

Enter a topic when prompted.

Example:

How can we save stray dogs in India?

The generated report is saved in the research folder.

## Security

Never share your API key or commit your .env file to GitHub.

## Limitations

Reports are generated from the model's available knowledge.
Live web search and independent source verification are
not included in this version.
