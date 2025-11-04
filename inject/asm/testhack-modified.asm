.gba
.open "Naruto - Konoha Senki English translation.gba","output.gba",0x08000000 

//============== HOOK ======================
.org 0x08066276
	bl namelabel_check

.org 0x0809e700
namelabel_check:
	;check if in range of charnames
	push {r7, r14}
	ldr r6, =lower_addr
	ldr r6, [r6]
	ldr r7, =higher_addr
	ldr r7, [r7]
	cmp r2, r7
	bge finale ;get outta here!
	cmp r2, r6
	bge subvert_nametable
finale:
	add r6, r0, 0h
	str r1, [sp, 1Ch]
	pop {r7, r14}
	bx lr
subvert_nametable:
	ldr r1, [r1]
	bl finale
	;we want to jump to my personal table with 2byte SJIS eng chars
	; you may need to push to stack also. not sure yet.

.pool
lower_addr:
	.word 0x085a57d0

higher_addr:
	.word 0x085a632f

.close