# Readme

Test setup for checking escaping paths wihin scons that include spaces
This has been run under windows using gcc from a MSYS2 install

  * Tested under Windows 10 / python 2.7 / Scons 3.0.1

## Visual Studio Code

Visual Studio Code files included so if you have the python extension installed
you should just be able to open this as a folder using File -> Open Folder
it should just be a case of selecting "Python 2.7: Run scons SConstruct file" from the debug profile list

## Virtual Environment

Also the VSCode files are setup use a python virtual env which can be setup via

  * virtenv\setup_venv.bat
  * virtenv\setup_venv.sh

This uses tox to setup a virtual env

