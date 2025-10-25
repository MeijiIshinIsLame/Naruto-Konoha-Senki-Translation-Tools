.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
	
.org 0x080662fa
	bl namelabel_check
	pop {r6, r7}

.org 0x0809e700
namelabel_check:
	push {r6, r7}
	ldr r6, =lower_addr
	ldr r6, [r6]
	ldr r7, =higher_addr
	ldr r7, [r7]
	cmp r0, r7
	bge jump_to_lr
	cmp r0, r6
	bge big_text
	bx lr

big_text:
	push {r3}
	mov r1, 82h
	ldrb r0,[r0]
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
	pop {r3}
	bx lr
	
make_uppercase_zenkaku_sjis:
	mov r3, 1Fh
	add r0, r0, r3
	pop {r3}
	bx lr

.pool
lower_addr:
	.word 0x085a57d0

higher_addr:
	.word 0x085a632f

.close