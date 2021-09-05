from flask import Flask, render_template, redirect, request
from contextlib import closing
import os.path, json, sqlite3, tabula, random, csv
from selenium import webdriver
from time import sleep


k = {
    "english":"en",
    "aesthetics":"ar",
    "economics":"ec",
    "humanities":"hm",
    "language-arts":"la",
    "mother-tongue":"mt",
    "mathematics-junior-high":"ma",
    "physical-education":"pe",
    "project-work":"pw",
    "science-junior-high":"scj",
    "science-senior-high":"scs"
}

j = {
    "en":["1EN2", "1KI2", "1el2A", "1en2A1", "1en2A3", "1en2B1", "1en2B3", "1gp1A01", "1gp1A02", "1gp1A03", "1gp1A04", "1gp1A05", "1gp1A06", "1gp1A07", "1gp1B08", "1gp1B09", "1gp1B10", "1gp1B11", "1gp1B12", "1gp1B13", "1gp1B14", "1gp1C15", "1gp1C16", "1gp1C17", "1gp1C18", "1gp1C19", "1gp1C20", "1ki2A"],
    "ar":["1ar2A", "1mu2A"],
    "ec":["1ec1H", "1ec1I", "1ec1J", "1ec1K", "1ec2A", "1ec2B", "1ec2E", "1ec2F", "1ec2G", "1ec2L", "1ec2M", "1ec2N", "1ec2O", "1ec2P", "1ec2Q", "1ec2R", "1ec2S", "1ec2T"],
    "hm":["1GE2", "1HI2", "1ge2A", "1ge2B1", "1ge2B2", "1hi2A", "1hi2B"],
    "mt":["1cl(B)", "1cl1A1", "1cl1A2", "1cl1B1", "1cl1B2", "1cl1C1", "1cl1C2", "1cn2A", "1hl1A", "1ml(B)", "1ml1A", "1mn2A", "1tl1A", "1tn2A"],
    "ma":["1MA2", "1fm2A", "1ma1A", "1ma1B", "1ma2A", "1ma2C", "1ma2D", "1ma2G", "1ma2H", "1ma2I", "1ma2J", "1ma2K", "1ma2L", "1ma2M", "1ma2N", "1ma2O", "1ma2Q", "1ma2V", "1ma2W", "1ma2X", "1ma2Y", "1ma2Z"],
    "pe":["1peA1", "1peA2", "1peB1", "1peB2", "1peC1", "1peC2", "1peD1", "1peD2", "1peE1", "1peE2", "1peF1", "1peF2", "1peG1", "1peG2", "1peH1", "1peH2", "1peI1", "1peI2", "1peJ1", "1peJ2", "1peK1", "1peK2", "1peL1", "1peL2", "1peM1", "1peM2", "1peN1", "1peN2", "1peO1", "1peO2", "1peP1", "1peP2", "1peQ1", "1peQ2", "1peR1", "1peR2", "1peS1", "1peS2", "1peT1", "1peT2"],
    "pw":["1pw1A01", "1pw1A02", "1pw1A03", "1pw1A04", "1pw1A05", "1pw1A06", "1pw1A07", "1pw1B01", "1pw1B02", "1pw1B03", "1pw1B04", "1pw1B05", "1pw1B06", "1pw1B07", "1pw1B08", "1pw1C01", "1pw1C02", "1pw1C03", "1pw1C04", "1pw1C05", "1pw1C06", "1pw1C07"],
    "scs":["1BI2", "1CM2", "1PH2", "1bi1A", "1bi2A", "1bi2A(P)", "1bi2H", "1bi2H(P)", "1bi2I", "1bi2I(P)", "1bi2L", "1bi2L(P)", "1bi2M", "1bi2M(P)", "1bi2N", "1bi2N(P)", "1cm1A", "1cm2C", "1cm2C(P)", "1cm2D", "1cm2D(P)", "1cm2E", "1cm2E(P)", "1cm2H", "1cm2H(P)", "1cm2I", "1cm2I(P)", "1cm2J", "1cm2J(P)", "1cm2K", "1cm2K(P)", "1cm2L", "1cm2L(P)", "1cm2M", "1cm2M(P)", "1cm2N", "1cm2N(P)", "1cm2O", "1cm2O(P)", "1cm2P", "1cm2P(P)", "1cm2Q", "1cm2Q(P)", "1cm2R", "1cm2R(P)", "1cm2S", "1cm2S(P)", "1cm2T", "1cm2T(P)", "1ph1A", "1ph2C", "1ph2C(P)", "1ph2F", "1ph2F(P)", "1ph2G", "1ph2G(P)", "1ph2J", "1ph2J(P)", "1ph2K(P)", "1ph2K1", "1ph2K2", "1ph2O", "1ph2O(P)", "1ph2P", "1ph2P(P)", "1ph2Q", "1ph2Q(P)", "1ph2R", "1ph2R(P)", "1ph2S(P)", "1ph2S1", "1ph2S2", "1ph2T", "1ph2T(P)"]
}


