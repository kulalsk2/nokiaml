
import requests

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
    urlAltitude = "https://api.opentopodata.org/v1/aster30m?locations="+str(lat)+","+str(long)+""  
    resAltimeter = requests.request("GET", urlAltitude).json()
    altimeter=float(resAltimeter['results'][0]['elevation'])
    X  = [cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure,altimeter]
    return X


def getCorrectUnit(X):
    X[0] = X[0]/100
    X[1] = 0.621371 *X[1] #0.621371 
    X[5] = 2.23694 *X[5]   #2.23694 
    pmb = X[6]
    hm = X[7]
    X[6] = 0.02953 *X[6] #0.02953
    pmbmin0_3 = pmb-0.3
    pmbmin0_3toPower0_190284 = pmbmin0_3**0.190284
    hmBYpmbmin0_3toPower0_190284 = hm/pmbmin0_3toPower0_190284
    rightEq = (1+0.0000842288*hmBYpmbmin0_3toPower0_190284)**5.25530260032
    X[7] = pmbmin0_3*rightEq
    X[7]= 0.02953*X[7]
    return X
