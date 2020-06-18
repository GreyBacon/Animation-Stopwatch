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
    btn_start.config(text="Start")

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
root.minsize(width=270, height = 400)

#Running timer
lbl_counter = Label(root, text="0.00", font=('Helvetica', 35 ,'bold'))
lbl_counter.pack()


#Frame counter
frame_framecount = Frame(root)
frame_framecount.pack()
lbl_framecount = Label(frame_framecount, text="0")
lbl_framecount.pack(side=LEFT)
lbl_framecount_label = Label(frame_framecount, text="frames")
lbl_framecount_label.pack(side=LEFT)

#Frame input
frame_fps = Frame(root)
frame_fps.pack()
lbl_input_label = Label(frame_fps, text="Frames per second:")
lbl_input_label.pack(side=LEFT)
input_fps = Entry(frame_fps, text="", width=4)
input_fps.pack(side=LEFT)

#Wanted to have a notification about the spacebar shortcut but it was too intrusive
#lbl_spacebar_message = Label(root, text="Spacebar works for marking too!", font=('Helvetica', 8))
#lbl_spacebar_message.pack()

#Control buttons
frame_buttons = Frame(root)
frame_buttons.pack(padx=5, pady=5)
btn_start = Button(frame_buttons, text="Start", command = start_timer, width = 10, height = 2)
btn_start.pack(side=LEFT, padx=10)
btn_reset = Button(frame_buttons, text="Reset", command = reset, height = 2)
btn_reset.pack(side=LEFT)

#Output for checkpoints
frame_output = Frame(root)
frame_output.pack(padx=5, pady=5)
scrollbar = Scrollbar(frame_output, orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)
output = Text(frame_output, state=DISABLED, width= 35, yscrollcommand=scrollbar.set)
output.pack(fill=X)
scrollbar.config(command=output.yview)

#Register spacekey presses
root.bind("<space>",start_timer)

root.mainloop()