# ls = set()
# driver = webdriver.Chrome()
# for i in k.keys():
#     driver.get("https://nationaljc.moe.edu.sg/about-us/staff/" + i)
#     sleep(3)
#     elems = driver.find_elements_by_xpath("//span[@style='font-size: 10pt;']")
#     for j in elems:
#         j = j.find_elements_by_xpath(".//strong")
#         if len(j):
#             ls.add((j[0].get_attribute("innerHTML"), k[i]))
# driver.close()
# ls = list(ls)
# lss = []
# for i in ls:
#     i = list(i)
#     i[0] = i[0].replace("&nbsp;", "")
#     i[0] = i[0].replace("<br>", "")
#     i[0] = i[0].replace("</br>", "")
#     i[0] = i[0].replace("<b>", "")
#     i[0] = i[0].replace("</b>", "")
#     if "(" in i[0] and ")" in i[0]:
#         i[0] = i[0][:i[0].index("(")] + i[0][i[0].index(")")+1:]
#     i[0] = i[0].strip()
#     if i[0] != "":
#         i = tuple(i)
#         lss.append(i)
# lss = set(lss)
# lss = list(lss)
# print()

lsss = ["Woon Yoke Fun",
"Lin Qiao",
"Dassiah Victor John",
"Teo Chwee Hock",
"Mao Yong Qing",
"Artina Bte Selamat",
"Iryianna Binte Ahmad",
"Guo Lan Hua",
"Zhang Jianping",
"Lin Huaizu",
"Mathiyalagan S/O Sankaran",
"Zhang Jianli",
"Huang Shan"]

lsd = {'en': ['Andrew S/O Andeny', 'Er Yinghui Junice', 'Lin Li Josephine', 'Wan Wai Sum', 'Narayanan Rakunathan', 'Oh Jia Lin Karen', 'Meena Malinder Kaur', 'Joel Poh Weinan', 'Low Jeng Wye', 'Chia Han Chin Desmond', 'Wong Hsien Ming David', 'Ng Siang Nan Carmen', 'Soh Huiqing Sylvia'], 'ar': ['Teo Chor Howe', 'Eng Wei Ping Michelle'], 'ec': ['Mun Lynn', 'Stephanie Foo Li Min', 'Lee Ching Ching Christine', 'Tan Lee Hui', 'Lim Zong Liang', 'Yew Shinn How Daniel', 'Lim Lai Har Karen', 'Pauline Yeong Pao Lian', 'Gao Peirong Jessica', 'Low Wei Jie Donavan'], 'hm': ['Ang Li-Jin Wendy', 'Tan Wei Ren Bryan', 'Cher Caifeng Valerie'], 'mt': ['Zhang Jianping', 'Teo Chwee Hock', 'Lin Huaizu', 'Woon Yoke Fun', 'Zhang Jianli', 'Artina Selamat', 'Iryianna Binte Ahmad'], 'ma': ['Pok Wern Jian', 'Chew Joo Oon', 'Chan Yoon Teng', 'Chong Hur Ling Marcus', 'Fong Chee Hoe', 'Feng Pingping', 'Kwek Yuan Chia', 'Wong Yew Chong', 'Lee Jian Hao Jason', 'Liew Yew Tze'], 'pe': ['Tan Joe-sie', 'Taranpal Singh', 'Sng Yeow Boon Henry', 'Yeo Shengqiang Jeremy', 'Ong Ming Ann', 'Yong Man Yun', 'Shanmugadas S/O Kumaresadas', 'Neo Ko Hui', 'Ang Xing Tai Shaun', 'Lim Lee Huang Winnie'], 'pw': ['Wang Shiliang', 'Ng Kian Tiong', 'Linda Faustina', 'Chuah Lay Yen', 'Chiang Cher Siang', 'Senthil Kumaran S/O Kunasegaran', 'Hue Hoe Ping', 'Ng Chinn Min Veronica'], 'scs': ['Lim Eng Soon', 'Ang Si Ling Sheryl', 'Yeo Chin Theng', 'Lim Wei Li', 'Chng Chwee Ying', 'Tan Peng Hui Samuel', 'Goh Nai Lee Mark', 'Lim Kim Hock', 'Ng Yee Lee', 'Darshini D/O Radha Krishnan', 'Tan Soon Heng Simon', 'Tan Chin Hui', 'Chua Manping', 'Nyam Ching Wee', 'Lim Hwee Ke', 'Hon Tin Seng', 'Ng Joon Hong']}

