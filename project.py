from flask import Flask, render_template, redirect, request
import os.path, json, sqlite3, random, csv
import itertools


def inters(t1, t2):
    for i in t1:
        for j in t2:
            if i[0] == j[0]:
                if int(i[1]) < int(j[1]) < int(i[2]) or int(j[1]) < int(i[2]) < int(j[2]) or int(j[1]) < int(i[1]) < int(j[2]) or int(j[1]) < int(i[2]) < int(j[2]) or (j[1] == i[1] and j[2] == i[2]):
                    return True
    return False

def clash():
    con = sqlite3.connect("database/School.db")
    for teach in con.execute("SELECT ID FROM Teacher"):
        courses = [i[0] for i in con.execute(f"SELECT CourseID FROM TeacherCourse WHERE TeacherID = '{teach[0]}'")]
        if len(courses) <= 1:
            continue
        for i in itertools.combinations(courses, 2):
            ses1 = con.execute(f"SELECT Day, StartTime, EndTime FROM CourseSession WHERE CourseID = {i[0]}")
            ses2 = con.execute(f"SELECT Day, StartTime, EndTime FROM CourseSession WHERE CourseID = {i[1]}")
            if inters(ses1, ses2):
                print(teach[0], list(con.execute(f"SELECT Name FROM Teacher WHERE ID = '{teach[0]}'"))[0][0], i[0], list(con.execute(f"SELECT Name FROM Course WHERE ID = '{i[0]}'"))[0][0], i[1], list(con.execute(f"SELECT Name FROM Course WHERE ID = '{i[1]}'"))[0][0])

