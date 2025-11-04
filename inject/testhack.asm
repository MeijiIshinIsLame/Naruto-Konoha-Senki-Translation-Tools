.gba
.open "{source}", "{dest}", 0x08000000

//============== HOOK ======================
.org 0x080662fa
    bl namelabel_check
    pop {r6, r7}

.org 0x0809E700
namelabel_check:
    push {r6, r7}
    ldr r6, =lower_addr
    ldr r6, [r6]
    ldr r7, =higher_addr
    ldr r7, [r7]

    cmp r0, r6
    blt return_lr
    cmp r0, r7
    bge return_lr

    push {r3}
    ldrb r0, [r0]
    cmp r0, 0x40
    blt end_check
    cmp r0, 0x5A
    blt upper_sjis
    cmp r0, 0x60
    blt end_check
    cmp r0, 0x7A
    blt lower_sjis
    b end_check

upper_sjis:
    add r0, r0, #0x1F
    b end_check

lower_sjis:
    add r0, r0, #0x20

end_check:
    pop {r3}
return_lr:
    pop {r6, r7}
    bx lr

.pool
lower_addr: .word 0x085A57D0
higher_addr: .word 0x085A632F

.close