# con = sqlite3.connect("database/School.db")
# cd = {i:j for (j, i) in con.execute("SELECT * FROM Course")}
# td = {i:j for (j, i) in con.execute("SELECT ID, Name FROM Teacher")}
# with con:
#     for subj in j.keys():
#         assign = {i:[] for i in lsd[subj]}
#         for course in j[subj]:
#             if course in ("1EN2", "1KI2", "1GE2", "1HI2", "1MA2", "1BI2", "1CM2", "1PH2"):
#                 for teach in lsd[subj]:
#                     con.execute(f"INSERT INTO TeacherCourse VALUES ('{td[teach]}', {cd[course]})")
#             else:
#                 counts = {teach: assign.values().count(teach) for teach in lsd[subj]}
#                 kkk = []
#                 for teach in lsd[subj]:
#                     if counts[teach] == min(counts.values()):
#                         kkk.append(teach)
#                 assign[random.choice(kkk)].append(course)
#         for courses in assign.values():



# ls = [('Lim Yi’En', 'la'), ('Tan Joe-sie', 'pe'), ('Gayle Sim', 'ar'), ('Mun Lynn', 'ec'), ('Goh Nai Lee Mark', 'scs'), ('Tan Wei Ren Bryan', 'hm'), ('Chan Yoon Teng', 'ma'), ('Chung Yeong Hui', 'ma'), ('Lim Kim Hock', 'scs'), ('Darryl Chew Ching Yan', 'la'), ('Aileen Tang', 'en'), ('Yew Shinn How Daniel', 'ec'), ('Chin Kai Qing Juliana', 'scj'), ('Lim Hui Chi', 'ar'), ('Oh Jia Lin Karen', 'en'), ('Feng Pingping', 'ma'), ('Lim Wei Li', 'scs'), ('Clare Low Siew Ching', 'la'), ('Ho Hui Lin', 'hm'), ('Ling Hwee Cheng', 'ma'), ('Lim Hwee Ke', 'scs'), ('Lim Eng Soon', 'scs'), ('Teo Chor Howe', 'ar'), ('Teo Tze Wei', 'ma'), ('Lim Hui Mei Jan', 'la'), ('Ang Si Ling Sheryl', 'scs'), ('Ang Li Jin Wendy', 'hm'), ('Nayentika Pramchandran', 'la'), ('Andrew s/o Andeny', 'en'), ('Tai Mei En', 'scj'), ('Ting Der Huoy Claudia Anne', 'hm'), ('Mak Wei Shan', 'hm'), ('Taranpal Singh', 'pe'), ('Chuah Lay Yen', 'ma'), ('Goh Yinglun Allan', 'scj'), ('Liu Wai Ling Vivian', 'la'), ('Low Wei Jie Donavan', 'ec'), ('Sng Yeow Boon Henry', 'pe'), ('Nicholas Tan Aum Yeow', 'scj'), ('Chong Hur Ling Marcus', 'ma'), ('Chua Manping', 'scs'), ('Bek Aik Chiang Alvin', 'ma'), ('Ng Yee Lee', 'scs'), ('Chng Chwee Ying', 'scs'), ('Stephanie Foo Li Min', 'ec'), ('Tan Chin Hui', 'scs'), ('Reef Koh Junjie', 'scs'), ('Tay Wen Lin Melanie', 'scs'), ('Ng Joon Hong', 'scs'), ('Lee Tat Leong', 'scs'), ('Neo Shu Ting', 'la'), ('Lye Wai Leng', 'ma'), ('Lim Zong Liang', 'ec'), ('Sim Geok Yan', 'ma'), ('Tan Shu-Wei', 'hm'), ('Lim Lai Har Karen', 'ec'), ('Ling Wee Lee', 'scj'), ('Meena Malinder Kaur', 'en'), ('Fong Su Fern Vivien', 'hm'), ('Lum Zhi Yong Aaron', 'ar'), ('Lai Yishan Louisa', 'ec'), ('Yeo Shengqiang Jeremy', 'pe'), ('Kao Peixin Jamie', 'en'), ('Ong Chye Meng', 'hm'), ('See Yeow Hoe', 'ma'), ('Lim Jinwei Sherry', 'scj'), ('Teo Tai Wei', 'scj'), ('Chia Han Chin Desmond', 'en'), ('Wang Shiliang', 'pw'), ('Pauline Yeong Pao Lian', 'ec'), ('Liew Yew Tze', 'ma'), ('Joel Poh Weinan', 'en'), ('Wang Muran', 'ma'), ('Ng Kian Tiong', 'pw'), ('Ong Ming Ann', 'pe'), ('Chew Joo Oon', 'ma'), ('Linda Faustina', 'pw'), ('Chua Chin Yang', 'la'), ('Chuah Lay Yen', 'pw'), ('Hon Tin Seng', 'scs'), ('Yong Man Yun', 'pe'), ('Ning Hwee Tiang', 'scj'), ('Chen Liangcai', 'la'), ('Lee Shan Shan', 'scj'), ('Low Jeng Wye', 'en'), ('Ng Xiu-Li', 'scj'), ('Tan Peng Hui Samuel', 'scs'), ('Lim Chin Min', 'scj'), ('Yeo Chin Kent Ernest', 'ar'), ('Darshini d/o Radha Krishnan', 'scs'), ('Gao Peirong Jessica', 'ec'), ('Cheong Swee Choo Marianne', 'la'), ('Adrian Loh Sin Loy', 'scj'), ('Wong Hsien Ming David', 'en'), ('Tan Xuan Wen Jeffrey', 'ma'), ('Chiang Cher Siang', 'pw'), ('Wee Keng Han', 'scs'), ('Yap Teck Sheng Terence', 'scs'), ('Shanmugadas s/o Kumaresadas', 'pe'), ('Cher Caifeng Valerie', 'hm'), ('Low Kit Ping Serene', 'la'), ('Tan Soon Heng Simon', 'scs'), ('Lee Ching Ching Christine', 'ec'), ('Kuah Wei Fen', 'scj'), ('Senthil Kumaran S/O Kunasegaran', 'pw'), ('Wong Yew Chong', 'ma'), ('Beertino Romerow Woe', 'ma'), ('Neo Ko Hui', 'pe'), ('Nyam Ching Wee', 'scs'), ('Chua Siok Kheng', 'ma'), ('Ho Jin Qing', 'scj'), ('Kwek Yuan Chia', 'ma'), ('Phang Wei Cheng', 'ma'), ('Er Yinghui Junice', 'en'), ('Ong Jou-Jinn', 'ma'), ('Benzie Dio', 'en'), ('Yeo Chin Theng', 'scs'), ('Lee Jian Hao Jason', 'ma'), ('Ang Xing Tai Shaun', 'pe'), ('Fong Chee Hoe', 'ma'), ('Hue Hoe Ping', 'pw'), ('Priya V. Jothi', 'ar'), ('Ganesh Issardas Udasi', 'hm'), ('Eng Wei Ping Michelle', 'ar'), ('Lim Lee Huang Winnie', 'pe'), ('Ng Siang Nan Carmen', 'en'), ('Oh Wei Ting', 'scj'), ('Joey Goh Qinyuan', 'scj'), ('Koh Sheng Wei Demas', 'ec'), ('Soh Huiqing Sylvia', 'en'), ('Sing Nigel Jon', 'ar'), ('Tan Lee Hui', 'ec'), ('Narayanan Rakunathan', 'en'), ('Goh Chong Meng Arthur', 'scs'), ('Wan Wai Sum', 'en'), ('Pok Wern Jian', 'ma'), ('Ethel Tan Yi', 'hm'), ('Heng Li Li Amanda', 'scs'), ('Sharon Phua Phek Heng', 'en'), ('Lin Li Josephine', 'en')]
# tecs = [[] for i in range(9)]
# for i in ls:
#     if i[1] == "ar":
#         tecs[0].append(i[0])
#     if i[1] == "hm":
#         tecs[1].append(i[0])
#     if i[1] == "ec":
#         tecs[2].append(i[0])
#     # if i[1] == "mt":
#     #     tecs[3].append(i[0])
#     if i[1] == "ma":
#         tecs[4].append(i[0])
#     if i[1] == "pw":
#         tecs[5].append(i[0])
#     if i[1] == "pe":
#         tecs[6].append(i[0])
#     if i[1] == "en":
#         tecs[7].append(i[0])
#     if i[1] == "scs":
#         tecs[8].append(i[0])
# sbts["ar"] = random.sample(tecs[0], 2)
# sbts["hm"] = random.sample(tecs[1], 3)
# sbts["ec"] = random.sample(tecs[2], 10)
# sbts["mt"] = random.sample(lsss, 7)
# sbts["ma"] = random.sample(tecs[4], 10)
# sbts["pw"] = tecs[5]
# sbts["pe"] = tecs[6]
# sbts["en"] = random.sample(tecs[7], 13)
# sbts["scs"] = random.sample(tecs[8], 20)

