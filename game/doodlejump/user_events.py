from .constants import *


def data2event(data, status):
    status["enter"] = data["enter"] > 0
    status["up"] = data["up"] > 0
    status["move"] = data["move"]
