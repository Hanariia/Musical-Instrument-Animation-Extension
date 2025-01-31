import bpy
from ..operators.setup_video_reference import SetupVideoReferenceOperator
from ..operators.hand_pose_overlay import HandPoseOverlayOperator


class EstimatedHandPosesReferencePanel(bpy.types.Panel):
    bl_idname = "ESTIMATED_HAND_POSES_REFERENCE_PT_Panel"
    bl_label = "Estimated Hand Poses Reference"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Musical Instrument Animation"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(SetupVideoReferenceOperator.bl_idname, text=SetupVideoReferenceOperator.bl_label)
        row = layout.row()
        row.operator(HandPoseOverlayOperator.bl_idname, text="Import Estimated Hand Poses")

