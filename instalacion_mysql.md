# Guía de Instalación: MySQL Server, MySQL Workbench y DataGrip

**Taller: Desarrollo Web con Python — Sesión 1**
**Sistemas cubiertos: Windows 10/11 · Ubuntu 22.04 / 24.04 LTS**

---

## Tabla de Contenidos

1. [MySQL Server en Windows](#1-mysql-server-en-windows)
2. [MySQL Workbench en Windows](#2-mysql-workbench-en-windows)
3. [Variables de Entorno en Windows](#3-variables-de-entorno-de-mysql-en-windows)
4. [MySQL Server en Ubuntu](#4-mysql-server-en-ubuntu)
5. [MySQL Workbench en Ubuntu](#5-mysql-workbench-en-ubuntu)
6. [DataGrip en Windows](#6-datagrip-en-windows)
7. [DataGrip en Ubuntu](#7-datagrip-en-ubuntu)
8. [Errores Comunes y Soluciones](#8-errores-comunes-y-soluciones)

---

## 1. MySQL Server en Windows

### 1.1 Requisitos previos

- Windows 10 version 1903 o superior, o Windows 11
- Cuenta con privilegios de administrador
- Microsoft Visual C++ Redistributable 2019 o superior instalado
- Al menos 1 GB de espacio libre en disco

### 1.2 Descarga del instalador

1. Abrir el navegador y dirigirse a: `https://dev.mysql.com/downloads/installer/`
2. Seleccionar **Windows (x86, 32-bit), MSI Installer** — este instalador de 32 bits contiene los paquetes de 64 bits y es el recomendado.
3. Hacer clic en **Download**.
4. En la siguiente pantalla aparece un formulario de registro. Hacer clic en el enlace **No thanks, just start my download** ubicado en la parte inferior de la página para descargar sin registrarse.

### 1.3 Ejecución del instalador

1. Ejecutar el archivo descargado `mysql-installer-community-X.X.X.X.msi` como administrador (clic derecho → **Ejecutar como administrador**).
2. Si Windows Defender SmartScreen muestra una advertencia, hacer clic en **Mas información** y luego en **Ejecutar de todas formas**.
3. En la pantalla **Choosing a Setup Type**, seleccionar **Custom** para tener control total sobre qué componentes instalar.

### 1.4 Selección de productos

En la pantalla **Select Products**:

1. Expandir **MySQL Servers → MySQL Server → MySQL Server 8.0**.
2. Seleccionar **MySQL Server 8.0.X** (la versión más reciente disponible) y hacer clic en la flecha verde para moverlo a la columna derecha.
3. Expandir **Applications → MySQL Workbench → MySQL Workbench 8.0**.
4. Seleccionar **MySQL Workbench 8.0.X** y moverlo a la columna derecha.
5. Hacer clic en **Next** y luego en **Execute** para descargar e instalar los componentes seleccionados.

### 1.5 Configuración del servidor

Después de la instalación, el asistente inicia la configuración del servidor:

**Pantalla: Type and Networking**

- **Config Type**: Development Computer (consume menos RAM, adecuado para desarrollo local)
- **Connectivity**:
  - Protocol: TCP/IP
  - Port: `3306` (dejar el valor por defecto)
  - Marcar la casilla **Open Windows Firewall port for network access**
- Hacer clic en **Next**.

**Pantalla: Authentication Method**

- Seleccionar **Use Strong Password Encryption for Authentication (RECOMMENDED)**.
- Hacer clic en **Next**.

**Pantalla: Accounts and Roles**

- En el campo **MySQL Root Password**, escribir una contraseña segura.
- **Importante**: anotar esta contraseña. Se usará para conectarse al servidor y no se puede recuperar si se olvida.
- No es necesario agregar usuarios adicionales para el taller.
- Hacer clic en **Next**.

**Pantalla: Windows Service**

- Dejar todas las opciones por defecto:
  - **Configure MySQL Server as a Windows Service**: marcado
  - **Windows Service Name**: `MySQL80`
  - **Start the MySQL Server at System Startup**: marcado (puede desmarcarse si se prefiere iniciar manualmente)
  - **Run Windows Service as**: Standard System Account
- Hacer clic en **Next**.

**Pantalla: Server File Permissions**

- Dejar la opción por defecto: **Yes, grant full access to the user running the Windows Service and to the administrators group only**.
- Hacer clic en **Next** y luego en **Execute**.

### 1.6 Verificación de la instalación

Una vez completada la configuración:

1. Abrir el **Símbolo del sistema** (CMD) o **PowerShell** como administrador.
2. Escribir el siguiente comando:

```
mysql -u root -p
```

3. Cuando solicite la contraseña, escribir la contraseña configurada en el paso anterior.
4. Si la instalación fue exitosa, aparecerá el prompt de MySQL:

```
mysql>
```

5. Para salir escribir: `exit`

---

## 2. MySQL Workbench en Windows

Si se siguió la instalación mediante el MySQL Installer del paso anterior, Workbench ya está instalado. En ese caso pasar directamente al paso 2.3.

### 2.1 Instalación independiente

Si se necesita instalar Workbench por separado:

1. Ir a: `https://dev.mysql.com/downloads/workbench/`
2. Seleccionar el sistema operativo **Microsoft Windows**.
3. Descargar el instalador MSI.
4. Ejecutar el instalador como administrador y seguir los pasos del asistente (Next → Next → Install → Finish).

### 2.2 Requisito: Microsoft .NET Framework

MySQL Workbench 8.0 requiere .NET Framework 4.5.2 o superior. En Windows 10 y 11 suele estar instalado por defecto. Si el instalador muestra un error relacionado con .NET:

1. Ir a: `https://dotnet.microsoft.com/download/dotnet-framework`
2. Descargar e instalar la versión 4.8 (la más reciente de la rama 4.x).

### 2.3 Primera conexión en Workbench

1. Abrir **MySQL Workbench** desde el menú de inicio.
2. En la pantalla principal, bajo **MySQL Connections**, hacer clic en el icono **+** para crear una nueva conexión.
3. Completar los campos:
   - **Connection Name**: `Local (taller)`
   - **Connection Method**: Standard (TCP/IP)
   - **Hostname**: `127.0.0.1`
   - **Port**: `3306`
   - **Username**: `root`
4. Hacer clic en **Store in Vault** para guardar la contraseña. Escribir la contraseña de root y confirmar.
5. Hacer clic en **Test Connection**. Debe aparecer el mensaje: **Successfully made the MySQL connection**.
6. Hacer clic en **OK** para guardar la conexión.
7. Hacer doble clic en la conexión creada para abrirla.

---

## 3. Variables de Entorno de MySQL en Windows

Este paso permite ejecutar el comando `mysql` desde cualquier directorio en el Símbolo del sistema o PowerShell, sin tener que escribir la ruta completa al ejecutable.

### 3.1 Localizar el directorio de instalación

La ruta de instalación por defecto de MySQL es:

```
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

Verificar que esta carpeta exista y que contenga el archivo `mysql.exe`. Si MySQL fue instalado en otro directorio, buscar esa ruta.

### 3.2 Abrir las variables de entorno del sistema

**Metodo 1 (recomendado): Desde el Panel de Control**

1. Hacer clic derecho sobre el icono de **Este equipo** (o **Mi PC**) en el escritorio o en el Explorador de archivos.
2. Seleccionar **Propiedades**.
3. En el panel izquierdo, hacer clic en **Configuracion avanzada del sistema**.
4. En la ventana que se abre, hacer clic en el botón **Variables de entorno...** ubicado en la parte inferior.

**Metodo 2: Desde Configuracion de Windows**

1. Presionar `Windows + S` y escribir `variables de entorno`.
2. Seleccionar **Editar las variables de entorno del sistema**.
3. Hacer clic en el botón **Variables de entorno...**.

**Metodo 3: Desde Ejecutar**

1. Presionar `Windows + R`.
2. Escribir `sysdm.cpl` y presionar Enter.
3. Ir a la pestaña **Opciones avanzadas**.
4. Hacer clic en **Variables de entorno...**.

### 3.3 Editar la variable Path del sistema

En la ventana **Variables de entorno**:

1. En la sección **Variables del sistema** (la sección inferior), buscar la variable llamada **Path**.
2. Seleccionarla con un clic y hacer clic en **Editar...**.
3. En la ventana **Editar variable de entorno**, hacer clic en **Nuevo**.
4. Escribir la ruta completa al directorio bin de MySQL:

```
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

5. Hacer clic en **Aceptar** para cerrar la ventana de edicion.
6. Hacer clic en **Aceptar** para cerrar la ventana **Variables de entorno**.
7. Hacer clic en **Aceptar** para cerrar las propiedades del sistema.

### 3.4 Verificar que el Path fue agregado correctamente

**Importante**: los cambios en las variables de entorno no afectan a las ventanas de CMD o PowerShell que ya estén abiertas. Es necesario cerrarlas y abrir una nueva.

1. Cerrar todas las ventanas de CMD o PowerShell que estén abiertas.
2. Abrir una nueva ventana de CMD o PowerShell.
3. Escribir el siguiente comando:

```
mysql --version
```

4. La respuesta debe ser similar a:

```
mysql  Ver 8.0.XX Distrib 8.0.XX, for Win64 (x86_64)
```

Si aparece ese mensaje, el Path fue configurado correctamente. Si aparece el error `'mysql' no se reconoce como un comando interno o externo`, revisar el paso 3.3 y asegurarse de que la ruta sea exacta y no tenga espacios adicionales.

### 3.5 Verificar que el servicio MySQL esta activo

1. Presionar `Windows + R`, escribir `services.msc` y presionar Enter.
2. Buscar el servicio **MySQL80** en la lista.
3. El estado debe ser **En ejecucion**. Si no lo está, hacer clic derecho y seleccionar **Iniciar**.

Alternativamente, desde CMD con privilegios de administrador:

```
net start MySQL80
```

Para detener el servicio:

```
net stop MySQL80
```

---

## 4. MySQL Server en Ubuntu

### 4.1 Requisitos previos

- Ubuntu 22.04 LTS o 24.04 LTS
- Acceso a la terminal con privilegios `sudo`
- Conexion a internet activa

### 4.2 Actualizar los repositorios del sistema

Antes de instalar cualquier paquete, actualizar la lista de repositorios:

```bash
sudo apt update
sudo apt upgrade -y
```

### 4.3 Instalar MySQL Server

```bash
sudo apt install mysql-server -y
```

Este comando instala el servidor MySQL desde los repositorios oficiales de Ubuntu. La version instalada depende de la version de Ubuntu:

- Ubuntu 22.04: MySQL 8.0
- Ubuntu 24.04: MySQL 8.0

### 4.4 Verificar que el servicio esta activo

```bash
sudo systemctl status mysql
```

La salida debe mostrar `Active: active (running)`. Si el servicio no está activo, iniciarlo:

```bash
sudo systemctl start mysql
```

Para que MySQL se inicie automaticamente con el sistema:

```bash
sudo systemctl enable mysql
```

### 4.5 Ejecutar el script de seguridad inicial

Ubuntu no asigna contraseña al usuario root de MySQL por defecto. El siguiente script permite configurarla junto con otras opciones de seguridad:

```bash
sudo mysql_secure_installation
```

El script realizará las siguientes preguntas. Se recomienda responder de la siguiente manera para el entorno del taller:

```
VALIDATE PASSWORD COMPONENT can be used to test passwords...
Press y|Y for Yes, any other key for No: N

Please set the password for root here.
New password: [escribir una contraseña segura]
Re-enter new password: [repetir la contraseña]

Remove anonymous users? (Press y|Y for Yes): Y

Disallow root login remotely? (Press y|Y for Yes): Y

Remove test database and access to it? (Press y|Y for Yes): Y

Reload privilege tables now? (Press y|Y for Yes): Y
```

### 4.6 Configurar autenticacion para el usuario root

En versiones recientes de MySQL en Ubuntu, el usuario root utiliza el plugin `auth_socket` por defecto, lo que significa que solo puede conectarse desde el sistema operativo sin contraseña. Para poder conectarse con contraseña desde aplicaciones Python y herramientas como Workbench o DataGrip, cambiar el plugin de autenticacion:

1. Abrir la consola de MySQL como superusuario del sistema:

```bash
sudo mysql
```

2. Ejecutar los siguientes comandos dentro de la consola de MySQL:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tu_contraseña_aqui';
FLUSH PRIVILEGES;
EXIT;
```

Reemplazar `tu_contraseña_aqui` por la contraseña elegida. Anotarla.

3. Verificar que el cambio funcionó intentando conectarse con contraseña:

```bash
mysql -u root -p
```

Ingresar la contraseña cuando se solicite. Debe aparecer el prompt `mysql>`.

### 4.7 Verificar la instalacion

```bash
mysql --version
```

Salida esperada:

```
mysql  Ver 8.0.XX Distrib 8.0.XX, for Linux (x86_64)
```

### 4.8 Crear la base de datos del taller

Una vez dentro de la consola MySQL:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE taller_flask;
SHOW DATABASES;
EXIT;
```

---

## 5. MySQL Workbench en Ubuntu

### 5.1 Instalar dependencias necesarias

MySQL Workbench en Ubuntu requiere algunas librerias adicionales:

```bash
sudo apt install -y libpcrecpp0v5 libglib2.0-0 libgtk-3-0 libatkmm-1.6-1v5 libgdk-pixbuf2.0-0
```

### 5.2 Metodo 1: Instalar desde el repositorio oficial de MySQL (recomendado)

Este metodo garantiza obtener la version mas reciente y recibir actualizaciones automaticas.

**Paso 1**: Descargar el paquete de configuracion del repositorio APT de MySQL.

Para Ubuntu 22.04:

```bash
wget https://dev.mysql.com/get/mysql-apt-config_0.8.30-1_all.deb
```

**Paso 2**: Instalar el paquete de configuracion:

```bash
sudo dpkg -i mysql-apt-config_0.8.30-1_all.deb
```

Durante la instalacion aparecera un menu. Seleccionar **MySQL 8.0** si no está seleccionado por defecto y confirmar con **OK**.

**Paso 3**: Actualizar los repositorios e instalar Workbench:

```bash
sudo apt update
sudo apt install mysql-workbench-community -y
```

### 5.3 Metodo 2: Instalar el paquete .deb directamente

1. Ir a `https://dev.mysql.com/downloads/workbench/` en el navegador.
2. Seleccionar **Ubuntu Linux** como sistema operativo y la version correspondiente.
3. Descargar el archivo `.deb`.
4. Instalar el paquete descargado:

```bash
cd ~/Downloads
sudo dpkg -i mysql-workbench-community_8.0.XX-1ubuntu22.04_amd64.deb
```

5. Si `dpkg` reporta dependencias faltantes, resolver con:

```bash
sudo apt --fix-broken install -y
```

### 5.4 Abrir MySQL Workbench

Buscar **MySQL Workbench** en el menu de aplicaciones o ejecutar desde terminal:

```bash
mysql-workbench
```

La primera vez que se abre puede tardar unos segundos mientras inicializa la configuracion.

### 5.5 Crear la primera conexion en Ubuntu

1. En la pantalla principal, hacer clic en el icono **+** junto a **MySQL Connections**.
2. Completar los campos:
   - **Connection Name**: `Local Ubuntu (taller)`
   - **Hostname**: `127.0.0.1`
   - **Port**: `3306`
   - **Username**: `root`
3. Hacer clic en **Store in Vault** y escribir la contraseña del root de MySQL.
4. Hacer clic en **Test Connection**.
5. Si la conexion es exitosa, hacer clic en **OK**.

---

## 6. DataGrip en Windows

DataGrip es el IDE de bases de datos de JetBrains. Soporta MySQL, PostgreSQL, SQLite y muchos otros motores. Requiere licencia de pago, pero ofrece una prueba gratuita de 30 dias. Los estudiantes universitarios pueden obtener una licencia gratuita en `https://www.jetbrains.com/student/`.

### 6.1 Descarga

1. Ir a `https://www.jetbrains.com/datagrip/download/`
2. Seleccionar **Windows**.
3. Descargar el instalador `.exe`.

### 6.2 Instalacion

1. Ejecutar el instalador `datagrip-XXXX.X.X.exe` como administrador.
2. En la pantalla **Installation Options**, marcar las casillas:
   - **Add "Open Folder as DataGrip Project"** (opcional pero util)
   - **Add launchers dir to the PATH** (recomendado)
   - **Create Desktop Shortcut** segun preferencia
3. Hacer clic en **Next** y luego en **Install**.
4. Al finalizar, marcar **Run DataGrip** y hacer clic en **Finish**.

### 6.3 Primera ejecucion y activacion

1. En la pantalla de bienvenida, seleccionar **Start trial** para iniciar la prueba de 30 dias, o ingresar la licencia si se tiene.
2. Se requiere iniciar sesion con una cuenta de JetBrains. Si no se tiene, crear una en `https://account.jetbrains.com/login`.
3. Seleccionar el tema de la interfaz (Darcula o Light) segun preferencia.

### 6.4 Conectar DataGrip a MySQL en Windows

1. En la pantalla principal de DataGrip, hacer clic en **+** en el panel **Database** (panel izquierdo) o ir al menu **File → New → Data Source → MySQL**.
2. En la ventana de configuracion de la fuente de datos:
   - **Name**: `MySQL Local (taller)`
   - **Host**: `localhost`
   - **Port**: `3306`
   - **User**: `root`
   - **Password**: escribir la contraseña de root de MySQL
   - **Database**: `taller_flask` (o dejar en blanco para ver todas)
3. En la parte inferior de la ventana aparecera un aviso **Download missing driver files**. Hacer clic en **Download** para que DataGrip descargue automaticamente el conector JDBC de MySQL. Esto requiere conexion a internet.
4. Hacer clic en **Test Connection**. Debe aparecer: **Successful**.
5. Hacer clic en **OK** para guardar.

---

## 7. DataGrip en Ubuntu

### 7.1 Metodo 1: Instalar via Toolbox App (recomendado)

JetBrains Toolbox es el gestor de aplicaciones oficial. Facilita la instalacion, actualizacion y gestion de todos los productos de JetBrains.

**Paso 1**: Descargar Toolbox App:

```bash
wget https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.X.X.XXXXX.tar.gz
```

Alternativamente, descargar el archivo desde `https://www.jetbrains.com/toolbox-app/` en el navegador.

**Paso 2**: Extraer el archivo:

```bash
tar -xzf jetbrains-toolbox-*.tar.gz
cd jetbrains-toolbox-*/
```

**Paso 3**: Ejecutar Toolbox:

```bash
./jetbrains-toolbox
```

**Paso 4**: En la interfaz de Toolbox, buscar **DataGrip** y hacer clic en **Install**.

Toolbox instala DataGrip en `~/.local/share/JetBrains/Toolbox/apps/DataGrip/` y crea un acceso directo en el menu de aplicaciones.

### 7.2 Metodo 2: Instalar el paquete tar.gz manualmente

1. Ir a `https://www.jetbrains.com/datagrip/download/` y descargar el archivo `.tar.gz` para Linux.

2. Extraer en el directorio de instalaciones:

```bash
sudo tar -xzf datagrip-XXXX.X.X.tar.gz -C /opt/
```

3. Navegar al directorio y ejecutar DataGrip:

```bash
cd /opt/DataGrip-XXXX.X.X/bin/
./datagrip.sh
```

4. Para crear un acceso directo en el menu de aplicaciones, desde dentro de DataGrip ir a **Tools → Create Desktop Entry**.

### 7.3 Dependencias adicionales en Ubuntu

DataGrip puede requerir las siguientes librerias en Ubuntu. Instalarlas si la aplicacion no abre:

```bash
sudo apt install -y libxss1 libgbm1 libnspr4 libnss3 fonts-liberation
```

### 7.4 Conectar DataGrip a MySQL en Ubuntu

El proceso es identico al descrito en la seccion 6.4 para Windows:

1. Abrir DataGrip.
2. Hacer clic en **+** en el panel **Database**.
3. Seleccionar **Data Source → MySQL**.
4. Completar los campos:
   - **Host**: `localhost`
   - **Port**: `3306`
   - **User**: `root`
   - **Password**: contraseña de root de MySQL
5. Hacer clic en **Download** si aparece el aviso de driver faltante.
6. Hacer clic en **Test Connection → OK**.

---

## 8. Errores Comunes y Soluciones

### Error: `Access denied for user 'root'@'localhost'`

**Causa**: La contraseña ingresada es incorrecta, o el plugin de autenticacion del usuario root no permite conexiones con contraseña.

**Solucion en Windows**:

1. Abrir CMD como administrador.
2. Detener el servicio de MySQL:
   ```
   net stop MySQL80
   ```
3. Iniciar MySQL en modo sin privilegios:
   ```
   mysqld --skip-grant-tables --skip-networking
   ```
4. En otra ventana de CMD, conectarse:
   ```
   mysql -u root
   ```
5. Dentro de MySQL, restablecer la contraseña:
   ```sql
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'nueva_contraseña';
   EXIT;
   ```
6. Reiniciar el servicio normalmente:
   ```
   net start MySQL80
   ```

**Solucion en Ubuntu**:

```bash
sudo mysql
```

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'nueva_contraseña';
FLUSH PRIVILEGES;
EXIT;
```

---

### Error: `Can't connect to MySQL server on 'localhost' (10061)` — Windows

**Causa**: El servicio de MySQL no está en ejecucion.

**Solucion**:

1. Presionar `Windows + R`, escribir `services.msc`.
2. Buscar **MySQL80** en la lista.
3. Hacer clic derecho → **Iniciar**.

O desde CMD como administrador:

```
net start MySQL80
```

---

### Error: `Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock'` — Ubuntu

**Causa**: El servicio de MySQL no está corriendo o el socket no fue creado correctamente.

**Solucion**:

```bash
sudo systemctl start mysql
sudo systemctl status mysql
```

Si el servicio falla al iniciar, revisar los logs:

```bash
sudo journalctl -u mysql --no-pager -n 50
```

Si el error en los logs menciona permisos en `/var/lib/mysql`, corregir con:

```bash
sudo chown -R mysql:mysql /var/lib/mysql
sudo systemctl start mysql
```

---

### Error: `ERROR 2003 (HY000): Can't connect to MySQL server on '127.0.0.1' (111)`

**Causa**: MySQL está escuchando en el socket local pero no en la interfaz TCP/IP, o el puerto 3306 está bloqueado.

**Solucion en Ubuntu**:

1. Abrir el archivo de configuracion de MySQL:
   ```bash
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```
2. Verificar o agregar la linea:
   ```
   bind-address = 127.0.0.1
   ```
3. Verificar que el puerto no esté comentado:
   ```
   port = 3306
   ```
4. Guardar y reiniciar MySQL:
   ```bash
   sudo systemctl restart mysql
   ```

---

### Error: `mysql is not recognized as an internal or external command` — Windows

**Causa**: El directorio `bin` de MySQL no fue agregado a la variable Path del sistema, o la ventana de CMD fue abierta antes de agregar el Path.

**Solucion**:

1. Verificar que el Path fue agregado correctamente siguiendo los pasos de la seccion 3.
2. Cerrar todas las ventanas de CMD o PowerShell.
3. Abrir una nueva ventana y ejecutar `mysql --version`.

Si el problema persiste, verificar que la ruta exacta sea:

```
C:\Program Files\MySQL\MySQL Server 8.0\bin
```

No debe tener comillas, espacios adicionales al inicio o al final, ni caracteres especiales.

---

### Error: `The MySQL service could not be started` — Windows

**Causa**: Conflicto con otra instancia de MySQL, puerto 3306 ocupado por otro proceso, o permisos incorrectos en el directorio de datos.

**Solucion**:

1. Verificar si el puerto 3306 está ocupado:
   ```
   netstat -ano | findstr :3306
   ```
2. Si aparece un proceso usando ese puerto, anotar el PID (ultimo numero) y cerrarlo:
   ```
   taskkill /PID [numero_pid] /F
   ```
3. Intentar iniciar el servicio nuevamente:
   ```
   net start MySQL80
   ```

Si persiste, revisar el log de errores de MySQL ubicado en:

```
C:\ProgramData\MySQL\MySQL Server 8.0\Data\[nombre-del-equipo].err
```

---

### Error al instalar Workbench en Ubuntu: `dpkg: dependency problems`

**Causa**: Faltan librerias del sistema requeridas por MySQL Workbench.

**Solucion**:

```bash
sudo apt --fix-broken install -y
sudo apt install -y libpcrecpp0v5 libglib2.0-0 libgtk-3-0
sudo dpkg -i mysql-workbench-community_*.deb
```

---

### DataGrip: `Connection to MySQL server failed. SSL connection error`

**Causa**: DataGrip intenta conectarse con SSL pero el servidor local no está configurado para ello.

**Solucion**:

1. En la ventana de configuracion de la fuente de datos en DataGrip, ir a la pestaña **Advanced**.
2. Buscar la propiedad `useSSL` y cambiar su valor a `false`.
3. Buscar `requireSSL` y cambiar a `false`.
4. Volver a hacer clic en **Test Connection**.

Alternativamente, agregar el parametro directamente en la URL de conexion:

```
jdbc:mysql://localhost:3306/taller_flask?useSSL=false&allowPublicKeyRetrieval=true
```

---

### DataGrip: `Public Key Retrieval is not allowed`

**Causa**: El plugin de autenticacion `caching_sha2_password` (predeterminado en MySQL 8) requiere el intercambio de clave publica, que DataGrip bloquea por seguridad.

**Solucion 1** (recomendada para desarrollo local):

En las propiedades avanzadas de la fuente de datos en DataGrip, establecer:

```
allowPublicKeyRetrieval = true
useSSL = false
```

**Solucion 2**: Cambiar el plugin de autenticacion del usuario al mas compatible `mysql_native_password`:

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tu_contraseña';
FLUSH PRIVILEGES;
```

---

### MySQL Workbench: No abre en Ubuntu (pantalla en blanco o se cierra)

**Causa**: Incompatibilidad con el compositor de ventanas o con la version de OpenGL.

**Solucion**:

```bash
LIBGL_ALWAYS_SOFTWARE=1 mysql-workbench
```

Para hacer este cambio permanente, editar el archivo `.desktop` de Workbench:

```bash
sudo nano /usr/share/applications/mysql-workbench.desktop
```

Cambiar la linea `Exec=` por:

```
Exec=env LIBGL_ALWAYS_SOFTWARE=1 mysql-workbench %f
```

Guardar y volver a abrir Workbench.

---

## Referencias

- MySQL Community Downloads: `https://dev.mysql.com/downloads/`
- MySQL 8.0 Reference Manual: `https://dev.mysql.com/doc/refman/8.0/en/`
- DataGrip Documentation: `https://www.jetbrains.com/help/datagrip/`
- JetBrains Student License: `https://www.jetbrains.com/student/`
- Ubuntu MySQL Guide: `https://ubuntu.com/server/docs/databases-mysql`