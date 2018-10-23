import bpy
from .align_operator import *


bl_info = {
    "name": "Align Origin",
    "description": "Tool to align object's origin",
    "version": (0, 0, 1),
    "category": "Object",
}


def register():
    bpy.utils.register_class(AlignOriginOperator)
    bpy.utils.register_class(AlignOriginPanel)


def unregister():
    bpy.utils.unregister_class(AlignOriginOperator)
    bpy.utils.unregister_class(AlignOriginPanel)
