####################################
##      SCRIPT AVEC PAGE WEB      ##
####################################
##  Author : David DESPLANQUE     ##
##  Version : 1.7.4               ##
##  Made for : Alliance Telecom   ##
####################################

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
os.system('mkdir /usr/share/ombutel/www/alliance 2> /dev/null')
h = open('/usr/share/ombutel/www/alliance/result.html','wb')

initWEB = """<html>
<head></head>
<body><p><h1>Resultat du script :</h1></p></body>
<table style="border-collapse: collapse;">
<tr>
        <td style="border: 2px solid black; padding: 10px;">Extension</td>
        <td style="border: 2px solid black; padding: 10px;">Adresse IP (derniere connue)</td>
        <td style="border: 2px solid black; padding: 10px;">Model de poste</td>
        <td style="border: 2px solid black; padding: 10px;">Status</td>
</tr>"""

h.write(initWEB)
h.close()
compteur = 0

for i in cursor:
        filename = "temp"
        extension = i[0]
        os.environ['extension'] = extension
        os.system('asterisk -rx "sip show peer $extension" | grep "Reg. Contact" | cut -d ":" -f 3 | cut -d "@" -f 2 | cut -d ":" -f 1 > temp')
        with open(filename) as f:
                content = f.read().splitlines()
                IPAutocom = content[0]
        
        os.system('asterisk -rx "sip show peer $extension" | grep Useragent | cut -d ":" -f 2 | sed "s/^.//" > temp')
        with open(filename) as f:
                content = f.read().splitlines()
                useragent = content[0]
        
        os.system('asterisk -rx "sip show peer $extension" | grep "Status" | cut -d ":" -f 2 | sed "s/^.//" > temp')
        with open(filename) as f:
                content = f.read().splitlines()
                status  = content[0]

        with open('/usr/share/ombutel/www/alliance/result.html','ab') as valWEB:
                valWEB.write("    <tr>")
                valWEB.write("\n\t\t<td style=\"border: 2px solid black; padding: 10px;\">")
                valWEB.write(str(extension))
                valWEB.write("</td>")
                valWEB.write("\n\t\t<td style=\"border: 2px solid black; padding: 10px;\"><a href=\"http://")
                valWEB.write(str(IPAutocom))
                valWEB.write("\" target=\"_blank\">")
                valWEB.write(str(IPAutocom))
                valWEB.write("</a></td>")
                valWEB.write("\n\t\t<td style=\"border: 2px solid black; padding: 10px;\">")
                valWEB.write(str(useragent))
                valWEB.write("</td>")
                if str(status) == "UNKNOWN":
                        valWEB.write("\n\t\t<td style=\"border: 2px solid black; padding: 10px; color:red;\">")
                        valWEB.write(str(status))
                        valWEB.write("</td>\n")
                else:
                        valWEB.write("\n\t\t<td style=\"border: 2px solid black; padding: 10px; color:green;\">")
                        valWEB.write(str(status))
                        valWEB.write("</td>\n")
                valWEB.write("    </tr>\n")
        
h = open('/usr/share/ombutel/www/alliance/result.html','ab')

endWEB ="""       
</table>
</html>"""

h.write(endWEB)
h.close()
os.system('rm -rf temp')

print("Le resultat du script est accessible via http://localhost/alliance/result.html")
