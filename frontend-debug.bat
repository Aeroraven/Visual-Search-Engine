@echo off
echo ###################################################
echo #                                                 #
echo #  Assignment 2 of Human Computer Interaction     #
echo #  Information Retrieval                          #
echo #  Author: 1950641                                #
echo #                                                 #
echo ###################################################
echo .
echo ======== Installing front-end Node.js dependencies (Step 1 of 2) ========
echo .
echo This may take a few minutes. Time depends on your network condition.
echo .
cd frontend
cmd /c npm install
cd ..
echo .
echo ======== Setting up Vite development server... (Step 2 of 2) ========
echo .
cd frontend
cmd /c npm run dev
cd ..
echo .