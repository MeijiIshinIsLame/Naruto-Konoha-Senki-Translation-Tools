
vram = 0x06002220

JUST_INSERT = 0
OP_ADD = 1
OP_SUB = 2

LEN_0BITS = 0
LEN_1BITS = 1
LEN_2BITS = 2
LEN_3BITS = 3
LEN_4BITS = 4

bitmask_remainder = [
    ((LEN_2BITS, OP_SUB, 0x3E), (LEN_2BITS, OP_ADD, 0x3E)),  # 0
    ((LEN_2BITS, OP_ADD, 0x1), (LEN_2BITS, OP_ADD, 0x3E)),  # 1
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 2
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 3
    ((LEN_0BITS, OP_ADD, 0x4), (LEN_0BITS, JUST_INSERT, 0x0)),  #4,  add some extra
    
    ((LEN_2BITS, OP_SUB, 0x3E), (LEN_2BITS, OP_ADD, 0x3E)),  # 0
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 1
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 2
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 3
    ((LEN_0BITS, OP_ADD, 0x4), (LEN_0BITS, JUST_INSERT, 0x0)),  #4,  add some extra
    
    ((LEN_2BITS, OP_SUB, 0x3E), (LEN_2BITS, OP_ADD, 0x3E)),  # 0
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 1
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 2
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 3
    ((LEN_0BITS, OP_ADD, 0x4), (LEN_0BITS, JUST_INSERT, 0x0)),  #4,  add some extra
    
    ((LEN_2BITS, OP_SUB, 0x3E), (LEN_2BITS, OP_ADD, 0x3E)),  # 0
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 1
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 2
    ((LEN_2BITS, OP_SUB, 0x3A), (LEN_2BITS, OP_ADD, 0x3E)),  # 3
    ((LEN_0BITS, OP_ADD, 0x4), (LEN_0BITS, JUST_INSERT, 0x0)),  #4,  add some extra
]

for i, run in enumerate(bitmask_remainder):
    length, op, amount = run[0]
    
    if op == OP_ADD:
        vram = vram + amount
    if op == OP_SUB:
        vram = vram - amount
    
    print(f"run: {i}")
    print(f"length: {length}")
    print(f"operation: {i}")
    print(f"amount: {hex(amount)}")
    print(f"VRAM: {hex(vram)}")
    print("---------------------------")
    
    length, op, amount = run[1]
    
    if op == OP_ADD:
        vram = vram + amount
    if op == OP_SUB:
        vram = vram - amount
    
    print(f"run: {i}")
    print(f"length: {length}")
    print(f"operation: {i}")
    print(f"amount: {hex(amount)}")
    print(f"VRAM: {hex(vram)}")
    print("---------------------------")