import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import asyncio

class WebServer():
    def __init__(self, ssid = 'Asus_5C' , password = 'zakarias'):
        self.ssid = ssid 
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.webpage = self.webpage
        self.temperature = 0
        self.state = 'OFF'
        self._isConnected = self.wlan.isconnected()
        pico_led.off()
        while not self.wlan.isconnected():
            self.connect()
            print('Setting up webserver...') 
    
    def disconnect(self):
        return self.wlan.disconnect()
    def connect(self):
    #Connect to WLAN
        
        self.wlan.active(True)
        self.wlan.config(pm=0xa11140)
        self.wlan.connect(self.ssid, self.password)
        max_wait = 10                # Maximum wait time for connection (seconds)
        while max_wait > 0 and not self.wlan.isconnected():
            max_wait -= 1           # Decrement wait time
            print('waiting for connection...')
            sleep(1)           # Wait for 1 second       

        if not self.wlan.isconnected():
            print('Network Connection has failed')  # Print failure message if connection fails
        else:
            print('Connected to the network successfully.')  # Print success message if connection successful
            status = self.wlan.ifconfig()  # Get network interface configuration
            print('Enter this address in browser-> ' + status[0])
            self._isConnected = self.wlan.isconnected()# Print IP address for accessing the web server
            return status[0]
    
    @property
    def isConnected(self):
        return self._isConnected
    
    def webpage(self):
        #Template HTML
        html = """<!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Raspberry Pi Pico Web Server</title>
          <style>
            html {
              font-family: Arial;
              display: inline-block;
              margin: 0px auto;
              text-align: center;
            }
            h1 {
              font-family: Arial;
              color: #2551cc;
            }
            .button1,
            .button2 {
              border: none;
              color: white;
              padding: 15px 32px;
              text-align: center;
              text-decoration: none;
              display: inline-block;
              font-size: 16px;
              margin: 4px 2px;
              cursor: pointer;
              border-radius: 10px;
            }
            .button1 {
              background: #339966;
            }
            .button2 {
              background: #993300;
            }
          </style>
        </head>
        <body>
          <h1>Raspberry Pi Pico Web Server</h1>
          <p>Led %s</p>
          <p>
            <a href="/lighton?"><button class="button1">LED On</button></a>
          </p>
          <p>
            <a href="/lightoff?"><button class="button2">LED Off</button></a>
          </p>
          <p>Temperature: %s°C (%s°F)</p>
        </body>
        </html>
        """
        return html

    async def serve(self, reader, writer):
        #Start a web server
        print("Client connected")
        request_line = await reader.readline()
        print('Request:', request_line)
    
        # Skip HTTP request headers
        while await reader.readline() != b"\r\n":
            pass
    
        request = str(request_line, 'utf-8').split()[1]
        print('Request:', request)

        if request == '/lighton?':
            pico_led.on()
            self.state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            self.state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = self.webpage() % (self.state, "{:.2f}".format(temperature), "{:.2f}".format(temperature * 9/5 + 32))
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        writer.write(html)
        await writer.drain()
        await writer.wait_closed()
        print('Client Disconnected')
