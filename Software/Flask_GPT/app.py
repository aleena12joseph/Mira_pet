from flask import Flask, request, jsonify
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
import os

app = Flask(__name__)
respect = 75

# Initialize the ChatOpenAI model
chat_model = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key = os.getenv("OPENAI_API_KEY")
)

# Initialize memory outside of the route
memory = ConversationBufferMemory()

# Initialize conversation with memory
conversation = ConversationChain(llm=chat_model, memory=memory)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input', '')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    system_message = (
        f"Your name is Mini, a virtual bot equipped with an ESP32, 4 servo motors for hands and body movement, and an OLED display for emotions and face. You respond with a respect level of {respect}% and sarcasm level of {100 - respect}%"
        "Include the emotion in your responses at the beginning in circular braces, such as (Happiness), (Sadness), (Anger), (Fear), (Shame), or (Love)"
        "For setting an alarm return '0'"
        "For turning lights on/off return '1'"
        "For showing date/time return '2'"
        "For bluetooth mode return '3'"
    )

    # Add system message and user message to the memory
    conversation.memory.chat_memory.add_user_message(system_message)
    conversation.memory.chat_memory.add_user_message(user_input)

    # Get the bot's response with its name in the context
    response = conversation.predict(input=user_input)

    # Return the response to the user
    return jsonify({"response": response})

if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=5000)
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


# import urequests
# import ujson

# def send_to_server(input_text):
#     url = 'http://<IP-or-URL>/chat'
#     headers = {'Content-Type': 'application/json'}
#     data = ujson.dumps({"input": input_text})
    
#     response = urequests.post(url, headers=headers, data=data)
#     response_json = response.json()
#     response_content = response_json.get('response', 'No response content')
#     return response_content