# print(sbts)


auth, resp = 0, 0

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
    if db.upper() not in ("SCHOOL", "ACCOUNT") or (db.upper() == "ACCOUNT" and auth < 2):
        return f"<h2>Unable to Access Database: {db}</h2>"
    db = db.title()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, f"database/{db}.db")
    if auth == 2:
        try:
            conn = sqlite3.connect(db_path)
            if len(cmds) == 1:
                return list(conn.execute(cmds[0]))
            return [list(conn.execute(cmd)) for cmd in cmds]
        except sqlite3.OperationalError as e:
            return f"<h2>sqlite3.OperationalError: {e}</h2>"
        finally:
            conn.close()
    try:
        conn = sqlite3.connect(db_path)
        if len(cmds) == 1:
            return list(conn.execute(cmds[0]))
        return [list(conn.execute(cmd)) for cmd in cmds]
    except sqlite3.OperationalError as e:
        return f"<h2>sqlite3.OperationalError: {e}</h2>"
    finally:
        conn.close()

pre = {"Pok Wern Jian": "1fm2A", "Lin Li Josephine": "1gp1A07", "Beertino Romerow Woe": "1cz2A", "Lee Jian Hao Jason": "1ma2G", "Lee Jian Hao Jason": "1MA2", "Chng Chwee Ying": "1ph2G", "Chng Chwee Ying": "1PH2", "Ang Xing Tai Shaun": "1peG2", "Sng Yeow Boon Henry": "1peG1", "Ng Kian Tiong": "1pw1A01", "Gao Peirong Jessica": "1ec2G", "Lee Ching Ching Christine": "1ec2G"}

