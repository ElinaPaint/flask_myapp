from flask import Flask, jsonify, request, render_template
# import pymongo
import json
import pickle
from sqlalchemy import create_engine, text
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd




app = Flask(__name__)
grafica = pd.read_csv('csv_Data.csv')
app.config["DEBUG"] = True

@app.route("/")
def hello():
    return '''<h1>Distant Wine Archive</h1>
            <h2>This is an API to predict the quality of red wine. the Portuguese Vinho Verde wine </h2>
            <p> Use this link to predict the quality of your wine </p>'''
    # return str(model.predict([[7.5, 0.8, 0.0, 1.9, 0.076, 9.0, 40.0, 0.9978, 3.51, 0.57, 9.4]])[0])

@app.route('/api/v0/resources/predict/<float:n1>/<float:n2>/<float:n3>/<float:n4>/<float:n5>/', methods=['GET'])
def predict(n1,n2,n3,n4,n5):
    prediction = model.predict([[n1,n2,n3,n4,n5]])
    return jsonify({"prediction": str(prediction[0])})


@app.route('/api/v0/resources/Graph', methods=['GET'])
def graph():
    plt.figure(figsize=(6,6))
    plt.bar(x = grafica.columns, height = grafica.values[0])
    plt.xlabel("Features")
    plt.ylabel("Importance");
    return render_template('untitled1.html', name = plt.show())




app.run()
