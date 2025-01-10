import bpy


class SetupVideoReferenceOperator(bpy.types.Operator):
    """Adds an area with a video reference to the screen."""
    bl_idname = "screen.setup_video_reference"
    bl_label = "Setup Video Reference"

    @classmethod
    def poll(cls, context):
        for area in context.screen.areas.values():
            if area.type == 'VIEW_3D':
                return True
        return False

    def execute(self, context):
        view_3d_area = self.__find_area(context, 'VIEW_3D')

        with context.temp_override(area=view_3d_area):
            bpy.ops.screen.area_split(direction='VERTICAL')
            bpy.context.area.ui_type = 'SEQUENCE_EDITOR'
            bpy.context.space_data.view_type = 'PREVIEW'
        return {'FINISHED'}

    @staticmethod
    def __find_area(context, area_type: str) -> bpy.types.Area:
        for area in context.screen.areas:
            if area.type == area_type:
                return area
