from flask import Flask, render_template, redirect, request
import os.path, json, sqlite3, random
import itertools


auth, resp, update = 0, 0, 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
school_db = os.path.join(BASE_DIR, "database/School.db")
school_copy_db = os.path.join(BASE_DIR, "database/School_copy.db")
school_backup_db = os.path.join(BASE_DIR, "database/School_backup.db")
account_db = os.path.join(BASE_DIR, "database/Account.db")
account_backup_db = os.path.join(BASE_DIR, "database/Account_backup.db")
        
def intersect(t1, t2=None):
    """
    Returns whether two time intervals in (Day, StartTime, EndTime) format of two courses intersect
    """
    if t2 is None:
        for i in itertools.combinations(t1, 2):
            if i[0][0] == i[1][0]:
                if int(i[0][1]) <= int(i[1][1]) < int(i[0][2]) or int(i[1][1]) < int(i[0][2]) <= int(i[1][2]) or int(i[1][1]) <= int(i[0][1]) < int(i[1][2]) or int(i[1][1]) < int(i[0][2]) <= int(i[1][2]) or (i[1][1] == i[0][1] and i[1][2] == i[0][2]):
                    return True
    else:
        for i in itertools.product(t1, t2):
            if i[0][0] == i[1][0]:
                if int(i[0][1]) <= int(i[1][1]) < int(i[0][2]) or int(i[1][1]) < int(i[0][2]) <= int(i[1][2]) or int(i[1][1]) <= int(i[0][1]) < int(i[1][2]) or int(i[1][1]) < int(i[0][2]) <= int(i[1][2]) or (i[1][1] == i[0][1] and i[1][2] == i[0][2]):
                    return True
    return False

def clash():
    """
    Prints out all clashes in schedule for teachers and returns True if clash is found
    """
    clash = False
    conn = sqlite3.connect(school_db)
    for teach in conn.execute("SELECT ID FROM Teacher"):
        courses = [i[0] for i in conn.execute(f"SELECT CourseID FROM TeacherCourse WHERE TeacherID = '{teach[0]}'")]
        if len(courses) == 0:
            continue
        for i in itertools.combinations_with_replacement(courses, 2):
            ses1 = list(conn.execute(f"SELECT Day, StartTime, EndTime FROM CourseSession WHERE CourseID = {i[0]}"))
            ses2 = list(conn.execute(f"SELECT Day, StartTime, EndTime FROM CourseSession WHERE CourseID = {i[1]}"))
            if i[0] == 103 or i[1] == 103:
                print(i, ses1,ses2)
            if (i[0] != i[1] and intersect(ses1, ses2)) or intersect(ses1):
                print(teach[0], i[0], i[1])
                clash = True
    return clash

def read_data(*cmds, db="School"):
    """
    Executes given SQL commands without commiting and returns the results
    *cmds : str
        SQL commands to execute
    db : str
        Database to access (School/Account)
    """
    if cmds[0] is None:
        return ""
    if db.upper() not in ("SCHOOL", "ACCOUNT") or (db.upper() == "ACCOUNT" and auth < 2):
        return f"<h2>Unable to Access Database: {db}</h2>"
    db = db.title()
    try:
        if db.upper() == "SCHOOL":
            conn = sqlite3.connect(school_db)
        else:
            conn = sqlite3.connect(account_db)
        if len(cmds) == 1:
            return list(conn.execute(cmds[0]))
        return [list(conn.execute(cmd)) for cmd in cmds]
    except sqlite3.OperationalError as e:
        return f"<h2>sqlite3.OperationalError: {e}</h2>"
    finally:
        conn.close()

