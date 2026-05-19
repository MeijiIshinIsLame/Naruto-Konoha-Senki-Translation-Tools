**How reading a dialog cutscene works**

The opcode processor is the label at 080977e0

Works like this:
Read first opcode, process it, then move to next.


**Opcodes**

| Opcode | Bytes read | Effect                                    |
| :----- | :--------- | :---------------------------------------- |
| 0x0    | 1          | Read next byte for opcode                 |
| 0x1    | Unknown    | Unknown                                   |
| 0x2    | 2          | Display character icon on left side       |
| 0x3    | Unknown    | Unknown                                   |
| 0x4    | Unknown    | Unknown                                   |
| 0x5    | Unknown    | Unknown                                   |
| 0x6    | Unknown    | Unknown                                   |
| 0x7    | Unknown    | Unknown                                   |
| 0x8    | 2          | Display character icon on right side      |
| 0x9    | Unknown    | Unknown                                   |
| 0xA    | Unknown    | Unknown                                   |
| 0xB    | Unknown    | Unknown                                   |
| 0xC    | Unknown    | Unknown                                   |
| 0xD    | Unknown    | Unknown                                   |
| 0xE    | Unknown    | Unknown                                   |
| 0xF    | Unknown    | Unknown                                   |
| 0x10   | Unknown    | Unknown                                   |
| 0x11   | Unknown    | Unknown                                   |
| 0x12   | Unknown    | Unknown                                   |
| 0x13   | Unknown    | Unknown                                   |
| 0x14   | Unknown    | Unknown                                   |
| 0x15   | 2          | Select music and addr for dialog cutscene |
| 0x16   | Unknown    | Unknown                                   |
| 0x17   | Unknown    | Unknown                                   |
| 0x18   | Unknown    | Unknown                                   |
| 0x19   | 3          | Go to scene select                        |
| 0x1A   | Unknown    | Unknown                                   |
| 0x1B   | 2          | Choose music then run next opcode         |
| 0x1C   | Unknown    | Unknown                                   |
| 0x1D   | Unknown    | Unknown                                   |
| 0x1E   | Unknown    | Unknown                                   |
| 0x1F   | Unknown    | Unknown                                   |
| 0x20   | Dynamic    | Display custom name                       |
| 0x21   | Unknown    | Unknown                                   |
| 0x22   | Unknown    | Unknown                                   |
| 0x23   | Unknown    | Unknown                                   |
| 0x24   | 0    | Default failsafe that forces stage select or read next opcode                                  |
| 0x32   | Unknown    | Unknown                                   |
| 0x33   | Unknown    | Unknown                                   |
| 0x34   | Unknown    | Unknown                                   |
| 0x35   | Unknown    | Unknown                                   |
| 0x36   | Unknown    | Unknown                                   |
| 0x37   | Unknown    | Unknown                                   |
| 0x38   | Unknown    | Unknown                                   |
| 0x39   | Unknown    | Unknown                                   |
