from flask import Flask,render_template
from predict import predict,plot_graph
from database_conn import Database_write
import os

app = Flask(__name__)

@app.route('/')
def home():
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
        print(ex.args())
        return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=int(os.getenv('PORT', 8000)))
    #app.run(debug=True)ii