.gba
.open "{source}","{dest}",0x08000000 

//============== HOOK ======================
	
.org 0x080662fa
	bl namelabel_check
	pop {r6, r7}

.org 0x0809d13a
namelabel_check:
	push {r6, r7}
	ldr r6, =lower_addr
	ldr r6, [r6]
	ldr r7, =higher_addr
	ldr r7, [r7]
	cmp r0, r7
	bgt jump_to_lr
	cmp r0, r6
	bgt big_text
	bx lr

big_text:
	mov r1, 82h
	ldr r0,[r0]
	mov r3, 20h
	add r0, r0, r3
	bx lr

jump_to_lr:
	bx lr
	

.pool
lower_addr:
	.word 0x085a57d0

higher_addr:
	.word 0x085a632f

.close