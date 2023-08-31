# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['server.py', 'main.py', 'utils.py', 'metrics.py', 'merger.py', 'datasets.py', 'neural_network.py', 'rgb_transform.py', 'server_utils.py', 'svs.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
a.datas+=Tree('./tissue_recogniser_idc', prefix='tissue_recogniser_idc')
a.datas+=Tree('./py_wsi', prefix='py_wsi')
a.datas+=Tree('./openslide', prefix='openslide')
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='server',
)