# j = {
#     "en":["1EN2", "1KI2", "1el2A", "1en2A1", "1en2A3", "1en2B1", "1en2B3", "1gp1A01", "1gp1A02", "1gp1A03", "1gp1A04", "1gp1A05", "1gp1A06", "1gp1A07", "1gp1B08", "1gp1B09", "1gp1B10", "1gp1B11", "1gp1B12", "1gp1B13", "1gp1B14", "1gp1C15", "1gp1C16", "1gp1C17", "1gp1C18", "1gp1C19", "1gp1C20", "1ki2A"],
#     "ar":["1ar2A", "1mu2A"],
#     "ec":["1ec1H", "1ec1I", "1ec1J", "1ec1K", "1ec2A", "1ec2B", "1ec2E", "1ec2F", "1ec2G", "1ec2L", "1ec2M", "1ec2N", "1ec2O", "1ec2P", "1ec2Q", "1ec2R", "1ec2S", "1ec2T"],
#     "hm":["1GE2", "1HI2", "1ge2A", "1ge2B1", "1ge2B2", "1hi2A", "1hi2B"],
#     "mt":["1cl(B)", "1cl1A1", "1cl1A2", "1cl1B1", "1cl1B2", "1cl1C1", "1cl1C2", "1cn2A", "1hl1A", "1ml(B)", "1ml1A", "1mn2A", "1tl1A", "1tn2A"],
#     "ma":["1MA2", "1fm2A", "1ma1A", "1ma1B", "1ma2A", "1ma2C", "1ma2D", "1ma2G", "1ma2H", "1ma2I", "1ma2J", "1ma2K", "1ma2L", "1ma2M", "1ma2N", "1ma2O", "1ma2Q", "1ma2V", "1ma2W", "1ma2X", "1ma2Y", "1ma2Z"],
#     "pe":["1peA1", "1peA2", "1peB1", "1peB2", "1peC1", "1peC2", "1peD1", "1peD2", "1peE1", "1peE2", "1peF1", "1peF2", "1peG1", "1peG2", "1peH1", "1peH2", "1peI1", "1peI2", "1peJ1", "1peJ2", "1peK1", "1peK2", "1peL1", "1peL2", "1peM1", "1peM2", "1peN1", "1peN2", "1peO1", "1peO2", "1peP1", "1peP2", "1peQ1", "1peQ2", "1peR1", "1peR2", "1peS1", "1peS2", "1peT1", "1peT2"],
#     "pw":["1pw1A01", "1pw1A02", "1pw1A03", "1pw1A04", "1pw1A05", "1pw1A06", "1pw1A07", "1pw1B01", "1pw1B02", "1pw1B03", "1pw1B04", "1pw1B05", "1pw1B06", "1pw1B07", "1pw1B08", "1pw1C01", "1pw1C02", "1pw1C03", "1pw1C04", "1pw1C05", "1pw1C06", "1pw1C07"],
#     "bi":["1BI2", "1bi2A", "1bi2A(P)", "1bi2H", "1bi2H(P)", "1bi2I", "1bi2I(P)", "1bi2L", "1bi2L(P)", "1bi2M", "1bi2M(P)", "1bi2N", "1bi2N(P)"],
#     "cm":["1CM2", "1cm1A", "1cm2C", "1cm2C(P)", "1cm2D", "1cm2D(P)", "1cm2E", "1cm2E(P)", "1cm2H", "1cm2H(P)", "1cm2I", "1cm2I(P)", "1cm2J", "1cm2J(P)", "1cm2K", "1cm2K(P)", "1cm2L", "1cm2L(P)", "1cm2M", "1cm2M(P)", "1cm2N", "1cm2N(P)", "1cm2O", "1cm2O(P)", "1cm2P", "1cm2P(P)", "1cm2Q", "1cm2Q(P)", "1cm2R", "1cm2R(P)", "1cm2S", "1cm2S(P)", "1cm2T", "1cm2T(P)"],
#     "ph":["1PH2", "1ph2C", "1ph2C(P)", "1ph2F", "1ph2F(P)", "1ph2G", "1ph2G(P)", "1ph2J", "1ph2J(P)", "1ph2K(P)", "1ph2K1", "1ph2K2", "1ph2O", "1ph2O(P)", "1ph2P", "1ph2P(P)", "1ph2Q", "1ph2Q(P)", "1ph2R", "1ph2R(P)", "1ph2S(P)", "1ph2S1", "1ph2S2", "1ph2T", "1ph2T(P)"]
# }
# lsd = {'en': ['Andrew S/O Andeny', 'Er Yinghui Junice', 'Lin Li Josephine', 'Wan Wai Sum', 'Narayanan Rakunathan', 'Oh Jia Lin Karen', 'Meena Malinder Kaur', 'Joel Poh Weinan', 'Low Jeng Wye', 'Chia Han Chin Desmond', 'Wong Hsien Ming David', 'Ng Siang Nan Carmen', 'Soh Huiqing Sylvia'], 'ar': ['Teo Chor Howe', 'Eng Wei Ping Michelle'], 'ec': ['Mun Lynn', 'Foo Li Min Stephanie', 'Lee Ching Ching Christine', 'Tan Lee Hui', 'Lim Zong Liang', 'Yew Shinn How Daniel', 'Lim Lai Har Karen', 'Pauline Yeong Pao Lian', 'Gao Peirong Jessica', 'Low Wei Jie Donavan'], 'hm': ['Ang Li-Jin Wendy', 'Tan Wei Ren Bryan', 'Cher Caifeng Valerie'], 'mt': ['Zhang Jianping', 'Teo Chwee Hock', 'Lin Huaizu', 'Woon Yoke Fun', 'Zhang Jianli', 'Artina Selamat', 'Iryianna Binte Ahmad'], 'ma': ['Pok Wern Jian', 'Chew Joo Oon', 'Chan Yoon Teng', 'Chong Hur Ling Marcus', 'Fong Chee Hoe', 'Feng Pingping', 'Kwek Yuan Chia', 'Wong Yew Chong', 'Lee Jian Hao Jason', 'Liew Yew Tze'], 'pe': ['Tan Joe-sie', 'Taranpal Singh', 'Sng Yeow Boon Henry', 'Yeo Shengqiang Jeremy', 'Ong Ming Ann', 'Yong Man Yun', 'Shanmugadas S/O Kumaresadas', 'Neo Ko Hui', 'Ang Xing Tai Shaun', 'Lim Lee Huang Winnie'], 'pw': ['Wang Shiliang', 'Ng Kian Tiong', 'Linda Faustina', 'Chuah Lay Yen', 'Chiang Cher Siang', 'Senthil Kumaran S/O Kunasegaran', 'Hue Hoe Ping', 'Ng Chinn Min Veronica'], 'scs': ['Lim Eng Soon', 'Ang Si Ling Sheryl', 'Yeo Chin Theng', 'Lim Wei Li', 'Chng Chwee Ying', 'Tan Peng Hui Samuel', 'Goh Nai Lee Mark', 'Lim Kim Hock', 'Ng Yee Lee', 'Darshini D/O Radha Krishnan', 'Tan Soon Heng Simon', 'Tan Chin Hui', 'Chua Manping', 'Nyam Ching Wee', 'Lim Hwee Ke', 'Hon Tin Seng', 'Ng Joon Hong']}
# lsd["bi"] = ['Chua Manping', 'Ang Si Ling Sheryl', 'Ng Yee Lee']
# lsd["cm"] = ['Yap Teck Sheng Terence', 'Nyam Ching Wee', 'Lim Hwee Ke', 'Ng Joon Hong', 'Yeo Chin Theng', 'Lim Wei Li', 'Lim Kim Hock', 'Darshini D/O Radha Krishnan']
# lsd["ph"] = ['Tan Chin Hui', 'Chng Chwee Ying', 'Tan Peng Hui Samuel', 'Tan Soon Heng Simon', 'Hon Tin Seng']

