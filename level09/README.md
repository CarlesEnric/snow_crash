# TL;DR / TLTR
##### Connectem amb el següent nivell
```bash
flag08@SnowCrash:~$ ssh level09@192.168.122.220 -p 4242
Could not create directory '/home/flag/flag08/.ssh'.
The authenticity of host '[192.168.122.220]:4242 ([192.168.122.220]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/flag/flag08/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level09@192.168.122.220's password: 25749xKZ8L7DkSCwJkT9dyv6f
```
##### Mirem dins de token
```bash
level09@SnowCrash:~$ cat token 
f4kmm6p|=�p�n��DB�Du{��
```
##### Llistem drectori /home
```bash
level09@SnowCrash:~$ ls
level09  token
level09@SnowCrash:~$ ls -la
total 24
dr-x------ 1 level09 level09  140 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level09 level09  220 Apr  3  2012 .bash_logout
-r-x------ 1 level09 level09 3518 Aug 30  2015 .bashrc
-r-x------ 1 level09 level09  675 Apr  3  2012 .profile
-rwsr-sr-x 1 flag09  level09 7640 Mar  5  2016 level09
----r--r-- 1 flag09  level09   26 Mar  5  2016 token
```
##### Obtenim un fitxer SUID anomenat level09 i un anomenat token, provem d'executar-ho plegats
```bash
level09@SnowCrash:~$ ./level09 token
tpmhr
```
##### Tenim un resultat curiós
```text
Al executar ./level09 token -> tpmhr
entrada:  t  o  k  e  n
sortida:  t  p  m  h  r
moviment: 0  1  2  3  4
```
##### Creem un script python per moure els caràcters en ordre invers al (i+1), és a dir, (i-1)
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open("/home/user/level09/token", "rb") as f:
    data = f.read().rstrip(b'\n')

result = ""
for i in range(len(data)):
    byte = ord(data[i])
    result += chr((byte - i) % 256)
print(result)
```
##### Un cop hem creat l'script li passem la cadena del guest i ho executem dins del host
```bash
./script.py 'f4kmm6p|=pnDBDu{'
f3iji1ju5gd967gl
FAIL: falten caràcters no imprimibles, i si els passem directament del guest al host es corrompen. Hem de executar directament en la guest l'script.py
```
##### Enviem amb scp l'script.py en el directori /tmp, l'únic que tenim permisos
```bash
hostUser@hostName:~/Documents/42outerCore/snow_crash/snow_crash/level09/resources$ scp -P 4242 script.py level09@192.168.122.220:/tmp
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun


level09@192.168.122.220's password: 25749xKZ8L7DkSCwJkT9dyv6f 
script.py                                 100%  181   160.7KB/s   00:00 

level09@SnowCrash:~$ ls -ld /tmp
d-wx-wx-wx 4 root root 100 Mar 22 04:10 /tmp
```
##### Donem permisos del guest al script que prové del host:
```bash
level09@SnowCrash:~$ chmod +x /tmp/script.py
```
##### Provem d'executar:
```bash
level09@SnowCrash:~$ /tmp/script.py /home/user/level09/token
f3iji1ju5yuevaus41q1afiuq
level09@SnowCrash:~$
```
##### Ara ens disposem a obtenir la flag:
```bash
level09@SnowCrash:~$ su flag09
Password: 
Don't forget to launch getflag !
flag09@SnowCrash:~$ getflag
Check flag.Here is your token : s5cAJpM8ev6XHw998pRWG728z
flag09@SnowCrash:~$
```


