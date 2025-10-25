.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
	
.org 0x0806627e
	bl namelabel_check
	pop {r6, r7}

.org 0x0809e700
namelabel_check:
	push {r6, r7}
	ldr r6, =lower_addr
	ldr r6, [r6]
	ldr r7, =higher_addr
	ldr r7, [r7]
	cmp r2, r7
	bge jump_to_lr
	cmp r2, r6
	bge big_text
	bx lr

big_text:
	push {r3}
	mov r1, 82h
	ldrb r0,[r2]
	cmp r0, 40h
	blt jump_to_lr
	cmp r0, 5Ah
	blt make_uppercase_zenkaku_sjis
	cmp r0, 60h
	blt jump_to_lr
	cmp r0, 7Ah
	blt make_lowercase_zenkaku_sjis
	bx lr

jump_to_lr:
	bx lr

make_lowercase_zenkaku_sjis:
	mov r3, 20h
	add r0, r0, r3
	lsl r1, r1, 8h
	pop {r3}
	push {r9}
	pop {r7}
	pop {r6}
	bl 0x08066300
	
make_uppercase_zenkaku_sjis:
	mov r3, 1Fh
	add r0, r0, r3
	lsl r1, r1, 8h
	pop {r3}
	push {r9}
	pop {r7}
	pop {r6}
	bl 0x08066300

.pool
lower_addr:
	.word 0x085a57d0

higher_addr:
	.word 0x085a632f

.close