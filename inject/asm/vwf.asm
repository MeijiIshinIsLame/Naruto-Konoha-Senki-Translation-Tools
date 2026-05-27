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
store_nibble_counter:
	push {r0, r1}
	ldr r0, =nibble_counter
	ldr r0, [r0]
	ldrb r1, [r0]
	cmp r0, 0h
	bne draw
	mov r1, 1h
	strb r1, [r0]
	pop {r0, r1}
	b pre_finale
	
	
draw:
	push {r0}
	ldr r0, =prev_width_addr
	ldr r0, [r0]
	ldrb r0, r0
	cmp r0, 8h
	pop {r0}
	bne draw_with_offset
	
	push {r0}
	ldr r0, =offset_flag
	ldr r0, [r0]
	ldrb r0, r0
	cmp r0, 0h
	pop {r0}
	bne draw_with_offset
	
	strh r1, [r3, 0h]
    add r3, 2h
	b pre_finale
	
draw_with_offset:
	strh r1, [r3, 0h]
    add r3, 2h
	b pre_finale

.pool
prev_width_addr:
	.word 0x0202f2b0
nibble_counter: ;checks if were drawing nibble to right or left
	.word 0x0202f2b4
pixels_drawn:
	.word 0x0202f2b8
drawback_addr_drawn:
	.word 0x0202f2bc
offset_flag: ; determines whether offset is tripped or not to start calculating back addresses
	.word 0x0202f2c0
	
.close