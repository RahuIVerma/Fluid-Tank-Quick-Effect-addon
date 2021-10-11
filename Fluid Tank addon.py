bl_info = {
    "name": "Fluid Tank",
    "author": "Rahul Verma",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Object > Quick Effects > Fluid Tank",
    "description": "Setup Fluid Tank simulation",
    "warning": "",
    "doc_url": "",
    "category": "Physics",
}

import bpy
from mathutils import Vector

class FluidTank(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.quick_fluidtank"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Quick Fluid Tank"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        # Wireframe Mode
        my_areas = bpy.context.workspace.screens[0].areas
        my_shading = 'WIREFRAME'  # 'WIREFRAME' 'SOLID' 'MATERIAL' 'RENDERED'


        for area in my_areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = my_shading
        print("Wireframe DONE")
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')  # Origin to Geometery

        #Make selected objects a collidor
        sel_obj = bpy.context.selected_objects  # sel_obj is the list of All selected objects
        for i in sel_obj:
            if not "Fluid" in i.modifiers:
                bpy.context.view_layer.objects.active = i
                bpy.ops.object.modifier_add(type='FLUID')
                bpy.context.object.modifiers["Fluid"].fluid_type = 'EFFECTOR'
                
        #Get the location of domain object
        verts_sel = [ x.location for x in sel_obj]
        domainLoc = sum(verts_sel, Vector()) / len(verts_sel)  # domainLoc is the location of domain object

        #Get bounding box size
        Xmin = sel_obj[0].location.x
        Ymin = sel_obj[0].location.y
        Zmin = sel_obj[0].location.z
        Xmax = sel_obj[0].location.x
        Ymax = sel_obj[0].location.y
        Zmax = sel_obj[0].location.z
        Xmin_margin = sel_obj[0].dimensions.x/2
        Ymin_margin = sel_obj[0].dimensions.y/2
        Zmin_margin = sel_obj[0].dimensions.z/2
        Xmax_margin = sel_obj[0].dimensions.x/2
        Ymax_margin = sel_obj[0].dimensions.y/2
        Zmax_margin = sel_obj[0].dimensions.z/2
        if len(sel_obj) > 1:
            for j in sel_obj:
                if j.location.x < Xmin:
                    Xmin = j.location.x
                    Xmin_margin = j.dimensions.x/2
                if j.location.y < Ymin:
                    Ymin = j.location.y
                    Ymin_margin = j.dimensions.y/2
                if j.location.z < Zmin:
                    Zmin = j.location.z
                    Zmin_margin = j.dimensions.z/2
                if j.location.x > Xmax:
                    Xmax = j.location.x
                    Xmax_margin = j.dimensions.x/2
                if j.location.y > Ymax:
                    Ymax = j.location.y
                    Ymax_margin = j.dimensions.y/2
                if j.location.z > Zmax:
                    Zmax = j.location.z
                    Zmax_margin = j.dimensions.z/2

        tempX = Xmax-Xmin+Xmax_margin+Xmin_margin
        tempY = Ymax-Ymin+Ymax_margin+Ymin_margin
        tempZ = Zmax-Zmin+Zmax_margin+Zmin_margin

        boundDimen = Vector((tempX, tempY, tempZ))
        #bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(domainLoc), scale=(boundDimen)) # Just for seeing bounding box
        print(boundDimen)

         # Get the dimensions of the active object
        domainHeight = domainLoc.z + (boundDimen.z/2) +1
        tankScale = 5

         #Create another object for flow object
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(domainLoc.x, domainLoc.y, domainHeight/4), scale=(tankScale*boundDimen.x/2, tankScale*boundDimen.y/2, domainHeight/2))
        print("flow obj is created")

        #Rename it
        bpy.context.object.name = "Fluid Source"

        #Disable rendering
        bpy.context.object.hide_render = True

        #Wireframe in shading
        bpy.context.object.display_type = 'WIRE'

        #Make it Fluid domain
        bpy.ops.object.modifier_add(type='FLUID')
        bpy.context.object.modifiers["Fluid"].fluid_type = 'FLOW'
        bpy.context.object.modifiers["Fluid"].flow_settings.flow_type = 'LIQUID'

        # Create object for domain

        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(domainLoc.x, domainLoc.y, domainHeight/2), scale=(tankScale*boundDimen.x/2, tankScale*boundDimen.y/2, domainHeight))
        print("Domain obj is created")

        #Rename it
        bpy.context.object.name = "Fluid Tank"

        #Make it Fluid domain
        bpy.ops.object.modifier_add(type='FLUID')
        bpy.context.object.modifiers["Fluid"].fluid_type = 'DOMAIN'
        bpy.context.object.modifiers["Fluid"].domain_settings.domain_type = 'LIQUID'
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(FluidTank.bl_idname)

def register():
    bpy.utils.register_class(FluidTank)
    bpy.types.VIEW3D_MT_object_quick_effects.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(FluidTank)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()