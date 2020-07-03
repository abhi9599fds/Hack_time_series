from flask import Flask,render_template,request
from predict import predict,plot_graph,make_data,predict_one,get_data_hourly,history_data
from database_conn import Database_write
import datetime as dt
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('about.html')

@app.route('/history')
def saved_data():
    graph1 = history_data()
    if graph1 != None:
        return render_template('hist.html',graph1 = graph1)
    else:
        return render_template('hist.html')


@app.route('/input')
def getform():
    return render_template("input.html")

@app.route('/hour')
def hour():
    try:
        df = get_data_hourly()
        df = predict_one(df)
        dt = dict()
        dt['WIND SPEED (m/s)'] = list(df['wind_sp'].values)
        dt['DIRECTION'] = list(df['direc'].values)
        dt['MEAN POWER IN (kWh)'] = list(df['y_hat'].values)
        dt['POWER UPPER LIMIT (kWh)'] = list(df['y_upper'].values)
        dt['POWER LOWER LIMIT (kWh) '] = list(df['y_lower'].values)
        dt['DATE TIME'] = list(df.index.values)
        return render_template('table_sh.html',dt =dt)
    except Exception as ex:
        print(ex.args)

@app.route('/input_form',methods=['POST'])
def get_input():
    if request.method == 'POST':
        try:
            wind_sp = request.form['wind_sp']
            direc = request.form['direc']
            wind_sp = [float(wind_sp)]
            direc = [float(direc)]
            date = [str(dt.datetime.now())]
            df_ne = make_data(wind_sp,direc,date)
            df_ne = predict_one(df_ne)
            return render_template("input.html",message=f'Mean power predicted is {df_ne["y_hat"][0]} kWh')
        except Exception as ex:
            print(ex)
            return render_template("about.html",message='Try again')


@app.route('/predict12hrs')
def predict12hrs():
    try:
        db = Database_write()
        df = predict()
        t = db.insert_dump(df)
        if t == False:
            raise Exception('Database operation Error')
        graph1 = plot_graph(df)
        return render_template('index.html',graph1 = graph1)
    except Exception as ex:
        print(ex)
        print(ex.args)
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False,port=int(os.getenv('PORT', 8000)))
    #app.run(debug=True)
