# MISW4101-202214-Grupo005
Espacio de trabajo del grupo 005
 
## Reporte
[GitInspector](https://misw-4101-practicas.github.io/MISW4101-202214-Grupo005/reports)

## Lanzar applicacion
Para facilidad de las revisiones se implemento el run_App.bat que contiene las siguientes funciones
#### General:
- Crea un virtual enviroment para la App con todos sus requisitos.
#### Especifica:
- El commando APP  - Lanzar la Aplicacion Auto-Perfecto
- El commando TEST - Correr Pruebas de Unitarias d desarrollo
- El commando COVER - Correr Analisis de Cobertura de Codigo

## Pipelines
- Al hacer commint que incluta la descripcion de "Develop Ready" en un branch llamado feature_xxxxxx, un pipeline de GitHub action se lanzara que de estar todas las pruebas validas hara el merge automatico a Develop (habiendo previamente actualizado el branch feature_xxxxx con los cambios mas recierntes de develop).
