from Modules.Module_Basic import *
from Modules.Module_SQL import *
from Utils.sendLog import sendLogging
from Utils.randoms import randomNum
from discord import PermissionOverwrite, CategoryChannel


class teamCreate(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="팀_등록", description="팀원을 등록 하세요")
    @app_commands.describe(team_title="팀명을 입력 해주세요.")
    @app_commands.describe(team_member_list="팀장을 빼고 팀원들만 입력 해주세요.")
    async def teamCreate(self, interaction: Interaction, team_title: str, team_member_list: str):
        members = list()
        membersIds = list()
        _users = team_member_list.split()

        if len(_users) != 3:
            await sendLogging(self.client, f"팀등록 - 4명의 팀원이 필요 합니다.\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})")
            return await interaction.response.send_message("4명 이상의 팀원이 필요합니다.", ephemeral=True)
    
        for users in _users:
            members.append(self.client.get_user(int(users.replace('<@', '').replace('>', ''))))
        
        for checkUser in members:
            membersIds.append(checkUser.id)
        
        if interaction.user.id in membersIds:
            await sendLogging(self.client, f"팀등록 - 팀장을 제외한 팀원만 작성해 주세요.\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})")
            return await interaction.response.send_message("팀장을 제외한 팀원만 작성해 주세요.", ephemeral=True)
        
        teamId = randomNum()
        members.append(interaction.user)
        result, resultMsg = await insertUserData(teamId=teamId, title=team_title, users=members)
        
        if result == True:
            category: CategoryChannel = interaction.guild.get_channel(1166622198551806042)
            overwrites = {
                interaction.guild.default_role: PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
                interaction.user: PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True)
            }
            for member in members:
                overwrites[member] = PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True)
            
            textChannel = await interaction.guild.create_text_channel(name=team_title, category=category, overwrites=overwrites)
            voiceChannel = await interaction.guild.create_voice_channel(name=team_title, category=category, overwrites=overwrites)
            
            await sendLogging(self.client, f"팀등록 - 정상적으로 완료 하였습니다.\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})\n채팅채널 : <#{textChannel.id}> | 보이스채널 : <#{voiceChannel.id}>")
            await interaction.response.send_message(resultMsg, ephemeral=True)
        else:
            await sendLogging(self.client, f"팀등록 - ERROR\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})\n ERROR : {resultMsg}")
            await interaction.response.send_message("운영팀에게 문의 해주세요.", ephemeral=True)

async def setup(client: commands.Bot):
    await client.add_cog(teamCreate(client))