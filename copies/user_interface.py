# File for tkinter User Interface
import tkinter as tk
from tkinter import ttk

def retrieve1():
    states = [state_listbox.get(idx) for idx in state_listbox.curselection()]
    outcomes = [outcomes_listbox.get(idx) for idx in outcomes_listbox.curselection()]
    print("states" + str(states))
    print("outcomes" + str(outcomes))

def retrieve2():
    outcome = outcomes_combobox.get()
    policies = [policies_listbox.get(idx) for idx in policies_listbox.curselection()]
    print("outcome: " + str(outcome))
    print("policies" + str(policies))

### Creating main window named root ###

root = tk.Tk()
root["bg"] = "white"
#getting screen width and height of display 
screen_width = root.winfo_screenwidth()  #in pixels
screen_height= root.winfo_screenheight() #in pixels
#setting tkinter window size 
root.geometry("%dx%d" % (screen_width, screen_height))
root.title("CS122 TJJE Project: Examining State Policies and Educational Outcomes")
# yscroll = tk.Scrollbar(command=root.yview, orient=tk.VERTICAL)
# yscroll.grid(row=0, column=1, sticky='ns')
# root.configure(yscrollcommand=yscroll.set)

### Setting master frame 
##################################################################################

class VerticalScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so 
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)
# Taken from https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8

master_frame = VerticalScrolledFrame(
    root, 
    bg="white",
    cursor="arrow",
    height= screen_height,
    width=screen_width
    )
master_frame.pack()

##################################################################################

### Creating 3 frames for master_frame: intro, user input option 1, user input option 2 ###

welcome_frame = tk.Frame(master_frame, bg = "blue")
#welcome_frame.pack(side="top", fill="both", expand=True)
welcome_frame.grid(column = 0, row = 0)
#welcome_frame.grid_columnconfigure(0, weight=1)
default_opt_frame = tk.Frame(master_frame, bg = "green")
default_opt_frame.grid(column = 0, row = 1)
#default_opt_frame.grid_columnconfigure(0, weight=1)
special_opt_frame = tk.Frame(master_frame, bg = "pink")
special_opt_frame.grid(column = 0, row = 2)

### Enter text data for top frame ###

welcome_text_box = tk.Text(welcome_frame, height = 12, bg = "white", bd = 0, relief = tk.FLAT, wrap = tk.WORD)
welcome_text_box.grid(column = 0, row = 0)
intro = "Hello and welcome to our program! This tool will allow you to evaluate the effectivness and correlations of American educational policies on its outcomes, on a per state, per outcome, or per policy basis"
sources = "We ulilize data from the National Council on Teacher Quality (NCTQ) and the National Center for Education Statistics (NCES)"
note = "*For a small number of missing datapoints, we filled them in with the US national average"
#welcome_text_box.tag_configure("center", justify='center'
welcome_text_box.insert(tk.END, intro + "\n"*2 + sources + "\n"*2 + note)
#welcome_text_box.tag_add("center", "1.0", "end")
welcome_text_box.configure(state='disabled')

### Enter widgets for default user input frame ###
option1_label = ttk.Label(default_opt_frame, text = "Retrieve information on how effective a state's relevant policies are for all or particulr educational outcomes: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)

# State Selection Label
state_label = ttk.Label(default_opt_frame, text = "Select one state, or select multiple to compare").grid(column = 0,  
        row = 1, padx = 35, pady = 25) 

# State Selection listbox widget
state_listbox = tk.Listbox(default_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
state_listbox.grid(column = 0, row = 2)

state_scrollbar = tk.Scrollbar(state_listbox, orient="vertical")
state_scrollbar.config(command=state_listbox.yview)
#scrollbar.pack(side="right", fill="y")

state_listbox.config(yscrollcommand=state_scrollbar.set)

states = ["US", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

for each_item in range(len(states)): 
      
    state_listbox.insert(tk.END, states[each_item]) 
    state_listbox.itemconfig(each_item, bg = "light blue") 


### outcomes selection listbox widget ###
# outcomes Selection Label
outcomes_label = ttk.Label(default_opt_frame, text = "Select the outcomes you want to investigate:").grid(column = 1,  
        row = 1, padx = 35, pady = 25) 

# outcomes Selection listbox widget
outcomes_listbox = tk.Listbox(default_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
outcomes_listbox.grid(column = 1, row = 2)

outcomes_scrollbar = tk.Scrollbar(outcomes_listbox, orient="vertical")
outcomes_scrollbar.config(command=outcomes_listbox.yview)
#scrollbar.pack(side="right", fill="y")

outcomes_listbox.config(yscrollcommand=outcomes_scrollbar.set)

outcomes = ["Select all trend outcomes", "trend outcome1", "trend outcome2", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

for each_item in range(len(outcomes)): 
      
    outcomes_listbox.insert(tk.END, outcomes[each_item]) 
    outcomes_listbox.itemconfig(each_item, bg = "light blue")

button = tk.Button(default_opt_frame, text="Calculate!", bd = "5", command=retrieve1)
button.grid(column = 3, row = 2)

### Enter widgets for special user input frame ###
option2_label = ttk.Label(special_opt_frame, text = "Retrieve information on how particular policies interact with a given outcome: ").grid(column = 0,  
        row = 0, padx = 35, pady = 25)

ttk.Label(special_opt_frame, text = "Select one outcome to investigate:").grid(column = 0,  
        row = 1, padx = 35, pady = 25) 

outcome_combo = tk.StringVar() 
outcomes_combobox = ttk.Combobox(special_opt_frame, width = 27,  
                            textvariable = outcome_combo, exportselection=0)

outcomes_combobox['values'] = ("AL", "AL", "AR" "fill rest in") 
outcomes_combobox.grid(column = 0, row = 2) 

# policies selection label
policies_label = ttk.Label(special_opt_frame, text = "Select which policies to consider:").grid(column = 1,  
        row = 1, padx = 35, pady = 25) 

# policies Selection listbox widget
policies_listbox = tk.Listbox(special_opt_frame, selectmode = "multiple", exportselection = False, width=20, height=10)
policies_listbox.grid(column = 1, row = 2)

outcomes_scrollbar = tk.Scrollbar(policies_listbox, orient="vertical")
outcomes_scrollbar.config(command=policies_listbox.yview)
#scrollbar.pack(side="right", fill="y")

policies_listbox.config(yscrollcommand=outcomes_scrollbar.set)

policies = ["Select all policies", "policy1", "policy2", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

for each_item in range(len(policies)): 
      
    policies_listbox.insert(tk.END, policies[each_item]) 
    policies_listbox.itemconfig(each_item, bg = "light blue")

button2 = tk.Button(special_opt_frame, text="Calculate!", bd = "5", command=retrieve2)
button2.grid(column = 2, row = 2)

root.mainloop()
