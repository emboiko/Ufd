from distutils.util import strtobool
from sys import argv
from src.Ufd.Ufd import Ufd

arguments = {
    "title":"Universal File Dialog",
    "icon":"",
    "show_hidden":False,
    "include_files":True,
    "multiselect":True,
    "select_dirs":True,
    "select_files":True,
    "unix_delimiter":True,
    "stdout":False,
}

args = [arg for arg in argv[1:]]

for arg in args:
    if arg.startswith("title="):
        arguments["title"] = arg[6:]
    
    if arg.startswith("icon="):
        arguments["icon"] = arg[5:]

    if arg.startswith("show_hidden="):
        arguments["show_hidden"] = strtobool(arg[12:])

    if arg.startswith("include_files="):
        arguments["include_files"] = strtobool(arg[14:])

    if arg.startswith("multiselect="):
        arguments["multiselect"] = strtobool(arg[12:])

    if arg.startswith("select_dirs="):
        arguments["select_dirs"] = strtobool(arg[12:])

    if arg.startswith("select_files="):
        arguments["select_files"] = strtobool(arg[13:])

    if arg.startswith("unix_delimiter="):
        arguments["unix_delimiter"] = strtobool(arg[15:])

    if arg.startswith("stdout="):
        arguments["stdout"] = strtobool(arg[7:])

dialog = Ufd(**arguments)
dialog()
