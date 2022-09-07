## autoUniCalendar

Un script en Python para convertir el calendario de la intranet de la Universidad de Oviedo en un calendario de Outlook o Google Calendar.

![](/assets/cat.jpg)
![](/assets/script.jpg)

## Explicación e instalación

El script utiliza la cookie de sesión del usuario para acceder a los datos de su calendario tramitando solicitudes GET y POST al servidor de la Universidad de Oviedo.
Estas solicitudes fueron analizadas y automatizadas en el script utilizando Burpsuite y las librerías `requests` e `ics` de Python, necesarias para el funcionamiento del programa.

Puede instalarse con `python3 -m pip install <librería>` en Windows o `pip install <librería>` en Linux

![](/assets/burp.jpg)

Para ejecutar el script, es. El procedimiento para obtenerlos es muy sencillo, se debe entrar en el [SIES](https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml), autenticarse normalmente, acceder al calendario, y presionar `F12`. Según el navegador, dirijirse a `Almacenamiento --> Cookies` y copiar los dos valores, JSESSIONID y oam.Flash.RENDERMAP.TOKEN, pues son los parámetros del comando para ejecutar el script.

![](/assets/cookies.jpg)

Una vez hecho esto, se puede ejecutar el programa abriendo una consola en la carpeta donde esté ubicado el script y ejecutando el comando `python3 autoUniCalendar.py <JSessionID>`. El script generará un archivo .ics que puede ser leído y procesado tanto por Outlook como por Google Calendar, y posiblemente otros calendarios.
