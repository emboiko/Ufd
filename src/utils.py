from os.path import exists, isdir, splitext, split
from posixpath import join
from re import findall, sub
from subprocess import run
from json import loads


def flip_slashes(path, direction):
    """
        Normalizes path delimiters.
    """

    if direction == "forward":
        new_path=sub("\\\\", "/", path)
        return new_path
    if direction == "back":
        new_path=sub("/", "\\\\", path)
        return new_path


def get_disks():
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
