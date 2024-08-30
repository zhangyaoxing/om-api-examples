#!/usr/bin/env python3
from utils import *
from om_api import *

LOGGER_NAME = "Alerts"
logger = get_logger(LOGGER_NAME)
config = load_config()

# Wrapper of create alert.
# If project_id exists, create project level alert.
# Otherwise create global alert.
def create_alert(payload, project_id=None):
    if project_id == None:
        return create_global_alert(payload)
    else:
        return create_project_alert(project_id, payload)

# Wrapper of update alert.
# If project_id exists, update project level alert.
# Otherwise update global alert.
def update_alert(alert_id, payload, project_id=None):
    if project_id == None:
        return update_global_alert(alert_id, payload)
    else:
        return update_project_alert(project_id, alert_id, payload)
    
def alert_exists(payload, existing_alerts):
    # If payload has eventTypeName == "OUTSIDE_METRIC_THRESHOLD", use metricThreshold.metricName as comparison field
    alert_type = payload["eventTypeName"]
    if alert_type == "OUTSIDE_METRIC_THRESHOLD":
        metric = payload["metricThreshold"]["metricName"]
        for alert in existing_alerts["results"]:
            if "metricThreshold" in alert:
                if "metricName" in alert["metricThreshold"]:
                    if alert["metricThreshold"]["metricName"] == metric:
                        return alert["id"]
    else:
        # Just look for the type
        for alert in existing_alerts["results"]:
            if alert["eventTypeName"] == alert_type:
                return alert["id"]

    return None

def upsert_alert(payload, existing_alerts, project_id=None):
    alert_id = alert_exists(payload, existing_alerts)
    event_type = payload["eventTypeName"]
    if event_type == "OUTSIDE_METRIC_THRESHOLD":
        metric_name = " - %s" % payload["metricThreshold"]["metricName"]
    else:
        metric_name = ""
    if alert_id == None:
        logger.info("Creating alert: {event_type}{metric_name}"
                          .format(event_type=cyan(event_type), metric_name=cyan(metric_name)))
        result = create_alert(payload, project_id)
        logger.info(green("Alert created!"))
    else:
        logger.info("Alert {event_type}{metric_name} exists. Updating..."
                          .format(event_type=yellow(event_type), metric_name=yellow(metric_name)))
        result = update_alert(alert_id, payload, project_id)
        logger.info(green("Alert updated!"))
    return result

def apply_alerts(alerts, project_id=None):
    if project_id == None:
        # Applying global alerts
        existing_alerts = get_all_global_alerts()
    else:
        # Applying project alerts
        existing_alerts = get_all_project_alerts(project_id)
    for alert in alerts: 
        with open(alert) as fd:
            payload = json.load(fd)
            logger.debug("Alert config: {alert}".format(alert=payload))
            result = upsert_alert(payload, existing_alerts, project_id)
            logger.debug(result)

# Set global alerts
alerts_listing = os.listdir("./alerts")
# Global alerts = .json files in ./alerts folder
global_alerts = ["./alerts/%s" % filename for filename in alerts_listing if os.path.isfile("./alerts/%s" % filename)]
logger.info(bold(green("Setting global alerts.")))
apply_alerts(global_alerts)

# Set project level alerts
# Project alerts = .json files in subfolders of ./alerts
pids = [filename for filename in alerts_listing if os.path.isdir("./alerts/%s" % filename)]
for pid in pids:
    logger.info("Setting alerts for project: {pid}".format(pid=bold(green(pid))))
    project_specific_alerts = ["./alerts/%s/%s" % (pid, filename) for filename in os.listdir("./alerts/%s" % pid) if True ]
    apply_alerts(project_specific_alerts, pid)