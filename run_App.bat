@echo off
echo '                                                                 '
echo '                                                                 '
echo ' Practicas esenciales de ingenieria de software para el agilismo '
echo ' Equipo 5                                                        '
echo '                                                                 '
echo ' Integrantes:                                                    '
echo ' - Andres Soler                                                  '
echo ' - Shiomar Salazar                                               '
echo '                                                                 '
echo '                                                                 '
color 0A
set work_dir=%cd%

if exist %work_dir%\venv\ (
	echo ' Virtual env ya existe en: %work_dir%\venv\
) else (
	echo Creando virtual env en: %work_dir%
	python -m venv %work_dir%\venv
	echo Instalando todas las depencias para el virtual environment
	%work_dir%\venv\Scripts\python.exe -m pip install --upgrade pip
	%work_dir%\venv\Scripts\python.exe -m pip install -r %work_dir%\requirements.txt
)
echo '                                                                 '
echo '               Operaciones Soportadas                            '
echo '                                                                 '
echo '  * APP  - Lanzar la Aplicacion Auto-Perfecto                    '
echo '  * TEST - Correr Pruebas de Unitarias                           '
echo '  * COVER - Correr Analisis de Cobertura de Codigo               ' 
echo '                                                                 '
set /p "id=Indique Operacion: "

if /I %id%==APP (%work_dir%\venv\Scripts\python.exe %work_dir%\__main__.py)
if /I %id%==TEST (%work_dir%\venv\Scripts\python.exe -m unittest discover -s tests -v)
if /I %id%==COVER (%work_dir%\venv\Scripts\coverage erase
	%work_dir%\venv\Scripts\coverage run -m unittest discover -s tests -v
%work_dir%\venv\Scripts\coverage report -m)
PAUSE
