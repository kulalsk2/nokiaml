from flask import Flask,render_template,request
import pickle

model = pickle.load(open('model.pkl','rb'))
max = [1.0,10.0,28.18,25.02,97.85,24.83,29.87,30.67,40245,2017,12,31]
min = [0.0,1.15,-16.06,-18.72,21.25,1.03,8.59,29.48,580,2016,1,1]
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
    X = list([cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure,altimeter,2017,7,5])
    Xmax = [1.0,10.0,28.18,25.02,97.85,24.83,29.87,30.67,2017,12,31]
    Xmin = [0.0,1.15,-16.06,-18.72,21.25,1.03,8.59,29.48,2016,1,1]
    XN= [x-xmn for x, xmn in zip(X, Xmin)]
    XD = [xmx-xmn for xmx, xmn in zip(Xmax, Xmin)]
    scaled =  [xn / xd for xn, xd in zip(XN, XD)]
    scaled = list([scaled])
    pred = model.predict(scaled)
    print(pred)
    return render_template('after.html',data=pred)


    

if(__name__=="__main__"):
    app.run(debug=True)


#Xsc=(X−Xmin)/(Xmax−Xmin)
#0.52	0.849718	0.847425	0.860949	0.798447	0.243697	0.977444	0.596639	0.0	0.727273	0.433333
#X = [0.03,9.29,25.32,21.64,79.37,4.97,29.28,30.08,2017,7,5]