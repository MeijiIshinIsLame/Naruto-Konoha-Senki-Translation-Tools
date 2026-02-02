.gba
.open "{source}","{dest}",0x08000000 

//============== Change Menu Width ======================
.org 0x0808b9d8
	mov r3, 0xc

.close
