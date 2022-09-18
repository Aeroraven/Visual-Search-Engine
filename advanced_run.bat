@echo off
echo ###################################################
echo #                                                 #
echo #  Assignment 2 of Human Computer Interaction     #
echo #  Information Retrieval                          #
echo #  Author: 1950641                                #
echo #                                                 #
echo ###################################################
echo .
echo ======== Installing python dependencies (Step 1 of 5) ========
echo .
echo This may take a few minutes. Time depends on your network condition.
echo Note: Package PyTorch installation might consume a lot of time.
echo .
pip3 install Flask
pip3 install torch torchvision
pip3 install tqdm
pip3 install albumentations
pip3 install matplotlib
pip3 install opencv-python
echo .
echo ======== Installing front-end Node.js dependencies (Step 2 of 5) ========
echo .
echo This may take a few minutes. Time depends on your network condition.
echo .
cd frontend
cmd /c npm install
cd ..
echo .
echo ======== Building front-end pages... (Step 3 of 5) ========
echo .
cd frontend
cmd /c npm run build
cd ..
echo .
echo ======== Copying front-end pages... (Step 4 of 5) ========
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
echo ======== Setting up Flask framework... (Step 5 of 5) ========
echo .
set FLASK_APP=main
flask run
pause