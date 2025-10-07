@echo off
REM Bible Analysis & Visualization Project
REM Master Launcher - Starts All Three Applications

echo.
echo ========================================================
echo  Bible Analysis ^& Visualization Project
echo  Starting All Three Applications...
echo ========================================================
echo.

REM 1. Start Web Visualizer Server
echo [1/3] Starting Web Visualizer (http://localhost:8000)...
start "Bible Web Server" cmd /k "cd bible-visualizer-web && python -m http.server 8000"

REM Wait 2 seconds for server to start
timeout /t 2 /nobreak >nul

REM Open browser to web visualizer
start http://localhost:8000/index.html
echo       Web Visualizer: LAUNCHED
echo.

REM 2. Start Desktop Visualizer
echo [2/3] Starting Desktop Visualizer (Python GUI)...
start "Bible Desktop Visualizer" cmd /c "cd bible-visualizer-desktop && python visualizer_app.py"
echo       Desktop Visualizer: LAUNCHED
echo.

REM 3. Start CMD Bible Reader
echo [3/3] Starting CMD Bible Reader (Command Line)...
start "Bible CMD Reader" cmd /k "cd bible-analysis-tool && python bible_reader.py"
echo       CMD Reader: LAUNCHED
echo.

echo ========================================================
echo  All Three Applications Launched Successfully!
echo ========================================================
echo.
echo You should see:
echo   - Web Browser: http://localhost:8000/index.html
echo   - Python Window: Desktop Visualizer
echo   - Command Window: Bible CMD Reader
echo.
echo To stop the web server, close the "Bible Web Server" window
echo or press Ctrl+C in that window.
echo.
echo Press any key to close this launcher window...
pause >nul
