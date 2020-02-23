from tkinter import (
    Tk,
    Toplevel,
    PanedWindow,
    Listbox,
    Button,
    Label,
    Scrollbar,
    PhotoImage,
    messagebox
)
from tkinter.ttk import Treeview
from posixpath import join, isdir, exists
from re import split, findall, sub
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
        show_hidden_files:bool=False,
        include_files:bool=False,
        tree_xscroll:bool=False,
        multiselect:bool=True,
        select_dirs:bool=True,
        select_files:bool=True,
    ):

        """
            Init kwargs as object attributes, save references to 
            Tk PhotoImages, & define the widgets + layout
        """

        self.title = title

        if show_hidden_files:
            self.show_hidden_files = True
        else:
            self.show_hidden_files = False
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

        # Tkinter:
        self.dialog = Tk()
        self.dialog.withdraw()
        self.dialog.title(self.title)
        self.dialog.minsize(width=300, height=200)
        self.dialog.geometry("500x300")

        self.file_icon=PhotoImage(
            file="file.gif"
        ).subsample(50)
        self.folder_icon=PhotoImage(
            file="folder.gif"
        ).subsample(15)
        self.disk_icon=PhotoImage(
            file=f"disk.gif"
        ).subsample(15)

        self.dialog.iconbitmap("main_icon.ico")
        
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

        self.dialog.focus()

        self.dialog_selection=[]

        for disk in self.get_disks():
            self.treeview.insert(
                "",
                index="end",
                text=disk,
                image=self.disk_icon,
            )


    def __call__(self):
        """
            Display dialog & return selection
        """

        self.dialog.deiconify()
        (width_offset, height_offset)=self.get_offset(self.dialog)
        self.dialog.geometry(f"+{width_offset}+{height_offset}")

        self.dialog.wait_window()
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
        f" show_hidden_files={self.show_hidden_files},"\
        f" include_files={self.include_files},"\
        f" tree_xscroll={self.treeview_xscroll},"\
        f" multiselect={self.multiselect},"\
        f" select_dirs={self.select_dirs},"\
        f" select_files={self.select_files})"\
        f" @ {hex(id(self))}"


    def get_disks(self):
        """
            Returns all mounted disks
        """

        logicaldisks=run([
            "wmic",
            "logicaldisk",
            "get",
            "name"
        ], capture_output=True)

        disks=findall("[A-Z]:", str(logicaldisks.stdout))
        
        return [disk + "/" for disk in disks]


    def list_dir(self, path, force=False):
        """
            Reads a directory with a shell call to dir, 
            returning contents based on the boolean FORCE
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
        list_output=split("\r\n", str_output)
        
        return sorted([item for item in list_output if item])

#####################
    def dialog_populate(self, event=None):
        """
            Dynamically populates & updates the treeview and listbox
        """
        #embarrassingly bad code. 

        error=False

        children = self.treeview.get_children(self.treeview.focus())
        if children:
            for child in children:
                self.treeview.delete(child)

        tree_item_name = self.treeview.item(self.treeview.focus())["values"]
        tree_item_name = [str(piece) for piece in tree_item_name]
        tree_item_name = " ".join(tree_item_name)

        if isdir(tree_item_name):
            try:
                if self.show_hidden_files:
                    items=self.list_dir(tree_item_name, force=True)
                else:
                    items=self.list_dir(tree_item_name, force=False)
                    
            except Exception as err:
                messagebox.showerror("Error.", err)

                items=[]
                error=True
                self.treeview.master.lift()

            for item in items:
                path=join(tree_item_name, item)

                if isdir(path): 
                    self.treeview.insert(
                        self.treeview.focus(),
                        index="end",
                        text=item,
                        value=path,
                        image=self.folder_icon
                    )

                elif self.include_files:
                    self.treeview.insert(
                        self.treeview.focus(),
                        index="end",
                        text=item,
                        value=path,
                        image=self.file_icon
                    )

        while self.file_list.size():
            self.file_list.delete(0)

        if not error:
            if isdir(tree_item_name):
                for item in items:
                    path=join(tree_item_name, item)
                    if self.select_dirs and isdir(path):
                        self.file_list.insert("end", path)
                    else:
                        if self.select_files and (not isdir(path)):
                            self.file_list.insert("end", path)
            else:
                self.file_list.insert("end", tree_item_name)


    def selection_populate(self, event=None):
        """
            Dynamically refreshes the array of selected items in the
            listbox (Callback for <<ListboxSelect>>).
        """

        self.dialog_selection.clear()
        selection_indices=self.file_list.curselection()

        for i in selection_indices:
            self.dialog_selection.append(self.file_list.get(i))


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
