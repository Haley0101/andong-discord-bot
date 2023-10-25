from Modules.Module_Basic import *
from Modules.Module_SQL import *
from Utils.jsonData import roleJsonData
from Utils.sendLog import sendLogging

class certification_btn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="로그인", style=discord.ButtonStyle.green, custom_id="ok_btn")
    async def certification_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        class modal(ui.Modal, title="아래의 항목에 정보를 작성해주세요."):
            user_SchoolType = ui.TextInput(
                label="학과명",
                style=discord.TextStyle.short,
                placeholder="예시) 컴퓨터공학과",
                default="",
                required=True,
                max_length=10,
            )
            user_ClassNum = ui.TextInput(
                label="학번",
                style=discord.TextStyle.short,
                placeholder="예시) 20230101",
                default="",
                required=True,
                max_length=9,
            )
            user_Name = ui.TextInput(
                label="이름",
                style=discord.TextStyle.short,
                placeholder="예시) 박세찬",
                default="",
                required=True,
                max_length=9,
            )

            async def on_submit(self, interaction: Interaction) -> None:
                db, SQL = get_SQL()
                if db is False:
                    return await interaction.response.send_message(
                        f"서버와의 연결이 불안정 합니다.", ephemeral=True
                    )

                try:
                    SQL.execute(
                        f"SELECT * FROM USER_DATA WHERE CLASS_NUM = '{str(self.user_ClassNum)}' and USER_NAME = '{str(self.user_Name)}' and SCHOOL_TYPE = '{str(self.user_SchoolType)}'"
                    )
                    ResultData = SQL.fetchone()
                    if ResultData == None or ResultData == False:
                        await sendLogging(interaction.client, "ERROR - `users_joinMember.py` 서버에서 사용자가 조회 되지 않음")
                        return await interaction.response.send_message(f"서버에서 사용자가 조회되지 않습니다.", ephemeral=True)
                    
                    updateDiscordIdResult = await updateDiscordId(
                        discordId=interaction.user.id,
                        classNum=str(self.user_ClassNum),
                        userName=str(self.user_Name),
                        schoolType=str(self.user_SchoolType),
                    )
                    if updateDiscordIdResult != True:
                        await sendLogging(interaction.client, "ERROR - `users_joinMember.py` 디스코드 아이디 업데이트 되지 않음")
                        return await interaction.response.send_message(f"디스코드 계정에 이상이 있습니다. <@833277196947947531>에게 문의 해주세요!", ephemeral=True)

                    if str(self.user_ClassNum) == "7966":
                        await interaction.user.add_roles(interaction.guild.get_role((1143519495550410872)))  
                        await interaction.user.edit(
                            nick=f"{self.user_SchoolType}_{self.user_Name}교수"
                        )
                        await interaction.response.send_message(
                            f"안녕하세요. {interaction.user.mention}!! \n{self.user_SchoolType} {self.user_Name} 교수님!!",
                            ephemeral=True,
                        )
                        await interaction.client.get_channel(1166636388070989874).send(
                            f"Log - {self.user_SchoolType} | {self.user_Name}({self.user_ClassNum}) 인증 완료 되었습니다."
                        )


                    try:
                        await interaction.user.add_roles(interaction.guild.get_role((int(roleJsonData["학생"]))))
                    except Exception as e:
                        print(e)
                        await sendLogging(interaction.client, f"ERROR - {e}")
                        pass
                    
                    await interaction.user.edit(
                        nick=f"{self.user_SchoolType}_{self.user_Name}"
                    )
                    await interaction.response.send_message(
                        f"안녕하세요. {interaction.user.mention}!! \n{self.user_SchoolType} / {self.user_ClassNum} / {self.user_Name}님!!",
                        ephemeral=True,
                    )
                    await interaction.client.get_channel(1166636388070989874).send(
                        f"Log - {self.user_SchoolType} | {self.user_Name}({self.user_ClassNum}) 인증 완료 되었습니다."
                    )

                except Exception as e:
                    print("error", e)
                    await interaction.response.send_message(
                        f"서버에서 사용자가 조회되지 않습니다.", ephemeral=True
                    )

        await interaction.response.send_modal(modal())


class users_joinMember(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    def get_btn(self):
        return certification_btn()

    @app_commands.command(name="로그인버튼_생성", description="로그인 버튼을 생성 합니다.")
    async def JoinMember_System(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("운영팀이 아닙니다.", ephemeral=True)
        view = certification_btn()
        _channel = self.client.get_channel(1166632566242152468)
        await interaction.response.send_message(f"정상적으로 생성 되었습니다.", ephemeral=True)
        await _channel.send(
            "# 아래의 버튼을 눌러 참가자 등록을 완료 해주세요! \n### 학교명, 학번, 이름을 입력해 역할을 받으세요!", view=view
        )


async def setup(client: commands.Bot):
    await client.add_cog(users_joinMember(client))