# con = sqlite3.connect("database/School.db")
# with con:
#     cd = {i:j for (j, i) in con.execute("SELECT * FROM Course")}
#     td = {i:j for (j, i) in con.execute("SELECT ID, Name FROM Teacher")}
#     for i in range(20):
#         tts = list(con.execute(f"SELECT ID FROM Teacher WHERE ClassID = {i+1}"))
#         cor = i+9
#         for j in tts:
#             con.execute(f"INSERT INTO TeacherCourse VALUES ('{j[0]}',{cor})")
#     tts = list(con.execute(f"SELECT ID FROM Teacher WHERE ClassID"))
#     for i in tts:
#         con.execute(f"INSERT INTO TeacherCourse VALUES ('{i[0]}',249)")
# con.close()

# with open("project/PMs.csv") as f:
#     reader = {i[1]:i[2] for i in csv.reader(f)}
# print(reader)
# cs = {i:j for j,i in conn.execute("SELECT ID, Name FROM Class")}
# with conn:
#     conn.execute("DELETE FROM Teacher")
#     for i in reader.keys():
#         if "," in reader[i]:
#             reader[i] = reader[i].split(",")
#         else:
#             reader[i] = reader[i].split(";")
#         a = [i[0] for i in conn.execute("SELECT ID FROM Student")] + [i[0] for i in conn.execute("SELECT ID FROM Teacher")]
#         while True:
#             ic = gen_ic(bool(random.randint(0,99)), int(min(max(random.gauss(1983, 10.2), 1956), 1997)))
#             if ic not in a:
#                 break
#         conn.execute(f"INSERT INTO Teacher VALUES ('{ic}','{reader[i][0].strip()}',{cs[i]})")
#         if len(reader[i]) == 2:
#             a = [i[0] for i in conn.execute("SELECT ID FROM Student")] + [i[0] for i in conn.execute("SELECT ID FROM Teacher")]
#             while True:
#                 ic = gen_ic(bool(random.randint(0,99)), int(min(max(random.gauss(1983, 10.2), 1956), 1997)))
#                 if ic not in a:
#                     break
#             conn.execute(f"INSERT INTO Teacher VALUES ('{ic}','{reader[i][1].strip()}',{cs[i]})")



