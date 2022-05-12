import foam_ct_phantom
from PIL import Image

# paths and filenames
filename = "test_foam"
phantom_save_path = 'data/foam/phantoms/'+ filename + '.h5'
volume_save_path = "data/foam/geometries/" + filename + '.h5'
img_save_path = "data/foam/images/" + filename + '.png'

# set n_spheres to a low value for faster computation time
# and less 'holes' in the phantom
n_spheres = 1000  

# extra control variables
random_seed = 69  # to 'reproduce' results, lol
generate_foam = True
display_img = False
img_save = True

# generate phantom
if generate_foam:
    foam_ct_phantom.FoamPhantom.generate(phantom_save_path,random_seed,nspheres_per_unit=n_spheres)
# load phantom
phantom = foam_ct_phantom.FoamPhantom(phantom_save_path)
# generate phantom geometry
geom = foam_ct_phantom.VolumeGeometry(256,256,1,3/256)
# generate phantom volume from phantom geometry
phantom.generate_volume(volume_save_path, geom)
# load volume
vol = foam_ct_phantom.load_volume(volume_save_path)

# visualize and save image
img = Image.fromarray(vol[0]*255)
img = img.convert('L')
if img_save:
    img.save(img_save_path)
if display_img:
    img.show()