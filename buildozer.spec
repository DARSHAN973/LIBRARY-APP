[app]
title = Library Mobile App
version = 0.1
package.name = libraryapp
package.domain = org.example.libraryapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db
requirements = python3,kivy,kivymd,requests,python-dotenv
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2