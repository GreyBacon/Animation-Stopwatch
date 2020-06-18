import time
from tkinter import *


#Global variables
flag_running = False #Flags if the stopwatch is running
time_start = 0 #Keeps track of perf_counter() at the start
time_total = 0 #Tracks
frames = 0 #Total frames
fps = 0 #Takes the user inputted frames per second
flag_pause = False

#Runs the timer 
def step_counter():
    global flag_pause, flag_running, time_start, time_total, fps, frames
    
    #Runs checkpointing if the timer is already running
    if not flag_running: 
        time_start = time.perf_counter()
    
    #Tracks and outputs timer
    time_total = time.perf_counter() - time_start
    frames = time_total * fps
    lbl_counter['text'] = "%.2f"%(time_total)
    lbl_framecount['text'] = "%.2f"%(frames)
    
    root.after(10, step_counter)
    
#Resets the counter
def reset():
    global flag_running, time_start, time_total
    flag_pause = True
    flag_running = False
    time_start = 0
    time_total = 0
    output.config(state=NORMAL)
    output.delete(1.0,END)
    output.config(state=DISABLED)
    

   
"""
Runs when start button is pressed
Starts the counter if not already running and
outputs the current time to the output field if it is
Validates fps input before passing it to the counter as well

"""  
def start_timer(event=None):
    global flag_running, flag_pause, fps
    #Validate fps field
    try:
        fps = int(input_fps.get())
        if 1 <= fps <= 120:
            print("fps: " + str(fps))
            #Adds checkpoints to the output if the timer is running
            if flag_running:
                output.config(state=NORMAL)
                output.insert(END, "%.2f"%(time_total) + " seconds, %.2f"%(frames) + " frames\n")
                output.config(state=DISABLED)
            flag_pause = False
            step_counter()
            flag_running = True
            btn_start.config(text="Mark")
        else: print("Must be between 1-120 (" + input_fps.get() + ")")        
    except:
        print("Error, input is \"" + input_fps.get() + "\"")
    
#Create window
root = Tk()
root.title("Stopwatch")
root.geometry("250x500")
root.minsize(width=250, height = 400)

#Running timer
lbl_counter = Label(root, text="0.00", font=('Helvetica', 35 ,'bold'))
lbl_counter.pack()


#Frame counter
lbl_framecount = Label(root, text="0 frames")
lbl_framecount.pack()

#Frame input
frame_fps = Frame(root)
frame_fps.pack()
lbl_input_label = Label(frame_fps, text="Frames per second:")
lbl_input_label.pack()
input_fps = Entry(frame_fps, text="24")
input_fps.pack()


#Control buttons
frame_buttons = Frame(root)
frame_buttons.pack(padx=5, pady=5)
btn_start = Button(frame_buttons, text="Start", command = start_timer, width = 10, height = 2)
btn_start.pack(side=LEFT, pady=10, padx=10)
btn_reset = Button(frame_buttons, text="Reset", command = reset, height = 2,relief=RIDGE)
btn_reset.pack(side=LEFT)

#Output for checkpoints
frame_output = Frame(root)
frame_output.pack()
output = Text(frame_output, state=DISABLED)
output.pack()

#Register spacekey presses
root.bind("<space>",start_timer)

root.mainloop()