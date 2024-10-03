#Import necessary libraries
import cv2
import os
import csv


import pandas as pd
import tkinter as tk
import random
from sklearn.linear_model import LogisticRegression
import tkinter as tk
from tkinter import scrolledtext


# Set the directory where the images are stored
directory = "C:/Users/Joshua Nian/PycharmProjects/4AI3 Project/Resources/Pictures/Test_Pictures"

# Set the name of the CSV file, if there is no such a file, it will automatically create one
csv_file = "data_set.csv"

# Initialize a list to hold the data from the image names
data = []

# Walk through the directory tree and find the images
for dirpath, dirnames, filenames in os.walk(directory):

    for filename in filenames:

        if filename.endswith(".jpg"):
            # Load the image through director address
            image = cv2.imread(os.path.join(dirpath, filename))

            # Display the image in a window
            cv2.imshow(filename, image)
            # Use trained cascade to detect positive part
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            haar_cascade = cv2.CascadeClassifier(
                'C:\\Users\\Joshua Nian\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\cascade_v5.xml')
            defect_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)

            # Draw rectangle to highlight defect part
            for (x, y, w, h) in defect_rect:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
            cv2.imshow('Detected Defect Part', image)

            # Wait for a key press to move to the next image
            cv2.waitKey(0)
            # Close all windows
            cv2.destroyAllWindows()

            # Based on whether part is defect, attach 1 or 0 to the end of file names, 1 stands for pass, 0 stands for fail(defect)
            if len(defect_rect) == 0:
                base_filename, extension = os.path.splitext(filename)
                new_filename = base_filename
                new_filename = "_".join(base_filename.split("_")[:]) + "_1"
            else:
                base_filename, extension = os.path.splitext(filename)
                new_filename = base_filename
                new_filename = "_".join(base_filename.split("_")[:]) + "_0"

            # Rename the file
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))

            # Split the new filename by "_" to get the individual components
            components = new_filename.split("_")

            # Append the components to the data list
            data.append(components)

# Write the data to the CSV file
with open(csv_file, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)

#To add headers to the csv, in order to run logistic regression later on
# Open the existing CSV file
with open('data_set.csv', 'r') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]

# Create a new header row
header_row = ['temperature', 'humidity', 'cooling time', 'cooling rate', 'defect']

# Insert the new header row at the beginning of the list of rows
rows.insert(0, header_row)

# Write the updated rows to a new CSV file
with open('data_set_updated.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)


# Logistic regression analysis
# Read data_set_updated.csv and store as data frame
df = pd.read_csv('data_set_updated.csv')

#Display data frame information
df.info()
df_all = df.iloc[:].copy()
print (df_all)

# Create a new window
window = tk.Tk()
window.title("Data Frame Viewer")

# Create a scrolled text widget to display the data
text_widget = scrolledtext.ScrolledText(window, width=80, height=30)

# Add the data frame information to the scrolled text widget
text_widget.insert(tk.INSERT, str(df_all))

# Pack the scrolled text widget into the window
text_widget.pack()

# Start the event loop to display the window
window.mainloop()

#Calculate all the attributes' mean values, and print them out
mean_temperature = df["temperature"].mean()
mean_humidity = df["humidity"].mean()
mean_coolingTime = df["cooling time"].mean()
mean_coolingRate = df["cooling rate"].mean()
print("The mean value of temperature is " + str(mean_temperature))
print("The mean value of humidity is " + str(mean_humidity))
print("The mean value of cooling time is " + str(mean_coolingTime))
print("The mean value of cooling rate is " + str(mean_coolingRate))

#Use temperature and defect as example to display logistic regression analysis
temperature = df[["temperature"]]
defect = df[["defect"]]

# Logistic regression
model_temperature = LogisticRegression()
model_temperature.fit(temperature, defect)
model_temperature.coef_, model_temperature.intercept_

#Print out theta 1 and theta 0
print("Theta 1 is " + str(model_temperature.coef_))
print("Theta 0 is " + str(model_temperature.intercept_))


#Open a new window and print out the following string "Thank you for watching! Don't forget to give our team a FULL MAKR!"
def flash_text():
    # generate a random color from RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    # set the text color to the random color
    label.config(fg=color)

    # schedule the next color change after 500 milliseconds
    root.after(500, flash_text)


# create the main window
root = tk.Tk()

# create a label with the text and set the font size
label = tk.Label(root, text="Thank you for watching! Don't forget to give our team a FULL MARK!",
                 font=("Helvetica", 32))

# fit the label to the screen
label.pack(fill=tk.BOTH, expand=True)

# start flashing the text
flash_text()

# run the window mainloop
root.mainloop()
