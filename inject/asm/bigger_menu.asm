.gba
.open "{source}","{dest}",0x08000000 

//============== Change Main Menu Width ======================
.org 0x0808b9d6
	mov r1, 0xa ;x position to start drawing
	mov r3, 0xc ;x width

//============== Change Location Select Menu Width ======================
.org 0x08009a9b
	.byte 0x10 ;x position to start drawing
	.byte 0x00 ;padding
	.byte 0xd ;x width	
.close