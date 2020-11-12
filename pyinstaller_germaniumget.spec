# -*- mode: python -*-

block_cipher = None

datas=[]

a = Analysis(['application.py'],
             pathex=['.'],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

print("Binaries: %s" % a.binaries)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='germanium-get',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          uac_admin=True)