# con = sqlite3.connect("database/School.db")
# cd = {i:j for (j, i) in con.execute("SELECT * FROM Course")}
# csd = {i[0]:[] for i in con.execute("SELECT ID FROM Course")}
# for i in con.execute("SELECT * FROM CourseSession"):
#     csd[i[0]].append(i[1:])
# td = {i:j for (j, i) in con.execute("SELECT ID, Name FROM Teacher")}
# cont = True
# with con:
#     while True:
#         assign = {i:[] for i in lsd['bi']}
#         for course in j['bi']:
#             if course in ("1BI2",):
#                 if cont:
#                     for teach in lsd["bi"]:
#                         # print(teach, course, td[teach], cd[course])
#                         con.execute(f"INSERT INTO TeacherCourse VALUES ('{td[teach]}', {cd[course]})")
#             elif "(P)" in course:
#                 pass
#             else:
#                 counts = {teach: len(assign[teach]) for teach in lsd['bi']}
#                 kkk = []
#                 for teach in lsd['bi']:
#                     if counts[teach] == min([len(assign[teach]) for teach in lsd['bi']]):
#                         kkk.append(teach)
#                 tchoi = random.choice(kkk)
#                 assign[tchoi].append(course)
#                 if course in ("1ph2K1", "1ph2S1"):
#                     assign[tchoi].append(course[:-1] + "(P)")
#                 elif "1bi2" in course and course[-1] != "2":
#                     assign[tchoi].append(course + "(P)")
#         cont = False
#         leave = False
#         for courses in assign.values():
#             if leave:
#                 break
#             for subset in itertools.combinations(courses, 2):
#                 if inters(csd[cd[subset[0]]], csd[cd[subset[1]]]):
#                     leave = True
#                     break
#         if not leave:
#             break
#     print(assign)
#     for teach in assign.keys():
#         for course in assign[teach]:
#             try:
#                 con.execute(f"INSERT INTO TeacherCourse VALUES ('{td[teach]}', {cd[course]})")
#             except sqlite3.IntegrityError as e:
#                 print(teach, course, td[teach], cd[course])
#                 raise e


auth, resp = 2, 0 #CHANGE BACK TO 0

def add_t(a,b):
    return (a//100+b//60)*100+(a%100+b%60)//60*100+(a%100+b%60)%60

def gen_ic(sg, year):
    tot = 0
    if sg:
        if year < 2000:
            ic = "S" + str(year)[-2:] if year >= 1968 else "S" + str(random.randint(0,1))
        else:
            ic = "T" + str(year)[-2:]
            tot += 4
        check = ["J", "Z", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
    else:
        if year < 2000:
            ic = "F"
        else:
            ic = "G"
            tot += 4
        check = ["X", "W", "U", "T", "R", "Q", "P", "N", "M", "L", "K"]
    for i in range(8 - len(ic)):
        ic += str(random.randint(0,9))
    tot += int(ic[1])*2 + int(ic[2])*7 + int(ic[3])*6 + int(ic[4])*5 + int(ic[5])*4 + int(ic[6])*3 + int(ic[7])*2
    ic += check[tot % 11]
    return ic

def read_data(*cmds, db="School"):
    if cmds[0] is None:
        return ""
    if db.upper() not in ("SCHOOL", "ACCOUNT") or (db.upper() == "ACCOUNT" and auth < 2):
        return f"<h2>Unable to Access Database: {db}</h2>"
    db = db.title()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, f"database/{db}.db")
    try:
        conn = sqlite3.connect(db_path)
        if len(cmds) == 1:
            return list(conn.execute(cmds[0]))
        return [list(conn.execute(cmd)) for cmd in cmds]
    except sqlite3.OperationalError as e:
        return f"<h2>sqlite3.OperationalError: {e}</h2>"
    finally:
        conn.close()

def update_data(*cmds, db="School"):
    if cmds[0] is None:
        return ""
    if db.upper() not in ("SCHOOL", "ACCOUNT") or (db.upper() == "SCHOOL" and auth == 0) or (db.upper() == "ACCOUNT" and auth < 2):
        return f"<h2>Unable to Access Database: {db}</h2>"
    for cmd in cmds:
        if any(i in cmd.upper() for i in ("CREATE", "DROP", "ALTER", "RENAME", "GRANT", "REVOKE")):
            return f"<h2>Unauthorised Command</h2>"
    db = db.title()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, f"database/{db}.db")
    try:
        conn = sqlite3.connect(db_path)
        if len(cmds) == 1:
            conn.execute(cmds[0])
        else:
            for cmd in cmds:
                conn.execute(cmd)
        conn.commit()
        return "<h2>Command Executed</h2>"
    except sqlite3.OperationalError as e:
        return f"<h2>sqlite3.OperationalError: {e}</h2>"
    finally:
        conn.close()

