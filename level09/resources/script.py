#!/usr/bin/env python
# -*- coding: utf-8 -*-
# El shebang de python indica al sistema que aquest script s'ha d'executar amb el binari "python"
# que es trobi al PATH (en aquesta VM/guest serà Python2 i no pas Python3 com en el host)
# La segona línia es declara el encoding utf8, perquè no salti error pels caràcters (à,é,ç,...etc)

with open("/home/user/level09/token", "rb") as f:
    # Obrim el fitxer "token" en mode binari ("rb" = read binary)
    # Llegim bytes exactes, sense interpretació de text

    data = f.read().rstrip(b'\n')
    # Llegim TOT el contingut del fitxer com a bytes
    # rstrip(b'\n') elimina el salt de línia final (\n = byte 0x0A)

result = ""
# Inicialitzem una cadena buida on anirem construint el resultat desxifrat

for i in range(len(data)):
    # Iterem sobre cada posició del contingut del fitxer
    # i = 0, 1, 2, 3, ..., len(data)-1

    byte = ord(data[i])
    # data[i] és un caràcter (string de longitud 1)
    # ord() el converteix al seu valor ASCII (enter entre 0 i 255)

    result += chr((byte - i) % 256)
    # 1. byte - i → desfem el desplaçament aplicat pel binari
    # 2. % 256 → assegurem que el resultat està dins del rang de byte (0–255)
    # 3. chr(...) → convertim el número a caràcter
    # 4. += → afegim el caràcter al resultat final

print(result)
# Mostrem per pantalla el token desxifrat
