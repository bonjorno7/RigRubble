import bpy


class RigRubble(bpy.types.Operator):
    """Automatically rig objects in a collection to an armature"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "armature.rig_rubble"
    bl_label = "Rig Rubble"

    def execute(self, context):
        return {'FINISHED'}
