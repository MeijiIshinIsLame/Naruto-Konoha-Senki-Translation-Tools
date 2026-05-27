.gba
.thumb
.open "{source}","{dest}",0x08000000 

.org 0x08065f4c
    bl entry
	
.org 0x08065f5a
    cmp r6, 10h

;god help me, if you are reading this I'm so sorry
.org 0x080a39a0
entry:
	cmp r6, 0h
	beq handle_newchar
	b draw
pre_finale:
	cmp r6, 10h
	bgt clean_up_ram
finale:
	bx lr
clean_up_ram:
	b finale
	
	
handle_newchar:
	push {r7}
	ldr r7, [sp, 10h]
	cmp r7, 1h
	pop {r7}
	bne draw ;if counter is at 2 its not a newchar
;r0 = prev width addr
;r1 = next width addr
;r2 = prev width
;r3 = next width
store_width:
	push {r0, r1, r2, r3}
	ldr r0, =prev_width_addr
	ldr r0, [r0]
	mov r1, r0
	add r1, 1h
	ldrb r2, [r1]
	ldrb r3, [r5]
	strb r3, [r1]
	strb r2, [r0]
	pop {r0, r1, r2, r3}
	b pre_finale
draw:
	strh r1, [r3, 0h]
    add r3, 2h
	b pre_finale

.pool
prev_width_addr:
	.word 0x030012f0
.close