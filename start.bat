@echo off
chcp 65001 > nul
title Predictor de Coeficiente de Refraccion KL

echo.
echo ================================================
echo    PREDICTOR DE COEFICIENTE DE REFRACCION KL
echo ================================================
echo.

echo Verificando instalacion de Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor, instala Python desde https://www.python.org/downloads/
    echo y asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo  Python detectado correctamente
echo.

echo Verificando e instalando dependencias...
echo.

:: Verificar e instalar customtkinter
python -c "import customtkinter" > nul 2>&1
if errorlevel 1 (
    echo Instalando customtkinter...
    pip install customtkinter
) else (
    echo  customtkinter ya esta instalado
)

:: Verificar e instalar scikit-learn
python -c "import sklearn" > nul 2>&1
if errorlevel 1 (
    echo Instalando scikit-learn...
    pip install scikit-learn
) else (
    echo  scikit-learn ya esta instalado
)

:: Verificar e instalar joblib
python -c "import joblib" > nul 2>&1
if errorlevel 1 (
    echo Instalando joblib...
    pip install joblib
) else (
    echo  joblib ya esta instalado
)

:: Verificar e instalar pandas
python -c "import pandas" > nul 2>&1
if errorlevel 1 (
    echo Instalando pandas...
    pip install pandas
) else (
    echo  pandas ya esta instalado
)

:: Verificar e instalar numpy
python -c "import numpy" > nul 2>&1
if errorlevel 1 (
    echo Instalando numpy...
    pip install numpy
) else (
    echo  numpy ya esta instalado
)

:: Verificar e instalar Pillow
python -c "from PIL import Image" > nul 2>&1
if errorlevel 1 (
    echo Instalando Pillow...
    pip install Pillow
) else (
    echo  Pillow ya esta instalado
)

echo.
echo ================================================
echo Todas las dependencias estan listas!
echo Iniciando la interfaz...
echo ================================================
echo.

:: Esperar 2 segundos antes de ejecutar
timeout /t 2 /nobreak > nul

:: Ejecutar la interfaz
python interfaz.py

:: Si la interfaz se cierra, pausar para ver posibles errores
if errorlevel 1 (
    echo.
    echo  Hubo un error al ejecutar la interfaz
    echo Presiona cualquier tecla para salir...
    pause > nul
)