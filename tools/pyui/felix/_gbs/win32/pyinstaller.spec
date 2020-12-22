# -*- mode: python -*-

block_cipher = None

import os


ALLOWED_EXTENSIONS=['.js', '.html', '.png', '.chm']


def add_module(m, module_name):
    for module_path in m.__path__:
        add_files(module_path, module_name)


def add_files(module_path, module_name):
    for root, dirs, files in os.walk(module_path):
        for name in files:
            _, file_extension = os.path.splitext(name)

            if file_extension not in ALLOWED_EXTENSIONS:
                continue

            full_path = os.path.join(root, name)
            #print(full_path)
            datas.append( (full_path, os.path.join(module_name + root[len(module_path):]) ) )

datas = []


datas.append(('germanium_build_monitor/resources/favicon.ico', 'germanium_build_monitor/resources/'))
add_files("germanium_build_monitor", "germanium_build_monitor")

def add_files(m):
    for root, dirs, files in os.walk(m.__path__):
        for name in files:
            full_path = os.path.join(root, name)

a = Analysis(['germanium_build_monitor/mainapp.py'],
             pathex=['./germanium_build_monitor'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='felixbm',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='germanium_build_monitor/resources/favicon.ico',
)

