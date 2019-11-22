import bpy
from . rig_rubble import RigRubble


bl_info = {
    "blender": (2, 80, 0),
    "name": "Rig Rubble",
    "description": "Automatically rig objects in a collection to an armature",
    "author": "bonjorno7",
    "version": (0, 0, 1),
    "location": "Search Menu",
    "category": "Rigging",
    "warning": "",
}


def register():
    bpy.utils.register_class(RigRubble)


def unregister():
    bpy.utils.unregister_class(RigRubble)
