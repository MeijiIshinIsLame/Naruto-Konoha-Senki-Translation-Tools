.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
.org 0x0809c514
	bl get_new_placenames

.org 0x0809e780
get_new_placenames:
	; instructions we wrote over
	; we need to fix the 4 byte alignment thing
	ldr r2,[r2]
	ldrb r0,[r2]
	strb r0,[r3]
	; end instructions we wrote over
	bx lr
.close
