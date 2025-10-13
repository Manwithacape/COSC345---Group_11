# app.spec
# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Collect CLIP data files
clip_datas = []
try:
    clip_datas = collect_data_files('clip')
except:
    # Manual collection if automatic fails
    import clip
    clip_root = os.path.dirname(clip.__file__)
    vocab_file = os.path.join(clip_root, 'bpe_simple_vocab_16e6.txt.gz')
    if os.path.exists(vocab_file):
        clip_datas = [(vocab_file, 'clip')]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('schema.sql', '.'),
        ('logo/autocull_logo.webp', 'logo'),
    ] + clip_datas,
    hiddenimports=[
        'google.genai',
        'google.genai.client', 
        'google.genai.batches',
        'google.auth',
        'google.auth.transport.requests',
        'pydantic',
        'pydantic.main',
        'pydantic.fields',
        'clip',
        'clip.clip',
        'clip.model',
        'clip.simple_tokenizer',
        'torch',
        'torchvision',
        'transformers',
        'cv2',
        'sklearn',
        'skimage',
        'PIL',
        'numpy',
        'psycopg2',
        'rawpy',
        'piexif',
        'imagehash',
        'ttkbootstrap',
        'exifead'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)