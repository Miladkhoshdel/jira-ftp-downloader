#Created By: Milad Khoshdel
#Blog: https://blog.regux.com
#Email: miladkhoshdel@gmail.com
#Telegram: @miladkho5hdel

from ftplib import FTP
from datetime import datetime
import sqlite3
import os


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def read_config(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM config")
    rows = cur.fetchall()
    number_rows = len(rows)
    print("+ Number of servers: " + str(len(rows)))
    return rows, number_rows


def ftp_connect(ip, user, password, file, cwddir):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    try:
        ftp = FTP(ip)
        ftp.login(user, password)
        ftp.cwd("/" + cwddir)
        files = ftp.nlst()
        if not os.path.exists(dir_path + "\\download\\" + ip):
            os.makedirs(dir_path + "\\download\\" + ip)

        print("  - Downloading " + file + " from " + ip)
        ftp.retrbinary("RETR " + file,
                       open(dir_path + "\\download\\" + ip + "\\" + file, 'wb').write)
        print("  - Downloading Done.")
        ftp.close()
    except Exception as e:
        print("  - Error: " + str(e))
        pass


def insertdb(ip, filename):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    try:
        with open(dir_path + "\\download\\" + ip + "\\" + filename) as f:
            content = f.readlines()
        print("  - Reading File ...")
        items = []
        for i in content:
            b = i.strip().split(":")
            print("   - " + b[0] + ": " + b[1])
            items.append(b[1])
        print("  - Reading File Done...")
        items.append(ip)
        database = dir_path + r"\newdb.sqlite"
        conn = create_connection(database)
        cur = conn.cursor()
        print("  - inserting data in DB ...")
        cur.execute("SELECT * FROM informations WHERE ipaddress = ?", (ip,))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute(
                "INSERT INTO 'informations' ('webserver','databaseserver','ftpserver','ipaddress') VALUES (?,?,?,?)",
                items)
            conn.commit()
        else:
            cur.execute(
                '''UPDATE informations SET webserver = ?, databaseserver = ?, ftpserver = ? WHERE ipaddress = ?''',
                items)
            conn.commit()
        print("  - inserting data in DB Done.")
    except Exception as e:
        print(e)
        pass


def main():
    start = datetime.now()
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path + "\\download"):
        os.makedirs(dir_path + "\\download")
    database = dir_path + r"\newdb.sqlite"
    conn = create_connection(database)
    with conn:
        print()
        print("+ Reading FTP Config Files ...")
        config_data = read_config(conn)
        for x in range(0, config_data[1]):
            print("+ Connectiong to " + config_data[0][x][0])
            ftp_connect(config_data[0][x][0], config_data[0][x][1], config_data[0][x][2], config_data[0][x][3],
                        config_data[0][x][4])
            insertdb(config_data[0][x][0], config_data[0][x][3])


if __name__ == '__main__':
    main()
