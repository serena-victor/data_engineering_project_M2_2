from flask import Flask, render_template, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import start_http_server
import sys

from detoxify import Detoxify

app = Flask(__name__)

toxicity = Detoxify('unbiased')
metrics = PrometheusMetrics(app)

@app.route('/', methods=['POST','GET'])
def root():
    if request.method == 'GET':
        return render_template('web_app.html')
    if request.method == 'POST':
        data = request.form.get('text_to_send')
        results = toxicity.predict(data)
        
        text_to_render = f'<br><strong>results for : "</strong>{data}"<br><br>'
        for key in results :
            key_percent = (results[key]*100).round(3)
            text_to_render += f'<p id="{key}">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{key} : {key_percent}%</p>'

        return render_template('result.html', toxicity_results = text_to_render)


#app.run(host='flask-app', port=5000, threaded=True)