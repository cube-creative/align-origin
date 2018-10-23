import bpy
from mathutils import Vector


def align_object_origin(object, axis, align):
    bbox = object.bound_box

    # convert object to world coordinates
    world_bbox = []
    for c in bbox:
        world_bbox.append(list(object.matrix_world * Vector(tuple(c))))

    if not (0 <= axis <= 2):
        raise "Invalid axis."

    min_along_axis = min([c[axis] for c in world_bbox])
    max_along_axis = max([c[axis] for c in world_bbox])

    print([c[axis] for c in world_bbox])

    if align == 'min':
        new_coordinate = min_along_axis
    if align == 'max':
        new_coordinate = max_along_axis
    if align == 'center':
        new_coordinate = (min_along_axis + max_along_axis) / 2

    print(new_coordinate)

    saved_location = bpy.context.scene.cursor_location.copy()  # returns a vector
    bpy.context.scene.cursor_location = object.location
    bpy.context.scene.cursor_location[axis] = new_coordinate
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor_location = saved_location


class AlignOriginOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.align_origin_operator"
    bl_label = "Origin Alignment Operator"
    bl_options = {'REGISTER', 'UNDO'}

    axis = bpy.props.EnumProperty(items=[("0", "X", "Align Axis"), ("1", "Y", "Align Axis"), ("2", "Z", "Align Axis")],
                                  description="World axis for alignment", default="0")
    align_type = bpy.props.EnumProperty(
        items=[("min", "Min", "Minimum"), ("center", "Center", "Center"), ("max", "Max", "Maximum")],
        description="Alignment type", default="center")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        objects = bpy.context.selected_objects.copy()
        for o in objects:
            bpy.ops.object.select_all(action='DESELECT')
            o.select = True
            align_object_origin(o, int(self.axis), self.align_type)
        bpy.ops.object.select_all(action='DESELECT')
        for o in objects:
            o.select = True
        return {'FINISHED'}


class AlignOriginPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Align Origin"
    bl_category = "Tools"

    def draw(self, context):

        row = self.layout.row(align=True)
        row_col = row.column(align=True)
        row_col.label(text='')
        row_col.label(text='X')
        row_col.label(text='Y')
        row_col.label(text='Z')

        row_col = row.column(align=True)
        row_col.label(text='Min')
        b = row_col.operator("object.align_origin_operator", text="", icon='ZOOMOUT')
        b.axis = '0'
        b.align_type = 'min'
        b = row_col.operator("object.align_origin_operator", text="", icon='ZOOMOUT')
        b.axis = '1'
        b.align_type = 'min'
        b = row_col.operator("object.align_origin_operator", text="", icon='ZOOMOUT')
        b.axis = '2'
        b.align_type = 'min'

        row_col = row.column(align=True)
        row_col.label(text='Center')
        b = row_col.operator("object.align_origin_operator", text="", icon='SPACE3')
        b.axis = '0'
        b.align_type = 'center'
        b = row_col.operator("object.align_origin_operator", text="", icon='SPACE3')
        b.axis = '1'
        b.align_type = 'center'
        b = row_col.operator("object.align_origin_operator", text="", icon='SPACE3')
        b.axis = '2'
        b.align_type = 'center'

        row_col = row.column(align=True)
        row_col.label(text='Max')
        b = row_col.operator("object.align_origin_operator", text="", icon='ZOOMIN')
        b.axis = '0'
        b.align_type = 'max'
        b = row_col.operator("object.align_origin_operator", text="", icon='ZOOMIN')
        b.axis = '1'
        b.align_type = 'max'
        b = row_col.operator("object.align_origin_operator", text="", icon='ZOOMIN')
        b.axis = '2'
        b.align_type = 'max'
