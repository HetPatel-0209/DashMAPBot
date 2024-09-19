from flask import Flask, request, jsonify, render_template
import requests
from markdown import markdown
from bs4 import BeautifulSoup
import os
from typing import Any, Text, Dict, List
app = Flask(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    
    bot_response = get_llm_response(user_message)
    
    formatted_response = apply_formatting(bot_response)
    
    return jsonify({"response": formatted_response})

def get_llm_response(user_message):
    prompt = generate_prompt(user_message)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.4
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        groq_response = response.json()
        if 'choices' in groq_response and groq_response['choices']:
            return groq_response['choices'][0]['message']['content']
        else:
            return "Sorry, I couldn't retrieve a valid response. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"I apologize, but I couldn't retrieve an answer at the moment. Error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def generate_prompt(user_message: str) -> str:
    return f"""
    You are DashBot, an AI assistant specializing in answering technical queries and troubleshooting. Your primary focus is on programming, debugging, and explaining technical concepts. Follow these guidelines in your interactions:\n
    ----------------------------------\n
    Only when asked about your name or identity:\n
        Always respond with: "I'm DashBot, here to assist you with your learning journey."
        Maintain a professional and helpful tone throughout the conversation.\n
    ----------------------------------\n
    Handling Technical Questions:\n
        Provide helpful, concise, and accurate responses to technical queries. Offer code snippets when relevant, using appropriate markdown formatting. Provide step-by-step guidance for troubleshooting or problem-solving.\n
    ----------------------------------\n
    Responding to Non-Technical Questions:\n
        For non-technical or unrelated questions (e.g., personal questions, entertainment, bollywood, hollywood), respond politely but firmly.\n
    --------------------\n
    User Query : {user_message}
    """

def format_code_blocks(text: str) -> str:
    lines = text.split('\n')
    formatted_lines = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith('```'):  # Detect code block markers
            in_code_block = not in_code_block
            if in_code_block:
                formatted_lines.append('<pre><code>')
            else:
                formatted_lines.append('</code></pre>')
        elif in_code_block:
            formatted_lines.append(f"{line}")  # Keep code as-is in the block
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

def apply_formatting(text):
    # Convert markdown to HTML
    text_with_code = format_code_blocks(text)  # First, process code blocks
    html = markdown(text_with_code)  # Convert markdown to HTML
    
    # Parse the generated HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Convert markdown-style bullets to list items
    for p in soup.find_all('p'):
        if p.text.startswith('- '):
            p.name = 'li'
            p.string = p.text[2:]
    
    # Wrap consecutive list items in a ul tag
    current_ul = None
    for li in soup.find_all('li'):
        prev_tag = li.find_previous_sibling()
        if not (prev_tag and prev_tag.name == 'li'):
            current_ul = soup.new_tag('ul')
            li.insert_before(current_ul)
        current_ul.append(li)

    # Convert strong tags to h3 for headers
    for strong in soup.find_all('strong'):
        if strong.parent.name == 'p' and strong.parent.contents[0] == strong:
            strong.name = 'h3'
    
    # Add classes for special formatting (mimicking ChatGPT's formatting)
    for tag in soup(['p', 'ul', 'ol', 'li', 'h3', 'code', 'pre']):
        tag['class'] = tag.get('class', []) + ['message-content']
    
    return f"<div class='response-wrapper'>{str(soup)}</div>"

if __name__ == '__main__':
    app.run(debug=True)