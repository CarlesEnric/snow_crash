# Level14

```console
level14@SnowCrash:~$ ls -la
total 12
dr-x------ 1 level14 level14  100 Mar  5  2016 .
d--x--x--x 1 root    users    340 Aug 30  2015 ..
-r-x------ 1 level14 level14  220 Apr  3  2012 .bash_logout
-r-x------ 1 level14 level14 3518 Aug 30  2015 .bashrc
-r-x------ 1 level14 level14  675 Apr  3  2012 .profile
level14@SnowCrash:~$ 
```

```console
level14@SnowCrash:~$ which getflag
/bin/getflag
```

```console
level14@SnowCrash:~$ id
uid=2014(level14) gid=2014(level14) groups=2014(level14),100(users)
```

```console
level14@SnowCrash:~$ printf "%x\n" 2014
7de
```

```console
level14@SnowCrash:~$ cat /etc/passwd | grep flag14
flag14:x:3014:3014::/home/flag/flag14:/bin/bash
```

```console
level14@SnowCrash:~$ printf "%x\n" 3014
bc6
```

```console
level14@SnowCrash:~$ ltrace /bin/getflag
__libc_start_main(0x8048946, 1, 0xbffff6f4, 0x8048ed0, 0x8048f40 <unfinished ...>
ptrace(0, 0, 1, 0, 0)                         = -1
puts("You should not reverse this"You should not reverse this
)           = 28
+++ exited (status 1) +++
```

```console
level14@SnowCrash:~$ gdb /bin/getflag
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i686-linux-gnu".
For bug reporting instructions, please see:
<http://bugs.launchpad.net/gdb-linaro/>...
Reading symbols from /bin/getflag...(no debugging symbols found)...done.
(gdb) disas main
Dump of assembler code for function main:
...
   0x08048989 <+67>:    call   0x8048540 <ptrace@plt>
   0x0804898e <+72>:    test   %eax,%eax
   0x08048990 <+74>:    jns    0x80489a8 <main+98>
...
0x08048afd <+439>:   call   0x80484b0 <getuid@plt>
   0x08048b02 <+444>:   mov    %eax,0x18(%esp)
   0x08048b06 <+448>:   mov    0x18(%esp),%eax
   0x08048b0a <+452>:   cmp    $0xbbe,%eax
   0x08048b0f <+457>:   je     0x8048ccb <main+901>
   0x08048b15 <+463>:   cmp    $0xbbe,%eax
   0x08048b1a <+468>:   ja     0x8048b68 <main+546>
   0x08048b1c <+470>:   cmp    $0xbba,%eax
   0x08048b21 <+475>:   je     0x8048c3b <main+757>
   0x08048b27 <+481>:   cmp    $0xbba,%eax
   0x08048b2c <+486>:   ja     0x8048b4d <main+519>
   0x08048b2e <+488>:   cmp    $0xbb8,%eax
   0x08048b33 <+493>:   je     0x8048bf3 <main+685>
   0x08048b39 <+499>:   cmp    $0xbb8,%eax
...
   0x08048bb6 <+624>:   cmp    $0xbc6,%eax
   0x08048bbb <+629>:   je     0x8048de5 <main+1183>
...
```

```console
0x08048989 <+67>: call 0x8048540 <ptrace@plt>: Aquí és on el programa crida el programa "guardaespatlles" ptrace

0x08048990 <+74>: jns 0x80489a8: Aquí el programa decideix: "Si NO hi ha debugger, continuo a la 89a8. Si N'HI HA, vaig a la 8992 i plego".

    Per això hem de forçar el salt a la 0x80489a8.

0x08048afd <+439>: call 0x80484b0 <getuid@plt>: Aquí el programa et pregunta: "Qui ets?". La resposta serà "Sóc el 2014", però volem dir "3014"

0x08048bb6 <+624>:   cmp    $0xbc6,%eax: Aquí el programa mira si ets el 3014 (que és 0xbc6 en hexadecimal). Si ho ets, t'ensenya la flag.
```

```console
level14@SnowCrash:~$ gdb /bin/getflag
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i686-linux-gnu".
For bug reporting instructions, please see:
<http://bugs.launchpad.net/gdb-linaro/>...
Reading symbols from /bin/getflag...(no debugging symbols found)...done.
(gdb) break main
Breakpoint 1 at 0x804894a
(gdb) run
Starting program: /bin/getflag 

Breakpoint 1, 0x0804894a in main ()
(gdb) set $eip = 0x08048de5
(gdb) continue
Continuing.
7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
*** stack smashing detected ***: /bin/getflag terminated
======= Backtrace: =========
/lib/i386-linux-gnu/libc.so.6(__fortify_fail+0x45)[0xb7f2fd95]
/lib/i386-linux-gnu/libc.so.6(+0x103d4a)[0xb7f2fd4a]
/bin/getflag[0x8048ec7]
/lib/i386-linux-gnu/libc.so.6(__libc_start_main+0xf3)[0xb7e454d3]
/bin/getflag[0x8048571]
======= Memory map: ========
08048000-0804a000 r-xp 00000000 07:00 12700      /bin/getflag
0804a000-0804b000 r--p 00001000 07:00 12700      /bin/getflag
0804b000-0804c000 rw-p 00002000 07:00 12700      /bin/getflag
0804c000-0806d000 rw-p 00000000 00:00 0          [heap]
b7e07000-b7e23000 r-xp 00000000 07:00 14117      /lib/i386-linux-gnu/libgcc_s.so.1
b7e23000-b7e24000 r--p 0001b000 07:00 14117      /lib/i386-linux-gnu/libgcc_s.so.1
b7e24000-b7e25000 rw-p 0001c000 07:00 14117      /lib/i386-linux-gnu/libgcc_s.so.1
b7e2b000-b7e2c000 rw-p 00000000 00:00 0 
b7e2c000-b7fcf000 r-xp 00000000 07:00 14123      /lib/i386-linux-gnu/libc-2.15.so
b7fcf000-b7fd1000 r--p 001a3000 07:00 14123      /lib/i386-linux-gnu/libc-2.15.so
b7fd1000-b7fd2000 rw-p 001a5000 07:00 14123      /lib/i386-linux-gnu/libc-2.15.so
b7fd2000-b7fd5000 rw-p 00000000 00:00 0 
b7fd9000-b7fdd000 rw-p 00000000 00:00 0 
b7fdd000-b7fde000 r-xp 00000000 00:00 0          [vdso]
b7fde000-b7ffe000 r-xp 00000000 07:00 14081      /lib/i386-linux-gnu/ld-2.15.so
b7ffe000-b7fff000 r--p 0001f000 07:00 14081      /lib/i386-linux-gnu/ld-2.15.so
b7fff000-b8000000 rw-p 00020000 07:00 14081      /lib/i386-linux-gnu/ld-2.15.so
bffdf000-c0000000 rw-p 00000000 00:00 0          [stack]

Program received signal SIGABRT, Aborted.
0xb7fdd428 in __kernel_vsyscall ()
(gdb)
```

```console
TLTR:
   0x08048bb6 <+624>:   cmp    $0xbc6,%eax
   0x08048bbb <+629>:   je     0x8048de5 <main+1183>
0xbc6 és el número d'usuari (UID) de flag14 (3014 en decimal).
La instrucció je 0x8048de5 diu: "Si l'usuari és el 3014, salta a l'adreça 0x08048de5".
Per tant, deduïm que a partir de 0x08048de5 comença el codi que genera i imprimeix la flag final.
```