def restore(db):
    if db.upper() == "ACCOUNT":
        with open("database/Account.db", "wb") as f:
            with open("database/Account_backup.db", "rb") as g:
                f.write(g.read())
    elif db.upper() == "SCHOOL":
        with open("database/School.db", "wb") as f:
            with open("database/School_backup.db", "rb") as g:
                f.write(g.read())

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=["GET", "POST"])
def root():
    global resp
    resp = 0
    data_accs = None
    if auth == 2:
        data_accs = read_data("SELECT * FROM Account", db="Account")
    return render_template("user.html", data=read_data("SELECT Name FROM Student", "SELECT Name FROM Teacher", "SELECT Name FROM Class", "SELECT Name FROM Course", "SELECT Name FROM CCA"), data_accs=data_accs, auth=auth)

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", resp=resp)

@app.route("/loginprocess", methods=["GET", "POST"])
def login_process():
    global auth, resp
    if request.form["username"] == request.form["password"] == "":
        resp = 4
        return redirect("/login")
    if request.form["username"] == "":
        resp = 2
        return redirect("/login")
    if request.form["password"] == "":
        resp = 3
        return redirect("/login")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database/Account.db")
    conn = sqlite3.connect(db_path)
    cur = list(conn.execute("SELECT Level FROM Account WHERE Username = ? AND Password = ?", (request.form["username"], request.form["password"])))
    conn.close()
    if cur == []:
        resp = 1
        return redirect("/login")
    auth = cur[0][0]
    resp = 0
    return redirect("/")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    global auth
    auth = 0
    return redirect("/")

@app.route("/getdata", methods=['GET','POST'])
def get_data():
    db = "School" if not request.args.get("db") else request.args.get("db")
    cmd = request.args.get("cmd")
    if request.method == "GET":
        data = read_data(cmd, db=db)
        if isinstance(data, str):
            return data
        return json.dumps([i for i in data] if data != [] and not isinstance(data, str) else data)

@app.route("/postdata", methods=['GET','POST'])
def post_data():
    db = "School" if not request.args.get("db") else request.args.get("db")
    cmd = request.args.get("cmd")
    resp = update_data(cmd, db=db)
    return resp

@app.route("/backup", methods=['GET','POST'])
def backup():
    db = "School" if not request.args.get("db") else request.args.get("db")
    restore(db)
    return redirect("/")

@app.route("/availability", methods=['GET', 'POST'])
def availability():
    times = {
        "Monday": [i for i in range(800, 1900, 10) if i % 100 < 60],
        "Tuesday": [i for i in range(800, 1900, 10) if i % 100 < 60],
        "Wednesday": [i for i in range(800, 1900, 10) if i % 100 < 60],
        "Thursday": [i for i in range(800, 1900, 10) if i % 100 < 60],
        "Friday": [i for i in range(800, 1900, 10) if i % 100 < 60]
    }
    time_intervals = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
    st = "('" + "', '".join(request.form.getlist('st')) + "')"
    tc = "('" + "', '".join(request.form.getlist('tc')) + "')"

    bad_times = read_data("SELECT Day, StartTime, EndTime FROM CourseSession " +\
                         "WHERE CourseID IN (SELECT CourseID FROM StudentCourse " +\
                         f"WHERE StudentID IN {st}) " +\
                         "UNION SELECT Day, StartTime, EndTime FROM CCASession " +\
                         "WHERE CCAID IN (SELECT CCAID FROM StudentCCA " +\
                         f"WHERE StudentID IN {st}) " +\
                         "UNION SELECT Day, StartTime, EndTime FROM CourseSession " +\
                         "WHERE CourseID IN (SELECT CourseID FROM TeacherCourse " +\
                         f"WHERE TeacherID IN {tc})")
    if len(bad_times) == 0:
        return redirect("/")
    for i in list(set(bad_times)):
        for j in sorted(times[i[0]]):
            if int(i[1]) <= j < int(i[2]):
                times[i[0]].remove(j)
            elif j >= int(i[2]):
                break
    for i in times.keys():
        for j in times[i]:
            if len(time_intervals[i]) > 0 and j == time_intervals[i][-1][1]:
              time_intervals[i][-1][1] = j + (j % 100 == 50)*40 + 10
            else:
              time_intervals[i].append([j, j + (j % 100 == 50)*40 + 10])
    times = []
    for i in time_intervals.keys():
        for j in time_intervals[i]:
            times.append([i, "0"*(j[0]<1000) + str(j[0]) + " - " + "0"*(j[1]<1000) + str(j[1])])
    return render_template("search.html", times = times)
      
if __name__ == "__main__":
    app.run()