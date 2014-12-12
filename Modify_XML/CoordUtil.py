import math

pi = 3.1415926535897932384626;  
a = 6378245.0;  
ee = 0.00669342162296594323;  

def wgs84_to_gcj02(lat,lng):	        
    return transform(lat, lng)

def wgs84_to_bd09(lat,lng):
    gcj02_lat, gcj02_lng = wgs84_to_gcj02(lat, lng)
    bd09_lat, bd09_lng = gcj02_to_bd09(gcj02_lat,gcj02_lng)
    return bd09_lat,bd09_lng

def gcj02_to_wgs84(lat,lng):
    t_lat, t_lng = transform(lat, lng)
    t_lat = lat * 2 - t_lat
    t_lng = lng * 2 - t_lng
    return t_lat,t_lng

def gcj02_to_bd09(lat,lng):
    x= lng
    y = lat  
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * pi);  
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * pi);  
    bd_lon = z * math.cos(theta) + 0.0065;  
    bd_lat = z * math.sin(theta) + 0.006;  
    return bd_lat,bd_lon

def bd09_to_wgs84(lat,lng):
    gcj02_lat, gcj02_lng = bd09_to_gcj02(lat, lng)
    wgs84_lat, wgs84_lng = gcj02_to_wgs84(gcj02_lat,gcj02_lng)
    return wgs84_lat, wgs84_lng
    
def bd09_to_gcj02(lat,lng):
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * pi);  
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * pi);  
    gg_lon = z * math.cos(theta);  
    gg_lat = z * math.sin(theta);  
    return gg_lat,gg_lon

def outOfChina(lat,lng):
    return (lng < 72.004 or lng > 137.8347 or lat < 0.8293 or lat > 55.8271)

def transform(lat,lng):
    if outOfChina(lat, lng):
        return lat,lng
    
    dLat = transformLat(lng - 105.0, lat - 35.0);  
    dLon = transformLng(lng - 105.0, lat - 35.0);  
    radLat = lat / 180.0 * pi;  
    magic = math.sin(radLat);  
    magic = 1 - ee * magic * magic;  
    sqrtMagic = math.sqrt(magic);  
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi);  
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi);  
    mgLat = lat + dLat;  
    mgLon = lng + dLon;  
    return mgLat,mgLon
    
    
def transformLat(x,y) :
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));  
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0;  
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0;  
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0;  
    return ret;  


def transformLng(x,y) : 
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));  
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0;  
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0;  
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0  
            * pi)) * 2.0 / 3.0;  
    return ret;  




