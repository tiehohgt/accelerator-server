#!/usr/bin/env bash
# Сборка APK внутри WSL/Ubuntu.
# Запуск из этой папки:  bash build_wsl.sh
set -e

echo "==> Ставим системные зависимости"
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo6 cmake libffi-dev libssl-dev

echo "==> Ставим buildozer и cython"
pip3 install --user --upgrade buildozer cython

export PATH="$HOME/.local/bin:$PATH"

echo "==> Сборка APK (первый раз долго: скачает Android SDK и NDK, ~30-60 мин)"
buildozer android debug

echo
echo "==> Готово. Файл здесь:"
ls -lh bin/*.apk
