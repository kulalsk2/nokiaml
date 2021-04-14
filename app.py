from flask import Flask,render_template,request
import pickle

model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html') #this by itself selects template folder

@app.route('/predict',methods=['POST'])
def home():
    lat = float(request.form['lat'])
    long = float(request.form['long'])
    visibility = float(request.form['visibility'])
    cloudcoverage = float(request.form['cloudcoverage'])
    temperature = float(request.form['temperature'])
    dewpoint = float(request.form['dewpoint'])
    relativehumidity = float(request.form['relativehumidity'])
    windspeed = float(request.form['windspeed'])
    stationpressure = float(request.form['stationpressure'])
    altimeter = float(request.form['altimeter'])
    arr = list([[cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure,altimeter,0.0,0.727273,0.433333]])
    
    print(arr)   
    pred = model.predict(arr)
    print(pred)
    return render_template('after.html',data=pred)


    

if(__name__=="__main__"):
    app.run(debug=True)

