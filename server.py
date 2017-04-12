from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from flask_cors import CORS, cross_origin

import config as conf
import subprocess
import os
import re

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
        python_env = conf.chatbot['python_env']
        model_dir = predict_dir + 'runs/' + model_id
        subprocess.call([python_env, predict_dir + 'demo_prediction.py', '--model_dir=' + model_dir, '--raw_query=' + "'" + question + "'"])
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
def parse_output(output_path):
    f = open(output_path,'r')
    pred_labels = []
    for line in f:
        line = line.strip()
        if len(line.split()) == 3:
            pred_label = line.split()[2]
            pred_labels.append(pred_label)
    return " ".join(pred_labels)

@app.route('/opinion')
def getOpinion():
    return render_template('opinion_target.html')

@app.route('/opinion/<input>', methods=['POST'])
def submitOpinion(input):
    if request.method == 'POST':
        script_dir = conf.ate['path'] + 'run_demo.py'
        predict_dir = conf.ate['path'] + '/predictions/predictions.txt'
        python_env = conf.ate['python_env']
        response = ""
        subprocess.call([python_env, script_dir, '--sentence', '"'+ input + '"'])
        answer = parse_output(predict_dir)
        print("Question received for ATE project", answer)
        answer = {'labels': answer}
        return jsonify(answer)

# NER route handling
@app.route('/ner')
def getNER():
    return render_template('ner.html')

@app.route('/ner/<input>', methods=['POST'])
def submitNER(input):
    if request.method == 'POST':
        script_dir = conf.ner['path'] + 'run_demo.py'
        predict_dir = conf.ner['path'] + 'predictions/predictions.txt'
        response = ""
        subprocess.call(['python', script_dir, '--sentence', '"'+ input + '"'])
        answer = parse_output(predict_dir)
        print("Question received for NER project", answer)
        answer = {'labes': answer}
        return jsonify(answer)

# KP Extraction route handling
@app.route('/kp')
def getKP():
    return render_template('kp_extraction.html')

@app.route('/kp/<path:input>', methods=['POST'])
def submitKP(input):
    if request.method == 'POST':
        text_content = subprocess.check_output([conf.kpextract['python_env'], conf.kpextract['fetcher_path'], input]).decode('utf-8')
        subprocess.call([conf.kpextract['python_env'], '-m', 'kpextract.models.singlerank', text_content, '6', '14', os.path.join(conf.kpextract['path'],'tmp')])
        html_doc, list_kp = read_kp_output()
        return render_template('kpboard.html', html_doc=html_doc, list_kp=list_kp)

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def read_kp_output():
    processed_text = read_file(os.path.join(conf.kpextract['path'],'tmp','result_text.txt'))
    processed_text = re.sub('\n+', '\n', processed_text)
    html_doc = processed_text.replace('\n', '</div><div class=start></br>')
    html_doc = html_doc.replace('<phrase>', '<span class=kp>')
    html_doc = html_doc.replace('</phrase>', '</span>')
    html_doc = '<div class=start>' + html_doc + '</div>'

    list_kp_text =  read_file(os.path.join(conf.kpextract['path'],'tmp','result_kp.txt'))
    list_kp = list_kp_text.split(';')
    
    return html_doc, list_kp


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

if __name__ == '__main__':
    app.run(host= '127.0.0.1')
