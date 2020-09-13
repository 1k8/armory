from arm.logicnode.arm_nodes import *

class GetVisibleNode(ArmLogicTreeNode):
    """Get visible node"""
    bl_idname = 'LNGetVisibleNode'
    bl_label = 'Get Visible'
    arm_version = 1

    def init(self, context):
        super(GetVisibleNode, self).init(context)
        self.add_input('ArmNodeSocketObject', 'Object')
        self.add_output('NodeSocketBool', 'Visible')

add_node(GetVisibleNode, category=PKG_AS_CATEGORY, section='props')
