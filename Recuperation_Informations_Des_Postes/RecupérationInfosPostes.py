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

os.system('rm resultat')
compteur = 0

for i in cursor:
        extension = i[0]
        os.environ['extension'] = extension
        os.system('echo $extension >> resultat')
        os.system('asterisk -rx "sip show peer $extension" | grep "Reg. Contact" | cut -d "@" -f 2 | cut -d ":" -f 1 >> resultat')
        os.system('asterisk -rx "sip show peer $extension" | grep Useragent | cut -d " " -f 8- >> resultat')
        os.system('asterisk -rx "sip show peer $extension" | grep "Status" | cut -d ":" -f 2 | sed "s/^.//" >> resultat ')
        os.system('echo " " >> resultat')
        compteur = compteur + 1
os.system('cat resultat')

####################################
####### SCRIPT SANS PAGE WEB #######
####################################

