@echo off
echo ###################################################
echo #                                                 #
echo #  Assignment 2 of Human Computer Interaction     #
echo #  Information Retrieval                          #
echo #  Author: 1950641                                #
echo #                                                 #
echo ###################################################
echo .
echo ======== Building front-end pages... (Step 1 of 3) ========
echo .
cd frontend
cmd /c npm run build
cd ..
echo .
echo ======== Copying front-end pages... (Step 2 of 3) ========
echo .
cd templates
mkdir dist
cd dist
mkdir assets
cd ..
cd ..
del /f /s /q templates\dist\assets\*.*
copy frontend\dist templates\dist
copy frontend\dist\assets templates\dist\assets
echo .
echo ======== Setting up Flask framework... (Step 3 of 3) ========
echo .
set FLASK_APP=main
flask run
pause