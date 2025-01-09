import bpy
from .panels.estimated_hand_poses_reference import EstimatedHandPosesReferencePanel

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
    EstimatedHandPosesReferencePanel
]

register, unregister = bpy.utils.register_classes_factory(classes)