def update_data(*cmds, db="School"):
    """
    Executes and commits given SQL commands
    *cmds : str
        SQL commands to execute
    db : str
        Database to access (School/Account)
    """
    global update
    if cmds[0] is None:
        return ""
    if db.upper() not in ("SCHOOL", "ACCOUNT") or (db.upper() == "SCHOOL" and auth == 0) or (db.upper() == "ACCOUNT" and auth < 2):
        return f"<h2>Unable to Access Database: {db}</h2>"
    for cmd in cmds:
        if any(i in cmd.upper() for i in ("CREATE", "DROP", "ALTER", "RENAME", "GRANT", "REVOKE")):
            return "<h2>Unauthorised Command</h2>"
    with open(school_copy_db, "wb") as f:
        with open(school_db, "rb") as g:
            f.write(g.read())
    try:
        if db.upper() == "SCHOOL":
            conn = sqlite3.connect(school_db)
        else:
            conn = sqlite3.connect(account_db)
        print(cmds)
        if len(cmds) == 1:
            conn.execute(cmds[0])
        else:
            for cmd in cmds:
                conn.execute(cmd)
        conn.commit()
        conn.close()
        if clash():
            print("A")
            update = 0
            with open(school_db, "wb") as f:
                with open(school_copy_db, "rb") as g:
                    f.write(g.read())
            return "<h2>Schedule Error</h2>"
        print("B")
        update = 1
        return "<h2>Command Executed</h2>"
    except sqlite3.OperationalError as e:
        return f"<h2>sqlite3.OperationalError: {e}</h2>"
    except sqlite3.IntegrityError as e:
        return f"<h2>sqlite3.IntegrityError: {e}</h2>"
    finally:
        conn.close()

def gen_ic(sg, year):
    """
    Returns a random NRIC/FIN number not in the School database
    sg : bool
        Whether or not the person is a Singaporean
    year : int
        Year of birth of the person
    """
    while True:
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
        if ic not in map(lambda x: x[0], read_data("SELECT ID FROM Student UNION SELECT ID FROM Teacher")):
            return ic

def restore(db):
    """
    Restores the database to a backup
    db : str
        Name of the database (School/Account)
    """
    if db.upper() == "ACCOUNT":
        with open(account_db, "wb") as f:
            with open(account_backup_db, "rb") as g:
                f.write(g.read())
    elif db.upper() == "SCHOOL":
        with open(school_db, "wb") as f:
            with open(school_backup_db, "rb") as g:
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
    return render_template(
        "user.html",
        data_names=read_data("SELECT Name FROM Student", "SELECT Name FROM Teacher", "SELECT Name FROM Class", "SELECT Name FROM Course", "SELECT Name FROM CCA"),
        data_ids=read_data("SELECT ID FROM Student", "SELECT ID FROM Teacher", "SELECT ID FROM Class", "SELECT ID FROM Course", "SELECT ID FROM CCA"),
        data_times=read_data("SELECT DISTINCT StartTime FROM CourseSession", "SELECT DISTINCT EndTime FROM CourseSession", "SELECT DISTINCT StartTime FROM CCASession", "SELECT DISTINCT EndTime FROM CCASession"),
        data_accs=data_accs,
        auth=auth
    )

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

@app.route("/getdata", methods=["GET","POST"])
def get_data():
    db = "School" if not request.args.get("db") else request.args.get("db")
    cmd = request.args.get("cmd")
    data = read_data(cmd, db=db)
    if isinstance(data, str):
        return data
    return json.dumps([i for i in data] if data != [] and not isinstance(data, str) else data)

@app.route("/postdata", methods=["GET","POST"])
def post_data():
    db = "School" if not request.args.get("db") else request.args.get("db")
    cmd = request.args.get("cmd")
    return json.dumps(update_data(cmd, db=db))

@app.route("/backup", methods=["GET","POST"])
def backup():
    db = "School" if not request.args.get("db") else request.args.get("db")
    restore(db)
    return redirect("/")

@app.route("/availability", methods=["GET", "POST"])
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
      
@app.route("/update")
def get_update():
    return json.dumps(update);

if __name__ == "__main__":
    app.run()
