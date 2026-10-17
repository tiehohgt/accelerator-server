[app]

# Название приложения, которое видно на телефоне
title = Accelerator Server

# Имя пакета (только строчные буквы, цифры и точки)
package.name = acceleratorserver

# Домен-заглушка: итоговый ID приложения будет org.test.acceleratorserver
package.domain = org.test

# Откуда берётся исходный код (папка рядом со spec-файлом)
source.dir = .

# Какие файлы включать в сборку
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# Версия приложения
version = 0.1

# Зависимости: сам питон + Kivy. Больше ничего не нужно,
# sockets и threading входят в стандартную библиотеку.
requirements = python3,kivy

# Ориентация экрана
orientation = portrait

# 0 = показывать системные панели, 1 = на весь экран
fullscreen = 0

# Иконка приложения (раскомментируй, когда положишь файл рядом)
# icon.filename = %(source.dir)s/icon.png

# Разрешения Android.
# INTERNET критично важен: без него нельзя ни открыть серверный сокет,
# ни принимать входящие подключения на портах 45000/45001.
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_MULTICAST_STATE

# Автоматически принимать лицензии Android SDK при сборке
android.accept_sdk_license = True

# Архитектуры: arm64 для современных телефонов, armv7 для старых
android.archs = arm64-v8a, armeabi-v7a

# Минимальная и целевая версия Android
android.minapi = 24
android.api = 34
android.ndk_api = 24

# Собирать именно APK (а не AAB)
android.debug_artifact = apk

# Не удалять каталог сборки после успеха — удобно для отладки
p4a.bootstrap = sdl2

[buildozer]

# Подробность логов: 1 обычные, 2 подробные
log_level = 2

# Показывать предупреждения
warn_on_root = 1
