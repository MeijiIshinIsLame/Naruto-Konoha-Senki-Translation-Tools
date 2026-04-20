.gba
.open "{source}","{dest}",0x08000000 
.thumb

//============== HOOK ======================
.org 0x0809c514
	bl get_new_placenames

.org 0x0809e780
get_new_placenames:
	ldr r0, =lr_addr
	ldr r0, [r0]
	push {r1}
	mov r1, lr
	str r1, [r0]
	pop {r1}
	mov r0, #3
	bic r2, r0
	ldr r2,[r2]
loadit:
	ldrb r0,[r2]
	strb r0,[r3]
	push {r1}
	ldr r1, =lr_addr
	ldr r1, [r1]
	ldr r1, [r1]
	mov lr, r1
	pop {r1}
	; end instructions we wrote over
	bx lr


.org 0x0809c520
	bl keep_getting_letters


.org 0x0809e7c0
keep_getting_letters:
    	cmp r0, #0
    	beq skip
    	ldr r0, =loadit+1
    	bx r0
skip:
	; erase lr in ram
	bx lr

.pool
lr_addr:
	.word 0x02002D30
	
.close
