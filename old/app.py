from flask import Flask, render_template, request, jsonify
from bot import DynamicBot
from rag import RAGSystem
import threading
import uuid

app = Flask(__name__)
rag_system = RAGSystem()
bots = {}

@app.route('/')
def index():
    return render_template('index.html', bots=bots)

@app.route('/create_bot', methods=['POST'])
def create_bot():
    bot_id = str(uuid.uuid4())
    new_bot = DynamicBot(bot_id, rag_system)
    bots[bot_id] = new_bot
    threading.Thread(target=new_bot.run).start()
    return jsonify({"bot_id": bot_id})

@app.route('/stop_bot/<bot_id>', methods=['POST'])
def stop_bot(bot_id):
    if bot_id in bots:
        bots[bot_id].stop()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Bot not found"})

@app.route('/delete_bot/<bot_id>', methods=['POST'])
def delete_bot(bot_id):
    if bot_id in bots:
        bots[bot_id].stop()
        del bots[bot_id]
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Bot not found"})

@app.route('/bot_status/<bot_id>')
def bot_status(bot_id):
    if bot_id in bots:
        return jsonify(bots[bot_id].get_status())
    return jsonify({"status": "error", "message": "Bot not found"})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.json['question']
    response = rag_system.ask_question(question)
    return jsonify({"response": response})

@app.route('/add_task', methods=['POST'])
def add_task():
    bot_id = request.json['bot_id']
    task = request.json['task']
    priority = request.json.get('priority', 1)
    if bot_id in bots:
        bots[bot_id].add_task(task, priority)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Bot not found"})

if __name__ == '__main__':
    app.run(debug=True)
