# R2C2-ionic

Programa escrito en [Node](https://nodejs.org/en/) que comprende una colección de tareas automatizadas en servidor para el proyecto de [R2C2](https://github.com/gsinovsky/tesis)

## Requisitos
Se necesita [npm](https://docs.npmjs.com/getting-started/installing-node) 

## Instruciones de instalación
Para instalar el proyecto en una máquina local Linux primero se recomienda el uso de un entorno virtual, tal como [virtualenv](https://virtualenv.readthedocs.org/en/latest/), una vez cargado el entorno virtual, navegue hasta el directorio del proyecto y ejecute:

```bash
$ npm install
```

Luego navegue a la carpeta corecode y allí haga

```bash
$ pip install -r requirements.txt
```

Esto instalará todas las dependencias del proyecto. 

## Ejecución

Para correr el proyecto ejecute:
```bash
$ grunt
```
Esto iniciará el servidor local.

## Sincronizar cambios locales con el repositorio del código principal (tesis)
```bash
$ git remote add -f corecode git@github.com:gsinovsky/tesis.git
$ git pull -s subtree core-code master
```