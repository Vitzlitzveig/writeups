Что тут у нас? Камень ножницы бумага! Лезем по указанному адресу и видим:

```
$ nc 138.197.193.132 5002
----------- Let's play rock, paper, twister!
----------- Beat me 30 times in a row to win the flag, but this time, im going to be a little less predictable!!

Please choose: R / P / S
>>>R
You won! Consecutive wins: 1
I chose S based on 1702742885
Please choose: R / P / S
>>>P
You didn't win!
I chose P based on 1976601634
Please choose: R / P / S
>>>S
You won! Consecutive wins: 1
I chose P based on 2898038923
Please choose: R / P / S
>>>
```

Сервер играет в игру, запрашивая наш ход и выдавая ответ, основанный на числе. Небольшое исследование показывает, что ход компьютера выбирается остатком по модулю 3 от числа. Чтобы победить, надо угадать его ход 30 раз подряд! Причём природа числа неизвестна. Но попробуем угадать:
1. Числа выглядят довольно случайными, скорее всего, создаются каким-нибудь генератором случайных чисел.
2. Приглашение к ходу `>>>` скорее всего намекает на python. Но ведь в стандартном генераторе питона есть известная уязвимость! 

Для эксплуатации уязвимости нужен модуль `randcrack` и 624 числа, созданных генератором подряд. Мы можем сделать 624 тестовых запроса, а потом победить. Пишем код:

```python3
#!/usr/bin/env python3
import socket
from randcrack import RandCrack

def int2c(n:int):
    return "RPS"[n%3]

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('138.197.193.132', 5002))
    randoms = []
    # Pass the header
    data = str(s.recv(1024), 'ascii')
    data = str(s.recv(1024), 'ascii')
    for c in ['R']*624:
        s.sendall(bytes(c+'\n', 'ascii'))
        data = ''
        while 1:
            data += str(s.recv(1024), 'ascii')
            if data.count('>>>'): break
        print(data)
        randoms.append(int(data.split('based on ')[1].split()[0]))

    print(randoms)
    rc = RandCrack()
    for n in randoms: rc.submit(n)

    next30 = [rc.predict_getrandbits(32) for i in range(30)]
    for n in next30:
        c = int2c(n+1)
        s.sendall(bytes(c+'\n', 'ascii'))
        data = ''
        while 1:
            data = str(s.recv(1024), 'ascii')
            print(data)
            if data.count('>>>') or data.count('CTF'): break

    data += str(s.recv(1024), 'ascii')
    print(data)

    s.shutdown(socket.SHUT_WR)
    s.close()
```

запускаем и идём пить чай. Через несколько минут видим флаг на мониторе:
```
...
You won! Consecutive wins: 25

I chose P based on 280402615
Please choose: R / P / S
>>>
You won! Consecutive wins: 26

I chose S based on 1058210939
Please choose: R / P / S
>>>
You won! Consecutive wins: 27

I chose S based on 1537858085
Please choose: R / P / S
>>>
You won! Consecutive wins: 28

I chose P based on 2447992705
Please choose: R / P / S
>>>
You won! Consecutive wins: 29

I chose P based on 1897907512
Please choose: R / P / S
>>>
You won! Consecutive wins: 30
I chose S based on 3281852315
Wow, you're good, here's your flag!
CTFlearn{m3rs3nn3_kind4_c00l}
```
