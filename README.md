<h1 align="center">PhoneMirror</h1>

<p align="center">
  One-click Android screen mirroring for Windows.<br />
  <samp>PYTHON · CUSTOMTKINTER · SCRCPY · PYINSTALLER</samp>
</p>

### <samp>01 — WHAT IT IS</samp>

A small Windows app that mirrors an Android phone's screen to your PC over USB. It is a
friendly front end for [scrcpy](https://github.com/Genymobile/scrcpy): pick a frame rate
and quality, press one button, and the phone appears in a window.

There is nothing to set up by hand. If scrcpy is not on the machine yet, the app downloads
it on first run and keeps it in `%LOCALAPPDATA%\AndroidMirrorApp`.

### <samp>02 — WHAT YOU CAN SET</samp>

| Setting | Options |
|---|---|
| Frame rate | 30, 45, 60, 90 or 120 FPS |
| Quality | Video bitrate: 2M, 4M, 8M, 16M or 32M |
| Rotation | 0°, 90° left, 180°, 90° right |
| Turn the phone screen off | Keeps mirroring while the phone's own display is dark |
| Stay awake | Stops the phone from sleeping while it is plugged in |

The interface is in Hungarian.

### <samp>03 — USE IT</samp>

1. On the phone, enable **Developer options → USB debugging** and plug it in over USB.
2. Run `Installer/Setup_Mirror.exe` to install, or start `dist/Mirror.exe` directly.
3. Press the start button and accept the debugging prompt on the phone.

### <samp>04 — RUN FROM SOURCE</samp>

Windows only: it launches the Windows build of scrcpy.

```bash
pip install customtkinter
python Mirror.py
```

Rebuild the executable with PyInstaller:

```bash
pyinstaller Mirror.spec
```

### <samp>05 — LAYOUT</samp>

| Path | What it is |
|---|---|
| `Mirror.py` | The whole app: CustomTkinter UI, scrcpy download, launch |
| `Mirror.spec` | PyInstaller build recipe |
| `dist/Mirror.exe` | Prebuilt standalone executable |
| `Installer/Setup_Mirror.exe` | Prebuilt installer |

### <samp>06 — LICENCE</samp>

MIT. See [`LICENSE`](./LICENSE). scrcpy is a separate project under its own licence.

<br />

<p align="center">
  <a href="https://github.com/Deatron01"><img src="https://raw.githubusercontent.com/Deatron01/Deatron01/main/assets/icon.png" width="56" alt="Dea" /></a><br />
  <sub><i>Little chaos in a quiet mind.</i></sub><br />
  <sub><samp>MORE WORK AT <a href="https://github.com/Deatron01">GITHUB.COM/DEATRON01</a></samp></sub>
</p>
