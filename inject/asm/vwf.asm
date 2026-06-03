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
	
;r0 = total remainder
;r1 = total remainder addr in ram
;r2 = prev width
;r3 = 8, and we store total after sub
store_total_remainder:
	cmp r2, 0x0
	beq reset_op_counter
	
	ldr r1, =total_remainder
	ldr r1, [r1]
	ldrb r0, [r1]
	
	;get remainder from prev width
	mov r3, 0x8
	sub r3, r2 ;8 - remainder, stored in r2
	add r0, r3 ;add to total remainder
	cmp r0, 0x8
	bge shave_remainder
	b store_remainder
shave_remainder:
	sub r0, 0x8
store_remainder:
	strb r0, [r1]

reset_op_counter:
	mov r0, 0x0
	ldr r1, =op_counter
	ldr r1, [r1]
	strb r0, [r1]

prepare_counter_skip:
	add r5, 1h
	add r6, 1h
    pop {r0, r1, r2, r3}
	ldr r3, =skip_the_counter
	ldr r3, [r3]
	mov pc, r3
    

;find a way if you can manage the push and pops better
draw:
    b prepare_operation_run
 

; r0 = halfword pulled from vram (dest)
; r1 = 2 byte (4 pixels) value from rom
; r2 = free
; r3 = vram addr to insert at. DO NOT FUCK WITH THIS UNLESS YOU MEANT IT
; r4 = total remainder, then the operation based on total remainder
; r5 = op counter
; r6 = counter (do not pop or edit this)
; r7 = free
; r8 = copy of halfword to insert
prepare_operation_run:
	push {r0, r1, r2, r4, r5, r7, r8, r11}
	mov r11, r14
	mov r8, r1
	
	; load total remainder
	ldr r4, =total_remainder
	ldr r4, [r4]
	ldrb r4, [r4]
	
	;load op counter
	ldr r5, =op_counter
	ldr r5, [r5]
	ldrb r5, [r5]
	
	mov r1, r8
	
	;cmp r4, 0x0
	;beq draw_normal
	
	;cmp r4, 0x1
	;beq handle_remainder1
	b handle_remainder
	
end_operations:
	;inc the op counter
	add r5, 0x1
	ldr r7, =op_counter
	ldr r7, [r7]
	strb r5, [r7]
	mov r14, r11
	pop {r0, r1, r2, r4, r5, r7, r8, r11}
    b pre_finale
	
draw_normal:
	strh r1, [r3, 0h]
    add r3, 2h
	mov r11, r14
	pop {r0, r1, r2, r4, r5, r7, r8, r11}
	b pre_finale
    
	
; r0 = halfword pulled from vram (dest)
; r1 = 2 byte (4 pixels) value from rom
; r2 = free
; r3 = vram addr to insert at. DO NOT FUCK WITH THIS UNLESS YOU MEANT IT
; r4 = total remainder, then the operation based on total remainder
; r5 = op counter
; r6 = main counter (do not pop or edit this)
; r7 = free
; r8 = copy of halfword to insert
handle_remainder:
	cmp r4, 0x0
	beq load_remainder1_op
	cmp r4, 0x1
	beq load_remainder1_op
	cmp r4, 0x2
	beq load_remainder1_op
	cmp r4, 0x3
	beq load_remainder1_op
	cmp r4, 0x4
	beq load_remainder1_op
	cmp r4, 0x5
	beq load_remainder1_op
	cmp r4, 0x6
	beq load_remainder1_op
	cmp r4, 0x7
	beq load_remainder1_op
run_loaded_operation_block:
	b run_operations
end_operation_block_run:
	b end_operations


; r0 = halfword pulled from vram (dest)
; r1 = 2 byte (4 pixels) value from rom
; r2 =  FREE TO USE
; r3 = vram addr to insert at. DO NOT FUCK WITH THIS UNLESS YOU MEANT IT
; r4 = FREE TO USE
; r5 = FREE TO USE
; r6 = main counter - needs to be intact at the end - FREE TO USE IF POPPED RESPONSIBLY
; r7 = op addr
; r8 = copy of halfword to insert

; struct InsertOrder {
	; int insertAmount (1-4 bits)
	; int insertpos (1-4)
	; int addOrSubtract (0=none, 1=add, 2=subtract)
	; int addOrSubtractAmount
	
	; int insertAmount (1-4 bits)
	; int insertpos (1-4)
	; int addOrSubtract (0=none, 1=add, 2=subtract)
	; int addOrSubtractAmount
	
	;int increment counter or not
; }
run_operations:
	push {r0, r1, r2, r3, r4, r5, r6, r11}
	mov r11, r14
	
	;handle vram pos 1
	ldrb r4, [r7, 0x2] ; add or subtract
	ldrb r5, [r7, 0x3] ; by how much?
	
	cmp r4, 0x1
	beq add_vram_1
	
	cmp r4, 0x2
	beq sub_vram_1
