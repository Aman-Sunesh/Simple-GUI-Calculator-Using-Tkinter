from tkinter import *
import string 

# Create a GUI window
gui = Tk()

# Setting the title of the window
gui.title("Simple GUI Calculator")

# Setting the size of the window (increased height)
gui.geometry("420x720")

# Setting the background color of the window
gui.configure(background="black")

# Display Entry
display = Entry(
    gui,
    font=('Arial', 70),
    bg='black',
    fg='white',
    borderwidth=2,
    relief="solid",
    justify=RIGHT
)

display.grid(row=1, column=0, columnspan=5, sticky='nsew', pady=(0, 0))
display.insert(0, "0")  # Initialize display with '0'

# Function to handle button clicks
def button_click(item):
    current = display.get()

    if item == "AC":
        display.delete(0, END)
        display.insert(END, "0")

    elif item == "%":
        try:
            result = str(float(current) / 100)
            display.delete(0, END)
            display.insert(END, result)
        except:
            display.delete(0, END)
            display.insert(END, "Error")

    elif item == "+/-":
        try:
            # Determine if the current value is an integer or a float
            if '.' in current:
                # It's a float, convert to float and negate
                result = str(-1 * float(current))
            else:
                # It's an integer, convert to int and negate
                result = str(-1 * int(current))

            display.delete(0, END)
            display.insert(END, result)
        except:
            display.delete(0, END)
            display.insert(END, "Error")

    elif item == "=":
        try:
            result = str(eval(current.replace("x", "*")))
            display.delete(0, END)
            display.insert(END, result)

        except:
            display.delete(0, END)
            display.insert(END, "Error")

    else:
        if current == "0" and item not in ["+", "-", "x", "/"]:
            display.delete(0, END)
        # Insert "x" as is for display purposes
        display.insert(END, item)


# Function to create circular buttons on a canvas
def create_circle_button(canvas, x, y, radius, text, command):
    if text in ["/", "x", "-", "+", "="]:
        fill_color = 'orange'
    elif text.isdigit() or text == '.':
        fill_color = 'gray16'
    else:
        fill_color = 'gray64'

    circle_id = canvas.create_oval(
        x - radius, y - radius, x + radius, y + radius,
        fill=fill_color, outline='white', width=2
    )
    text_id = canvas.create_text(
        x, y, text=text, font=('Arial', 24, 'bold'), fill='white'
    )

    def on_click(event):
        command()

    # Bind the click event to both the circle and the text
    canvas.tag_bind(circle_id, '<Button-1>', on_click)
    canvas.tag_bind(text_id, '<Button-1>', on_click)


def create_rounded_rect_button(canvas, x, y, width, height, radius, text, command):
    fill_color = 'gray16'
    
    radius = min(radius, width/2, height/2)
    
    # Define points for the capsule shape
    points = [
        x - width/2 + radius, y - height/2,             
        x + width/2 - radius, y - height/2,            
        x + width/2, y - height/2,                      
        x + width/2, y + height/2 - radius,             
        x + width/2, y + height/2,                      
        x + width/2 - radius, y + height/2,             
        x - width/2 + radius, y + height/2,             
        x - width/2, y + height/2,                      
        x - width/2, y - height/2 + radius,             
        x - width/2, y - height/2,                      
        x - width/2 + radius, y - height/2               
    ]
    
    # Create the capsule shape using create_polygon with smooth curves
    rect_id = canvas.create_polygon(
        points,
        fill=fill_color,
        outline='white',
        width=2,
        smooth=True
    )
    
    # Add left-aligned text to the button
    padding = 10 
    text_id = canvas.create_text(
        x - width/2 + radius + padding, 
        y,
        text=text,
        font=('Arial', 24, 'bold'),
        fill='white',
        anchor='w'  
    )
    
    def on_click(event):
        command()
    
    # Bind the click event to both the rectangle and the text
    canvas.tag_bind(rect_id, '<Button-1>', on_click)
    canvas.tag_bind(text_id, '<Button-1>', on_click)


# Create a Canvas for buttons
canvas = Canvas(gui, bg='black', highlightthickness=0)
canvas.grid(row=2, column=0, rowspan=6, columnspan=5, sticky='nsew', pady=20)

# Positioning and creating buttons using the create_circle_button function
button_positions = [
    ("/", 360, 50),
    ("x", 360, 150),
    ("-", 360, 250),
    ("+", 360, 350),
    ("=", 360, 450),
    ("1", 60, 350),
    ("2", 160, 350),
    ("3", 260, 350),
    ("4", 60, 250),
    ("5", 160, 250),
    ("6", 260, 250),
    ("7", 60, 150),
    ("8", 160, 150),
    ("9", 260, 150),
    (".", 260, 450),
    ("AC", 60, 50),
    ("+/-", 160, 50),
    ("%", 260, 50)
]

for text, x, y in button_positions:
    if text != "0":
        create_circle_button(
            canvas,
            x=x,
            y=y,
            radius=40,
            text=text,
            command=lambda item=text: button_click(item)
        )

    # Create the '0' button as a rounded rectangle
    create_rounded_rect_button(
        canvas,
        x=110,  
        y=450,  
        width=180,  
        height=80,  
        radius=3000,  
        text="0",
        command=lambda item="0": button_click(item)
    )


# Configure the grid to expand the space
gui.rowconfigure(0, weight=1)
gui.rowconfigure(1, weight=1)

for row_index in range(2, 8):
    gui.rowconfigure(row_index, weight=1)
for col_index in range(5):
    gui.columnconfigure(col_index, weight=1)

gui.mainloop()
