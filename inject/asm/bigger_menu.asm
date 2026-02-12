.gba
.open "{source}","{dest}",0x08000000 

//============== Change Menu Width ======================
.org 0x0808b9d6
	mov r1, 0xa ;x position to start drawing
	mov r3, 0xc ;x width

.close
