import sqlite3
from flask import *

app = Flask(__name__)

def get_SQL():
    try:
        db = sqlite3.connect("./data/Haley.db")
        SQL = db.cursor()
        return db, SQL
    except:
        return False, False

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
        SQL.execute("SELECT teamId, teamTitle, teamLeader, teamMember1, teamMember2, teamMember3 FROM TEAM_DATA ORDER BY teamTitle")
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
    

app.run(host='0.0.0.0', port=1220)