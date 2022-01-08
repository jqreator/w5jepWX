#!/usr/bin/env python
#
#ke5zznWX v1.0
#Copyright (C)2022 Jacob Parks - jqreator at gmail dot com
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#Release notes:
#v1.0.0 - Initial release

#Retrieves weather station data from Weather Underground via API and upload via APRS
#Weather Underground provides free API access for weather station contributers 
#See http://www.wxqa.com/faq.html for details on required APRS WX formatting


import requests
import json
import datetime
import socket

#Edit this section with your values
server = "cwop.aprs.net"
port = 14580
callsign = "CALLSIGN" #Replace with your callsign
aprsPassword = "xxxxx" #Replace with your APRS password
position = '0000.00N/00000.00W' #Long/Lat format is ddmm.hhN/dddmm.hhW
address = callsign + ">APRS,TCPIP*:"
identity = "user " + callsign + " pass " + aprsPassword + " vers KE5ZZNWX 1.0" + "\n"
wuAPIkey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #Replace with your Weather Underground API key
wuEndpoint = "https://api.weather.com/v2/pws/observations/current?stationId=KTXPALES79&format=json&units=e&apiKey=" + wuAPIkey
utc_datetime = datetime.datetime.now()
time = utc_datetime.strftime("%d%H%M")

#Get data from Weather Underground and format it for APRS in variables
response = requests.get(wuEndpoint).text
response_info = json.loads(response)

temperature = str(response_info["observations"][0]["imperial"]["temp"]).rjust(3, "0")
humidity = str(response_info["observations"][0]["humidity"])
pressure = str(int(response_info["observations"][0]["imperial"]["pressure"] * 33.863886667) * 10).rjust(5, '0')
wind_degrees = str(response_info["observations"][0]["winddir"])
wind_mph = str(response_info["observations"][0]["imperial"]["windSpeed"]).rjust(3, '0')
wind_gust_mph = str(response_info["observations"][0]["imperial"]["windGust"]).rjust(3, '0')
precip_1hr_in = str(format(response_info["observations"][0]["imperial"]["precipRate"], '.2f')).replace('.','')
precip_today_in = str(format(response_info["observations"][0]["imperial"]["precipTotal"], '.2f')).replace('.','')

#Build APRS WX packet
aprswxpacket = address + "@" + str(time) + "z" + position + "_" + wind_degrees + "/" \
+ wind_mph + "g" + wind_gust_mph + "t" + temperature + "r" + precip_1hr_in \
+ "P" + precip_today_in + "b" + pressure + "h" + humidity + "\n"

#Encode packet and identity string for Python3
aprswxpacket_encoded = aprswxpacket.encode()
identity_encoded  = identity.encode()

print("Time: " + time)
print("Temperature: " + temperature)
print("Humidity: " + humidity)
print("pressure: " + pressure)
print("Wind Degrees: " + wind_degrees)
print("Wind MPH: " + wind_mph)
print("Wind Gust MPH: " + wind_gust_mph)
print("Precipitation last hour: " + precip_1hr_in)
print("Precipitation today: " + precip_today_in)
print("Login string: " + identity)
print("APRS packet: " + aprswxpacket)

#Send APRS Packet
sSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSock.connect((server, port))
sSock.send(identity_encoded)
sSock.send(aprswxpacket_encoded)
sSock.shutdown(0)
sSock.close()
