pyinstaller --uac-admin -F --specpath spec register_outer_menu.py
pyinstaller --uac-admin -F --specpath spec register_inner_menu.py
pyinstaller -w -F --specpath spec ftp_download.py
pyinstaller -w -F --specpath spec ftp_upload.py
copy /y ftp.json dist
pause