load_vram_to_r0_1:
	ldrh r0, [r3]
	
	;handle insert pos 1
	push {r2, r3}
	ldrb r2, [r7, 0x1]
	ldrb r3, [r7, 0x0]
	bl insert_at_position
	pop {r2, r3}
	strh r1, [r3, 0h]
	
	
	add r7, 0x4 ; inc read pos
	
	
	;handle vram pos 2
	ldrb r4, [r7, 0x2] ; add or subtract
	ldrb r5, [r7, 0x3] ; by how much?
	
	cmp r4, 0x1
	beq add_vram_2
	
	cmp r4, 0x2
	beq sub_vram_2
load_vram_to_r0_2:
	ldrh r0, [r3]
	
	;handle insert pos 2
	mov r1, r8
	push {r2, r3}
	ldrb r2, [r7, 0x1]
	ldrb r3, [r7, 0x0]
	bl insert_at_position
	pop {r2, r3}
	strh r1, [r3, 0h]
	
	add r7, 0x4
	
	mov r14, r11
	pop {r0, r1, r2, r3, r4, r5, r6, r11}
	
	;head into the finale to deal with the counter
	add r7, 0x1
	
	; handle counter
	ldrb r5, [r7]
	cmp r5, 0x1
	beq end_operation_block_run
	sub r6, 0x1 ;dec the main counter if we dont intend to inc it
	b end_operation_block_run

;r3 = vram addr
;r5 = add amt
add_vram_1:
	add r3, r5
	b load_vram_to_r0_1
	
sub_vram_1:
	sub r3, r5
	b load_vram_to_r0_1
	
	
add_vram_2:
	add r3, r5
	b load_vram_to_r0_2
	
sub_vram_2:
	sub r3, r5
	b load_vram_to_r0_2	

; r0 = halfword pulled from vram (dest)
; r1 = halfword pulled from rom (src)
; r2 = pos (from left to right as pixels - 12 34)
; r3 = len to insert (1-4)
; r4 = dest bitmask
; r5 = src bitmask
; at the end, r1 is the final thing 
; im gonna be real...i dont entirely understand why this works
insert_at_position:
    push    {r4, r5, lr}
	
	; src mask
    mov     r5, #0x1

    lsl     r4, r3, #0x2 ; r4 = len * 4
    lsl     r5, r4            

    sub     r5, #0x1          

    mov     r4, #0x5
    sub     r4, r2
    sub     r4, r3 ; r4 = 5 - pos - len

    lsl     r4, #0x2          
    lsl     r5, r4           

    ; dest mask = ~src mask & 0xffff (LITERALLY JUST BITFLIPPED)
    mov     r4, r5
    mvn     r4, r4
	; keep it 16bit boi
    lsl     r4, #0x10
    lsr     r4, #0x10

    and     r0, r4           
    and     r1, r5            
    orr     r1, r0  

    pop     {r4, r5, lr}
	
	

;operation loading
;r5 = counter
;r7 = base addr
;return r7 - starting addr of the operation block
load_remainder1_op:
	push {r5, r6}
	ldr r7, =ops_remainder_1
	
	; get starting addr
	mov r6, 0x9
	mul r5, r6
	add r7, r5
	
	pop {r5, r6}
	b run_loaded_operation_block
	
.pool


font_start:
	.word 0x080a2154
font_end:
	.word 0x080a392a

prev_widthOP_ADDr:
    .word 0x0202f2b0
total_remainder:
    .word 0x0202f2b4
op_counter:
	.word 0x0202f2b8
skip_the_counter:
	.word 0x08065f1c

	
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

.definelabel SKIP_COUNTERs_0x0, 0x0
.definelabel INC_COUNTERs_0x1, 0x1

.definelabel THE_END, 0xFF

.org 0x087c7870
.align 4
ops_remainder_1:
    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4
	
	.db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4
	
	.byte THE_END

ops_remainder_2:
    .db LEN_2BITS,POS_1,OP_SUB,0x3E,LEN_2BITS,POS_3,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_2BITS,POS_3,JUST_INSERT,0x0,LEN_2BITS,POS_1,OP_ADD,0x2,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4
	
	.db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4

    .db LEN_1BITS,POS_1,OP_SUB,0x3E,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 0
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 1
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 2
    .db LEN_1BITS,POS_1,OP_SUB,0x3A,LEN_3BITS,POS_2,OP_ADD,0x3E,INC_COUNTERs_0x1 ; 3
    .db LEN_0BITS,POS_0,OP_ADD,0x04,LEN_0BITS,POS_0,JUST_INSERT,0x00,SKIP_COUNTERs_0x0 ; 4
	
	.byte THE_END
	

.close