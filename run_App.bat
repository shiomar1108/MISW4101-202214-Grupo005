@echo off
echo '                                                                 '
echo '                                                                 '
echo ' Practicas esenciales de ingenieria de software para el agilismo '
echo ' Equipo 5                                                        '
echo '                                                                 '
echo '  Integrantes:                                                   '
echo '  Andres Soler                                                   '
echo '  Shiomar Salazar                                                '
echo '                                                                 '
echo '                                                                 '
color 0A
echo STEP 1: Set up Virtual Enviroment
set work_dir=%cd%
echo Working dir: %work_dir%
if exist %work_dir%\venv\ (
	echo "Virtual env is already exists: %work_dir%\venv\"
) else (
	echo "Creating virtual env at: %work_dir%"
	python -m venv %work_dir%\venv
	echo "Installing all dependencies into virtual environment"
	%work_dir%\venv\Scripts\python.exe -m pip install --upgrade pip
	%work_dir%\venv\Scripts\python.exe -m pip install -r %work_dir%\requirements.txt
)
echo STEP 2: Run App
%work_dir%\venv\Scripts\python.exe %work_dir%\__main__.py