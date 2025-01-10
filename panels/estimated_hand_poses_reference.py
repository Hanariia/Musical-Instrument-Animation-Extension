import bpy


class EstimatedHandPosesReferencePanel(bpy.types.Panel):
    bl_idname = "ESTIMATED_HAND_POSES_REFERENCE_PT_Panel"
    bl_label = "Estimated Hand Poses Reference"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Musical Instrument Animation"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("screen.setup_video_reference", text="Setup Video Reference")

