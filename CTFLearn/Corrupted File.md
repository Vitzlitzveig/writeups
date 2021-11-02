У нас в распоряжении есть файл [unopenable .gif](https://mega.nz/#!aKwGFARR!rS60DdUh8-jHMac572TSsdsANClqEsl9PD2sGl-SyDk). Попытка его открыть заканчивается предсказуемой неудачей. Лезем, смотрим, что в нём не так:

	$ hexedit unopenable.gif 
	9a..........:....::.:f..f.:..f.:. ...

Если сравнить начало файла со [спецификацией GIF](https://en.wikipedia.org/wiki/GIF#Example_GIF_file), то можно заметить недостающие 

	GIF8

Дописываем с помощью gedit, полчучаем рабочую анимацию с текстом:

	the flag is
	ZmxhZ3tn
	MWZfb3
	JfajFmfQ==
	DECODE IT

Расшифровываем:
	$ echo ZmxhZ3tnMWZfb3JfajFmfQ== | base64 -d
	flag{g1f_or_j1f}
