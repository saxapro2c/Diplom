[app]
title = VyatsuNews
package.name = vyatsu_news
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,xml,db
version = 1.0
requirements = python3,kivy,kivymd,requests,beautifulsoup4,flask,sqlite3
orientation = portrait
fullscreen = 1
entrypoint = main.py
icon.filename = %(source.dir)s/icon.png
android.archs = arm64-v8a, armeabi-v7a
presplash.filename = %(source.dir)s/data/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1

[app.android]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.minapi = 21
android.api = 31
android.ndk = 25b
android.gradle_dependencies = com.google.android.material:material:1.4.0
android.entrypoint = org.kivy.android.PythonActivity
android.packaging_options = 
    exclude 'META-INF/LICENSE.txt'
    exclude 'META-INF/NOTICE.txt'
    exclude 'META-INF/LICENSE'
    exclude 'META-INF/NOTICE'

[pythonforandroid]
p4a.branch = develop