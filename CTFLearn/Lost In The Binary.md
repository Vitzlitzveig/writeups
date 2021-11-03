Этот флаг будет бесячий до жути

Имеем бинарник `lost_in_bin`, который при запуске требует некий пароль:

	$ ./lost_in_bin 
	password : 12345
	bad password!

Недого думая, скармливаем его Гидре, находим main, и после некоторых переименований переменных получаем исходник:

```c
undefined8 _main(int argc,char **argv)
{
    int iVar1;
    long lVar2;
    size_t pass_len;
    int n;
    int j;
    int i;
    int m;
    int k;
    
    lVar2 = ptrace(PTRACE_TRACEME,0,0,0);
    if (lVar2 != -1) {
        if (argc < 5) {
            printf("password : ");
            __isoc99_scanf(&DAT_00400e7d,&pass_inp);
            pass_len = strlen(&pass_inp);
            if (pass_len < 17) {
                for (i = 0; pass_len = strlen(&pass_inp), (ulong)(long)i < pass_len; i = i + 1) {
                    (&pass_inp)[i] = (&pass_inp)[i] ^ 2;
                    (&pass_inp)[i] = (&pass_inp)[i] + '\x01';
                    (&pass_inp)[i] = ~(&pass_inp)[i];
                }
                iVar1 = memcmp(&pass_inp,pass_hash,9);
                if (iVar1 == 0) {
                    for (j = 0; pass_len = strlen((char *)flag_hash1), (ulong)(long)j < pass_len; j = j + 2) {
                        flag_hash1[j] = flag_hash1[j] ^ 0x45;
                        flag_hash1[j + 1] = flag_hash1[j + 1] ^ 0x26;
                    }
                    puts((char *)flag_hash1);
                }
                else {
                    puts("bad password!");
                }
                return 0;
            }
            puts("the password must be less than 16 character");
            exit(1);
        }
        arg1 = strtol(argv[1],(char **)0x0,10);
        if (((((arg1 != 0) && (arg2 = strtol(argv[2],(char **)0x0,10), arg2 != 0)) &&
                 (arg3 = strtol(argv[3],(char **)0x0,10), arg3 != 0)) &&
                ((arg4 = strtol(argv[4],(char **)0x0,10), arg4 != 0 &&
                 (arg4 * -0xc + arg1 * -0x18 + arg2 * -0x12 + arg3 * -0xf == -0x47d9)))) &&
             ((arg4 * -9 + (arg1 + arg2) * 0x12 + arg3 * 9 == 0x1143 &&
                ((arg4 * 2 + arg1 * 0x10 + arg2 * 0xc + arg3 * 4 == 0x1c84 &&
                 (arg4 * -0xb + (arg1 + arg2) * -6 + arg3 * -3 == -0x21a5)))))) {
            argsum = (arg1 * arg2 + arg3) - arg4;
            sprintf(&argsum_str,"%06x",argsum);
            pass_len = strlen(&argsum_str);
            MD5(&argsum_str,pass_len,&md5);
            for (n = 0; n < 16; n = n + 1) {
                sprintf(&flag_hash2 + n * 2,"%02x",(ulong)(byte)(&md5)[n]);
            }
            printf(PTR_s_FLAG-%s_00602080,&flag_hash2);
            exit(0);
        }
    }
    printf("password : ");
    __isoc99_scanf(&DAT_00400e7d,&pass_inp);
    pass_len = strlen(&pass_inp);
    if (16 < pass_len) {
        puts("the password must be less than 16 character");
        exit(1);
    }
    for (k = 0; pass_len = strlen(&pass_inp), (ulong)(long)k < pass_len; k = k + 1) {
        (&pass_inp)[k] = (&pass_inp)[k] ^ 6;
    }
    iVar1 = memcmp(&pass_inp,s_7Yq2hrYRn5Y`jga_00602090,16);
    if (iVar1 != 0) {
        puts("bad password!");
        exit(0);
    }
    pass_len = strlen(&pass_inp);
    MD5(&pass_inp,pass_len,&md5);
    for (m = 0; m < 0x10; m = m + 1) {
        sprintf(&flag_hash2 + m * 2,"%02x",(ulong)(byte)(&md5)[m]);
    }
    printf(PTR_s_FLAG-%s_00602080,&flag_hash2);
	exit(0);
}
```

Из этой простыни бросаются в глаза следующие части:
```c
lVar2 = ptrace(PTRACE_TRACEME,0,0,0);
if (lVar2 != -1) { ... }
```
Защита от дебага. Когда дебаггер отслвеживает эту программу, ptrace возвращает -1. Поэтому программа за пределами этого `if` нас не интересует.

Далее идёт проверка на число аргументов: если их меньше 5, то выполняется проверка пароля, и в случае удачи с помощью `xor` расшифровывается строка, хочется верить, флага:
```c
for (j = 0; pass_len = strlen((char *)flag_hash1), (ulong)(long)j < pass_len; j = j + 2) {
	flag_hash1[j] = flag_hash1[j] ^ 0x45;
	flag_hash1[j + 1] = flag_hash1[j + 1] ^ 0x26;
}
puts((char *)flag_hash1);
```

Простым скриптом восстанавливаем содержимое строки:
```python3
flag_hash1 = r'(O6U,H\"",06h,"$T\"S(C+R6&'
flag_hash1 = bytes(flag_hash1, 'ascii')
farr = [chr(a^0x45)+chr(b^0x26) for a,b in zip(flag_hash1[0::2], flag_hash1[1::2])]
s = ''.join(farr)
print(s)
# 'missin\x19\x04g\nu\x10-\ng\x02\x11zguments\x00'
```

За исключением некоторых символов, строка прекрасно читается: missing arguments. Значит нужно добавить аргументы, которые проверит следующий код:
```c
    arg1 = strtol(argv[1],(char **)0x0,10);
    if (((((arg1 != 0) && (arg2 = strtol(argv[2],(char **)0x0,10), arg2 != 0)) &&
         (arg3 = strtol(argv[3],(char **)0x0,10), arg3 != 0)) &&
        ((arg4 = strtol(argv[4],(char **)0x0,10), arg4 != 0 &&
         (arg4 * -0xc + arg1 * -0x18 + arg2 * -0x12 + arg3 * -0xf == -0x47d9)))) &&
       ((arg4 * -9 + (arg1 + arg2) * 0x12 + arg3 * 9 == 0x1143 &&
        ((arg4 * 2 + arg1 * 0x10 + arg2 * 0xc + arg3 * 4 == 0x1c84 &&
         (arg4 * -0xb + (arg1 + arg2) * -6 + arg3 * -3 == -0x21a5)))))) { ... }
