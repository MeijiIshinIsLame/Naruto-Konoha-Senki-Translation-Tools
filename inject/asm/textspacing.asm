.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
.org 0x0806611e       
    add r4, r4, 5h

.close