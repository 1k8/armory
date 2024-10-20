from arm.logicnode.arm_advanced_draw import *
from arm.logicnode.arm_nodes import *
from bpy.props import *
from bpy.types import Node

class BlendSpaceNode(ArmLogicTreeNode):
    """Activates the output when the given event is received.

    @seeNode Send Event to Object
    @seeNode Send Event"""
    bl_idname = 'LNBlendSpaceNode'
    bl_label = 'Blend Space'
    arm_version = 1
    arm_section = 'custom'

    property2: HaxeBoolProperty(
        'property2',
        name="Enable or Disable",
        description="A bool property",
        default = False
    )

    advanced_draw_run: BoolProperty(
        name = "Advance draw enabled",
        description="",
        default = False
    )

    def stop_modal(self):
        self.property2 = False
    
    def my_float_update(self, context):
        if self.property2:
            self.set_x_y_socket()

    property0: HaxeFloatVectorProperty(
        'property0',
        name = "Point Coordionates",
        description="",
        default = (0.0, 0.0, 
                   0.0, 1.0,
                   1.0, 1.0,
                   1.0, 0.0,
                   0.0, 0.0,
                   0.0, 0.0,
                   0.0, 0.0, 
                   0.0, 0.0, 
                   0.0, 0.0, 
                   0.0, 0.0,
                   0.5, 0.5),
        size = 22,
        update = my_float_update
    )

    active_point_index: IntProperty(
        default = -1
    )

    show_numbers: BoolProperty(
        name = "Show Point Numbers",
        description="",
        default = False
    )

    active_point_index_ref: IntProperty(
        default = 0
    )

    gui_bounds: FloatVectorProperty(
        name = "GUI bounds",
        description = "",
        default = (0.0, 0.0, 0.0),
        size = 3
    )

    point_size: FloatProperty(
        name = "Point Size",
        description = "",
        default = 0.015
    )

    property1: HaxeBoolVectorProperty(
        'property1',
        name = "Point enabled for view",
        description = "",
        default = (True,True,True,True, False, False, False, False, False, False, True),
        size = 11
    )

    draw_handler_dict = {}
    modal_handler_dict = {}

    def __init__(self):
        array_nodes[str(id(self))] = self
        if self.advanced_draw_run:
            self.add_advanced_draw()
    
    def create_blend_space(self):
        self.blend_space = BlendSpaceGUI(self)
    
    def free(self):
        self.remove_advanced_draw()
    
    def get_blend_space_points(self):
        if bpy.context.space_data.edit_tree == self.get_tree():
            return self.blend_space.points
    
    def draw_advanced(self):
        if bpy.context.space_data.edit_tree == self.get_tree():
            self.blend_space.draw()

    def arm_init(self, context):
        self.add_input('ArmNodeSocketObject', 'Object')
        self.add_input('ArmNodeSocketArray', 'Actions')
        self.add_input('ArmBlendSpaceSocket', 'Cursor X')
        self.add_input('ArmBlendSpaceSocket', 'Cursor Y')
        self.add_output('ArmNodeSocketAnimTree', 'Out')

    def add_advanced_draw(self):
        self.advanced_draw_run = True
        handler = self.draw_handler_dict.get(str(self.as_pointer()))
        if handler is None:
            self.create_blend_space()
            editor = getattr(bpy.types, 'SpaceNodeEditor')
            handler = editor.draw_handler_add(self.draw_advanced, (), 'WINDOW', 'POST_VIEW')
            self.draw_handler_dict[str(self.as_pointer())] = handler
            self.property2 = False


    def remove_advanced_draw(self):
        self.advanced_draw_run = False
        handler = self.draw_handler_dict.get(str(self.as_pointer()))
        if handler is not None:
            editor = getattr(bpy.types, 'SpaceNodeEditor')
            editor.draw_handler_remove(handler, 'WINDOW')
            self.draw_handler_dict.pop(str(self.as_pointer()))

    def set_x_y_cursor(self):
        self.property0[20] = self.inputs[2].get_default_value()
        self.property0[21] = self.inputs[3].get_default_value()
    
    def set_x_y_socket(self):
        self.inputs[2].set_default_value(self.property0[20])
        self.inputs[3].set_default_value(self.property0[21])


    def add_point(self):
        for i in range(len(self.property1)):
            if not self.property1[i]:
                self.property1[i] = True
                self.property0[i * 2] = 0.5
                self.property0[i * 2 + 1] = 0.5
                break  
    
    def remove_point(self):
        for i in range(len(self.property1) - 2, 2, -1):
            if self.property1[i]:
                self.property1[i] = False
                self.active_point_index_ref = i - 1
                break

        
    def draw_buttons(self, context, layout):
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        op = row.operator('arm.node_call_func', text='Show', icon='FULLSCREEN_ENTER', emboss=True, depress = self.advanced_draw_run)
        op.node_index = str(id(self))
        op.callback_name = 'add_advanced_draw'
        op = row.operator('arm.node_call_func', text='Hide', icon='FULLSCREEN_EXIT', emboss=True, depress = not self.advanced_draw_run)
        op.node_index = str(id(self))
        op.callback_name = 'remove_advanced_draw'
        if self.advanced_draw_run:
            col = layout.column()
            row = col.row(align=True)
            op = row.operator('arm.blend_space_operator', text = 'Edit', icon = 'EDITMODE_HLT', emboss = True, depress = self.property2)
            op.node_index = str(id(self))
            op = row.operator('arm.node_call_func', text = 'Exit Edit', icon = 'OBJECT_DATAMODE', emboss = True, depress = not self.property2)
            op.node_index = str(id(self))
            op.callback_name = 'stop_modal'
            layout.prop(self, 'show_numbers')
            if self.property2:
                col = layout.column()
                row = col.row(align=True)
                op = row.operator('arm.node_call_func', text = 'Add Point', icon = 'PLUS', emboss = True)
                op.node_index = str(id(self))
                op.callback_name = 'add_point'
                op = row.operator('arm.node_call_func', text = 'Remove Point', icon = 'X', emboss = True)
                op.node_index = str(id(self))
                op.callback_name = 'remove_point'
                cl =layout.column()
                actie_point = self.active_point_index_ref
                pos = ", Pos = " + str(round(self.property0[actie_point * 2], 2)) + ", " + str(round(self.property0[actie_point * 2 + 1], 2))
                if actie_point > 9:
                    cl.label(text = "Selected: Cursor" + pos)
                else:
                    cl.label(text = "Selected: " + str(self.active_point_index_ref + 1) + pos)
            else:
                self.set_x_y_cursor()
