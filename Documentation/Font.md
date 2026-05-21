**The motha fuckin font**

The draw and checks for 2byte vs 1byte is basically FUN_08065eb8

The image data is called at 08065ef6

by the time you get to 08065ef6 the registers tell the whole story
![Regs](Images/Screenshot.png)
03001170 is where initial vram drawtile loc is stored

formula to get character pixels from rom is:
```
r0 = sjis 2bytes (ex: 8340) 

r5 = 0x8367 (no idea what this represents lol, its actually a different number every time but it doesnt seem to matter much so watever)

start_of_2byte_sjis = 0809d954

r5 - r0 LSL0x5 + 0x0809d954

```

putting the whole draw thing here for personal reference

``` 

                             draw_pixel_in_vram_as_tile_08065flc             XREF[1]:     08065f5c(j)  
        08065f1c 23 68           ldr        r3,[r4,#0x0]=>local_30
                             **************************************************************
                             * load byte from font image, aka 4 pixels                    *
                             **************************************************************
        08065f1e 2a 78           ldrb       r2,[r5,#0x0]
                             **************************************************************
                             * do a bunch of calculations to convert it from 4bpp to s... *
                             **************************************************************
        08065f20 03 21           mov        r1,#0x3
        08065f22 11 40           and        r1,r2
        08065f24 57 46           mov        r7,r10
        08065f26 39 43           orr        r1,r7
        08065f28 0c 20           mov        r0,#0xc
        08065f2a 10 40           and        r0,r2
        08065f2c 4f 46           mov        r7,r9
        08065f2e 38 43           orr        r0,r7
        08065f30 80 00           lsl        r0,r0,#0x2
        08065f32 01 43           orr        r1,r0
        08065f34 30 20           mov        r0,#0x30
        08065f36 10 40           and        r0,r2
        08065f38 47 46           mov        r7,r8
        08065f3a 38 43           orr        r0,r7
        08065f3c 00 01           lsl        r0,r0,#0x4
        08065f3e 01 43           orr        r1,r0
        08065f40 c0 20           mov        r0,#0xc0
        08065f42 10 40           and        r0,r2
        08065f44 62 46           mov        r2,r12
        08065f46 10 43           orr        r0,r2
        08065f48 80 01           lsl        r0,r0,#0x6
        08065f4a 01 43           orr        r1,r0
                             **************************************************************
                             * BOOM store the pixel in VRAM                               *
                             **************************************************************
        08065f4c 19 80           strh       r1,[r3,#0x0]
        08065f4e 02 33           add        r3,#0x2
        08065f50 23 60           str        r3,[r4,#0x0]=>local_30
        08065f52 01 35           add        r5,#0x1
        08065f54 70 1c           add        r0,r6,#0x1
        08065f56 00 06           lsl        r0,r0,#0x18
        08065f58 06 0e           lsr        r6,r0,#0x18
        08065f5a 0f 2e           cmp        r6,#0xf
        08065f5c de d9           bls        draw_pixel_in_vram_as_tile_08065flc
        08065f5e 03 9f           ldr        r7,[sp,#local_24]
        08065f60 38 06           lsl        r0,r7,#0x18
        08065f62 01 0e           lsr        r1,r0,#0x18
        08065f64 01 29           cmp        r1,#0x1
        08065f66 d3 d9           bls        LAB_08065f10
        08065f68 01 20           mov        r0,#0x1
        08065f6a 02 e0           b          LAB_08065f72
 

```