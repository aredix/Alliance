import sys
import os
import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        database="ombutel"
)


mycursor = mydb.cursor()

mycursor.execute("select user from ombu_sip_devices")

cursor = mycursor

for i in cursor:
        filename = "temp"
        extension = i[0]
        print(extension)
        os.environ['extension'] = extension

        os.system('asterisk -rx "sip show peer $extension" | grep Useragent | cut -d " " -f 8- > temp')
        with open(filename) as f:
                content = f.read().splitlines()
        for useragent in content:
                print(useragent)
        
        os.system('asterisk -rx "sip show peer $extension" | grep "Reg. Contact" | cut -d "@" -f 2 | cut -d ":" -f 1 > temp')
        with open(filename) as f:
                content = f.read().splitlines()
        for IPAutocom in content:
                print(IPAutocom)

        os.system('asterisk -rx "sip show peer 2001_Accueil_1" | grep "Status" | cut -d ":" -f 2 | sed "s/^.//" > temp')
        with open(filename) as f:
                content = f.read().splitlines()
        for status in content:
                print(status)

        print("")