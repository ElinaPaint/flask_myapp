# How To Use Web Forms in a Flask Application

#libraries
from flask import Flask, render_template
from flask import Flask, render_template, request, url_for, flash, redirect
import json
import pickle
from sqlalchemy import create_engine, text
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime 
from io import BytesIO
import base64

# pickle
pickled_file_path = 'finished_model_me.pkl'
with open(pickled_file_path, 'rb') as file:
    model = pickle.load(file)

# engine = create_engine("sqlite:///db.db")
url = "postgresql://postgres:123456789@database-1.cczybszaj7ev.eu-north-1.rds.amazonaws.com:5432/postgres"
engine = create_engine(url)

# Grafica
grafica = pd.read_csv('csv_Data.csv')

# Flask, needed
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = '456caaebfac319e39ba76234faef1039ad0dc3b0ee769aa5'


# 
columnas = []

@app.route('/')
def index():
    return render_template('Index.html', messages=columnas)



@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        column1 = float(request.form['OH'])
        column2 = float(request.form['sulphates'])
        column3 = float(request.form['total_SO₂'])
        column4 = float(request.form['vol_acid'])
        column5 = float(request.form['dens']) 

        prediction_number = model.predict([[column1, column2, column3, column4,column5]])[0]

                
        input = str([column1, column2, column3, column4,column5])
        output = prediction_number
        fecha = str(datetime.now())[0:19]

        df = pd.DataFrame({
                "Fecha": [fecha],
                "input": [input],
                "prediction": [output]
            })
            
            
        df.to_sql("test", con=engine, if_exists="append", index=None)
        

        if not column1:
            flash('Field is required!')
        elif not column2:
            flash('Field is required!')
        elif not column3:
            flash('Field is required!')
        elif not column4:
            flash('Field is required!')
        elif not column5:
            flash('Field is required!')
        else:
            columnas.append({'column1': f"vol_acid: {column1}", 
                             'column2': f"free_SO₂: {column2}", 
                             'column3': f"total_SO₂: {column3}", 
                             'column4': f"sulphates: {column4}", 
                             'column5': f"alcohol: {column5}",
                             'prediction': f"Your prediction is {prediction_number}",
                             })
            return redirect(url_for('index'))
            

    return render_template('create.html')



# About the app
@app.route('/about/')
def about():
    return render_template('about.html')



@app.route("/check_logs", methods=["GET"])
def check_logs():
    
    filter = False
    start = request.args.get("start")
    end = request.args.get("end")
    filter = request.args.get("filter")
    
    # start = "2023-12-11 10:11:32"
    # end = "2023-12-11 10:11:34"
    if filter == True:

        query = f"""

            select * from test
            where fecha < "{end}"
            and fecha > "{start}";

        """
    else:
        query = f"""

            select * from test 
            
            """
            
    return pd.read_sql(query, con=engine).to_html()



@app.route('/Graph', methods=['GET'])
def graph():
    plt.figure(figsize=(6,6))
    plt.bar(x=grafica.columns, height=grafica.values[0])
    plt.xlabel("Features")
    plt.ylabel("Importance")
    
    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Encode plot to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Pass the base64 string to the HTML template
    return render_template('untitled1.html', plot_url=plot_url)

app.run()
