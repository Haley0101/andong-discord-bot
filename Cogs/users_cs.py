import asyncio
from Modules.Module_Basic import *
# from Modules.Module_API import *
from Modules.Module_SQL import *
from Utils.sendLog import sendLogging

class question_btn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="문의 글 작성하기", style=discord.ButtonStyle.green, custom_id="ok_btn")
    async def donation_from(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        class modal(ui.Modal, title="아래의 항목에 정보를 작성해주세요."):
            question_title = ui.TextInput(
                label="문의 글 제목",
                style=discord.TextStyle.long,
                placeholder="",
                default="",
                required=True,
                max_length=50,
            )

            question_content = ui.TextInput(
                label="문의 내용",
                style=discord.TextStyle.paragraph,
                placeholder="",
                default="",
                required=True,
                max_length=100,
            )

            async def on_submit(self, interaction: Interaction) -> None:
                category: CategoryChannel = interaction.guild.get_channel(1167826323939532881)
                overwrites = {
                    interaction.guild.default_role: PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
                    interaction.user: PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True)
                }
                textChannel = await interaction.guild.create_text_channel(name=f"문의-{interaction.user.display_name}", category=category, overwrites=overwrites)
                
                await interaction.guild.get_channel(textChannel.id).send(f"작성자 : {interaction.user.mention}({interaction.user.id})\n질문 제목 : {self.question_title} \n### 질문 내용\n{self.question_content}")
                await interaction.response.send_message(
                    f"질문을 정상적으로 작성 하였습니다. \n질문 제목 : {self.question_title} \n### 질문 내용\n{self.question_content}",
                    ephemeral=True,
                )

        await interaction.response.send_modal(modal())


class users_cs(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
    
    # @app_commands.command(name="팀정보", description="팀 정보를 확인 할 수 있습니다.")
    # async def teamCoinInfo(self, interaction: Interaction):
    #     db, SQL = get_SQL()
    #     if db == False:
    #         return await interaction.response.send_message("서버와의 연결이 불안정 합니다.", ephemeral=True)

    #     result, teamData = await API_teamInfo(get_teamId(interaction.user.id))
    #     if result:
    #         users = str(teamData['member']).split(', ')
    #         await interaction.response.send_message(f"## {teamData['name']}팀의 정보 \n- 보유 코인: {teamData['coin']} \n- 보유 머니: {teamData['money']} \n## 팀원정보\n- {users[0]} (팀장)\n- {users[1]}\n- {users[2]}\n- {users[3]}", ephemeral=True)    
        
    #     else:
    #         await sendLogging(self.client, f"팀정보 조회 ERROR - {interaction.user.mention} \n{teamData}")
    #         await interaction.response.send_message("팀을 조회 할 수 업습니다. 스태프에게 문의 해주세요.", ephemeral=True)


    # @app_commands.command(name="우리팀일어남", description="스태프에게 기상 하였다는 것을 알려줍니다.")
    # async def wakeUp(self, interaction: Interaction):
    #     teamName = get_teamName(get_teamId(interaction.user.id))
    #     if teamName == "False" or teamName is False or teamName == 'false':
    #         await sendLogging(self.client, f"ERROR 우리팀일어남 - 참가한 팀이 없습니다. \n사용자 : {interaction.user.mention}")
    #         interaction.response.send_message(f"## {teamName}팀 모두 기상하셨군요! 스태프에게 전달 해놓을게요~~", ephemeral=True)
    #     await sendLogging(self.client, f"## {teamName}팀이 기상하였습니다.")
    #     await interaction.response.send_message(f"## {teamName}팀 모두 기상하셨군요! 스태프에게 전달 해놓을게요~~", ephemeral=True)


    # @app_commands.command(name="신청곡", description="1코인으로 신청곡을 신청 합니다.")
    # @app_commands.describe(value="신청곡 URL 또는 제목과 가수명을 작성해 주세요.")
    # async def musicStaffSend(self, interaction: Interaction, value: str):
    #     await interaction.response.send_message(f"현재 준비중 입니다.", ephemeral=True)
    #     sendLogging(self.client, f"## 신청곡 \n {value}")
    #     await interaction.response.send_message(f"## 정상적으로 신청곡 신청이 완료 되었습니다! 스태프에게 전달 해놓을게요~~")


    @app_commands.command(name="문의하기", description="운영팀에게 질문 할 수 있습니다.")
    async def donationSend(self, interaction: Interaction):
        # await interaction.response.send_message(f"현재 준비중 입니다.", ephemeral=True)
        view = question_btn()
        await interaction.response.send_message(f"## 질문 유의 사항 \n- 운영팀 모두가 보는 질문 입니다. \n- 문의 작성자와 운영팀이 있는 채널이 생성 됩니다.", ephemeral=True, view=view)


    @app_commands.command(name="문의_종료", description="질문 채널에서 종료가 가능 합니다.")
    async def testBoardList(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("운영팀이 아닙니다.", ephemeral=True)
        try:
            await interaction.response.send_message(f"문의가 3초 뒤 종료 됩니다.")
            await asyncio.sleep(3)
            await interaction.channel.delete()
        except:
            pass

    # @app_commands.command(name='테스트')
    # async def adminTest(self, interaction: Interaction):
    #     if not interaction.user.guild_permissions.administrator:
    #         await interaction.response.send_message("운영팀이 아닙니다.", ephemeral=True)
        
    #     for user in interaction.guild.members:
    #         try:
    #             print(user.display_name.split('_'))
    #             name = user.display_name.split('_')
    #         except:
    #             pass
    #         db, SQL = get_SQL()
    #         if db == False:
    #             print("DB CONNECT ERROR")
    #         try:
    #             SQL.execute(
    #                 f"UPDATE USER_DATA SET DISCORD_ID = '{user.id}' WHERE USER_NAME = '{name[1]}' and SCHOOL_TYPE = '{name[0]}'"
    #             )
    #             db.commit()
    #             print(f'{name[0]} - {name[1]} 디스코드 아이디 업데이트 완료')
    #         except Exception as e:
    #             print(e)


async def setup(client: commands.Bot):
    await client.add_cog(users_cs(client))