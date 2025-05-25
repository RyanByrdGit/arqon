from flask import Flask, Response
import os
import time

app = Flask(__name__)
LOG_PATH = "communication.log"

def stream_logs():
    with open(LOG_PATH, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                yield f"data: {line}\n\n"
            else:
                time.sleep(0.5)

@app.route("/logs")
def logs():
    return Response(stream_logs(), mimetype="text/event-stream")

@app.route("/")
def home():
    return '''
        <html>
        <head><title>Arqon Console</title></head>
        <body>
            <h1>Arqon Console - Live Task Feed</h1>
            <pre id="log"></pre>
            <script>
                const log = document.getElementById("log");
                const evtSource = new EventSource("/logs");
                evtSource.onmessage = (e) => {
                    log.textContent += e.data + "\\n";
                    log.scrollTop = log.scrollHeight;
                };
            </script>
        </body>
        </html>
    '''

if __name__ == "__main__":
    app.run(debug=True, port=8080)
