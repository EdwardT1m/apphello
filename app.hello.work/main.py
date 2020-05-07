#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import jsonify, Flask, request, Response
import os
from prometheus_client import Counter, Histogram, start_http_server
import time
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)
health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")

FLASK_REQUEST_LATENCY = Histogram('flask_request_latency_seconds', 'Flask Request Latency',
				['method', 'endpoint'])
FLASK_REQUEST_COUNT = Counter('flask_request_count', 'Flask Request Count',
				['method', 'endpoint', 'http_status'])
				
def before_request():
	request.start_time = time.time()

def after_request(response):
	request_latency = time.time() - request.start_time
	FLASK_REQUEST_LATENCY.labels(request.method, request.path).observe(request_latency)
	FLASK_REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
	return response

def monitor(app, port=8000, host='0.0.0.0'):
	app.before_request(before_request)
	app.after_request(after_request)
	start_http_server(port, host)

@app.route('/api/v1/hello', methods=['GET'])
def say_hello():
	REAL_IP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	return Response("Hello {0}.\nI'm dokerized application =)\n".format(REAL_IP), status=200)


if __name__ == "__main__":
	# API_PORT = int(os.getenv('APW_API_PORT'))
	# API_HOST = os.getenv('APW_API_HOST')
	# MON_PORT = int(os.getenv('MON_PORT'))
	# MON_HOST = os.getenv('MON_HOST')
	API_PORT = 80
	API_HOST = "0.0.0.0"
	MON_PORT = 9201
	MON_HOST = "0.0.0.0"
	monitor(app, port=MON_PORT, host=MON_HOST)
	app.run(host=API_HOST, port=API_PORT)