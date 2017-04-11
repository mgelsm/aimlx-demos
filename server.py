from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from flask_cors import CORS, cross_origin

import config as conf
import subprocess

app = Flask(__name__)
CORS(app)

# Chatbot route handling
@app.route('/chatbot')
def getChatbot():
    return render_template('chatbot.html')

@app.route('/chatbot/<question>', methods=['POST'])
def submitChatbot(question):
    print("Question:", question)
    if request.method == 'POST':
        predict_dir = conf.chatbot['path']
        model_id = conf.chatbot['model_id']
        model_dir = predict_dir + 'runs/' + model_id
        subprocess.call(['python', predict_dir + 'demo_prediction.py', '--model_dir=' + model_dir, '--raw_query=' + "'" + question + "'"])
        # Generate answer here
        with open(predict_dir + "answers.txt", "r") as text_file:
            answer = text_file.readlines()[0]
        answer = answer.split('___|||___')
        encoder = answer[0].split('___***___');
        solr = answer[1].split('___***___');
        encoder = answer[0].split('___***___');
        answer = {'solr':solr, 'encoder': encoder}
        return jsonify(answer)

# Opinion target route handling
@app.route('/opinion')
def getOpinion():
    return render_template('opinion_target.html')

@app.route('/opinion/<input>', methods=['POST'])
def submitOpinion(input):
    if request.method == 'POST':
        # Generate answer here
        answer = {'your_json_answer_key': 'your_value'}
        return jsonify(answer)

# NER route handling
@app.route('/ner')
def getNER():
    return render_template('ner.html')

@app.route('/ner/<input>', methods=['POST'])
def submitNER(input):
    if request.method == 'POST':
        # Generate answer here
        answer = {'your_json_answer_key': 'your_value'}
        return jsonify(answer)

# KP Extraction route handling
@app.route('/kp')
def getKP():
    return render_template('kp_extraction.html')

@app.route('/kp/<input>', methods=['POST'])
def submitKP(input):
    if request.method == 'POST':
        # Generate answer here
        answer = {'your_json_answer_key': 'your_value'}
        return jsonify(answer)

# Summary route handling
@app.route('/summary')
def getSummary():
    return render_template('summary.html')

@app.route('/summary/<input>', methods=['POST'])
def submitSummary(input):
    if request.method == 'POST':
        # Generate answer here
        answer = {'your_json_answer_key': 'your_value'}
        return jsonify(answer)
