from Modules.Module_Basic import *
# from Modules.Module_API import *
from Modules.Module_SQL import *
from Utils.sendLog import sendLogging

class donation_btn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="도네이션 구매하기", style=discord.ButtonStyle.green, custom_id="ok_btn")
    async def donation_from(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        class modal(ui.Modal, title="아래의 항목에 정보를 작성해주세요."):
            user_Name = ui.TextInput(
                label="도네이션 텍스트",
                style=discord.TextStyle.paragraph,
                placeholder="와 엄청난 도네이션 인데요?",
                default="",
                required=True,
                max_length=50,
            )

            async def on_submit(self, interaction: Interaction) -> None:
                
                await interaction.response.send_message(
                    f"도네이션을 정상적으로 보냈습니다.",
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


    # @app_commands.command(name="도네이션", description="5코인으로 도네이션이 가능 합니다.")
    # async def donationSend(self, interaction: Interaction):
    #     await interaction.response.send_message(f"현재 준비중 입니다.", ephemeral=True)
    #     view = donation_btn()
    #     await interaction.response.send_message(f"아래의 버튼을 눌러 도네이션을 사용해 보세요!", ephemeral=True, view=view)


    # @app_commands.command(name="테스트_보드리스트", description="보드리스트")
    # async def testBoardList(self, interaction: Interaction):
    #     if not interaction.user.guild_permissions.administrator:
    #         await interaction.response.send_message("운영팀이 아닙니다.", ephemeral=True)
    #     print(boardList)
    #     await interaction.response.send_message(f"{boardList}", ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(users_cs(client))