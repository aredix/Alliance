
#!/bin/bash

rm -rf resultat

asterisk -rx 'sip show peers' | grep -v "192." | grep "OK (" > listEndpoints

cat listEndpoints | cut -d \/ -f 1 | grep -Eo '[0-9]{1,}' > listExtensionEndpointAvailable

compteur=`wc -l listExtensionEndpointAvailable | cut -d " " -f 1`

i=1
        for extension in $( cat listExtensionEndpointAvailable )
        do
                tableau_extension[$i]=$extension
                let i=i+1
        done

#echo ${tableau_extension[@]}

    for j in "${tableau_extension[@]}"
    do
        echo "Numero d'extension : $j" >> resultat
        useragent=`asterisk -rx "sip show peer $j" | grep Useragent | cut -d " " -f 9-`
        echo "Type de poste : $useragent" >> resultat
        AutocomIP=`asterisk -rx "sip show peers" | grep $j | sed -e "s/ /|/g" | cut -d "|" -f 18`
        echo "Adresse IP cote autocom : $AutocomIP" >> resultat
        InternalIP=`asterisk -rx "sip show peer $j" | grep "Reg. Contact" | cut -d @ -f 2 | cut -d : -f 1`
        echo "Adresse IP interne reférencee : $InternalIP" >> resultat
        Port=`asterisk -rx "sip show peer $j" | grep "Reg. Contact" | cut -d @ -f 2 | cut -d : -f 2`
        echo "Port de connexion : $Port" >> resultat
        echo "" >> resultat
        echo "" >> resultat
        rm -rf listEndpoints
        rm -rf listExtensionEndpointAvailable
    done

echo "Le résultat de cet outil est disponible là où se trouve le programme dans le fichier resultat"