```

что можно преобразовать в

```c
arg1 = strtol(argv[1],(char **)0x0,10);
arg2 = strtol(argv[2],(char **)0x0,10);
arg3 = strtol(argv[3],(char **)0x0,10);
arg4 = strtol(argv[4],(char **)0x0,10);

if (((arg1 != 0) && (arg2 != 0)) && (arg3 != 0) && (arg4 != 0))
if ((arg4 * -0xc + arg1 * -0x18 + arg2 * -0x12 + arg3 * -0xf == -0x47d9) &&
    (arg4 * -9   + arg1 *  0x12 + arg2 *  0x12 + arg3 *    9 ==  0x1143) &&
    (arg4 * 2    + arg1 *  0x10 + arg2 *  0xc  + arg3 *    4 ==  0x1c84) &&
    (arg4 * -0xb + arg1 *    -6 + arg2 * -6    + arg3 *   -3 == -0x21a5)) 
{ ... }
```

Ба! Да это же система линейных уравнений! Решаем:

```python3
import numpy as np
v1 = np.array([-0xc, -0x18, -0x12, -0xf])
v2 = np.array([-9, 0x12, 0x12, 9])
v3 = np.array([2, 0x10, 0xc, 4])
v4 = np.array([-0xb, -6, -6, -3])
A = np.array([v1, v2, v3, v4])
b = np.array([-0x47d9, 0x1143, 0x1c84, -0x21a5])
x = np.linalg.solve(A, b)
print(x)
# [510. 227. 115. 317.]

```

Запускаем (аргументы в коде перепутаны: arg4, arg1, arg2, arg3), иии...
```bash
$ ./lost_in_bin 227 115 317 510
FLAG-21a84f2c7c7fd432edf1686215db05ea
```

Готово
