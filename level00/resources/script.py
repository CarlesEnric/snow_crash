#!/usr/bin/python3

for i in range(26):
    print(i,"".join(chr((ord(c)-97-i)%26+97) for c in "cdiiddwpgswtgt"))
