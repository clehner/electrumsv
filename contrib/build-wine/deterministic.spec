# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
for i, x in enumerate(sys.argv):
    if x == '--name':
        cmdline_name = sys.argv[i+1]
        break
else:
    raise BaseException('no name')


home = 'C:\\electrum\\'

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = []
hiddenimports += collect_submodules('trezorlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')

# Add libusb binary
binaries = [("c:/python3.5.4/libusb-1.0.dll", ".")]

binaries += [('C:/tmp/libsecp256k1.dll', '.')]

# Workaround for "Retro Look":
binaries += [b for b in collect_dynamic_libs('PyQt5') if 'qwindowsvista' in b[0]]

datas = [
    (home+'electrumsv/lib/currencies.json', 'electrumsv'),
    (home+'electrumsv/lib/servers.json', 'electrumsv'),
    (home+'electrumsv/lib/servers_testnet.json', 'electrumsv'),
    (home+'electrumsv/lib/wordlist/english.txt', 'electrumsv/wordlist'),
    (home+'electrumsv/lib/locale', 'electrumsv/locale'),
    (home+'electrumsv/plugins', 'electrumsv_plugins'),
    ('C:\\Program Files (x86)\\ZBar\\bin\\', '.'),
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis([home+'electrum-sv',
              home+'electrumsv/gui/qt/main_window.py',
              home+'electrumsv/gui/text.py',
              home+'electrumsv/lib/util.py',
              home+'electrumsv/lib/wallet.py',
              home+'electrumsv/lib/simple_config.py',
              home+'electrumsv/lib/bitcoin.py',
              home+'electrumsv/lib/dnssec.py',
              home+'electrumsv/lib/commands.py',
              home+'electrumsv/plugins/cosigner_pool/qt.py',
              home+'electrumsv/plugins/email_requests/qt.py',
              home+'electrumsv/plugins/trezor/client.py',
              home+'electrumsv/plugins/trezor/qt.py',
              home+'electrumsv/plugins/keepkey/qt.py',
              home+'electrumsv/plugins/ledger/qt.py',
              #home+'packages/requests/utils.py'
              ],
             binaries=binaries,
             datas=datas,
             #pathex=[home+'lib', home+'gui', home+'plugins'],
             hiddenimports=hiddenimports,
             hookspath=[])


# http://stackoverflow.com/questions/19055089/pyinstaller-onefile-warning-pyconfig-h-when-importing-scipy-or-scipy-signal
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break

# hotfix for #3171 (pre-Win10 binaries)
a.binaries = [x for x in a.binaries if not x[1].lower().startswith(r'c:\windows')]

pyz = PYZ(a.pure)


#####
# "standalone" exe with all dependencies packed into it

#options = [ ('v', None, 'OPTION')]  - put this in the following exe list to debug and turn console=true

exe_standalone = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,  
    name=os.path.join('build\\pyi.win32\\electrum', cmdline_name + ".exe"),
    debug=False,
    strip=None,
    upx=False,
    icon=home+'icons/electrum-sv.ico',
    console=False)
    # console=True makes an annoying black box pop up, but it does make Electrum output command line commands, with this turned off no output will be given but commands can still be used

exe_portable = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas + [ ('is_portable', 'README.md', 'DATA' ) ],
    name=os.path.join('build\\pyi.win32\\electrum', cmdline_name + "-portable.exe"),
    debug=False,
    strip=None,
    upx=False,
    icon=home+'icons/electrum-sv.ico',
    console=False)

#####
# exe and separate files that NSIS uses to build installer "setup" exe

exe_dependent = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=os.path.join('build\\pyi.win32\\electrum', cmdline_name),
    debug=False,
    strip=None,
    upx=False,
    icon=home+'icons/electrum-sv.ico',
    console=False)

coll = COLLECT(
    exe_dependent,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=None,
    upx=True,
    debug=False,
    icon=home+'icons/electrum-sv.ico',
    console=False,
    name=os.path.join('dist', 'electrum'))
