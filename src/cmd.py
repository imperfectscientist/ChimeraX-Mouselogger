import math
import time
try:
    from PyQt6.QtCore import QTimer
except ImportError:
    from PyQt5.QtCore import QTimer

from chimerax.core.commands import CmdDesc
from chimerax.geometry import Place

class MouseTracker:
    def __init__(self, session):
        self.session = session
        self.start_positions = {}
        self.start_camera_pos = None
        
        self.last_positions = {}
        self.last_camera_pos = None
        
        self.last_move_time = 0
        self.is_moving = False
        
        # Initialize last positions
        self._save_state(self.last_positions, True)
        
        # Use a QTimer to poll positions every 50ms.
        # This guarantees we don't rely on 'new frame', which stops firing when idle.
        self.timer = QTimer()
        self.timer.timeout.connect(self._poll_positions)
        self.timer.start(50)

    def _save_state(self, target_dict, save_camera=False):
        from chimerax.geometry import Place
        target_dict.clear()
        for model in self.session.models.list():
            if hasattr(model, 'position'):
                target_dict[model.id] = Place(model.position.matrix)
                
        if save_camera and getattr(self.session, 'main_view', None) and self.session.main_view.camera:
            return Place(self.session.main_view.camera.position.matrix)
        return None

    def _has_moved(self):
        # compare current with last_positions
        for model in self.session.models.list():
            if hasattr(model, 'position'):
                if model.id not in self.last_positions:
                    return True
                old_p = self.last_positions[model.id]
                new_p = model.position
                delta = new_p * old_p.inverse()
                
                rot = getattr(delta, 'rotation_angle', 0)
                if callable(rot): rot = rot()
                if math.degrees(rot) > 0.001:
                    return True
                
                trans = getattr(delta, 'translation', [0,0,0])
                if callable(trans): trans = trans()
                if sum(x*x for x in trans) > 0.0001:
                    return True
        
        if getattr(self.session, 'main_view', None) and self.session.main_view.camera:
            if not self.last_camera_pos:
                return True
            delta = self.session.main_view.camera.position * self.last_camera_pos.inverse()
            rot = getattr(delta, 'rotation_angle', 0)
            if callable(rot): rot = rot()
            if math.degrees(rot) > 0.001:
                return True
                
            trans = getattr(delta, 'translation', [0,0,0])
            if callable(trans): trans = trans()
            if sum(x*x for x in trans) > 0.0001:
                return True
                
        return False

    def _poll_positions(self):
        moved = self._has_moved()
        current_time = time.time()
        
        if moved:
            self.last_move_time = current_time
            if not self.is_moving:
                self.is_moving = True
                self.start_camera_pos = self._save_state(self.start_positions, True)
                
            self.last_camera_pos = self._save_state(self.last_positions, True)
        else:
            if self.is_moving and (current_time - self.last_move_time) > 0.5:
                # Stopped moving for 0.5s
                self.is_moving = False
                self._calculate_and_log()
                
    def _calculate_and_log(self):
        commands_to_log = []
        
        # 1. Check specific models
        for model in self.session.models.list():
            if hasattr(model, 'position') and model.id in self.start_positions:
                start_place = self.start_positions[model.id]
                end_place = model.position
                delta = end_place * start_place.inverse()
                
                try:
                    if callable(getattr(delta, 'rotation_axis_and_angle', None)):
                        axis, rot = delta.rotation_axis_and_angle()
                        angle_deg = rot
                        if abs(angle_deg) > 0.1:
                            axis_str = f"{axis[0]:.3f},{axis[1]:.3f},{axis[2]:.3f}"
                            commands_to_log.append(f'<b><a title="Help for \'turn\' command" href="help:user/commands/turn.html">turn</a></b> {axis_str} {angle_deg:.1f} models #{model.id_string}')
                            
                    if callable(getattr(delta, 'translation', None)):
                        trans = delta.translation()
                        dist = math.sqrt(sum(x*x for x in trans))
                        if dist > 0.01:
                            trans_axis = [x/dist for x in trans]
                            axis_str = f"{trans_axis[0]:.3f},{trans_axis[1]:.3f},{trans_axis[2]:.3f}"
                            commands_to_log.append(f'<b><a title="Help for \'move\' command" href="help:user/commands/move.html">move</a></b> {axis_str} {dist:.2f} models #{model.id_string}')
                except Exception:
                    pass
        
        # 2. Check scene (camera) if no specific models moved
        if not commands_to_log and self.start_camera_pos and getattr(self.session, 'main_view', None) and self.session.main_view.camera:
            end_cam_place = self.session.main_view.camera.position
            delta = end_cam_place * self.start_camera_pos.inverse()
            
            # If models are selected, append them to the command so the user can apply the scene rotation to just those models
            model_suffix = ""
            if hasattr(self.session, 'selection'):
                sel_models = list(self.session.selection.models())
                if sel_models:
                    model_ids = ",".join([m.id_string for m in sel_models])
                    model_suffix = f" models #{model_ids}"
            
            try:
                if callable(getattr(delta, 'rotation_axis_and_angle', None)):
                    axis, rot = delta.rotation_axis_and_angle()
                    angle_deg = rot
                    if abs(angle_deg) > 0.1:
                        # Camera movement is inverse of scene movement
                        axis_str = f"{-axis[0]:.3f},{-axis[1]:.3f},{-axis[2]:.3f}"
                        commands_to_log.append(f'<b><a title="Help for \'turn\' command" href="help:user/commands/turn.html">turn</a></b> {axis_str} {angle_deg:.1f}{model_suffix}')
                        
                if callable(getattr(delta, 'translation', None)):
                    trans = delta.translation()
                    dist = math.sqrt(sum(x*x for x in trans))
                    if dist > 0.01:
                        # Camera translation is inverse of scene translation
                        trans_axis = [-x/dist for x in trans]
                        axis_str = f"{trans_axis[0]:.3f},{trans_axis[1]:.3f},{trans_axis[2]:.3f}"
                        commands_to_log.append(f'<b><a title="Help for \'move\' command" href="help:user/commands/move.html">move</a></b> {axis_str} {dist:.2f}{model_suffix}')
            except Exception:
                pass

        if commands_to_log:
            # Log the message explicitly to the logger
            for cmd_str in commands_to_log:
                self.session.logger.info(cmd_str, is_html=True)
            
        self.start_positions.clear()
        self.start_camera_pos = None

    def destroy(self):
        if hasattr(self, 'timer'):
            self.timer.stop()


_tracker_instance = None

def handle_mouselogger(session, action):
    global _tracker_instance
    if action == "start":
        if _tracker_instance is not None:
            session.logger.warning("Mouse logger is already running.")
            return
        _tracker_instance = MouseTracker(session)
        session.logger.info("3D Mouse tracking started. Run 'mouselogger stop' to stop.")
    elif action == "stop":
        if _tracker_instance is None:
            session.logger.warning("Mouse logger is not running.")
            return
        _tracker_instance.destroy()
        _tracker_instance = None
        session.logger.info("3D Mouse tracking stopped.")

from chimerax.core.commands import CmdDesc, EnumOf
mouselogger_desc = CmdDesc(
    required=[("action", EnumOf(["start", "stop"]))],
    optional=[],
    synopsis="Log 3D mouse rotations and translations"
)
