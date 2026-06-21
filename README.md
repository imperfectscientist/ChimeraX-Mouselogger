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

> **Note on Movement Tracking:** All generated `turn` and `move` commands are **relative** to the position the object was in right before you clicked and dragged the mouse (not absolute `0,0,0`). This means the commands are perfectly chainable—pasting multiple commands into a script will execute them sequentially, with each movement starting exactly where the previous one left off!

### Understanding the Output

#### The `turn` command (Rotation)
**Syntax:** `turn <axis> <angle> [models]`

* **`<axis>` (e.g., `1.000,0.000,0.000`)**: The 3D direction vector `(X, Y, Z)` that you are rotating *around*. 
  * `1,0,0` means rotating around the horizontal X-axis (nodding up/down).
  * `0,1,0` means rotating around the vertical Y-axis (spinning left/right).
  * `0,0,1` means rotating around the depth Z-axis (rolling like a steering wheel).
* **`<angle>` (e.g., `45.0`)**: The amount of rotation that occurred around the axis, measured in **degrees**.
* **`[models]` (e.g., `models #1`)**: *(Optional)* Appears if the rotation is restricted to specific selected models rather than the whole screen.

#### The `move` command (Translation)
**Syntax:** `move <axis> <distance> [models]`

* **`<axis>` (e.g., `0.000,1.000,0.000`)**: The 3D vector `(X, Y, Z)` that points in the direction the object is sliding. 
  * `1,0,0` means it slid to the Right.
  * `0,1,0` means it slid Upwards.
  * `0,0,1` means it slid Towards you.
* **`<distance>` (e.g., `10.00`)**: The physical distance the object traveled, measured in **Ångströms** (Å).
* **`[models]` (e.g., `models #1`)**: *(Optional)* Appears if the movement is restricted to specific selected models rather than the whole screen.

## Troubleshooting

- **"Unknown command: mouselogger start"**: Ensure the plugin is installed correctly. You can check installed plugins by clicking `Tools -> More Tools -> Tool Shed` or via `toolshed list`.
- **Logs not showing up**: Make sure your ChimeraX Log panel is open (`Tools -> General -> Log`). Wait about 0.5 seconds after moving the mouse; the plugin batches movements to prevent spamming your log during a continuous drag.
