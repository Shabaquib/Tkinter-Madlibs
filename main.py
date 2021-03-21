import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import os
from tkinter.messagebox import askyesno, showinfo
from functools import partial
import linecache

path = os.scandir(r".\Game_levels\\")
profile_images_ids = os.listdir(r".\Resources\Profile_images\\")
image_logo = Image.open(r".\Resources\Python-logo.png") #image on the levels label

class GameWindow(tk.Toplevel):
    def __init__(self, parent, param):
        """ Initializing the object window with param as the profile file name -User.txt-
        """
        super().__init__(parent)
        self.profile_selected = param[:-4] #profile name by stripping .txt from the file name passed
        self.txt_selected = param
        self.title("Madlibs")
        self.geometry('720x480+200+150')
        global image_logo
        self.iconbitmap(r'.\\Resources\\Python-logo.ico')
        self.resizable(tk.FALSE, tk.FALSE)
        self.main_menu = tk.Menu(self)
        self.python_logo = ImageTk.PhotoImage(image_logo)
        self.file_list = [] #saves the address of the text files that contain level contents

        save_button_logo = Image.open(r".\Resources\save-button.png")
        save_button_logo = save_button_logo.resize((20, 20))
        achieve_badge = Image.open(r".\Resources\completed.png")
        achieve_badge = achieve_badge.resize((100, 100))

        # appending the file adresses in the list for dynamic assignment
        for entry in path:
            self.buff = r".\Game_levels\\" + str(entry.name)
            self.file_list.append(self.buff)
        self.column_count = int(len(self.file_list) / 2)
        self.counter = 0

        # stores the frames in which the level button and label reside
        self.level_list = [None] * int(len(self.file_list))
        # self.withdraw()

        # determining the progress of the individual by acessing the number of lines populated
        self.profile_progress = len(open(r".\profiles\\"
                                         + str(param), "r").readlines())-2
        #getting image serial numberby accessing line 2 and stripping\n by rstrip in the profile text file
        self.image_id = int(str(linecache.getline(r".\profiles\\" + str(self.txt_selected), 2).rstrip()))
        self.image_buffer = Image.open(r".\Resources\Profile_images\\" + str(profile_images_ids[self.image_id]))
        self.image_buffer = self.image_buffer.resize((140, 140))
        self.image_on_profile = ImageTk.PhotoImage(self.image_buffer)

        #calling account pane to show itself default
        self.account_pane()


    def account_pane(self):
        """
        Window to show progress, profile picture, username
        """
        # the main container
        self.account_main_frame = tk.Frame(self, width=720, height=480)
        self.account_main_frame.grid(column=0, row=0, sticky='nsew')

        # Upper frame (username, and Profile picture container)
        self.upper_frame = tk.Frame(self.account_main_frame, width=720, height=192)
        self.upper_frame.grid(column=0, row=0, sticky='new')
        self.profile_pic = tk.Frame(self.upper_frame, width=180, height=192)
        self.profile_pic.grid(column=0, row=0, sticky=tk.W)
        self.user_detail = tk.Frame(self.upper_frame, width=540, height=192)
        self.user_detail.grid(column=1, row=0, sticky=tk.E)
        self.username_frame = tk.Frame(self.user_detail, width=540, height=96)
        self.username_frame.grid(column=0, row=0, sticky='sw')
        self.edit_label_frame = tk.Frame(self.user_detail, width=540, height=96)
        self.edit_label_frame.grid(column=0, row=1, sticky=tk.SW)

        # Upper frame widgets
        self.profile_image = tk.Label(self.profile_pic, image=self.image_on_profile)
        self.profile_image.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.name_label = ttk.Label(self.username_frame, text=self.profile_selected, font=("Arial", 25))
        self.name_label.place(relx=0.03, rely=1.0, anchor='sw')

        # lower frame (scoreboard)
        self.lower_frame = tk.Frame(self.account_main_frame, background="BLACK", width=720, height=288)
        self.lower_frame.grid(column=0, row=1, sticky=tk.S)
        self.lower_scrolling_frame = tk.Frame(self.lower_frame, width=700, height=288)#nesting frame to allow scrolling
        self.lower_scrolling_frame.grid(column=0, row=0, sticky=tk.S)

        # Canvas for the scrolling
        self.level_canvas = tk.Canvas(self.lower_scrolling_frame, width=700)
        self.level_bar = tk.Scrollbar(self.lower_scrolling_frame, orient='vertical', command=self.level_canvas.yview)
        self.level_frame = tk.Frame(self.level_canvas)
        self.level_canvas.pack(side="left", fill="x", expand=True)
        self.level_canvas.create_window((0, 0), window=self.level_frame, anchor="nw")
        self.level_canvas.configure(yscrollcommand=self.level_bar.set)
        self.level_bar.pack(side="right", fill="y")
        self.level_frame.bind(
            "<Configure>",
            lambda e: self.level_canvas.configure(
                scrollregion=self.level_canvas.bbox("all")
            )
        )

        self.progress_frame = [None]*6 # 6 frames for displaying the progress of all 6 levels indvidually

        for x in range(1, int((self.profile_progress/2)+1)):
            self.progress_frame[x] = tk.Frame(self.level_frame, width=700, height=130)
            self.progress_frame[x].grid(column=0, row=x, sticky="nw", padx=5, pady=5)
            self.left_part = tk.Frame(self.progress_frame[x], width=300, height=130)
            self.left_part.grid(column=0, row=0, sticky="nw", padx=5, pady=5)
            self.right_part = tk.Frame(self.progress_frame[x], width=400, height=130)
            self.right_part.grid(column=1, row=0, sticky="ne", padx=5, pady=5)
            self.level_text = tk.Label(self.left_part, text=f"Level {x}", anchor="center", font=("Arial", 16))
            self.level_text.grid(column=0, row=0, sticky="sw", ipadx=5, ipady=5)
            # acess one specific line to get the words entered by the user in one list
            self.l_inline = linecache.getline(r".\profiles\\" + str(self.txt_selected), (x*2)+2)
            #a revisit button to view the previous level's content
            self.revisit_button = tk.Button(self.right_part, text="Visit", command=partial(self.revisit_level, x))
            self.revisit_button.grid(column=0, row=0, sticky="e", padx=(0, 5), pady=5)
            self.level_content = tk.Label(self.right_part, text=self.l_inline, anchor="center", font=("Arial", 10))
            self.level_content.grid(column=1, row=0, ipadx=5, ipady=5)


    def revisit_level(self, arg):
        """
        Window to show the level previously played with the answers inserted in the disabled entries.
        :param arg: passes the index of the level file in the directory
        :return:
        """
        self.level_at = arg
        self.badge_logo = ImageTk.PhotoImage(achieve_badge)
        self.revisit_frame = tk.Frame(self, width=720, height=480)
        self.revisit_frame.grid(column=0, row=0, sticky='nsew')
        self.revisit_frame.grid_propagate(False)

        self.revisit_nest_frame = tk.Frame(self.revisit_frame, width=480, height=470)
        self.revisit_nest_frame.grid(column=0, row=0, sticky='nsew')
        self.revisit_nest_frame.grid_propagate(False)

        self.success_frame = tk.Frame(self.revisit_frame, width=240, height=480)
        self.success_frame.grid(column=1, row=0, sticky='ne')
        self.success_frame.grid_propagate(False)

        self.revisit_canvas = tk.Canvas(self.revisit_nest_frame, width=480, height=450)
        self.revisit_bar = tk.Scrollbar(self.revisit_nest_frame, orient='vertical', command=self.revisit_canvas.yview)
        self.revisit_inner_frame = tk.Frame(self.revisit_canvas)
        self.revisit_canvas.pack(side="left", fill="y", expand=True)
        self.revisit_canvas.create_window((0, 0), window=self.revisit_inner_frame, anchor="nw")
        self.revisit_canvas.configure(yscrollcommand=self.revisit_bar.set)
        self.revisit_bar.pack(side="right", fill="y", expand=True)
        self.revisit_inner_frame.bind(
            "<Configure>",
            lambda e: self.revisit_canvas.configure(
                scrollregion=self.revisit_canvas.bbox("all")
            )
        )

        self.input_cache = linecache.getline(r".\profiles\\"
                                             + str(self.txt_selected), (self.level_at*2)+2)

        #  separates the words in a list by using the separator ,
        self.saved_list = self.input_cache.split(',')

        if self.level_at == 1 or self.level_at == 5 or self.level_at == 6:
            self.Entry_filled_list = [None] * 22
        elif self.level_at == 2 or self.level_at == 3:
            self.Entry_filled_list = [None] * 10
        elif self.level_at == 4:
            self.Entry_filled_list = [None] * 13

        self.file_read = open(self.file_list[self.level_at-1], "r")
        self.line_list = self.file_read.readlines()
        entry_count = 0
        frame_counter = 0
        self.frame_list = [None] * len(self.line_list)
        # creating the content and entry points
        for line_entry in self.line_list:
            self.step = 0
            start_point = 0
            column_point = 0
            self.frame_list[frame_counter] = tk.Frame(self.revisit_inner_frame, width=670, height=15)
            self.frame_list[frame_counter].grid(column=0, row=frame_counter, sticky=tk.W)
            if line_entry.find("_") == -1:
                self.Label_frame = tk.Label(self.frame_list[frame_counter], text=str(line_entry))
                self.Label_frame.grid(column=0, row=0, sticky=tk.W)
            else:
                while line_entry.find("_", start_point) != -1:
                    # content = tk.StringVar()
                    if self.step >= 1:
                        self.dash_index = line_entry.find("_", start_point)
                        self.Label_frame = tk.Label(self.frame_list[frame_counter],
                                                    text=str(line_entry[start_point:self.dash_index]))
                        # print("Label frame:", self.Label_frame, str(line_entry[start_point:self.dash_index]))
                        self.Label_frame.grid(column=column_point, row=0, sticky=tk.W)
                        start_point = self.dash_index + 1
                        column_point += 1
                        self.Entry_filled_list[entry_count] = tk.Entry(self.frame_list[frame_counter],
                                                                       width=16)
                        self.Entry_filled_list[entry_count].grid(column=column_point, row=0, sticky=tk.W)
                        self.Entry_filled_list[entry_count].insert(0, self.saved_list[entry_count])
                        self.Entry_filled_list[entry_count].configure(state=tk.DISABLED)
                        entry_count += 1
                        self.step += 1
                        column_point += 1

                    elif self.step == 0:
                        self.dash_index = line_entry.find("_")
                        self.Label_frame = tk.Label(self.frame_list[frame_counter],
                                                    text=str(line_entry[start_point:self.dash_index]))
                        self.Label_frame.grid(column=0, row=0, sticky=tk.W)
                        column_point += 2
                        start_point = self.dash_index + 1
                        self.Entry_filled_list[entry_count] = tk.Entry(self.frame_list[frame_counter], width=16)
                        # textvariable=content)
                        self.Entry_filled_list[entry_count].grid(column=1, row=0, sticky=tk.W)
                        self.Entry_filled_list[entry_count].insert(0, self.saved_list[entry_count])
                        self.Entry_filled_list[entry_count].configure(state=tk.DISABLED)
                        entry_count += 1
                        self.step += 1

                    if line_entry.find("_", start_point) == -1:
                        self.Label_frame = tk.Label(self.frame_list[frame_counter],
                                                    text=str(line_entry[start_point:len(str(line_entry))]))
                        self.Label_frame.grid(column=column_point, row=0, sticky=tk.W)

            frame_counter += 1
            self.dash_index = 0
            self.revisit_inner_frame.update()
        frame_counter = 0

        self.completion_label = tk.Label(self.success_frame, text="Level Completed!", font=("Calibri", 20))
        self.completion_label.place(relx=0.5, rely=0.3, anchor='center')

        self.completion_badge = tk.Label(self.success_frame, image=self.badge_logo)
        self.completion_badge.place(relx=0.5, rely=0.5, anchor='center')


    def play_madlibs_pane(self, arg):
        """
        Creates a window in which the game is loaded, with empty entry points
        :param arg: numeral to specify level selected
        :return:
        """
        self.level_selected = arg
        self.play_ground_frame = tk.Frame(self, width=720, height=480)
        self.play_ground_frame.grid(column=0, row=0, sticky='nsew')
        self.play_ground_frame.grid_propagate(False)

        self.save_button_png = ImageTk.PhotoImage(save_button_logo)
        # all frames distinguished for elements
        # left frame created
        self.left_frame = tk.Frame(self.play_ground_frame, width=534, height=480)
        self.left_frame.grid(column=0, row=0, sticky=tk.W)
        self.left_frame.grid_propagate(False)
        # left frame nested
        self.left_upper_frame = tk.Frame(self.left_frame, width=534, height=480)
        self.left_upper_frame.grid(column=0, row=0, sticky=tk.N)
        self.left_upper_frame.grid_propagate(False)

        # right frame created
        self.right_frame = tk.Frame(self.play_ground_frame, width=186, height=480)
        self.right_frame.grid(column=1, row=0, sticky=tk.E)
        self.right_frame.grid_propagate(False)
        # right frame nested
        self.right_upper_frame = tk.Frame(self.right_frame, width=186, height=384)
        self.right_upper_frame.grid(column=0, row=0, sticky=tk.N)
        self.right_upper_frame.grid_propagate(False)
        self.right_lower_frame = tk.Frame(self.right_frame, width=186, height=96)
        self.right_lower_frame.grid(column=0, row=1, sticky=tk.S)
        self.right_lower_frame.grid_propagate(False)

        # scrollable madlibs
        self.text_canvas = tk.Canvas(self.left_upper_frame, width=480, height=450)
        self.mad_bar = tk.Scrollbar(self.left_upper_frame, orient='vertical', command=self.text_canvas.yview)
        self.mad_frame = tk.Frame(self.text_canvas)
        self.text_canvas.pack(side="left", fill="x", expand=True)
        self.text_canvas.create_window((0, 0), window=self.mad_frame, anchor="nw")
        self.text_canvas.configure(yscrollcommand=self.mad_bar.set)
        self.mad_bar.pack(side="right", fill="y")
        self.mad_frame.bind(
            "<Configure>",
            lambda e: self.text_canvas.configure(
                scrollregion=self.text_canvas.bbox("all")
            )
        )

        if self.level_selected == 1 or self.level_selected == 5 or self.level_selected == 6:
            self.Entry_list = [None] * 22
        elif self.level_selected == 2 or self.level_selected == 3:
            self.Entry_list = [None] * 10
        elif self.level_selected == 4:
            self.Entry_list = [None] * 13

        self.file_read = open(self.file_list[self.level_selected-1], "r")
        self.line_list = self.file_read.readlines()
        entry_count = 0
        frame_counter = 0
        self.frame_list = [None] * len(self.line_list)
        for line_entry in self.line_list:
            self.step = 0
            start_point = 0
            column_point = 0
            self.frame_list[frame_counter] = tk.Frame(self.mad_frame, width=495, height=15)
            self.frame_list[frame_counter].grid(column=0, row=frame_counter, sticky=tk.W)
            if line_entry.find("_") == -1:
                self.Label_frame = tk.Label(self.frame_list[frame_counter], text=str(line_entry))
                self.Label_frame.grid(column=0, row=0, sticky=tk.W)
            else:
                while line_entry.find("_", start_point) != -1:
                    content = tk.StringVar()
                    if self.step >= 1:
                        self.dash_index = line_entry.find("_", start_point)
                        self.Label_frame = tk.Label(self.frame_list[frame_counter],
                                                    text=str(line_entry[start_point:self.dash_index]))
                        # print("Label frame:", self.Label_frame, str(line_entry[start_point:self.dash_index]))
                        self.Label_frame.grid(column=column_point, row=0, sticky=tk.W)
                        start_point = self.dash_index + 1
                        column_point += 1
                        self.Entry_list[entry_count] = tk.Entry(self.frame_list[frame_counter], textvariable=content,
                                                                width=16)
                        # print("Entry:", self.Entry_list)
                        self.Entry_list[entry_count].grid(column=column_point, row=0, sticky=tk.W)
                        entry_count += 1
                        self.step += 1
                        column_point += 1

                    elif self.step == 0:
                        self.dash_index = line_entry.find("_")
                        self.Label_frame = tk.Label(self.frame_list[frame_counter],
                                                    text=str(line_entry[start_point:self.dash_index]))
                        self.Label_frame.grid(column=0, row=0, sticky=tk.W)
                        column_point += 2
                        start_point = self.dash_index + 1
                        self.Entry_list[entry_count] = tk.Entry(self.frame_list[frame_counter], width=16,
                                                                textvariable=content)
                        self.Entry_list[entry_count].grid(column=1, row=0, sticky=tk.W)
                        entry_count += 1
                        self.step += 1

                    if line_entry.find("_", start_point) == -1:
                        self.Label_frame = tk.Label(self.frame_list[frame_counter],
                                                    text=str(line_entry[start_point:len(str(line_entry))]))
                        self.Label_frame.grid(column=column_point, row=0, sticky=tk.W)

            frame_counter += 1
            self.dash_index = 0
            self.mad_frame.update()

        # showing the profile image of the user
        self.entry_label = ttk.Label(self.right_upper_frame, image=self.image_on_profile)
        self.entry_label.grid(column=0, row=0, pady=(60, 2), padx=(15, 15))
        self.entry_var = tk.StringVar()

        # save button to save the progress in a file
        self.save_button = ttk.Button(self.right_lower_frame, text="Save Progress", image=self.save_button_png,
                                      width=15, compound=tk.LEFT,
                                      command=partial(self.save_progress, self.level_selected, self.profile_selected))
        self.save_button.grid(column=1, row=0, sticky='e', padx=48, pady=31, ipadx=3, ipady=3)


    def close_window(self):
        """
        Closes the game
        :return:
        """
        self.confirmation = askyesno(title="Confirm Exit!", message="Are you sure to exit?")
        if self.confirmation:
            self.withdraw()


    def play_pane(self):
        """
        Lists all the level available in a scrollable window to support dynamic
        loading in future if new levels are appended
        :return:
        """
        # main frame
        self.list_mainframe = tk.Frame(self, width=720, height=480)
        self.list_mainframe.grid(column=0, row=0, sticky='nsew')

        # upper frame (Level list label)
        self.upper_frame = tk.Frame(self.list_mainframe, width=720, height=60, background="BLACK")
        self.upper_frame.grid(column=0, row=0, sticky='nw')

        # lower frame (list contents)
        self.lower_frame = tk.Frame(self.list_mainframe, height=400)
        self.lower_frame.grid(column=0, row=1, sticky='swe')
        self.canvas = tk.Canvas(self.lower_frame, height=380)
        self.canvas.pack(side="bottom", fill="both", expand=True)

        # horizontal scrollbar on top
        self.scrollbar = tk.Scrollbar(self.lower_frame, orient='horizontal', command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="bottom", fill="x")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.tokeniser = 1
        for entry in self.file_list:
            if self.tokeniser-1 < self.column_count:
                self.level_list[self.tokeniser-1] = tk.Frame(self.scrollable_frame, width=240,
                                                             height=200, background="RED")
                self.level_list[self.tokeniser-1].grid(column=self.tokeniser-1, row=0)
                self.level_icon = ttk.Label(self.level_list[self.tokeniser-1], image=self.python_logo)
                self.level_icon.place(relx=0.5, rely=0.5, anchor="center")
                self.level_select_button = ttk.Button(self.level_list[self.tokeniser-1],
                                                      text=f"Level {self.tokeniser}",
                                                      command=partial(self.play_madlibs_pane, self.tokeniser))
                self.level_select_button.place(relx=0.5, rely=0.9, anchor="center")
                self.level_list[self.tokeniser-1].grid_propagate(tk.FALSE)

            if self.tokeniser-1 >= self.column_count:
                self.level_list[self.tokeniser-1] = tk.Frame(self.scrollable_frame,
                                                             width=240, height=200, borderwidth=4)
                self.level_list[self.tokeniser-1].grid(column=self.tokeniser - self.column_count - 1, row=1)
                self.level_list[self.tokeniser-1].grid_propagate(tk.FALSE)

                self.level_icon = ttk.Label(self.level_list[self.tokeniser-1], image=self.python_logo)
                self.level_icon.place(relx=0.5, rely=0.5, anchor="center")

                self.level_select_button = ttk.Button(self.level_list[self.tokeniser-1],
                                                      text=f"Level {self.tokeniser}",
                                                      command=partial(self.play_madlibs_pane, self.tokeniser))
                self.level_select_button.place(relx=0.5, rely=0.9, anchor="center")

            # condition in loop to identify which level to be unlocked for the user
            if int(self.profile_progress) != 0 and self.tokeniser > self.profile_progress/2 + 1:
                self.level_select_button.state(['disabled'])

            if int(self.profile_progress) == 0 and self.tokeniser > 1:
                self.level_select_button.state(['disabled'])

            self.scrollable_frame.update()
            self.tokeniser += 1


    def menu_pane(self):
        """
        Menu bar on top of the windows
        :return:
        """
        self.main_menu.add_command(label="Account", command=self.account_pane)
        self.levels_menu = tk.Menu(self.main_menu, tearoff=0)
        self.levels_menu.add_command(label="Levels", command=self.play_pane)
        # determines the last level the user passed and straight opens the next level
        self.levels_menu.add_command(label="Continue", command=partial(self.play_madlibs_pane,
                                                                       int((self.profile_progress+2)/2)))

        self.main_menu.add_cascade(label="Level", menu=self.levels_menu)
        self.main_menu.add_command(label="Quit", command=self.close_window)
        self.config(menu=self.main_menu)


    def save_progress(self, level_arg, prof_arg):
        """
        saves the progress of the user in a text file
        :param level_arg: specifies which level the answer belongs to
        :param prof_arg: specifies which profile file to be accessed
        :return:
        """
        self.level = level_arg + 1
        self.profile = prof_arg
        self.list_to_copy = [] # stores
        self.count = 0
        for self.count in range(len(self.Entry_list)):
            if self.count <= len(self.Entry_list):
                self.list_to_copy.append(self.Entry_list[self.count].get())
                self.count += 1

        self.profile_path = ".\\profiles\\" +\
                            self.profile + ".txt"
        self.level_order = "Level " + str(self.level-1)
        self.progress_save = open(self.profile_path, "a")
        self.progress_save.write("Level" + str(self.level-1) + "\n")
        for entries in self.list_to_copy:
            self.progress_save.write(str(entries)+",") #write the inputs separated by a comma in a single line
        self.progress_save.write("\n")
        self.progress_save.close()

        showinfo(title='Progress Saved', message='Progress Saved!!\n Restart game for the progress to take effect')
        self.play_madlibs_pane(self.level)


