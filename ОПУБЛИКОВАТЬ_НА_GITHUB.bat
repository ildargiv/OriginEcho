@echo off
chcp 65001 >nul
title Публикация OriginEcho на GitHub
cd /d "%~dp0"

echo ================================================
echo   Публикация OriginEcho на GitHub
echo ================================================
echo.

set /p USER=Введите ваш GitHub-логин: 
if "%USER%"=="" (
  echo Не указан логин. Выход.
  pause
  exit /b 1
)

set REPO=https://github.com/%USER%/OriginEcho.git

echo.
echo Подключаю удалённый репозиторий:
echo    %REPO%
git remote remove origin 2>nul
git remote add origin %REPO%

echo.
echo Отправляю код...
echo (GitHub откроется в вашем браузере - нажмите Authorize)
echo.
git push -u origin main

if errorlevel 1 (
  echo.
  echo Не удалось отправить. Возможно, репозиторий ещё не создан.
  echo Создайте пустой репозиторий: https://github.com/new
  echo имя - OriginEcho, галочки README/.gitignore/license - НЕ ставить.
) else (
  echo.
  echo Готово! Проект опубликован:
  echo    https://github.com/%USER%/OriginEcho
)
echo.
pause
