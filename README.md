### Test Grupo R5

URL_API: https://libraryt-test.uc.r.appspot.com/

Se desarrollan todos los puntos de la prueba las tecnologias utilizadas fueron fastapi, mysql, google, graphql, python39, sqlachemy y appengine para el despliegue de la api.

La api provee dos endpoints:
	https://libraryt-test.uc.r.appspot.com/auth/
	https://libraryt-test.uc.r.appspot.com/books/

#Relacion db 
![](https://storage.googleapis.com/libraryt-test.appspot.com/db.png)

#Auth
El endpoint de auth nos provee dos mutaciones:

![](https://storage.googleapis.com/libraryt-test.appspot.com/create.png)

esta primera createUser brinda la creacion de usuarios los cuales el admin del sistema sera el unico de poderla realizar y activar el usuario.

La segunda:

![](https://storage.googleapis.com/libraryt-test.appspot.com/auth1.png)

Nos da un token de autenticacion a un usuario registrado y activo con este token sera la cabecera de authenticacion para el consumo del endpoint de books.

Cabecera:

![](https://storage.googleapis.com/libraryt-test.appspot.com/token.png)

#Books

CONSULTA:

Tenemos el servicio que nos brinda la consulta a los libros el cual el caso que no exista en la db interna consulta google books y openlibrary:

![](https://storage.googleapis.com/libraryt-test.appspot.com/query_books.png)

Los campos por los cuales se puede consultar son:
	 id,
	 title,
	 datePublish,
	 categories,
	 subtitle,
	 authors,
	 description,
	 source,
	 image

y nos devolvera un array de libros encontrados en cualquiera de las fuentes.

CREACION:

La creacion de libros requiere todos los campos mencionados anteriormente si no se envia alguno de los campos requeridos nos genera una excepcion.

![](https://storage.googleapis.com/libraryt-test.appspot.com/insert_books.png)

retorna el objeto del libro junto con el id que se genero en base de datos.

ELIMINACION:

Elimina un libro registrado en base de datos junto con sus dependencias el unico campo que se requiere es el id del libro para realizar la eliminacion.

![](https://storage.googleapis.com/libraryt-test.appspot.com/delete_books.png)