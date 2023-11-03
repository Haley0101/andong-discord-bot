import sqlite3
from flask import *
from flask_restx import Api, Resource, reqparse, fields

app = Flask(__name__)

api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

def get_SQL():
    try:
        db = sqlite3.connect("./data/Haley.db")
        SQL = db.cursor()
        return db, SQL
    except:
        return False, False


TeamUpdate_API = api.namespace('team', description='팀 아이디로 팀 정보를 수정 할 수 있습니다.')
@TeamUpdate_API.route('/delete/team-id/<int:teamId>')
@TeamUpdate_API.param('teamId', '팀 아이디')
@TeamUpdate_API.response(200, '정상 요청')
@TeamUpdate_API.response(500, '백엔드 Error')
class DeleteTeam(Resource):
    def delete(self, teamId):
        db, SQL = get_SQL()
        if db == False:
            return {"result": False, "msg": "DB CONNECT ERROR"}, 500
        
        try:
            SQL.execute(f"DELETE FROM TEAM_DATA WHERE teamId = '{teamId}'")
            db.commit()
            return {"result": True, "msg": f"{teamId} Delete"}, 200
        
        except Exception as e:
            return {"result": False, "msg": f"ERROR {e}"}, 500


model = TeamUpdate_API.model('Team Info Input', {
    'teamId': fields.String(title='팀 아이디', default='11111', required=True),
    'teamName': fields.String(title='팀 이름', default='코드코리아', required=True),
})

@TeamUpdate_API.route('/edit/team-name')
# @TeamUpdate_API.param('teamId', '팀 아이디')
# @TeamUpdate_API.param('teamName', '수정할 팀 이름')
@TeamUpdate_API.response(200, '정상 요청')
@TeamUpdate_API.response(500, '백엔드 Error')
class UpdateTeamName(Resource):
    @TeamUpdate_API.expect(model, validate=False)
    def post(self):
        body = request.json
        teamId = body['teamId']
        teamName = body['teamName']
        
        db, SQL = get_SQL()
        if db == False:
            return {"result": False, "msg": "DB CONNECT ERROR"}, 500
        
        try:
            SQL.execute(f"UPDATE TEAM_DATA SET teamTitle = '{teamName}' WHERE teamId = '{teamId}'")
            db.commit()
            return {"result": True, "msg": f"{teamId} {teamName} Update"}, 200
        
        except Exception as e:
            return {"result": False, "msg": f"ERROR {e}"}, 500



UserUpdate_API = api.namespace('user', description='유저정보 수정 및 추가가 가능 합니다.')
@UserUpdate_API.route('/edit/discord-id/<int:userId>/<int:classId>')
@UserUpdate_API.param('userId', '디스코드 유저 아이디')
@UserUpdate_API.param('classId', '유저 학번')
@UserUpdate_API.response(200, '정상 요청')
@UserUpdate_API.response(500, '백엔드 Error')
class editDiscordId(Resource):
    def get(self, userId, classId):
        db, SQL = get_SQL()
        if db == False:
            return {"result": False, "msg": "DB CONNECT ERROR"}, 500
        
        try:
            SQL.execute(f"UPDATE USER_DATA SET DISCORD_ID = '{userId}' WHERE CLASS_NUM = '{classId}'")
            db.commit()
            return {"result": True, "msg": f"{classId} is {userId} Update."}, 200
        
        except Exception as e:
            return {"result": False, "msg": f"ERROR {e}"}, 500


@app.route('/sechan/holymoly/dbView/<dbName>')
def dbView(dbName):
    db, SQL = get_SQL()
    if dbName == "user_data" or dbName == "USER_DATA" or dbName == "user-data":
        SQL.execute("SELECT DISCORD_ID, USER_NAME, CLASS_NUM, SCHOOL_TYPE FROM USER_DATA ORDER BY SCHOOL_TYPE, USER_NAME, CLASS_NUM")
        data = SQL.fetchall()  # 실행한 결과 데이터를 꺼냄

        data_list = []

        for obj in data: # 튜플 안의 데이터를 하나씩 조회해서
            data_dic = { # 딕셔너리 형태로
                # 요소들을 하나씩 넣음
                'DISCORD_ID': str(obj[0]),
                'USER_NAME': obj[1],
                'CLASS_NUM': obj[2],
                'SCHOOL_TYPE': obj[3]
            }
            data_list.append(data_dic) # 완성된 딕셔너리를 list에 넣음
        return render_template('db_table.html', dbName=dbName, data_list=data_list)
    
    elif dbName == "team_data" or dbName == "TEAM_DATA" or dbName == "team-data":
        SQL.execute("SELECT teamId, teamTitle, teamLeader, teamMember1, teamMember2, teamMember3 FROM TEAM_DATA ORDER BY teamId")
        data = SQL.fetchall()  # 실행한 결과 데이터를 꺼냄

        data_list = []

        for obj in data: # 튜플 안의 데이터를 하나씩 조회해서
            data_dic = { # 딕셔너리 형태로
                # 요소들을 하나씩 넣음
                'teamId': obj[0],
                'teamTitle': obj[1],
                'teamLeader': obj[2],
                'teamMember1': obj[3],
                'teamMember2': obj[4],
                'teamMember3': obj[5]
            }
            data_list.append(data_dic) # 완성된 딕셔너리를 list에 넣음
        return render_template('db_table.html', dbName=dbName, data_list=data_list)
    
    else:
        return "<h1>Hello?</h1>"
    

app.run(host='0.0.0.0', port=1220, debug=True)