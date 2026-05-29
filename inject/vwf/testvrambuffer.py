def bit_clear(number, position):
    mask = 1 << position
    return number & (~mask)

widths = [8, 8, 6]
offset_flag = 0

vram_addr = 0x060021a0
remainder_vram_adr = 0x060021a0
size = 32
j = 0

vrams = [vram_addr, vram_addr]

for width in widths:
    counter = 1
    if width < 8 and offset_flag == 0:
        print("OFFSET FLAG SET")
        offset_flag = 1
    while counter <= size:
        if offset_flag == 1:
            remainder = 0x8 - width
            the_rest = 0x4 - remainder
            if j == 0:
                print(the_rest)
                remainder_vram_addr = (vram_addr - 0x20) + the_rest
                print("-")
                print(f"width: {width} | iteration {counter} | remainder {remainder} | the_rest {the_rest}")
                print(f"insert positions: {remainder} at {hex(remainder_vram_addr)} | {the_rest} at {hex(vram_addr)}")
                vram_addr += bit_clear(remainder, 1)
            if j == 1:
                remainder_vram_addr = vram_addr
                vram_addr = vram_addr + 1
                print("-")
                print(f"width: {width} | iteration {counter} | remainder {remainder} | the_rest {the_rest}")
                print(f"insert positions: {remainder} at {hex(remainder_vram_addr)} | {the_rest} at {hex(vram_addr)}")
                remainder_vram_addr = vram_addr
                vram_addr += bit_clear(remainder , 1)
            j += 1
            if j ==  2:
                j = 0
        else:
            print(f"width: {width} | iteration {counter} | remainder 0 | the_rest 4 | remainder_vram_addr None | vram_addr {hex(vram_addr)}")
            vram_addr += 2
        counter += 1
    print("################################################")