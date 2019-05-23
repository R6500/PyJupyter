
echo off
echo Clean utility
echo This script removes all autogenerated files
echo Use it to reduce the number of files for PyJupyter realse

%SystemRoot%\System32\choice.exe /C YN /N /M "Are you sure [Y/N]? "
if errorlevel 2 goto :nothing

echo Start cleaning...
cd ..

echo Python pyc
del /S Code\*.pyc
rmdir /S /Q Code\__pycache__
rmdir /S /Q Code\slab\__pycache__

echo Code examples and tests
rmdir /S /Q Code\Examples
rmdir /S /Q Code\Tests 

echo Checkpoints
rmdir /S /Q Jupyter\.ipynb_checkpoints
rmdir /S /Q Jupyter\Audio\.ipynb_checkpoints
rmdir /S /Q Jupyter\Basics\.ipynb_checkpoints
rmdir /S /Q Jupyter\Circuits\.ipynb_checkpoints
rmdir /S /Q Jupyter\Mechanics\.ipynb_checkpoints
rmdir /S /Q Jupyter\Reference\.ipynb_checkpoints
rmdir /S /Q "Jupyter\Sandbox\.ipynb_checkpoints"
rmdir /S /Q Jupyter\User\*.*

echo Private 
rmdir /S/Q Jupyter\Private

echo Done

goto :EOF

:nothing
echo Cleaning aborted