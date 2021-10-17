from cx_Freeze import setup, Executable

executables = [Executable('main.py', targetName='My_game.exe')]


includes = ['aiogram', 'time', 'os', 'datetime', 'sqlite3', 'selenium', 'asyncio']

zip_include_packages = ['aiogram', 'time', 'os', 'datetime', 'sqlite3', 'selenium', 'asyncio']

include_files = ['state.py', 'datebase.py', 'keyboards.py', 'common.py', 'driver.py', 'users.db']

options = {
'build_exe': {
'include_msvcr': True,
'includes': includes,
'zip_include_packages': zip_include_packages,
'build_exe': 'build_linux',
'include_files': include_files,
}
}

setup(name='bot',
version='0.1.0',
description='bot',
executables=executables,
options=options)