class ChooseProfileDialog(tk.Toplevel):
    """
    A window that prompts user to select and create a profile
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('380x190+300+250')
        self.profile_path = os.listdir(r".\\Resources\\Profile_images\\")
        self.selected_profile = tk.StringVar()
        self.image_frame = [None] * 16 # 16 beacuse no of options for profile image is constant
        self.count = 0

        # save the image objects for profiles in a list called image_frame
        for entry in self.profile_path:
            self.buffer = Image.open(r".\\Resources\\Profile_images\\"+str(entry))
            self.buffer = self.buffer.resize((70, 70))
            self.image_frame[self.count] = ImageTk.PhotoImage(self.buffer)
            self.count += 1

        self.profile_pane()


    def profile_pane(self):
        """
        opens a window with list of profiles already saved in the game
        :return:
        """
        path_profile = os.scandir(r".\\profiles\\")
        self.topic_frame = tk.Frame(self, width=380, height=30)
        self.topic_frame.grid(column=0, row=0, sticky='nw')

        self.dialog_topic = tk.Label(self.topic_frame, text='Choose a Profile:', font=('Arial', 15))
        self.dialog_topic.grid(column=0, row=0, sticky='nw', pady=(5, 0), padx=(5, 0))
        self.profile_creator = tk.Button(self.topic_frame, text="Create one",
                                         command=partial(self.profile_pic_selection_window))
        self.profile_creator.grid(column=1, row=0, sticky='ne', padx=(140,10), pady=(5, 0))

        self.main_frame = tk.Frame(self, width=380, height=140)
        self.main_frame.grid(column=0, row=1, sticky='sw')
        self.main_canvas = tk.Canvas(self.main_frame, height=140)
        self.prof_scroll = tk.Scrollbar(self.main_frame, orient='horizontal', command=self.main_canvas.xview)
        self.prof_frame = tk.Frame(self.main_canvas)
        self.main_canvas.pack(side="top", fill="both", expand=True)
        self.main_canvas.create_window((0, 0), window=self.prof_frame, anchor="nw")
        self.main_canvas.configure(xscrollcommand=self.prof_scroll.set)
        self.prof_scroll.pack(side="bottom", fill="both")
        self.prof_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )
        )
        self.frame_list = [None]*len(os.listdir(r".\\profiles\\"))
        self.image_list = [None]*len(os.listdir(r".\\profiles\\"))

        counter = 0
        for profile in path_profile:
            self.name_var = str(profile.name)
            self.frame_list[counter] = tk.Frame(self.prof_frame, width=120, height=140)
            self.frame_list[counter].grid(column=counter, row=0, sticky='nw')
            self.selected_index = int(str(linecache.getline(r".\profiles\\" + self.name_var, 2).lstrip()))
            self.image_list[counter] = tk.Label(self.frame_list[counter], image=self.image_frame[self.selected_index])
            self.image_list[counter].place(relx=0.5, rely=0.5, anchor='center')
            self.profile_label = tk.Button(self.frame_list[counter], text=self.name_var[:-4],
                                           command=partial(self.profile_select, profile.name))
            self.profile_label.place(relx=0.5, rely=0.9, anchor='s')
            counter += 1
        self.prof_frame.update()

    def profile_select(self, arg):
        """
        opens when one of the profiles is selected
        :param arg: returns the numeral value of the place of profile in the list
        :return:
        """
        self.prof_content = arg
        self.password = str(linecache.getline(r".\profiles\\" + self.prof_content, 1))
        self.password = self.password.rstrip()
        self.paword = [None]*1
        self.paword[0] = self.password
        self.prompt_answer = simpledialog.askstring("Input", "Enter your password:", parent=self)
        print(self.prompt_answer)

        # password authentication system
        if self.prompt_answer == str(self.password):
            top_window = GameWindow(self, self.prof_content)
            top_window.deiconify()
            top_window.menu_pane()
            self.withdraw()
        else:
            messagebox.showerror("Error", "Wrong Password Entered!!")

    def create_profile(self, arg):
        """
        opens when the user wants to create a new profile
        :param arg: the numeral value returned by the radio button for the image selected
        :return:
        """
        self.selected_dp = arg
        self.profile_entry_frame = tk.Toplevel(self)
        self.profile_entry_frame.geometry('400x180+350+300')
        self.profile_entry_frame.title('Create profile')

        self.left_frame = tk.Frame(self.profile_entry_frame, width=150, height=180)
        self.left_frame.grid(column=0, row=0, sticky='nw')

        self.dp_image = tk.Button(self.left_frame, image=self.image_frame[self.selected_dp])
        self.dp_image.place(relx=0.5, rely=0.3, anchor='center')
        self.change_dp = tk.Button(self.left_frame,
                                   text="Select Profile!", command=partial(self.profile_pic_selected))
        self.change_dp.place(relx=0.5, rely=0.9, anchor='center')

        self.right_frame = tk.Frame(self.profile_entry_frame, width=250, height=180)
        self.right_frame.grid(column=1, row=0, sticky='ne')

        self.Username_label = tk.Label(self.right_frame, text="Username:")
        self.Username_label.grid(column=0, row=0, sticky='nw', padx=20, pady=(30, 10))
        self.user_file_name = tk.StringVar()
        self.username_field_entry = tk.Entry(self.right_frame, width=15, textvariable=self.user_file_name)
        self.username_field_entry.grid(column=1, row=0, sticky='ne', padx=20, pady=(30, 10))

        self.password_user = tk.StringVar()
        self.password_label = tk.Label(self.right_frame, text="Password:")
        self.password_label.grid(column=0, row=1, sticky='sw', padx=20, pady=10)
        self.password_field_entry = tk.Entry(self.right_frame, width=15, textvariable=self.password_user)
        self.password_field_entry.grid(column=1, row=1, sticky='se', padx=20, pady=10)

        self.set_profile_button = tk.Button(self.right_frame, text="Create", width=8,
                                            command=partial(self.create_profile_file))
        self.set_profile_button.grid(column=0, row=2, sticky='sw', padx=(10, 10), pady=(40, 10))

        # cancels the process and goes back to the profile lists
        self.cancel = tk.Button(self.right_frame, text="Discard", width=8, command=partial(self.continue_profile))
        self.cancel.grid(column=1, row=2, sticky='se', padx=(10, 10), pady=(40, 10))


    def create_profile_file(self):
        """
        invoked by the create button from the previous window (Username, password, and DP image selection)
        :return:
        """
        self.profile_entry_frame.withdraw()
        self.user_name = self.username_field_entry.get()
        self.pass_word = self.password_field_entry.get()

        # writes the password on the first line and the image position in the list in the second line
        with open(r".\\profiles\\"+str(self.user_name)+".txt", 'w') as profile:
            profile.write(str(self.pass_word) +
                          "\n" +
                          self.dp_value + "\n")

        self.profile_pane()

    def continue_profile(self):
        """
        withdraws the create profile prompt window to continue to the profile selection
        :return:
        """
        self.profile_entry_frame.withdraw()

    def profile_pic_selection_window(self):
        """
        displays  a list of sample images to choose the profile image from
        :return:
        """
        self.profile_select_frame = tk.Toplevel(self)
        self.profile_select_frame.geometry('335x480+50+50')
        self.profile_select_frame.title('Select profile image')
        self.profile_select_image_frame = tk.Frame(self.profile_select_frame, width=250, height=300)
        self.profile_select_image_frame.grid(column=0, row=0, sticky=tk.N+tk.W)

        self.profile_select_lower_frame = tk.Frame(self.profile_select_frame, width=335, height=70)
        self.profile_select_lower_frame.grid(column=0, row=1, sticky='sw')

        self.column_count = 4
        self.frame_image_list = [None]*16
        self.image_holder = [None]*16
        self.radio_list = [None]*16
        self.row_count = 0
        self.step_count = 0
        x = 0

        for entry in self.profile_path:
            if x <= 16:
                if x < 4:
                    self.frame_image_list[x] = tk.Frame(self.profile_select_image_frame, width=50, height=50)
                    self.frame_image_list[x].grid(column=x, row=0)

                    self.image_holder[x] = tk.Label(self.frame_image_list[x], image=self.image_frame[x])
                    self.image_holder[x].pack(padx=5, pady=(5, 0), anchor=tk.N)
                    self.radio_list[x] = ttk.Radiobutton(self.frame_image_list[x], value=x,
                                                         variable=self.selected_profile)
                    self.radio_list[x].pack(anchor=tk.S)

                if 8 > x >= 4:
                    self.frame_image_list[x] = tk.Frame(self.profile_select_image_frame, width=50, height=50)
                    self.frame_image_list[x].grid(column=x-4, row=1)

                    self.image_holder[x] = tk.Label(self.frame_image_list[x], image=self.image_frame[x])
                    self.image_holder[x].pack(padx=5, pady=5, anchor=tk.N)
                    self.radio_list[x] = ttk.Radiobutton(self.frame_image_list[x], value=x,
                                                         variable=self.selected_profile)
                    self.radio_list[x].pack(anchor=tk.S)

                if 12 > x >= 8:
                    self.frame_image_list[x] = tk.Frame(self.profile_select_image_frame, width=50, height=50)
                    self.frame_image_list[x].grid(column=x-8, row=2)

                    self.image_holder[x] = tk.Label(self.frame_image_list[x], image=self.image_frame[x])
                    self.image_holder[x].pack(padx=5, pady=5, anchor=tk.N)
                    self.radio_list[x] = ttk.Radiobutton(self.frame_image_list[x], value=x,
                                                         variable=self.selected_profile)
                    self.radio_list[x].pack(anchor=tk.S)

                if 16 > x >= 12:
                    self.frame_image_list[x] = tk.Frame(self.profile_select_image_frame, width=50, height=50)
                    self.frame_image_list[x].grid(column=x-12, row=3)

                    self.image_holder[x] = tk.Label(self.frame_image_list[x], image=self.image_frame[x])
                    self.image_holder[x].pack(padx=5, pady=5, anchor=tk.N)
                    self.radio_list[x] = ttk.Radiobutton(self.frame_image_list[x], value=x,
                                                         variable=self.selected_profile)
                    self.radio_list[x].pack(anchor=tk.S)
                x += 1

        self.choice_selected = tk.Button(self.profile_select_lower_frame, text="Set profile!",
                                         command=partial(self.changedp))
        self.choice_selected.place(relx=0.5, rely=0.5, anchor='center')

    def changedp(self):
        """
        invokes to set the dp_value to the value returned by the selected radio button
        :return:
        """
        self.dp_value = self.selected_profile.get()
        self.profile_select_frame.withdraw()
        self.create_profile(int(self.dp_value))


class IntroWindow(tk.Tk):
    """
    invoked before any other class or program in the whole script
    """
    def __init__(self):
        super().__init__()
        self.geometry('720x480+200+150')
        self.title("Madlibs")
        global image_logo
        self.iconbitmap(r'.\\Resources\\Python-logo.ico')
        self.python_logo = ImageTk.PhotoImage(image_logo)
        self.mainframe = tk.Frame(self, width=720, height=480)
        self.mainframe.pack()
        

    def intro_win(self):
        icon_1 = ttk.Label(self.mainframe, image=self.python_logo, text="Hello there!!")
        icon_1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        main_label = ttk.Label(self.mainframe, text="Welcome to Madlibs", font=("Arial", 25))
        main_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        next_window_button = ttk.Button(self.mainframe, text="Let's Start", command=self.open_play)
        next_window_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def open_play(self):
        """
        withdraws the introductory panel and invokes the profile selection
        :return:
        """
        profile_window = ChooseProfileDialog(self)
        profile_window.deiconify()
        self.withdraw()


if __name__ == "__main__":
    mad_app = IntroWindow()
    mad_app.intro_win()
    mad_app.mainloop()
