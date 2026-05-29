.gba
.thumb
.open "{source}","{dest}",0x08000000 
	
.org 0x08065f4c
    bl entry

.org 0x08065f5a
    cmp r6, 0x10

;god help me, if you are reading this I'm so sorry
.org 0x080a39a0
entry:
    cmp r6, 0h
    beq handle_newchar
    b draw
pre_finale:
    bx lr
    
    
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
	cmp r2, 8h
	beq prepare_counter_skip
activate_offset_flag:
	ldr r0, =offset_flag
	ldr r0, [r0]
	mov r1, 1h
	strb r1, [r0]
prepare_counter_skip:
	add r5, 1h
	add r6, 1h
    pop {r0, r1, r2, r3}
	ldr r3, =skip_the_counter
	ldr r3, [r3]
	mov pc, r3
    

;find a way if you can manage the push and pops better
draw:
    ldr r0, =prev_width_addr
    ldr r0, [r0]
    ldrb r0, [r0]
    cmp r0, 0h
    beq draw_normal
    
    ldr r0, =offset_flag
    ldr r0, [r0]
    ldrb r0, [r0]
    cmp r0, 0h
    bne draw_normal
	;u can do 2byte just work on storing the counter
 
draw_normal:
    strh r1, [r3, 0h]
	add r3, 2h
    b pre_finale
	
draw_with_offsets:
	ldrh r0, [r3]
    strh r1, [r3, 0h]
    add r3, 2h
	add r5, 1h
	ldrh r0, [r3]
    strh r1, [r3, 0h]
	add r3, 2h
	add r5, 1h
    b pre_finale
    
    
;r0 = halfword pulled from vram
;r1 = halfword pulled from rom
;r2 = pos (from left to right as pixels - 43 21)
;
;at the end, r1 is the final thing 
;
insert_bit_at_position:
    mov r4, 4h ; shift amount
    mov r5, 16h ;hard shift for the vram pull
    mov r6, 4h ; minus for remainder

    mul r4, r2
    add r5, r4
    
    lsl r0, r5
    lsr r0, r5
    lsr r1, r4
    lsl r1, r4
    
    and r0, r1
    sub r2, r4 
    bx lr

.pool
prev_width_addr:
    .word 0x0202f2b0
bit_pos: ;checks what bit to start drawing on
    .word 0x0202f2b4
pixels_drawn: ;how many pixels have been drawn (up to 8)
    .word 0x0202f2bc
offset_flag: ; determines whether offset is tripped or not to start calculating back addresses
    .word 0x0202f2c0
skip_the_counter:
	.word 0x08065f5a
.close