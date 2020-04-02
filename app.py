import connexion
from connexion import NoContent
import requests
import json
import yaml
from pykafka import KafkaClient
import datetime


try:
    with open('/config/app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())


def booking_details(deliveryDetails):
    headers = {'Content-type': 'application/json'}
    url = 'http://localhost:8090/booking_details'

    client = KafkaClient(hosts=app_config['kafka']['server'] + ":" + app_config['kafka']['port'])
    topic = client.topics[app_config['kafka']['topic']]
    producer = topic.get_sync_producer()
    msg = {
        "type": "booking_details",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": deliveryDetails}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    # post = requests.post(url, msg_str, headers=headers)
    # print(post)

    return NoContent, 201

def freight_assignment(freightAssignment):
    headers = {'Content-type': 'application/json'}
    url = 'http://localhost:8090/freight_assignment'

    client = KafkaClient(hosts=app_config['kafka']['server'] + ":" + app_config['kafka']['port'])
    topic = client.topics[app_config['kafka']['topic']]
    producer = topic.get_sync_producer()
    msg = {
        "type": "freight_assignment",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": freightAssignment}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    # post = requests.post(url, msg_str, headers=headers)
    # print(post)

    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)