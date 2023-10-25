from Modules.Module_Basic import *
import sqlite3

def get_SQL():
    try:
        db = sqlite3.connect("./data/Haley.db")
        SQL = db.cursor()
        return db, SQL
    except:
        return False, False


async def updateDiscordId(discordId, classNum, userName, schoolType):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(
            f"UPDATE USER_DATA SET DISCORD_ID = '{discordId}' WHERE CLASS_NUM = '{str(classNum)}' and USER_NAME = '{str(userName)}' and SCHOOL_TYPE = '{str(schoolType)}'"
        )
        db.commit()
        return True
    except:
        return False


async def insertTeamBuildBoardId(threadId, title, userId, tagName):
    db, SQL = get_SQL()
    if db == False:
        return False, "DB 연결 에러"
    try:
        SQL.execute(
            f"INSERT INTO TEAM_BUILD_LIST(threadId, title, leaderUid, tag) VALUES({threadId}, '{title}', {userId}, '{tagName}')"
        )
        db.commit()
        return True, "정상적으로 완료 되었음"
    except Exception as e:
        return False, f"{e}"


def get_classNum(discordId):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT CLASS_NUM FROM USER_DATA WHERE DISCORD_ID = '{discordId}'")
        result = SQL.fetchone()[0]
        if result == None:
            return False
        else:
            return result
    except:
        return False


def get_schoolType(discordId):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT SCHOOL_TYPE FROM USER_DATA WHERE DISCORD_ID = '{discordId}'")
        result = SQL.fetchone()[0]
        if result == None:
            return False
        else:
            return result
    except:
        return False


def get_userName(discordId):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT USER_NAME FROM USER_DATA WHERE DISCORD_ID = '{discordId}'")
        result = SQL.fetchone()[0]
        if result == None:
            return False
        else:
            return result
    except:
        return False


def get_userInfo(discordId):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT * FROM USER_DATA WHERE DISCORD_ID = '{discordId}'")
        result = SQL.fetchone()[0]
        if result == None:
            return {
                "userName": result[1],
                "classNum": result[2],
                "schoolType": result[3]
            }
        else:
            return result
    except:
        return False


# def get_teamId(discordId):
#     db, SQL = get_SQL()
#     if db == False:
#         return False
#     try:
#         SQL.execute(f"SELECT TEAM_ID FROM USER_DATA WHERE DISCORD_ID = '{discordId}'")
#         result = SQL.fetchone()[0]
#         if result == None:
#             return False
#         else:
#             return result
#     except:
#         return False


def get_teamName(teamId):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT teamTitle FROM TEAM_DATA WHERE teamId = '{teamId}'")
        result = SQL.fetchone()[0]
        if result == None:
            return False
        else:
            return result
    except:
        return False


def get_teamLeaderName(teamId):
    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT teamLeader FROM TEAM_DATA WHERE teamId = '{teamId}'")
        result = SQL.fetchone()[0]
        if result == None:
            return False
        else:
            return result
    except:
        return False


def converter_discordId(text):
    _ = text.replace("_", ",").replace("(", ",").replace(")", "")
    changeText = _.split(',')

    db, SQL = get_SQL()
    if db == False:
        return False
    try:
        SQL.execute(f"SELECT DISCORD_ID FROM USER_DATA WHERE USER_NAME = '{changeText[1]}' and CLASS_NUM = '{changeText[2]}'")
        result = SQL.fetchone()[0]
        if result == None:
            return False
        else:
            return result
    except:
        return False



async def insertUserData(teamId, title, users):
    db, SQL = get_SQL()
    if db == False:
        return False, "서버와의 통신이 불안정 합니다."

    # if len(users) == 3:
    try:
        SQL.execute(
            f"INSERT INTO TEAM_DATA(teamId, teamTitle, teamLeader, teamMember1, teamMember2, teamMember3) VALUES('{teamId}', '{title}', '{get_schoolType(users[0].id)}_{get_userName(users[0].id)}({get_classNum(users[0].id)})', '{get_schoolType(users[1].id)}_{get_userName(users[1].id)}({get_classNum(users[1].id)})', '{get_schoolType(users[2].id)}_{get_userName(users[2].id)}({get_classNum(users[2].id)})', '{get_schoolType(users[3].id)}_{get_userName(users[3].id)}({get_classNum(users[3].id)})')"
        )
        db.commit()
        return True, f"## 팀원이 정상적으로 등록 되었습니다. \n- 팀명 : {title} \n- 팀장 : {get_userName(users[0].id)} \n- 팀원1 : {get_userName(users[1].id)}\n- 팀원2 : {get_userName(users[2].id)}\n- 팀원3 : {get_userName(users[3].id)}"

    except Exception as e:
        print(e)
        return False, str(e)
    # else:
    #     return False, f"팀원 수가 맞지 않습니다. 4명으로 맞춰주세요."


# async def updateUserDataTeamID(teamId, users):
#     db, SQL = get_SQL()
#     if db == False:
#         return "서버와의 통신이 불안정 합니다."
    
