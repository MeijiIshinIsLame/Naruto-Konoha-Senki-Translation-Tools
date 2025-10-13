.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
.org 0x0806611e       
    add r5, r5, 5h
	add r5, r5, 5h
	add r5, r5, 5h
	add r5, r5, 5h
	add r5, r5, 5h
	add r5, r5, 5h
	add r5, r5, 5h
	add r5, r5, 5h

.close