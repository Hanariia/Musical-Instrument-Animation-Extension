import bpy
import site
import sys

from .operators.clear_reference import ClearReferenceOperator
from .operators.refresh_overlay_wrapper import RefreshOverlayWrapperOperator
from .operators.clear_overlay_wrapper import ClearOverlayWrapperOperator
from .settings_properties import OverlaySettings, VideoReferenceSettings
from .panels.estimated_hand_poses_reference import EstimatedHandPosesReferencePanel
from .panels.overlay_settings_panel import OverlaySettingsPanel
from .operators.setup_video_reference import SetupVideoReferenceOperator, VideoReferenceProperties
from .operators.check_sequencer_availability import CheckSequencerAvailabilityOperator
from .operators.import_hand_poses import ImportHandPosesOperator

user_site_pkgs = site.getusersitepackages()
if user_site_pkgs not in sys.path:
    sys.path.append(user_site_pkgs)

try:
    from .operators.hand_pose_overlay import HandPoseOverlayOperator, HandPoseOverlayProperties
except ImportError as import_error:
    raise Exception(f"{import_error.msg}. Please install the missing Pillow package with the following command:\n"
                    f"pip --python \"{sys.executable}\" install Pillow --target \"{user_site_pkgs}\"")

bl_info = {
    "name": "Musical Instrument Animation Reference Extension",
    "author": "Hana Drtílková",
    "description": "An add-on for displaying a reference video with hand pose data visualized as an overlay.",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Musical Instrument Animation",
    "warning": "",
    "doc_url": "https://github.com/Hanariia/Musical-Instrument-Animation-Reference-Extension/blob/main/README.md",
    "category": "Animation"
}

classes = [
    EstimatedHandPosesReferencePanel, SetupVideoReferenceOperator, HandPoseOverlayOperator, HandPoseOverlayProperties,
    OverlaySettingsPanel, CheckSequencerAvailabilityOperator, ImportHandPosesOperator, OverlaySettings,
    VideoReferenceSettings, VideoReferenceProperties, ClearOverlayWrapperOperator, RefreshOverlayWrapperOperator,
    ClearReferenceOperator
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register Properties
    bpy.types.WindowManager.reference_active = bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.overlay_properties = bpy.props.PointerProperty(type=HandPoseOverlayProperties)
    bpy.types.WindowManager.video_reference_properties = bpy.props.PointerProperty(type=VideoReferenceProperties)
    bpy.types.Scene.overlay_settings = bpy.props.PointerProperty(type=OverlaySettings)
    bpy.types.Scene.video_reference_settings = bpy.props.PointerProperty(type=VideoReferenceSettings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Unregister Properties
    del bpy.types.WindowManager.reference_active
    del bpy.types.WindowManager.overlay_properties
    del bpy.types.WindowManager.video_reference_properties
    del bpy.types.Scene.overlay_settings
    del bpy.types.Scene.video_reference_settings
