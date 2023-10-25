from Modules.Module_Basic import *

def changeType(values: str):
    if values == "webapp":
        return "웹/앱"
    elif values == "game":
        return "게임"
    elif values == "iot":
        return "IOT"
    else:
        return False