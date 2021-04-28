from flask import Flask,render_template,request
import pickle
from flask.helpers import flash
import requests
import time
from datetime import date
model = pickle.load(open('regressor.pkl','rb'))

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
    urlWeatherBit = "https://api.weatherbit.io/v2.0/history/hourly?lat="+str(lat)+"&lon="+str(long)+"&start_date=2021-04-26&end_date=2021-04-27&tz=local&key=c19308a05e44450f805946e96f0743d0"
    res = requests.request("GET", urlWeatherBit)
    resFromWebit = res.json()
    return resFromWebit

def locElevation(lat, long):
    urlAltitude = "https://api.opentopodata.org/v1/aster30m?locations="+str(lat)+","+str(long)+""  
    resAltimeter = requests.request("GET", urlAltitude).json()
    altimeter=float(resAltimeter['results'][0]['elevation'])
    return altimeter

def refinedData(resFromWebit, i):
    visibility = float(resFromWebit['data'][i]['vis'])
    cloudcoverage = float(resFromWebit['data'][i]['clouds'])
    temperature = float(resFromWebit['data'][i]['temp'])
    dewpoint = float(resFromWebit['data'][i]['dewpt'])
    relativehumidity = float(resFromWebit['data'][i]['rh'])
    windspeed = float(resFromWebit['data'][i]['wind_spd'])
    stationpressure = float(resFromWebit['data'][i]['pres'])
    hour = str(resFromWebit['data'][i]['timestamp_local'])
    hour = int(hour[11:13])
    # todayData = date.today().strftime("%d-%m-%Y")
    # day,month,year = tuple(str(todayData).split('-'))
    # year = int(year)
    # month = int(month)
    # day = int(day)
    X  = [hour,cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure]
    return X

def getCorrectUnit(X):
    X[1] = X[1]/100
    X[2] = 0.621371 *X[2] #0.621371 
    X[6] = 2.23694 *X[6]   #2.23694 
    pmb = X[7]
    hm = X[8]
    X[7] = 0.02953 *X[7] #0.02953
    pmbmin0_3 = pmb-0.3
    pmbmin0_3toPower0_190284 = pmbmin0_3**0.190284
    hmBYpmbmin0_3toPower0_190284 = hm/pmbmin0_3toPower0_190284
    rightEq = (1+0.0000842288*hmBYpmbmin0_3toPower0_190284)**5.25530260032
    X[8] = pmbmin0_3*rightEq
    X[8]= 0.02953*X[8]
    return X

@app.route('/predict',methods=['POST'])
def home():
    cityname = request.form['cityname']
    lat,long = latandlong(cityname)
    resFromWebit = getWeatherData(lat,long)
    altimeter = locElevation(lat, long)
    final = list()
    for i in range(0,24):
        X = refinedData(resFromWebit, i)
        X.append(altimeter)
        X = getCorrectUnit(X)
        print(X)
        X = list([X])
        pred = model.predict(X)
        final.append(pred)
        X = []
    print(final)
    output = sum(final)
    return render_template('after.html',data=output)

if(__name__=="__main__"):
    app.run(debug=True)