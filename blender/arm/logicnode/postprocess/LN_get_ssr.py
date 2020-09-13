from arm.logicnode.arm_nodes import *

class SSRGetNode(ArmLogicTreeNode):
    """Get SSR Effect"""
    bl_idname = 'LNSSRGetNode'
    bl_label = 'Get SSR'
    arm_version = 1

    def init(self, context):
        super(SSRGetNode, self).init(context)
        self.add_output('NodeSocketFloat', 'SSR Step')
        self.add_output('NodeSocketFloat', 'SSR Step Min')
        self.add_output('NodeSocketFloat', 'SSR Search')
        self.add_output('NodeSocketFloat', 'SSR Falloff')
        self.add_output('NodeSocketFloat', 'SSR Jitter')

add_node(SSRGetNode, category=PKG_AS_CATEGORY)
