from utils import *
from requests.auth import HTTPDigestAuth
from http import HTTPStatus
import requests

logger_name = "OMAPI"
logger = get_logger(logger_name)
def api_call(resource, method = "GET", payload = {}):
    config = load_config()
    url = config["api_base_url"] + resource
    auth = HTTPDigestAuth(config["public_key"], config["private_key"])
    if method == "GET":
        result = requests.get(url, auth = auth)
    elif method == "POST":
        result = requests.post(url, auth = auth, json = payload)
    elif method == "PUT":
        result = requests.put(url, auth = auth, json = payload)
    status = int(result.status_code)
    if status < 200 or status > 300:
        logger.error("Error returned by server: %s" % result.content)
        exit()

    return result.json()

def get_all_global_alerts():
    return api_call("/globalAlertConfigs", method="GET")

def get_all_project_alerts(project_id):
    return api_call("/groups/%s/alertConfigs" % project_id)

def create_global_alert(payload):
    return api_call("/globalAlertConfigs", method="POST", payload=payload)

def update_global_alert(alert_id, payload):
    return api_call("/globalAlertConfigs/%s" % alert_id, method="PUT", payload=payload)

def create_project_alert(project_id, payload):
    return api_call("/groups/%s/alertConfigs" % project_id, method="POST", payload=payload)

def update_project_alert(project_id, alert_id, payload):
    return api_call("/groups/%s/alertConfigs/%s" % (project_id, alert_id), method="PUT", payload=payload)