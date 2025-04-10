import bpy
from ..operators.setup_video_reference import SetupVideoReferenceOperator


class EstimatedHandPosesReferencePanel(bpy.types.Panel):
    bl_idname = "ESTIMATED_HAND_POSES_REFERENCE_PT_Panel"
    bl_label = "Estimated Hand Poses Reference"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Musical Instrument Animation"

    def draw(self, context):
        layout = self.layout
        layout.operator("mia.check_sequencer_availability", text=SetupVideoReferenceOperator.bl_label, icon='FILE_MOVIE')
        layout.operator("mia.import_hand_data", icon='IMPORT')

