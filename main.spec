# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['.\\utils\\CW.py', '.\\utils\\display_by_person.py', '.\\utils\\embedder.py', '.\\utils\\face_functions.py', '.\\utils\\facenet.py', '.\\utils\\sort_images.py','.\\gui\\core\\functions.py', '.\\gui\\core\\json_settings.py', '.\\gui\\core\\json_themes.py', '.\\gui\\core\\qt_core.py', '.\\gui\\uis\\columns\\ui_left_column.py', '.\\gui\\uis\\columns\\ui_right_column.py', '.\\gui\\uis\\pages\\ui_main_pages.py', '.\\gui\\uis\\windows\\main_window\\flow_layout.py', '.\\gui\\uis\\windows\\main_window\\functions_main_window.py', '.\\gui\\uis\\windows\\main_window\\setup_main_window.py', '.\\gui\\uis\\windows\\main_window\\ui_main.py', '.\\gui\\widgets\\py_checkbox\\py_checkbox.py', '.\\gui\\widgets\\py_circular_progress\\py_circular_progress.py', '.\\gui\\widgets\\py_credits_bar\\py_credits.py', '.\\gui\\widgets\\py_dialog\\py_dialog.py', '.\\gui\\widgets\\py_grips\\py_grips.py', '.\\gui\\widgets\\py_icon_button\\py_icon_button.py', '.\\gui\\widgets\\py_image\\py_image.py', '.\\gui\\widgets\\py_image_page\\py_image_page.py', '.\\gui\\widgets\\py_left_column\\py_icon.py', '.\\gui\\widgets\\py_left_column\\py_left_button.py', '.\\gui\\widgets\\py_left_column\\py_left_column.py', '.\\gui\\widgets\\py_left_menu\\py_div.py', '.\\gui\\widgets\\py_left_menu\\py_left_menu.py', '.\\gui\\widgets\\py_left_menu\\py_left_menu_button.py', '.\\gui\\widgets\\py_line_edit\\py_line_edit.py', '.\\gui\\widgets\\py_push_button\\py_push_button.py', '.\\gui\\widgets\\py_slider\\py_slider.py', '.\\gui\\widgets\\py_table_widget\\py_table_widget.py', '.\\gui\\widgets\\py_table_widget\\style.py', '.\\gui\\widgets\\py_title_bar\\py_div.py', '.\\gui\\widgets\\py_title_bar\\py_title_bar.py', '.\\gui\\widgets\\py_title_bar\\py_title_button.py', '.\\gui\\widgets\\py_toggle\\py_toggle.py', '.\\gui\\widgets\\py_window\\py_window.py', '.\\gui\\widgets\\py_window\\styles.py'],
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
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
