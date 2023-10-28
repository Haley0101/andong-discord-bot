from Modules.Module_Basic import *
from Modules.Module_Env import *

class HaleyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='.',
            intents=Intents.all(),
            enable_debug_events=True 
            # sync_command=True,
        )
        self.synced = False
        self.initial_extensions = []
        self.client = commands.Bot

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Cogs')

        for ext in os.listdir(path):
            if ext.endswith('.py'):
                filename = ext.split('.')[0]
                cog = f'Cogs.{filename}'
                self.initial_extensions.append(cog)
                print(f'FOUND : {cog}')
        
    async def setup_hook(self):
        try:
            for ext in self.initial_extensions:
                await self.load_extension(ext)
                print(f'LOAD : {ext}')
            if not self.synced:
                await client.tree.sync()
                self.synced = True
        except Exception as e:
            print(e)
            os.system('read')
        
        btn = self.get_cog("users_joinMember")
        self.add_view(btn.get_btn())

    async def on_ready(self):
        # os.system('clear')
        print("login")
        print("==============================\n")
        print(self.user.name)
        print(self.user.id)
        print("\n==============================")

    async def on_message(self, message):
        if message.author.bot:
            return None
        
        if message.content.startswith("#로드") and message.author.guild_permissions.administrator:
            filename = message.content.replace("#로드", "").replace(" ", "")
            await self.load_extension(f"Cogs.{filename}")
            await message.channel.send("ㅇㅇㅇ")
        elif message.content.startswith("#언로드") and message.author.guild_permissions.administrator:
            filename = message.content.replace("#언로드", "").replace(" ", "")
            await self.unload_extension(f"Cogs.{filename}")
            await message.channel.send("ㅇㅇㅇ")
        elif message.content.startswith("#리로드"):
            filename = message.content.replace("#리로드", "").replace(" ", "")
            await self.unload_extension(f"Cogs.{filename}")
            await self.load_extension(f"Cogs.{filename}")
            await message.channel.send("ㅇㅇㅇ")
        elif message.content.startswith("#cls"):
            os.system('clear')

client = HaleyBot()
client.run(botToken)