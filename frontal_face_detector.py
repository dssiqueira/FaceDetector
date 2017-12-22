import dlib
import scipy.misc
from skimage import io

# Add your image
file_name = "raw.jpg"

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()

# Load the image
image = io.imread(file_name)

win = dlib.image_window()

# Open a window on the desktop showing the image
win.set_image(image)

# Return all detected faces
faces = face_detector(image, 1)

for i, face in enumerate(faces):
    # Draw a box around each face
    win.add_overlay(face)

crop = image[face.top():face.bottom(),face.left():face.right()]
cropped_img = image[face.top()-250:face.bottom()+300,face.left()-150:face.right()+150]

# Save face
scipy.misc.imsave('crop.jpg', crop)

# Save image cropped with padding
scipy.misc.imsave('cropped_img.jpg', cropped_img)
	        
# Wait until the user hits <enter> to close the window	        
dlib.hit_enter_to_continue()