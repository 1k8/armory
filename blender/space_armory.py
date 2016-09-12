# Embedded player in Armory Space
import bpy
from bpy.types import Header
from bpy.app.translations import contexts as i18n_contexts
import utils
import make

class SPACEARMORY_HT_header(Header):
    bl_space_type = 'VIEW_GAME'

    info_text = ''
    is_paused = False

    def draw(self, context):
        layout = self.layout
        view = context.space_data
        obj = context.active_object
        toolsettings = context.tool_settings

        row = layout.row(align=True)
        # row.template_header()
        row.operator('arm.space_stop', icon='MESH_PLANE')
        if SPACEARMORY_HT_header.is_paused:
            row.operator('arm.space_resume', icon="PLAY")
        else:
            row.operator('arm.space_pause', icon="PAUSE")

        layout.label(SPACEARMORY_HT_header.info_text)

class ArmorySpaceStopButton(bpy.types.Operator):
    bl_idname = 'arm.space_stop'
    bl_label = 'Stop'
 
    def execute(self, context):
        area = bpy.context.area
        area.type = 'VIEW_3D'
        SPACEARMORY_HT_header.is_paused = False
        SPACEARMORY_HT_header.info_text = ''
        return{'FINISHED'}

class ArmorySpacePauseButton(bpy.types.Operator):
    bl_idname = 'arm.space_pause'
    bl_label = 'Pause'
 
    def execute(self, context):
        SPACEARMORY_HT_header.is_paused = True
        return{'FINISHED'}

class ArmorySpaceResumeButton(bpy.types.Operator):
    bl_idname = 'arm.space_resume'
    bl_label = 'Resume'
 
    def execute(self, context):
        SPACEARMORY_HT_header.is_paused = False
        return{'FINISHED'}

def register():
    if utils.with_chromium():
        bpy.utils.register_module(__name__)

def unregister():
    if utils.with_chromium():
        bpy.utils.unregister_module(__name__)
