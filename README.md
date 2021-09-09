## autoUniCalendar
An awesome script to convert the University Of Oviedo web calendar to Google or Outlook calendars.

![](/assets/cat.jpg)
![](/assets/script.jpg)

## Español

El script utiliza la cookie de sesión del usuario para acceder a los datos de su calendario tramitando solicitudes GET y POST al servidor de la Universidad de Oviedo.
Estas solicitudes fueron analizadas y automatizadas en el script utilizando Burpsuite y la librería requests de Python, necesaria para el funcionamiento del programa.

Puede instalarse con `python3 -m pip install requests` en Windows o `pip install requests` en Linux

![](/assets/burp.jpg)

Para ejecutar el script, son necesarios dos parámetros. El procedimiento para obtenerlos es muy sencillo, se debe entrar en el [SIES](https://sies.uniovi.es/serviciosacademicos/web/expedientes/calendario.xhtml), autenticarse normalmente, acceder al calendario, y presionar `F12`. Según el navegador, dirijirse a `Almacenamiento --> Cookies` y copiar los dos valores.

![](/assets/cookies.jpg)

Una vez hecho esto, se puede ejecutar el programa abriendo una consola en la carpeta donde esté ubicado el script y ejecutando el comando `python3 autoUniCalendar.py <JSessionID> <RenderToken>`. El script generará un archivo .CSV que puede ser leído y procesado tanto por Outlook como por Google Calendar, y posiblemente otros calendarios.
