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
### ENTRAR AL LEVEL01 AMB EL TOKEN OBTINGUT DE GETFLAG
```bash
flag00@SnowCrash:~$ su level01
Password: x24ti5gi3x0ol2eh4esiuxias
level01@SnowCrash:~$ 
```
### POSSIBLE PISTA LEVEL01 (cat /etc/passwd) -> (Observar la línia) flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash
