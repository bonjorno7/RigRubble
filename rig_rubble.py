import bpy
from mathutils import Vector


class RigRubble(bpy.types.Operator):
    """Automatically rig objects in a collection to an armature"""
    bl_options = {'REGISTER', 'UNDO'}
    bl_idname = "armature.rig_rubble"
    bl_label = "Rig Rubble"

    def execute(self, context):

        # Get the current active collection
        col = context.view_layer.active_layer_collection.collection

        # Get a list of all objects in the collection
        all_objs = col.all_objects

        # Get a list of mesh objects from the list of objects
        mesh_objs = [o for o in all_objs if o.type == 'MESH']

        # Get the first armature object from the list of objects
        arm_obj = next((o for o in all_objs if o.type == 'ARMATURE'), None)

        # If no armature was found, create one
        if not arm_obj:

            # First create the data block for the armature
            arm_data = bpy.data.armatures.new(name=col.name + " Armature")

            # Next create the object to hold that data
            arm_obj = bpy.data.objects.new(name=col.name + " Armature", object_data=arm_data)

            # Then link the object to the collection
            col.objects.link(arm_obj)

            # Finally set it to show in front of other objects
            arm_obj.show_in_front = True

        # Enter edit mode on the armature so we can edit the bones
        active = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Iterate through mesh objects to create the corresponding bones
        for obj in mesh_objs:

            # Get the armature's edit bones
            bones = arm_obj.data.edit_bones

            # Get the bone that matches this object in name
            bone = next((b for b in bones if b.name == obj.name), None)

            # If no matching bone was found, create one
            if not bone:
                bone = bones.new(obj.name)

            # Set the head to be at the origin minus almost half the height
            bone.head = obj.location - Vector((0.0, 0.0, obj.dimensions[2] * 0.4))

            # Set the tail to be at the origin plus almost half the height
            bone.tail = obj.location + Vector((0.0, 0.0, obj.dimensions[2] * 0.4))

        # Exit edit mode on the armature so we can get back to business
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = active

        # Iterate through mesh objects to parent them to the armature
        for obj in mesh_objs:

            # Clear any existing vertex groups
            obj.vertex_groups.clear()

            # Create a vertex group with the name of this object
            group = obj.vertex_groups.new(name=obj.name)

            # Add all of the object's vertices to the group
            group.add(index=list(range(len(obj.data.vertices))), weight=1.0, type='REPLACE')

            # Remove any existing armature modifiers
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE':
                    obj.modifiers.remove(mod)

            # Add new armature modifier with the right settings
            mod = obj.modifiers.new("Armature", 'ARMATURE')
            mod.use_vertex_groups = True
            mod.object = arm_obj

        # Tell the user what we did
        self.report({'INFO'}, f"Rigged {len(mesh_objs)} object(s)")

        # And finally return finished
        return {'FINISHED'}