#     try:
#         for i in range(len(users)):
#             SQL.execute(f"UPDATE USER_DATA SET TEAM_ID = '{teamId}' WHERE CLASS_NUM = '{get_classNum(users[i].id)}' and USER_NAME = '{get_userName(users[i].id)}' and SCHOOL_NAME = '{get_schoolType(users[i].id)}'")
        
#         # SQL.execute(f"UPDATE USER_DATA SET TEAM_ID = '{teamId}' WHERE CLASS_NUM = '{get_classNum(leaderUser.id)}' and USER_NAME = '{get_userName(leaderUser.id)}' and SCHOOL_NAME = '{get_schoolName(leaderUser.id)}'")
#         db.commit()
#         return True
#     except Exception as e:
#         print(e)
#         return str(e)

async def adminCoin(type, value, teamId):
    db, SQL = get_SQL()
    if db == False:
        return False, "연결이 불안정함"
    
    if type == 1 or type == "add":
        try:
            SQL.execute(f"UPDATE TEAM_DATA SET coin = coin + {value} WHERE teamId = '{teamId}'")
            db.commit()
            return True, "정상적으로 완료 되었습니다."
        except Exception as e:
            return False, str(e)

    elif type == 2 or type == "remove":
        try:
            SQL.execute(f"UPDATE TEAM_DATA SET coin = coin - {value} WHERE teamId = '{teamId}'")
            db.commit()
            return True, "정상적으로 완료 되었습니다."
        except Exception as e:
            return False, str(e)

    elif type == 3 or type == "set":
        try:
            SQL.execute(f"UPDATE TEAM_DATA SET coin = {value} WHERE teamId = '{teamId}'")
            db.commit()
            return True, "정상적으로 완료 되었습니다."
        except Exception as e:
            return False, str(e)

    else:
        return False


def checkUserSchoolNames(userDatas):
    # 검색해야 할 school_user_class_data에서 각 school의 개수 확인 후 1보다 크면 is_valid False 설정 
    is_valid = True

    # List comprehension to get all schools from userDatas
    schools = [data['school'] for data in userDatas]

    # If the number of unique schools is less than the total number of schools,
    # it means there are duplicates and set is_valid to False.
    if len(set(schools)) < len(schools):
        is_valid = False

    return is_valid

''' BackUp
def checkUserSchoolNames(userDatas):
    is_valid = True
    db, SQL = get_SQL()
    school_user_class_data = userDatas
    
    if db == False:
        return False

    # 필요한 학교 이름들 및 해당하는 유저와 클래스 정보의 리스트
    school_user_class_data = userDatas
    
    # SCHOOL_NAME으로 GROUP BY 쿼리를 실행하여 각 학교명의 개수를 얻음
    SQL.execute("SELECT SCHOOL_NAME, COUNT(*) FROM USER_DATA GROUP BY SCHOOL_NAME")
    rows = SQL.fetchall()
    print(rows)

    # school_counts 딕셔너리에 각 학교명과 그 개수 저장
    school_counts = {row[0]: row[1] for row in rows}

    # 검색해야 할 school_user_class_data에서 각 school의 개수 확인 후 1보다 크면 is_valid False 설정 
    is_valid = True

    for data in school_user_class_data:
        if data['school'] in school_counts and school_counts[data['school']] > 1:
            is_valid = False
            break
    
    # 연결 종료
    db.close()

    return is_valid
'''

async def checkTeamType(teamType):
    db, SQL = get_SQL()
    if db == False:
        return False
    
    # Game Check
    if teamType == 'game' or teamType == '게임':
        SQL.execute(f"SELECT COUNT(*) FROM TEAM_DATA WHERE teamType = '게임'")
        game_count = SQL.fetchone()[0]
        # if game_count != 4:
        #     return True, f"{game_count}개로 게임 분과 지원 가능합니다."
        # else:
        #     return False, f"{game_count}개로 게임 분과 지원 **불가**합니다."
    
    # IOT Check
    elif teamType == 'iot' or teamType == 'IOT':
        SQL.execute(f"SELECT COUNT(*) FROM TEAM_DATA WHERE teamType = 'IOT'")
        iot_count = SQL.fetchone()[0]
        # if iot_count != 4:
        #     return True, f"{iot_count}개로 IOT 분과 지원 가능합니다."
        # else:
        #     return False, f"{iot_count}개로 IOT 분과 지원 **불가**합니다."
        
    # Web/App Check
    elif teamType == 'webapp' or teamType == '웹/앱':
        SQL.execute(f"SELECT COUNT(*) FROM TEAM_DATA WHERE teamType = '웹/앱'")
        web_app_count = SQL.fetchone()[0]
        # if web_app_count != 14:
        #     return True, f"{web_app_count}개로 웹/앱 분과 지원 가능합니다."
        # else:
        #     return False, f"{web_app_count}개로 웹/앱 분과 지원 **불가**합니다."
    
    else:
        return False