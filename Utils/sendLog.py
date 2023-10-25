from Modules.Module_Basic import *

async def sendLogging(app, text):
    await app.get_channel(1143589941469782026).send(f"## [ log ] \n{text}")
    return True