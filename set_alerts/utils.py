from shutil import rmtree, move
import os
import json
import logging
import argparse

config = None
def load_config():
    global config
    if config == None:
        config = json.load(open("./config.json"))
        config["public_key"] = config.get("public_key", os.environ.get("public_key", None))
        config["private_key"] = config.get("private_key", os.environ.get("private_key", None))
        if config["public_key"] == None or config["private_key"] == None:
            logging.error("Public/private keys are not configured.")
            exit()
        if config["om_url"].endswith("/"):
            config["api_base_url"] = config["om_url"] + "api/public/v1.0"
        else:
            config["api_base_url"] = config["om_url"] + "/api/public/v1.0"

    return config

levels = logging._nameToLevel
parser = argparse.ArgumentParser(description="Alerts API Example")
parser.add_argument("--logLevel",
    help = "Set log level.",
    choices= ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"],
    default = "INFO")
args = parser.parse_args()
log_level = levels[args.logLevel]
logging.basicConfig(level = log_level)
def get_logger(name):
    logger = logging.getLogger(name)
    return logger

logging.basicConfig(level = log_level)
logger = logging.getLogger(__name__)
logger.info("Log level: %s" % args.logLevel)

def color_code(code): return f"\x1b[{code}m"
def colorize(code: int, s: str) -> str: return f"{color_code(code)}{str(s).replace(color_code(0), color_code(code))}{color_code(0)}"
def green(s: str) -> str: return colorize(32, s)
def yellow(s: str) -> str: return colorize(33, s)
def red(s: str) -> str: return colorize(31, s)
def cyan(s: str) -> str: return colorize(36, s)
def magenta(s: str) -> str: return colorize(35, s)
def bold(s: str) -> str: return colorize(1, s)
def info_log(*strs: str) -> None:
    for s in strs: print(yellow(s))
def warning_log(*strs: str) -> None:
    for s in strs: print(bold(yellow(s)))
def success_log(*strs: str) -> None:
    for s in strs: print(green(s))
def error_log(*strs: str) -> None:
    for s in strs: print(red(s))

if __name__ == "__main__":
    print(load_config())