# Blender script for generation of datasets of random 3d shape images
# The script generates objects with different locations, rotations and lightning.
# Written using Blender 2.80 and Python 3.7.0

# If Blender is added to path, it is possible to run the script directly in the
# command prompt with the command 'blender --background --python ImageGenerator.py'

import bpy
import math
import random

__author__      = "Linus Rickman"
__license__     = "GPL-3.0"
__version__     = "1.0"
__date__        = "26 September 2020"

# ---- Settings: ----
nr_images   = 50        # Number of images to be generated
type        = 'Cube'    # 'Cube', 'Sphere', 'Cone', 'Torus', 'Cylinder', or 'Monkey'.
image_size  = [28,28]   # Image dimension (pixels)
perspective = 'PERSP'   # 'ORTHO' or 'PERSP'
f_path      = '/'       # Filepath
# --------------------

# ---- Scene setup: ----
# Removes all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Sets up camera
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW',
                            location=(0, 0, 0), rotation=(math.pi*0.5, 0,
                            -math.pi*0.5))
camera = bpy.context.object
camera.data.type = perspective
bpy.context.scene.camera = camera
bpy.context.scene.render.image_settings.color_mode = 'BW'
scene = bpy.context.scene
scene.render.resolution_x = image_size[0]
scene.render.resolution_y = image_size[1]
scene.render.resolution_percentage = 100

#--- Image generation: ----
for n in range(nr_images):

    # Lights the scene with randomly located point source
    bpy.ops.object.light_add(type='POINT',  location=(-0.5,
                                14*random.random()-7, 8*random.random()-4))
    bpy.context.object.data.energy = 600

    # Randomly generates position and rotation
    theta = (random.random()-0.5)/3
    phi = (random.random()-0.5)/3
    distance = random.random()*3+6
    x_pos = distance*math.cos(theta)
    y_pos = distance*math.sin(theta)
    z_pos = distance*math.sin(phi)
    rotation_x = random.random()*2*math.pi
    rotation_y = random.random()*2*math.pi
    rotation_z = random.random()*2*math.pi

    # Adds object to scene
    if type=="Sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False,
                                            location=(x_pos, y_pos, z_pos))
    elif type=="Cube":
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False,
                                        location=(x_pos, y_pos, z_pos),
                                        rotation=(rotation_x,rotation_y,rotation_z))
    elif type=="Cone":
        bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2,
                                        enter_editmode=False,
                                        location=(x_pos, y_pos, z_pos),
                                        rotation=(rotation_x,rotation_y,rotation_z))
    elif type=="Torus":
        bpy.ops.mesh.primitive_torus_add(align='WORLD',
                                        location=(x_pos, y_pos, z_pos),
                                        rotation=(rotation_x,rotation_y,rotation_z),
                                        major_radius=1, minor_radius=0.25,
                                        abso_major_rad=1.25, abso_minor_rad=0.75)
    elif type=="Monkey":
        bpy.ops.mesh.primitive_monkey_add(enter_editmode=False,
                                        location=(x_pos, y_pos, z_pos),
                                            rotation=(rotation_x,rotation_y,rotation_z))
    elif type=="Cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2,
                                            enter_editmode=False,
                                            rotation=(rotation_x,rotation_y,rotation_z),
                                            location=(x_pos, y_pos, z_pos))
    else:
        print("Type not recognized")
        break

    # Renders the scene
    bpy.context.scene.render.filepath = f_path+'/'+type+'/'+type+str(n)+'.png'
    bpy.ops.render.render(write_still = True)

    # Removes light and mesh items for the next render
    objects = [obj for obj in bpy.context.scene.objects if obj.type in ('LIGHT', 'MESH')]
    bpy.ops.object.delete({"selected_objects": objects})

    print("Image "+str(n+1)+" of "+ str(nr_images)+" is rendered")
