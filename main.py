import numpy as np
from keras.models import load_model
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

# Load the pre-trained model
model = load_model('saved_model.h5')

# Map class indices to class names and corresponding precautions
class_names = {
    0: {'name': 'Coccidiosis', 'precaution': 'Keep the coop and surrounding area clean and dry. Practice good hygiene and biosecurity measures. Quarantine new chicken before introducing them to the flock. Monitor the Chicken for any signs of illness.'},
    1: {'name': 'Healthy', 'precaution': 'No precautions needed.'},
    2: {'name': 'Newcastle Disease', 'precaution': 'Vaccinate Chicken against Newcastle disease. Keep the coop and surrounding area clean and dry. Quarantine new Chicken before introducing them to the flock. Monitor the chicken for any signs of illness.'},
    3: {'name': 'Salmonellosis', 'precaution': 'Avoid cross-contamination of raw poultry and other foods. Practice good hygiene and food safety measures.'}
}

# Create a GUI window
root = Tk()
root.title('Disease prediction')

# Create a canvas to display the image
canvas = Canvas(root, width=300, height=300)
canvas.pack()

# Create a label to display the predicted class
label = Label(root, text='Select an image')
label.pack()

# Create a function to classify the image
def classify_image():
    # Open the image file
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    
    # Resize the image to 150x150 pixels
    image = image.resize((150, 150))
    
    # Convert the image to a numpy array
    image_array = np.array(image)
    
    # Normalize the image
    image_array = image_array / 255.0
    
    # Reshape the array to match the input shape of the model
    image_array = np.reshape(image_array, (1, 150, 150, 3))
    
    # Use the model to predict the class of the image
    prediction = model.predict(image_array)[0]
    predicted_class = np.argmax(prediction)
    
    # Map class index to class name and precaution
    predicted_class_name = class_names[predicted_class]['name']
    predicted_class_precaution = class_names[predicted_class]['precaution']
    
    # Update the label with the predicted class
    label.config(text=f'Predicted class: {predicted_class_name}')
    
    # Display the image on the canvas
    img = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.image = img
    
    # Display the precaution for the predicted class in a message box
    messagebox.showinfo('Precaution', predicted_class_precaution)

# Create a button to select an image and classify it
button = Button(root, text='Select an image', command=classify_image)
button.pack()

root.mainloop()
