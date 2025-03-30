import bpy
import site
import sys



user_site_pkgs = site.getusersitepackages()
if user_site_pkgs not in sys.path:
    sys.path.insert(0, user_site_pkgs)

try:
    from .operators.hand_pose_overlay import HandPoseOverlayOperator, HandPoseOverlayProperties
    from .panels.estimated_hand_poses_reference import EstimatedHandPosesReferencePanel
    from .panels.reference_settings_pannel import VideoReferenceSettingsPanel
    from .operators.setup_video_reference import SetupVideoReferenceOperator
    from .operators.check_sequencer_availability import CheckSequencerAvailabilityOperator
    from .operators.import_hand_data import ImportHandDataOperator
except ImportError as import_error:
    raise Exception(f"{import_error.msg}. Please install the missing packages to {user_site_pkgs}")

bl_info = {
    "name": "Musical Instrument Animation Extension",
    "author": "Hana Drtílková",
    "description": "",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}

classes = [
    EstimatedHandPosesReferencePanel, SetupVideoReferenceOperator, HandPoseOverlayOperator, HandPoseOverlayProperties, VideoReferenceSettingsPanel,
    CheckSequencerAvailabilityOperator, ImportHandDataOperator
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register Properties
    bpy.types.WindowManager.overlay_properties = bpy.props.PointerProperty(type=HandPoseOverlayProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # Unregister Properties
    del bpy.types.WindowManager.overlay_properties
