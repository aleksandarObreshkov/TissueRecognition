import slideio
import tensorflow as tf


image_path = "C:\\Users\\aleks\\Desktop\\image\\big3.svs"
scene = slideio.open_slide(image_path,'SVS').get_scene(0)
print(scene.num_z_slices)

(_, _, width, height) = scene.rect
print(f'Height is {height} pixels and width is {width} pixels')

h = 0
iterations = 0
while h<height:
    w = 0
    while w<width:
        block = scene.read_block((w, h, 224, 224), size=(0,0), channel_indices=[])
        tf.keras.preprocessing.image.save_img(f"C:\\Users\\aleks\\Desktop\\image\\cuts\{iterations}.tif",
                                              block)
        w+=224
        print(f"On {iterations} iteration")
        iterations+=1
    h+=224
