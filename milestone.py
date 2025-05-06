import tkinter as tk
import datetime

#path to icon image
icon_path = "cgev.ico"

#create the main window
root = tk.Tk()
root.title("Milestone Monitor")
root.configure(bg="#d8f3dc")
root.geometry("1900x300")
root.iconbitmap(icon_path)

#get today's date
today = datetime.date.today()
#get the original day of the year
date_of_year = today.timetuple().tm_yday
print(today)
print(date_of_year)


#progress stages colors
progress_stages=["#b7efc5","#6ede8a","#25a244","#1a7431","#04471c"]
#list to buttons
buttons=[]

#month names
months =["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

#fuction to create row of buttons for a week
def create_row(week):
    #display months label
    for i in range(0,12):
        month = tk.Label(root , text = months[i] , font = ("Helvetica",10) , background="#d8f3dc")
        month.grid(row=0, column=(1+i)*4 , padx=2 , pady=2)

    #create buttons for each day of a week
    for i in range(1,8):
        color_button = tk.Button( root, background="#ffffff", width= 1 , height = 0)
        color_button.bind("<Button-1>",change_button_color)
        color_button.grid( row=i , column=week , padx=2 , pady=2)
        buttons.append(color_button)

#function to chnage the color of a button
def change_button_color(event):

    #get a button widget and current color background  
    button = event.widget
    bg_color = button.cget("background")

    #iterate through progress stages
    for index , item in enumerate (progress_stages):
        #cahnge color if current color matches and index is within range
        if bg_color == item and index < 4:
            button.configure(bg = progress_stages[index+1])
            break

        #set the color to first color if not found in progress stages    
        if bg_color not in progress_stages:
            button.configure(bg = progress_stages[0])

def save_buttons():
    with open("buttons_data.txt","w") as file :
        for button in buttons :
            bg_color = button.cget("background")
            file.write(bg_color + "\n")
        root.destroy()

        
#functions to load button colors from file
def load_buttons():
    colors =[]
    try:
        with open("buttons_data.txt","r") as file :
            for line in file:
                bg_color = line.strip()
                colors.append(bg_color)
            return colors

    except FileNotFoundError:
        pass #do nothing if file does not found
    return colors

#variable to trak edit mode
edit = False

def button_edit_on_off() :
    global edit
    button_index = 0
    if not edit:
        #enable edit button
        for b in buttons:
            if button_index == date_of_year :
                button_index += 1
                bg_color = b.cget("background")
                if bg_color in progress_stages :
                    pass
                else :
                    b.configure(bg="#252422")
            else :
                b.configure(state="disabled")
                b.unbind("<Button-1>")
                button_index += 1
        edit = True # update edit mode
     # to disable edit mode
    else :
        for b in buttons   :
            b.configure(state="normal")
            b.bind("<Button-1>",change_button_color)
        edit = False    


#create rows of buttons
for i in range(1,52):
    create_row(i)

#load existing button colors from the file
existing_colors = load_buttons()
#apply existing colors to buttons
for button, colors in zip(buttons, existing_colors):
    button.configure(bg=colors)

#toggle edit mode
button_edit_on_off()

#display labels of progress colors
label_less =tk.Label(root , text="less" ,font=("Helvetica",12),bg="#d8f3dc")
label_less.grid(row=10, column=0 ,padx=2 ,pady=2)

for index,stage_color in enumerate(progress_stages):
    example_color = tk.Button(root, state="disabled" ,background=stage_color, width=1, height=0)
    example_color.grid(row=10, column=index+1 , padx=2, pady=2)     

#button to exit and save
exit = tk.Button(root, command=save_buttons , text="Save and Exit", background="#f07167" )
exit.grid(row=9, column=54 , padx=6, pady=2)     

#button to toggle edit mode
edit_button = tk.Button(root, command = button_edit_on_off , text="Edit", background="#f07167" )
edit_button.grid(row=9, column=53 , padx=6, pady=2)     


#run the application
root.mainloop()