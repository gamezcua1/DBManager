# DB Manager
# Python
## MySQL & PostgreSQL

![](https://github.com/gamezcua1/DBManager/blob/master/window.PNG "This is what the app looks like")


- Puede ser programada con cualquier herramienta o lenguaje (c#, java, phyton, c++, etc), salvo aquellos que estén 
basados en web (no usar interfaz web/HTML).
- Debe permitir establecer la conexión a diferentes servidores, escogiendo al menos menos 2 de estos: MS-Access, 
MySQL/MariaDB ó PostgreSQL.
- Con la selección de la fuente de datos, se identificarían las librerías correspondientes a utilizar. Con el paso de 
los parámetros de autentificación (login y password del usuario) se formaría dinámicamente la respectiva cadena de conexión. 
- De acuerdo al alcance de la conexión establecida, se deberán desplegar los respectivos objetos de datos a los que 
tiene visiblidad el usuario. Estos son sus respectivas BDs, Tablas, Campos, y propiedades básicas de los campos, incluyendo si tiene PKs o FKs. Se sugiere que para este punto se empleé un esquema de visualización de tipo árbol (TreeView), aunque ésto queda totalmente a su libre implementación.
- También, incluir un mecanismo simple para ejecutar comandos SQL básicos como SELECTs y desplegar en la pantalla los 
resultados. Puede ser un simple textbox y un botón para ejecutar el query, junto con un control tipo rejilla para el despliegue de los registros resultantes.
