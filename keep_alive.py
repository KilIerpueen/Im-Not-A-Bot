from flask import Flask, Markup
from threading import Thread
from waitress import serve
import os


app = Flask('')

ID = '1141489646254166066'
TOKEN = "MTEzMDM5NTI3NDY3ODkwMjg1NQ.G07gom.h67qAWKxlhxcwRXmlIzyDkUQt35UlPljhLYAJw"

# Define the Discord widget iframe
discord_widget = Markup('''
<iframe src="https://discord.com/widget?id=1141489646254166066&theme=dark" 
        width="350" height="500" allowtransparency="true" frameborder="0" 
        sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts">
</iframe>''')


@app.route('/')
def home():
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Bot Commands</title>
</head>
<body style="background-color: black; color: white;">
    <h1>Bot is back online</h1>

    <!-- Include the Discord widget iframe -->
    {discord_widget}
</body>
</html>'''

def run():
    serve(app, host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
