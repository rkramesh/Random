#!/bin/bash
set -vx
    ip="192.168.1.104"
    ssh-keygen -R $ip
    ssh-keyscan -H $ip >> ~/.ssh/known_hosts
sshpass -p toor ssh  -oStrictHostKeyChecking=no root@192.168.1.104
if  [  "$?" != "0" ]
then
          sshpass -p libreelec ssh -oStrictHostKeyChecking=no root@192.168.1.104 << 'EOF'
         # ssh-keygen -f "/home/jarvis/.ssh/known_hosts" -R 192.168.1.104
         if  [  "$?" == "0" ]
         then
                 cd  "/var/media/berryboot/data/"
                 echo "Kali_2.0.1.img192" >/var/media/berryboot/data/runonce
          fi
EOF
fi
