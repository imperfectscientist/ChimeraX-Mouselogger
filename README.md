# ChimeraX-MouseLogger

A ChimeraX plugin that logs user mouse interactions (scene rotation, translation, and specific model movement) into mathematically precise ChimeraX commands. 

This is incredibly useful if you want to perfectly replicate a specific camera angle or model placement in a script or command line exactly as you configured it with your mouse.

## Features
- **Automatic Polling:** Tracks mouse interactions seamlessly across Windows, macOS, and Linux without relying on platform-specific Qt event hooks.
- **Precision Logging:** Converts interactions into exact, repeatable `turn` and `move` commands.
- **Interactive UI Logs:** Outputs clickable HTML links in your ChimeraX Log so you can immediately view command documentation.
- **Cross-Platform:** Distributed as a pure Python `.whl` package with no compiled dependencies.

## Installation

### For End Users
If you received the `chimerax_mouselogger-*.whl` package, you can install it directly inside ChimeraX.

1. Open ChimeraX.
2. In the ChimeraX command line, run the following command (update the path to where your file is located):
   ```text
   toolshed install /path/to/downloads/chimerax_mouselogger-0.10-py3-none-any.whl
   ```

### For Developers
If you are modifying the source code and want to install the plugin directly from the directory:

1. Open a terminal or ChimeraX command line.
2. Run the `devel install` command pointing to the root directory of this repository:
   ```text
   devel install /path/to/ChimeraX/MouseLogger
   ```
*(Note: If you are using Flatpak on Linux, you may need to use `flatpak run edu.ucsf.rbvi.ChimeraX --nogui --cmd "devel install /path/to/ChimeraX/MouseLogger" --exit`)*

## Usage

Once the plugin is installed, you can start tracking your mouse interactions directly via the ChimeraX command line.

### Start Logging
To turn on the mouse logger, type:
```text
mouselogger start
```
*You will see a message confirming the logger has started.*

### Stop Logging
To turn off the mouse logger, type:
```text
mouselogger stop
```
*You will see a message confirming the logger has stopped.*

### Example Output
While the logger is active, rotate or translate your scene using the mouse. When you release the mouse (after about 0.5 seconds), the calculated commands will appear in your ChimeraX Log like this:
```text
turn 1.000,-0.000,-0.000 45.0
move -0.000,0.707,-0.707 10.00
```
If you move a specific molecule model (e.g. Model #1), the logger will automatically format the command for that model:
```text
turn 1.000,-0.000,-0.000 45.0 models #1
move -0.000,0.707,-0.707 10.00 models #1
```

You can copy and paste these exact lines directly into scripts or your command line to flawlessly reproduce your interaction!

## Troubleshooting

- **"Unknown command: mouselogger start"**: Ensure the plugin is installed correctly. You can check installed plugins by clicking `Tools -> More Tools -> Tool Shed` or via `toolshed list`.
- **Logs not showing up**: Make sure your ChimeraX Log panel is open (`Tools -> General -> Log`). Wait about 0.5 seconds after moving the mouse; the plugin batches movements to prevent spamming your log during a continuous drag.
