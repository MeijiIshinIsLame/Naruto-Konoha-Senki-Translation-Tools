from colorama import Fore,  Back, Style
import io
from pathlib import Path

file = Path("C:/projs/Naruto-Romhack/game/Naruto - Konoha Senki English translation.gba")

registers = {
    'r0':  0x085AEA23,
    'r1':  0x00000081,
    'r2':  0x085AEA23,
    'r3':  0x00000000,
    'r4':  0x00000002,
    'r5':  0x00000000,
    'r6':  0x0200A8A4,
    'r7':  0x08060D54,
    'r8':  0x08060D54,
    'r9':  0x08060D54,
    'r10': 0x00000000,
    'r11': 0x00000000,
    'r12': 0x00000000,
    'r13': 0x030011B8,
    'r14': 0x080978F9,
    'r15': 0x080662FA,
    'cpsr': 0x8000003F,
    'spsr': 0x0000001F
}

# Simulated memory stack
stack = []

def asm_to_json(file):
    with open(file, 'r') as f:
        pass


def adc(): pass


def add(): pass    


def and_(): pass


def asr(): pass


def b(): pass


def bic(): pass


def bl(): pass


def bx(): pass


def cmn(): pass


def cmp(): pass


def eor(): pass


def ldmia(): pass


def ldr(): pass


def ldrb(): pass


def ldrh(): pass


def ldrsb(): pass


def ldrsh(): pass


def lsl(): pass


def lsr(): pass


def mov(): pass


def mul(): pass


def mvn(): pass


def neg(): pass


def orr(): pass


def pop(): pass


def push(): pass


def ror(): pass


def sbc(): pass


def stmia(): pass


def str(): pass


def strb(): pass
def tst(): pass

# PUSH: emulate "STMFD SP!, {rX...}"
def push(*regs):
    for r in regs:
        val = registers[r]
        stack.append(val)
        registers['r13'] -= 4  # ARM stacks grow downward
    print(f"PUSH {regs} -> stack: {[hex(x) for x in stack]}")

# POP: emulate "LDMFD SP!, {rX...}"
def pop(*regs):
    for r in reversed(regs):  # reverse order to simulate LDM
        val = stack.pop()
        registers[r] = val
        registers['r13'] += 4
    print(f"POP {regs} -> stack: {[hex(x) for x in stack]}")
    

def print_with_focus(*focus_regs):
    for k, v in registers.items():
        if k in focus_regs:
            print(Fore.RED + f"{k}: {hex(v)}")
        else:
            print(Style.RESET_ALL + f"{k}: {hex(v)}")

def ldr(addr):
    with open(file, 'rb') as f:
        f.seek(addr)
        data = f.read(4)
        value = int.from_bytes(data, "little")
        return value

############### MAIN ###############
push("r6", "r7")
print_with_focus("r6")
registers['r6'] = 0x085A57D0
print_with_focus("r6")
registers['r6'] = ldr(registers['r6'] - 0x08000000)
print_with_focus("r6")
"""
.org 0x0806627e
    bl namelabel_check

.org 0x0809E700
namelabel_check:
    push {r6, r7}
    ldr r6, =lower_addr
    ldr r6, [r6]
    ldr r7, =higher_addr
    ldr r7, [r7]

    cmp r2, r6
    blt return_lr
    cmp r2, r7
    bge return_lr

    push {r3}
    ;ldrb r0, [r0]
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
	mov r3, 1Fh
    add r0, r0, r3
    b end_check

lower_sjis:
	mov r3, 20h
    add r0, r0, r3

end_check:
    pop {r3}
return_lr:
    pop {r6, r7}
	;ldrb r0, [r2]
    bx lr

.pool
lower_addr: .word 0x085A57D0
higher_addr: .word 0x085A632F

.close
"""