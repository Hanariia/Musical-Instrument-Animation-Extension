import bpy
import site
import sys


user_site_pkgs = site.getusersitepackages()
if user_site_pkgs not in sys.path:
    sys.path.insert(0, user_site_pkgs)

try:
    from .operators.hand_pose_overlay import HandPoseOverlayOperator
    from .panels.estimated_hand_poses_reference import EstimatedHandPosesReferencePanel
    from .operators.setup_video_reference import SetupVideoReferenceOperator
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
    EstimatedHandPosesReferencePanel, SetupVideoReferenceOperator, HandPoseOverlayOperator
]

register, unregister = bpy.utils.register_classes_factory(classes)
