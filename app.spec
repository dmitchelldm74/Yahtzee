# -*- mode: python -*-

block_cipher = None

"""added_files = [
         ( 'a folder', 'b folder' ),  # Loads the 'a folder' folder (left) and creates
                                      # an equivalent folder called 'b folder' (right)
                                      # on the destination path
         ( 'level_1/level2', 'level_2' ),  # Loads the 'level_2' folder
                                           # that's inside the 'level_1' folder
                                           # and outputs it on the root folder
         ( 'comic_sans.ttf', '.'),  # Loads the 'comic_sans.ttf' file from
                                    # your root folder and outputs it with
                                    # the same name on the same place.
         ( 'folder/*.mp3', '.')  # Loads all the .mp3 files from 'folder'.
         ]"""
added_files = [
      ( 'assets', 'assets' )
      ]

a = Analysis(['app.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
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
          name='Yahtzee',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,icon='C:\\Users\\Admin\\Documents\\yahtzee\\assets\\images\\icon.ico')