# app = Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# @app.route("/", methods=["GET", "POST"])
# def root():
#     global resp
#     resp = 0
#     data_accs = None
#     if auth == 2:
#         data_accs = read_data("SELECT * FROM Account", db="Account")
#     return render_template("user.html", data=read_data("SELECT Name FROM Student", "SELECT Name FROM Teacher", "SELECT Name FROM Class", "SELECT Name FROM Course", "SELECT Name FROM CCA"), data_accs=data_accs, auth=auth)

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     return render_template("login.html", resp=resp)

# @app.route("/loginprocess", methods=["GET", "POST"])
# def login_process():
#     global auth, resp
#     if request.form["username"] == request.form["password"] == "":
#         resp = 4
#         return redirect("/login")
#     if request.form["username"] == "":
#         resp = 2
#         return redirect("/login")
#     if request.form["password"] == "":
#         resp = 3
#         return redirect("/login")
    
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     db_path = os.path.join(BASE_DIR, "database/Account.db")
#     conn = sqlite3.connect(db_path)
#     cur = list(conn.execute("SELECT Level FROM Account WHERE Username = ? AND Password = ?", (request.form["username"], request.form["password"])))
#     conn.close()
#     if cur == []:
#         resp = 1
#         return redirect("/login")
#     auth = cur[0][0]
#     resp = 0
#     return redirect("/")

# @app.route("/logout", methods=["GET", "POST"])
# def logout():
#     global auth
#     auth = 0
#     return redirect("/")

# @app.route("/getdata", methods=['GET','POST'])
# def data_get():
#     db = request.args.get("db")
#     cmd = request.args.get("cmd")
#     if request.method == "GET":
#         data = read_data(cmd, db=db)
#         if isinstance(data, str):
#             return data
#         return json.dumps([i for i in data] if data != [] and not isinstance(data, str) else data)
#     else:
#         print(request.get_text())
#         return "OK", 200

# if __name__ == "__main__":
#     app.run()