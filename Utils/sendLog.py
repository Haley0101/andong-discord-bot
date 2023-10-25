from Modules.Module_Basic import *

async def sendLogging(app, text):
    await app.get_channel(1166636388070989874).send(f"## [ log ] \n{text}")
    return True