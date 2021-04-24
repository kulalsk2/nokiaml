from flask import Flask,render_template,request
import pickle
from flask.helpers import flash
import requests

model = pickle.load(open('model.pkl','rb'))
max = [1.0,10.0,28.18,25.02,97.85,24.83,29.87,30.67,40245,2017,12,31]
min = [0.0,1.15,-16.06,-18.72,21.25,1.03,8.59,29.48,580,2016,1,1]
app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html') #this by itself selects template folder

def latandlong(cityname):
    urlRapid = "https://community-open-weather-map.p.rapidapi.com/find"
    querystringRapid = {"q":cityname,"mode":"null","lon":"0","type":"link, accurate","lat":"0","units":"imperial, metric"}
    headersRapid = {
    'x-rapidapi-key': "38dbf9e34dmshbfaff0223d0ac4fp180cc3jsnb22b375a7fad",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    res = requests.request("GET", urlRapid, headers=headersRapid, params=querystringRapid)
    resFromRapid = res.json()
    lat = float(resFromRapid['list'][0]['coord']['lat'])
    long = float(resFromRapid['list'][0]['coord']['lon'])
    return lat,long

def getWeatherData(lat,long):
    urlWeatherBit = "https://api.weatherbit.io/v2.0/current?lat="+str(lat)+"&lon="+str(long)+"&key=f6bba80d9ad242b4b82bfb54364059ea"
    res = requests.request("GET", urlWeatherBit)
    resFromWebit = res.json()
    visibility = float(resFromWebit['data'][0]['vis'])
    cloudcoverage = float(resFromWebit['data'][0]['clouds'])
    temperature = float(resFromWebit['data'][0]['temp'])
    dewpoint = float(resFromWebit['data'][0]['dewpt'])
    relativehumidity = float(resFromWebit['data'][0]['rh'])
    windspeed = float(resFromWebit['data'][0]['wind_spd'])
    stationpressure = float(resFromWebit['data'][0]['pres'])
    urlAltitude = "https://api.opentopodata.org/v1/aster30m?locations="+str(lat)+","+str(long)+""  #"https://api.opentopodata.org/v1/eudem25m?locations="+str(lat)+","+str(long)+""
    resAltimeter = requests.request("GET", urlAltitude).json()
    altimeter=float(resAltimeter['results'][0]['elevation'])
    X = [cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure,altimeter,2017,7,5]
    return X

def getCorrectUnit(X):
    X[1] = 1.60934449789 *X[1] #1/0.621371 
    X[5] = 0.44703925898*X[5]   #1/2.23694 
    pmb = X[6]
    hm = X[7]
    X[6] =  33.8638672536 *X[6] #1/0.02953
    pmbmin0_3 = pmb-0.3
    pmbmin0_3toPower0_190284 = pmbmin0_3**0.190284
    hmBYpmbmin0_3toPower0_190284 = hm/pmbmin0_3toPower0_190284
    rightEq = (1+0.0000842288*hmBYpmbmin0_3toPower0_190284)**5.25530260032
    X[7] = pmbmin0_3*rightEq
    return X

@app.route('/predict',methods=['POST'])
def home():
    cityname = request.form['cityname']
    lat,long = latandlong(cityname)
    X = getWeatherData(lat,long)
    print("before :",X)
    X = getCorrectUnit(X)
    print("after :",X)
    X = list(X)
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