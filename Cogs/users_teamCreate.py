from Modules.Module_Basic import *
from Modules.Module_SQL import *
from Utils.sendLog import sendLogging
from Utils.randoms import randomNum
from Utils.duplicates import check_multiple_duplicates
from discord import PermissionOverwrite, CategoryChannel


class teamCreate(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="팀_등록", description="팀원을 등록 하세요")
    @app_commands.describe(team_title="팀명을 입력 해주세요.")
    @app_commands.describe(team_member_list="팀장을 빼고 팀원들만 입력 해주세요.")
    async def teamCreate(self, interaction: Interaction, team_title: str, team_member_list: str):
        members = list()
        membersDiscordIds = list()
        _users = team_member_list.split()

        if len(_users) != 3:
            await sendLogging(self.client, f"팀등록 오류 - 4명의 팀원이 필요 합니다.\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})")
            return await interaction.response.send_message("4명 이상의 팀원이 필요합니다.", ephemeral=True)
    
        for users in _users:
            members.append(self.client.get_user(int(users.replace('<@', '').replace('>', ''))))
        
        for checkUser in members:
            membersDiscordIds.append(checkUser.id)
        
        if interaction.user.id in membersDiscordIds:
            await sendLogging(self.client, f"팀등록 오류 - 팀장을 제외한 팀원만 작성해 주세요.\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})")
            return await interaction.response.send_message("팀장을 제외한 팀원만 작성해 주세요.", ephemeral=True)

        teamId = randomNum()
        members.insert(0, interaction.user)
        membersDiscordIds.insert(0, interaction.user.id)

        schoolTypeList = [get_schoolType(membersDiscordIds[0]), get_schoolType(membersDiscordIds[1]), get_schoolType(membersDiscordIds[2]), get_schoolType(membersDiscordIds[3])]
        checkMultipleDuplicatesResult = check_multiple_duplicates(schoolTypeList)
        if checkMultipleDuplicatesResult == False:
            await sendLogging(self.client, f"팀등록 오류 - 같은학과가 2명 이상 중복 됨\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id}) \n학과 리스트: {schoolTypeList}")
            return await interaction.response.send_message("같은학과가 2명 이상 중복 되었습니다. 팀을 다시 구성해주세요.", ephemeral=True)

        result, resultMsg = await insertUserData(teamId=teamId, title=team_title, users=members)
        
        if result == True:
            category: CategoryChannel = interaction.guild.get_channel(1166622198551806042)
            
            overwrites = {
                interaction.guild.default_role: PermissionOverwrite(read_messages=False, view_channel=False, send_messages=False),
                interaction.user: PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True),
                members[1]: PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True),
                members[2]: PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True),
                members[3]: PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True),
            }
            
            textChannel = await interaction.guild.create_text_channel(name=team_title, category=category, overwrites=overwrites)
            voiceChannel = await interaction.guild.create_voice_channel(name=team_title, category=category, overwrites=overwrites)
            
            tags = interaction.guild.get_channel(1167745355807473725).available_tags
            applied_tags = list(filter(lambda tag : tag.name == "완료", tags))
            await interaction.channel.edit(locked=True, applied_tags=applied_tags)
            await sendLogging(self.client, f"팀등록 - 정상적으로 완료 하였습니다.\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})\n채팅채널 : <#{textChannel.id}> | 보이스채널 : <#{voiceChannel.id}>")
            await interaction.response.send_message(resultMsg, ephemeral=True)
        else:
            await sendLogging(self.client, f"팀등록 - ERROR\n팀명: {team_title} | 사용자 : {interaction.user.mention}({interaction.user.id})\n ERROR : {resultMsg}")
            await interaction.response.send_message("운영팀에게 문의 해주세요.", ephemeral=True)

async def setup(client: commands.Bot):
    await client.add_cog(teamCreate(client))