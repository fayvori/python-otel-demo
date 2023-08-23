import os
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from flask import Flask, request
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from random import randint
from time import sleep
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

JAEGER_SERVICE_NAME = "python.dice"
JAEGER_HOST = os.environ["JAEGER_HOST"]
JAEGER_PORT = os.environ["JAEGER_PORT"]

provider = TracerProvider(resource=Resource.create({SERVICE_NAME: JAEGER_SERVICE_NAME}))

jaeger_exporter = JaegerExporter(
    agent_host_name=JAEGER_HOST,
    agent_port=int(JAEGER_PORT),
) 

span_processer = BatchSpanProcessor(jaeger_exporter)

trace.set_tracer_provider(provider)
trace.get_tracer_provider().add_span_processor(span_processer)

tracer = trace.get_tracer(JAEGER_SERVICE_NAME)

app = Flask(__name__)

@app.route("/rolldice")
def roll_dice():
    sleep_arg = request.args.get("sleep")

    if sleep_arg == None:
        sleep_arg = 0

    return str(do_roll(int(sleep_arg)))

def do_roll(arg):
    with tracer.start_as_current_span("do_roll") as rollspan:
        res = randint(1, 6)
        sleep(arg)
        return res
