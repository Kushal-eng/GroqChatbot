from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv  
import os

app = Flask(__name__)

load_dotenv()  

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    
    if request.method == "POST":
        user_input = request.form["user_input"]

        # Groq API Call
        formatted_prompt = f"""
You are an expert assistant. When answering user questions, always follow this response format:

- Start with a 2–3 line introduction about the topic.
- Then list important facts or details in bullet points.
- End with a 2-line conclusion or summary.

Now, answer this question clearly and concisely:

{user_input}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ Your original model kept
            messages=[  
                {
                    "role": "user",
                    "content": formatted_prompt
                }
            ]
        )

        response_text = completion.choices[0].message.content

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
