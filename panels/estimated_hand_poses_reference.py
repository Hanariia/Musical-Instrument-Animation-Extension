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
        # IMPORT VIDEO
        layout.label(text="Video Reference")
        layout.prop(context.scene.video_reference_settings, "start_frame")
        layout.operator("mia.check_sequencer_availability", text=SetupVideoReferenceOperator.bl_label,
                        icon='FILE_MOVIE')

        # IMPORT ESTIMATED HAND POSES
        layout.operator("mia.import_hand_data", icon='IMPORT')

        # RESUME/PAUSE OVERLAY GENERATION
        if context.window_manager.overlay_properties.pause_overlay_generation:
            layout.prop(context.window_manager.overlay_properties, "pause_overlay_generation",
                        text='Resume Overlay Generation', icon='PLAY')
        else:
            layout.prop(context.window_manager.overlay_properties, "pause_overlay_generation", icon='PAUSE')
