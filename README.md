# w5jepWX
This script is designed to retrieve personal weather station data from the Weather Underground API and upload it to APRS/CWOP.

My Acurite 5-in-1 weather station does not natively support pulling the weather data directly, but it will upload to WU. This seemed like a decent compromise to leverage the weather data with APRS without having to capture the packets midstream since the WU API is free to contributers.

Just enter your Callsign, Coordinates, APRS password, and WU API key. I run this in a cron job every 5 mins from a Raspberry Pi as it is the max recommended submission frequncy.
 
Example cron job:
*/5 * * * * /home/w5jep/w5jepWX/w5jepWX.py >/dev/null 2>&1

More information about APRS weather and CWOP can be found at http://www.wxqa.com

#hamradio #aprs
