.gba
.thumb

.open "{source}","{dest}",0x08000000

.org 0x08065f4c
    bl entry

.org 0x08065f5a
    cmp r6, 0x10

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
    bne draw

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

    cmp r2, 0h
    beq reset_vwf_state
    cmp r2, 8h
    beq reset_vwf_state

add_to_total_remainder:
    push {r4, r5, r6, r7}

    mov r5, 8h
    sub r5, r2

    ldr r6, =total_remainder
    ldr r6, [r6]
    ldrb r4, [r6]

    add r4, r5
    strb r4, [r6]

    pop {r4, r5, r6, r7}

set_offset_flag:
    ldr r0, =offset_flag
    ldr r0, [r0]

    ldr r1, =total_remainder
    ldr r1, [r1]
    ldrb r2, [r1]

    cmp r2, 0h
    beq clear_flag_only

    mov r3, 1h
    strb r3, [r0]
    b reset_draw_vars

clear_flag_only:
    mov r3, 0h
    strb r3, [r0]
    b reset_draw_vars


reset_vwf_state:
    ldr r0, =offset_flag
    ldr r0, [r0]
    mov r1, 0h
    strb r1, [r0]

    ldr r0, =total_remainder
    ldr r0, [r0]
    strb r1, [r0]

reset_draw_vars:
    ldr r0, =pixels_drawn
    ldr r0, [r0]
    mov r1, 0h
    strb r1, [r0]

    ldr r0, =last_4bit_pos
    ldr r0, [r0]
    strb r1, [r0]

    ldr r0, =drawing_backwards_flag
    ldr r0, [r0]
    strb r1, [r0]

prepare_counter_skip:
    add r5, 1h
    add r6, 1h

    pop {r0, r1, r2, r3}

    ldr r3, =skip_the_counter
    ldr r3, [r3]
    mov pc, r3


draw:
    ldr r0, =prev_width_addr
    ldr r0, [r0]
    ldrb r0, [r0]

    cmp r0, 0h
    beq draw_normal

    cmp r0, 8h
    beq draw_normal

    b draw_from_pos


draw_from_pos:
    push {r0, r1, r2, r3, r4, r5, r6, r7, lr}

    mov r7, r1

load_last_values:
    ldr r2, =last_4bit_pos
    ldr r2, [r2]
    ldrb r2, [r2]

    ldr r4, =pixels_drawn
    ldr r4, [r4]
    ldrb r4, [r4]

    mov r5, 0h

start_drawing:
    mov r1, r7

    add r2, 1h
    cmp r2, 4h
    bls pos_ok

    mov r2, 1h
    add r5, 1h

pos_ok:
    add r4, 1h

calculate_addr:
    push {r0, r1, r5, r7}

    mov r1, 8h

    ldr r0, =prev_width_addr
    ldr r0, [r0]
    ldrb r0, [r0]

    sub r1, r0

    ldr r5, =drawing_backwards_flag
    ldr r5, [r5]
    ldrb r7, [r5]

    cmp r7, 2h
    beq insert_the_bits

    cmp r4, r1
    bls should_be_back

should_be_forward:
    cmp r7, 1h
    bne mark_addr_done

    add r3, 40h
    sub r3, r1
    mov r2, 1h

mark_addr_done:
    mov r7, 2h
    strb r7, [r5]
    b insert_the_bits

should_be_back:
    cmp r7, 0h
    bne insert_the_bits

    sub r3, 40h
    add r3, r1

    mov r7, 1h
    strb r7, [r5]
    mov r2, 1h

insert_the_bits:
    pop {r0, r1, r5, r7}

    ldrh r0, [r3]
    bl insert_bit_at_position
    strh r1, [r3]

    cmp r5, 4h
    bls start_drawing

cleanup:
    add r3, 2h

store_relevant_values:
    ldr r6, =last_4bit_pos
    ldr r6, [r6]
    strb r2, [r6]

    ldr r7, =pixels_drawn
    ldr r7, [r7]

    cmp r4, 8h
    blo store_pixels_drawn
    mov r4, 0h

store_pixels_drawn:
    strb r4, [r7]

exit_draw:
    pop {r0, r1, r2, r3, r4, r5, r6, r7, pc}


draw_normal:
    strh r1, [r3]
    add r3, 2h
    b pre_finale


insert_bit_at_position:
    push {r3, r4, r5}

    mov r3, 2h
    mul r3, r2

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

prev_width_addr:
    .word 0x0202f2b0

last_4bit_pos:
    .word 0x0202f2b4

total_remainder:
    .word 0x0202f2b8

pixels_drawn:
    .word 0x0202f2bc

offset_flag:
    .word 0x0202f2c0

skip_the_counter:
    .word 0x08065f5a

drawing_backwards_flag:
    .word 0x0202f2cb


bitmask_pos_dest:
    .halfword 0x0000
    .halfword 0x0fff
    .halfword 0xf0ff
    .halfword 0xff0f
    .halfword 0xfff0

bitmask_pos_src:
    .halfword 0x0000
    .halfword 0xf000
    .halfword 0x0f00
    .halfword 0x00f0
    .halfword 0x000f

.close