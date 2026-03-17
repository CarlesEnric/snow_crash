# TL;DR / TLTR
```bash
level00@SnowCrash:~$ find / -user flag00 2>/dev/null
/usr/sbin/john
/rofs/usr/sbin/john
level00@SnowCrash:~$ cat /usr/sbin/john
cdiiddwpgswtgt
level00@SnowCrash:~$ python
Python 2.7.3 (default, Jun 22 2015, 19:43:34) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> for i in range(26): print(i,"".join(chr((ord(c)-97-i)%26+97) for c in "cdiiddwpgswtgt"))
... 
(0, 'cdiiddwpgswtgt')
(1, 'bchhccvofrvsfs')
(2, 'abggbbunequrer')
(3, 'zaffaatmdptqdq')
(4, 'yzeezzslcospcp')
(5, 'xyddyyrkbnrobo')
(6, 'wxccxxqjamqnan')
(7, 'vwbbwwpizlpmzm')
(8, 'uvaavvohykolyl')
(9, 'tuzzuungxjnkxk')
(10, 'styyttmfwimjwj')
(11, 'rsxxsslevhlivi')
(12, 'qrwwrrkdugkhuh')
(13, 'pqvvqqjctfjgtg')
(14, 'opuuppibseifsf')
(15, 'nottoohardhere')
(16, 'mnssnngzqcgdqd')
(17, 'lmrrmmfypbfcpc')
(18, 'klqqllexoaebob')
(19, 'jkppkkdwnzdana')
(20, 'ijoojjcvmyczmz')
(21, 'hinniibulxbyly')
(22, 'ghmmhhatkwaxkx')
(23, 'fgllggzsjvzwjw')
(24, 'efkkffyriuyviv')
(25, 'dejjeexqhtxuhu')
>>> exit()
level00@SnowCrash:~$ su flag00
Password: nottoohardhere
Don't forget to launch getflag !
flag00@SnowCrash:~$ getflag
Check flag.Here is your token : x24ti5gi3x0ol2eh4esiuxias
```
