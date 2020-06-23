import joblib
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def model_load():
    try:
        model = joblib.load('hack_model.jb')
        sc = joblib.load('y_sc.jb')
        sc1 = joblib.load('y_ind.jb')
        return model, sc , sc1
    except Exception as ex:
        print(ex)
        #Error Happen in Model Load
        return 101

def get_data_api():
    try:
        r = requests.get("http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/2132755?apikey=MdceFU8V9cxQfSebdGS7RAiGHnyyqg3A&language=en-us&details=true&metric=true")
        if r.status_code != 200:
            raise Exception('Error happend in Api Request')
        t = r.json()
        date = []
        wind = []
        direc = []
        for i in t:
            date.append(i['DateTime'][:-6])
            wind.append(i["Wind"]['Speed']['Value'])
            direc.append(i["Wind"]['Direction']['Degrees'])
        df_ne = pd.DataFrame({'wind_sp':wind,'direc':direc},index =date)
        return df_ne
    except Exception as ex:
        print(ex)
        print(ex)
        print(ex.args())
        #Error Happen in Api Loading
        return 102

def predict():
    try:
        model, sc , sc1 = model_load()
        df_ne = get_data_api()
        df_ne.iloc[:, 0:2] = sc1.transform(df_ne.iloc[:, 0:2])
        y_api = model.predict(n_periods=12 , exogenous=df_ne.iloc[:,0:2],return_conf_int=True,alpha=0.05)
        df_ne['y_hat'] = sc.inverse_transform(y_api[0].reshape(-1,1))
        df_ne['y_lower'] = sc.inverse_transform(y_api[1][:,0:1])
        df_ne['y_upper'] = sc.inverse_transform(y_api[1][:,1:2])
        df_ne[['wind_sp','direc']] = sc1.inverse_transform(df_ne[['wind_sp','direc']])
        return df_ne
    except Exception as ex:
        print(ex)
        print(ex.args())
        #Error happen in prediction
        return 103

def plot_graph(df_ne):
    mig = make_subplots(rows=3, cols=1,
                        specs=[[{"type": "scatter", "type": "scatter", "type": "scatter"}],
                               [{"type": "scatter"}],
                               [{"type": "scatter"}]] , subplot_titles=('Power Prediction Plot','Wind Speed Plot','Direction Plot'))
    mig.add_trace(go.Scatter(x=df_ne.index, y=df_ne['y_hat'],
                             line=dict(color='red', width=4, dash='dot'),name ='Mean Predicted Power'), 1, 1)
    mig.add_trace(go.Scatter(x=df_ne.index, y=df_ne['y_lower'],
                        line=dict(color='royalblue', width=2, dash='dash'),name='Lower Range Power'), 1,1)
    mig.add_trace(go.Scatter(x=df_ne.index, y=df_ne['y_upper'], fill='tonexty',
                             line=dict(color='royalblue', width=4, dash='dash'),name='Upper Range Power'), 1, 1)
    mig.add_trace(go.Scatter(x=df_ne.index, y=df_ne['wind_sp'],name='Wind Speed'), row=2, col=1)
    mig.add_trace(go.Scatter(x=df_ne.index, y=df_ne['direc'],name='Direction'), row=3, col=1)
    mig.update_yaxes(title_text="Power (KWh)", row=1, col=1)
    mig.update_yaxes(title_text="Wind speed (m/s)", row=2, col=1)
    mig.update_yaxes(title_text="Direction (in degree)", row=3, col=1)

    mig.update_xaxes(title_text="Datetime", row=1, col=1)
    mig.update_xaxes(title_text="Datetime", row=2, col=1)
    mig.update_xaxes(title_text="Datetime", row=3, col=1)

    mig.update_layout(height = 900)
    graph1 = mig.to_json()
    return graph1


#import ibm_db_dbi
import ibm_db
#str_conn = "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-07.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=bfr48077;PWD=3j4h-zwx77mzftr4"

#conn = ibm_db_dbi.connect(str_conn," "," ")