from tkinter import (
    Tk,
    Toplevel,
    PanedWindow,
    Listbox,
    Button,
    Label,
    Scrollbar,
    PhotoImage,
)
from tkinter.ttk import Treeview
from os.path import dirname, isdir, isfile, normpath, split as path_split
from re import findall, sub, split as re_split
from platform import system
from subprocess import run
from math import ceil


class Ufd:
    """
        Universal File Dialog - "UFD"
        
        Unopinionated, minimalist, reusable, slightly configurable,
        general-purpose file-dialog.
    """

    def __init__(
        self,
        title:str="Universal File Dialog",
        show_hidden:bool=False,
        include_files:bool=True,
        tree_xscroll:bool=False,
        multiselect:bool=True,
        select_dirs:bool=True,
        select_files:bool=True,
        unix_delimiter:bool=True,
    ):

        """
            Init kwargs as object attributes, save references to 
            Tk PhotoImages, & define the widgets + layout
        """

        if not isinstance(title, str):
            raise TypeError("Argument title must be type string.")
        else:
            self.title = title

        if show_hidden:
            self.show_hidden = True
        else:
            self.show_hidden = False
        if include_files:
            self.include_files = True
        else:
            self.include_files = False
        if tree_xscroll:
            self.treeview_xscroll = True
        else:
            self.treeview_xscroll = False
        if multiselect:
            self.multiselect = True
        else:
            self.multiselect = False
        if select_dirs:
            self.select_dirs = True
        else:
            self.select_dirs = False
        if select_files:
            self.select_files = True
        else:
            self.select_files = False
        if unix_delimiter:
            self.unix_delimiter = True
        else:
            self.unix_delimiter = False

        # Tkinter:
        self.dialog = Tk()
        self.dialog.withdraw()
        self.dialog.title(self.title)
        self.dialog.minsize(width=300, height=200)
        self.dialog.geometry("500x300")

        self.file_icon=PhotoImage(
            file=f"{dirname(__file__)}/file.gif"
        ).subsample(50)
        self.folder_icon=PhotoImage(
            file=f"{dirname(__file__)}/folder.gif"
        ).subsample(15)
        self.disk_icon=PhotoImage(
            file=f"{dirname(__file__)}/disk.gif"
        ).subsample(15)

        self.dialog.iconbitmap(f"{dirname(__file__)}/main_icon.ico")
        
        # Widgets:
        self.paneview = PanedWindow(
            self.dialog,
            sashwidth=7,
            bg="#cccccc",
            bd=0,
        )

        self.left_pane = PanedWindow(self.paneview, orient="vertical")
        self.right_pane = PanedWindow(self.paneview, orient="vertical")
        self.paneview.add(self.left_pane)
        self.paneview.add(self.right_pane)

        self.treeview_x_scrollbar=Scrollbar(self.left_pane, orient="horizontal")
        self.treeview_y_scrollbar=Scrollbar(self.left_pane, orient="vertical")
        self.file_list_x_scrollbar=Scrollbar(self.right_pane, orient="horizontal")
        self.file_list_y_scrollbar=Scrollbar(self.right_pane, orient="vertical")
        
        self.treeview=Treeview(
            self.left_pane,
            xscrollcommand=self.treeview_x_scrollbar.set,
            yscrollcommand=self.treeview_y_scrollbar.set,
            show="tree",
            selectmode="browse"
        )

        # Tkinter x_scroll is broken for treeview
        # https://stackoverflow.com/questions/49715456
        # https://stackoverflow.com/questions/14359906
        # Lousy bandaid:
        if self.treeview_xscroll:
            self.treeview.column("#0", minwidth=1000)

        self.file_list=Listbox(
            self.right_pane,
            xscrollcommand=self.file_list_x_scrollbar.set,
            yscrollcommand=self.file_list_y_scrollbar.set,
            width=34,
            highlightthickness=0,
            bd=2,
            relief="ridge"
        )

        if self.multiselect:
            self.file_list.config(selectmode="extended")
        else:
            self.file_list.config(selectmode="browse")

        self.browse_label = Label(self.left_pane, text="Browse")
        self.select_label = Label(self.right_pane, text="Select")

        self.cancel_button = Button(
            self.left_pane,
            text="Cancel",
            command=self.cancel
        )

        self.submit_button = Button(
            self.right_pane,
            text="Submit",
            command=self.submit
        )

        self.treeview_x_scrollbar.config(command=self.treeview.xview)
        self.treeview_y_scrollbar.config(command=self.treeview.yview)
        self.file_list_x_scrollbar.config(command=self.file_list.xview)
        self.file_list_y_scrollbar.config(command=self.file_list.yview)
        
        #Layout:
        self.dialog.rowconfigure(0, weight=1)
        self.dialog.columnconfigure(0, weight=1)

        self.left_pane.grid_rowconfigure(1, weight=1)
        self.left_pane.grid_columnconfigure(0, weight=1)
        self.right_pane.grid_rowconfigure(1, weight=1)
        self.right_pane.grid_columnconfigure(0, weight=1)

        self.paneview.paneconfigure(
            self.left_pane,
            minsize=100,
            #Start off w/ the sash centered in the GUI:
            width=(self.dialog.winfo_width() / 2) - ceil((self.paneview.cget("sashwidth") * 1.5)),
        )
        self.paneview.paneconfigure(self.right_pane, minsize=100)

        self.paneview.grid(row=0, column=0, sticky="nsew")

        self.browse_label.grid(row=0, column=0)
        self.select_label.grid(row=0, column=0)
        
        self.treeview.grid(row=1, column=0, sticky="nsew")
        self.treeview_y_scrollbar.grid(row=1, column=1, sticky="ns")
        self.treeview_x_scrollbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.file_list.grid(row=1, column=0, sticky="nsew")
        self.file_list_y_scrollbar.grid(row=1, column=1, sticky="ns")
        self.file_list_x_scrollbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.cancel_button.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.submit_button.grid(row=3, column=0, columnspan=2, sticky="e", padx=10, pady=10)
        
        #Bindings, Protocols, & Misc:
        self.treeview.bind("<Double-Button-1>", self.dialog_populate)
        self.treeview.bind("<Return>", self.dialog_populate)
        self.treeview.bind("<Right>", self.dialog_populate)
        self.file_list.bind("<<ListboxSelect>>", self.selection_populate)
        self.file_list.bind("<Return>", self.submit)
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)

        self.dialog_selection = []
        self.file_list_paths = []

        for disk in self.get_disks():
            self.treeview.insert(
                "",
                index="end",
                text=disk,
                image=self.disk_icon,
            )

        self.dialog.focus()


    def __call__(self):
        """
            Display dialog & return selection
        """

        self.dialog.deiconify()
        (width_offset, height_offset)=self.get_offset(self.dialog)
        self.dialog.geometry(f"+{width_offset}+{height_offset}")

        self.dialog.wait_window()

        if not self.unix_delimiter:
            for i, path in enumerate(self.dialog_selection):
                self.dialog_selection[i] = sub("/", "\\\\", path)

        return self.dialog_selection


    def __str__(self):
        """
            Return own address
        """

        return "Universal File Dialog"\
        f" @ {hex(id(self))}"


    def __repr__(self):
        """
            Return full string representation of constructor signature
        """

        return f"Ufd("\
        f"title=\"{self.title}\","\
        f" show_hidden={self.show_hidden},"\
        f" include_files={self.include_files},"\
        f" tree_xscroll={self.treeview_xscroll},"\
        f" multiselect={self.multiselect},"\
        f" select_dirs={self.select_dirs},"\
        f" select_files={self.select_files},"\
        f" unix_delimiter={self.unix_delimiter})"\
        f" @ {hex(id(self))}"


    @staticmethod
    def get_disks():
        """
            Returns all mounted disks (for Windows)

            >> ["A:", "B:", "C:"]
        """

        if system() != "Windows":
            raise OSError("For use with Windows platforms.")

        logicaldisks=run(
            ["wmic", "logicaldisk", "get", "name"],
            capture_output=True
        )

        disks=findall("[A-Z]:", str(logicaldisks.stdout))
        
        return [disk for disk in disks]


    @staticmethod
    def list_dir(path, force=False):
        """
            Reads a directory with a shell call to dir.
            Truthiness of bool force determines whether 
            hidden items are returned or not. (For Windows)
        """

        path = sub("/", "\\\\", path)

        if force:
            dir_listing=run([
                "dir",
                path,
                "/b",
                "/a"
            ], shell=True, capture_output=True)

        else:
            dir_listing=run([
                "dir",
                path,
                "/b"
            ], shell=True, capture_output=True)

        output=dir_listing.stdout
        err=dir_listing.stderr

        if not output:
            return []

        if err:
            err=err.decode("utf-8")
            raise Exception(err)

        str_output=output.decode("utf-8")
        list_output=re_split("\r\n", str_output)
        
        return sorted([item for item in list_output if item])


    def climb(self, item):
        """
            Builds & returns a complete path to root directory,
            including the item name itself as the path tail.
            An extra delimiter is appeneded for the subsequent
            child node, which is normalized in dialog_populate()
        """
        
        item_text = self.treeview.item(item)["text"]
        parent = self.treeview.parent(item)
        path = ""
        parents = []

        while parent:
            parents.append(self.treeview.item(parent)["text"] + "/")
            parent = self.treeview.parent(parent)

        for parent in reversed(parents):
            path += parent

        path += item_text + "/"
        return path


    def dialog_populate(self, event=None):
        """
            Dynamically populates & updates the treeview, listbox,
            and keeps track of the full paths corresponding to each
            item in the listbox
        """

        existing_children = self.treeview.get_children(self.treeview.focus())
        [self.treeview.delete(child) for child in existing_children]

        while self.file_list.size():
            self.file_list.delete(0)
            self.file_list_paths.pop()

        focus_item = self.treeview.focus()
        path = self.climb(focus_item)

        if self.show_hidden:
            children = self.list_dir(path, force=True)
        else:
            children = self.list_dir(path)

        for child in children:
            if isdir(path+child):

                self.treeview.insert(
                    focus_item,
                    index="end",
                    text=child,
                    image=self.folder_icon
                )

                if self.select_dirs:
                    self.file_list.insert("end", child)
                    self.file_list_paths.append(path+child)

            elif isfile(path+child):

                if self.include_files:
                    self.treeview.insert(
                        focus_item,
                        index="end",
                        text=child,
                        image=self.file_icon
                    )

                if self.select_files:
                    self.file_list.insert("end", child)
                    self.file_list_paths.append(path+child)
                    self.file_list.itemconfig("end", {"bg":"#EAEAEA"})

        if isfile(normpath(path)):
            (head, tail) = path_split(normpath(path))
            head = sub("\\\\", "/", head)
            
            self.file_list.insert("end", tail)
            self.file_list_paths.append(head + "/" + tail)
            self.file_list.itemconfig("end", {"bg":"#EAEAEA"})


    def selection_populate(self, event=None):
        """
            Dynamically refreshes the array of selected items in the
            listbox (Callback for <<ListboxSelect>>).
        """

        self.dialog_selection.clear()

        for i in self.file_list.curselection():
            self.dialog_selection.append(self.file_list_paths[i])


    def submit(self, event=None):
        """
            Satisfies wait_window() in self.__call__()

            (Callback for <Return>, <Button-1> on file_list, submit_button)
        """
        
        self.dialog.destroy()


    def cancel(self, event=None):
        """
            Satisfies wait_window() in self.__call__() 

            (Callback for <Button-1> on submit_button)
            (Callback for protocol "WM_DELETE_WINDOW" on self.dialog)
        """

        self.dialog_selection.clear()
        self.dialog.destroy()


    @staticmethod
    def get_offset(tk_window):
        """
            Returns an appropriate offset for a given tkinter toplevel,
            such that it always is created center screen on the primary display.
        """

        width_offset = int(
            (tk_window.winfo_screenwidth() / 2) - (tk_window.winfo_width() / 2)
        )

        height_offset = int(
            (tk_window.winfo_screenheight() / 2) - (tk_window.winfo_height() / 2)
        )

        return (width_offset, height_offset)
