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
	push {r0}

	ldr r0, =font_start
	ldr r0, [r0]
	cmp r5, r0
	blo thats_not_the_font_buddy

	ldr r0, =font_end
	ldr r0, [r0]
	cmp r5, r0
	bhi thats_not_the_font_buddy

	pop {r0}
its_the_font:	
    cmp r6, 0h
    beq handle_newchar
    b draw
pre_finale:
    bx lr
thats_not_the_font_buddy:
	pop {r0}
	b draw_normal
    
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
    ldr r0, =prev_widthOP_ADDr
    ldr r0, [r0]
    mov r1, r0
    add r1, 1h
    ldrb r2, [r1]
    ldrb r3, [r5]
    strb r3, [r1]
    strb r2, [r0]
prepare_counter_skip:
	add r5, 1h
	add r6, 1h
    pop {r0, r1, r2, r3}
	ldr r3, =skip_the_counter
	ldr r3, [r3]
	mov pc, r3
    

;find a way if you can manage the push and pops better
draw:
    b draw_from_pos
 

;free registers
; r2, r4, r5, r6
draw_from_pos:
	push {r7, lr}
	mov r7, r1
	mov r2, 4h
start_drawing:
	mov r1, r7
	
	ldrh r0, [r3]
	bl insert_bit_at_position
	
    strh r1, [r3, 0h]
	
	add r3, 2h
	pop {r7, lr}
    b pre_finale
	
draw_normal:
	strh r1, [r3, 0h]
    add r3, 2h
	b pre_finale
    
	
;r0 = halfword pulled from vram (dest)
;r1 = halfword pulled from rom (src)
;r2 = pos (from left to right as pixels - 43 21)
;
;at the end, r1 is the final thing 
;
insert_bit_at_position:
    push {r3, r4, r5}
	mov r3, 2h
	mul r3, r2 ; set up offset
	
	ldr r4, =bitmask_pos_dest
	add r4, r3
	ldrh r4, [r4]
	
	ldr r5, =bitmask_pos_src
	add r5, r3
	ldrh r5, [r5]
	
	and r0, r4
	and r1, r5
	orr r1, r0
	pop {r3, r4, r5}
	bx lr


.pool

font_start:
	.word 0x080a2154
font_end:
	.word 0x080a392a

prev_widthOP_ADDr:
    .word 0x0202f2b0
skip_the_counter:
	.word 0x08065f1c

bitmask_pos_dest:
	.halfword 0x0000
bitmask_pos1_dest:
	.halfword 0xf000
bitmask_pos2_dest:
	.halfword 0xff00
bitmask_pos3_dest:
	.halfword 0xf000
bitmask_pos4_dest:
	.halfword 0x0000

bitmask_pos_src:
	.halfword 0x0000
bitmask_pos1_src:
	.halfword 0x000f
bitmask_pos2_src:
	.halfword 0x00ff
bitmask_pos3_src:
	.halfword 0x0fff
bitmask_pos4_src:
	.halfword 0xffff
	
; This is a struct. LOL. And yes, I'm aware it's ridiculous. Think of it like this.
; struct InsertOrder {
	; int insertAmount (1-4 bits)
	; int insertpos (1-4)
	; int addOrSubtract (0=none, 1=add, 2=subtract)
	; int addOrSubtractAmount
	
	; int insertAmount (1-4 bits)
	; int insertpos (1-4)
	; int addOrSubtract (0=none, 1=add, 2=subtract)
	; int addOrSubtractAmount
; }
;its 2 times incase 2 operations need to happen

.definelabel JUST_INSERT, 0
.definelabel OP_ADD, 1
.definelabel OP_SUB, 2

.definelabel LEN_0BITS, 0
.definelabel LEN_1BITS, 1
.definelabel LEN_2BITS, 2
.definelabel LEN_3BITS, 3
.definelabel LEN_4BITS, 4

.definelabel POS_0, 0
.definelabel POS_1, 1
.definelabel POS_2, 2
.definelabel POS_3, 3
.definelabel POS_4, 4

.definelabel THE_END, 0xFF

.org 0x087c7870
.align 4
bitmask_remainder:
bitmask_remainder_0:
    .db LEN_4BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 0
    .db LEN_4BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 1
    .db LEN_4BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 2
    .db LEN_4BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 3
    .db LEN_4BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 4
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 5
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 6
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 7
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 8
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 9
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 10
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 11
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 12
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 13
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 14
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 15
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 16
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 17
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 18
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 19
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 20
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 21
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 22
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 23
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 24
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 25
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 26
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 27
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 28
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 29
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 30
    .db LEN_1BITS,JUST_INSERT,0,LEN_0BITS,OP_ADD,2 ; 31
	.byte THE_END

bitmask_remainder_1:
    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4
	.byte THE_END

bitmask_remainder_2:
    .db LEN_2BITS,POS_1,OP_SUB,0x3E,LEN_2BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_2BITS,POS_1,OP_SUB,0x3A,LEN_2BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_2BITS,POS_1,OP_SUB,0x3A,LEN_2BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_2BITS,POS_1,OP_SUB,0x3A,LEN_2BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0JUST_INSERT,0x00 ; 4
	.byte THE_END
	
bitmask_remainder_3:
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 0
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 1
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 2
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 3
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 4
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 5
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 6
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 7
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 8
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 9
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 10
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 11
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 12
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 13
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 14
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 15
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 16
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 17
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 18
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 19
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 20
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 21
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 22
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 23
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 24
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 25
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 26
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 27
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 28
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 29
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 30
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 31
	
bitmask_remainder_4:
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 0
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 1
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 2
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 3
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 4
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 5
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 6
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 7
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 8
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 9
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 10
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 11
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 12
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 13
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 14
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 15
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 16
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 17
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 18
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 19
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 20
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 21
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 22
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 23
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 24
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 25
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 26
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 27
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 28
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 29
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 30
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 31
	
bitmask_remainder_5:
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 0
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 1
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 2
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 3
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 4
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 5
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 6
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 7
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 8
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 9
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 10
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 11
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 12
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 13
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 14
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 15
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 16
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 17
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 18
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 19
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 20
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 21
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 22
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 23
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 24
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 25
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 26
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 27
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 28
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 29
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 30
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 31
	
bitmask_remainder_6:
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 0
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 1
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 2
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 3
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 4
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 5
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 6
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 7
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 8
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 9
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 10
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 11
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 12
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 13
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 14
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 15
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 16
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 17
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 18
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 19
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 20
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 21
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 22
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 23
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 24
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 25
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 26
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 27
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 28
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 29
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 30
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 31
	
bitmask_remainder_7:
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 0
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 1
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 2
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 3
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 4
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 5
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 6
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 7
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 8
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 9
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 10
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 11
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 12
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 13
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 14
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 15
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 16
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 17
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 18
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 19
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 20
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 21
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 22
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 23
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 24
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 25
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 26
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 27
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 28
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 29
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 30
    .db 4,JUST_INSERT,0,0,OP_ADD,2 ; 31
.close