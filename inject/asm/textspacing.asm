.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
.org 0x08066d62       
    add r7, r7, 4h

.close