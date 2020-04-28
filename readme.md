# Universal File Dialog

<p align="center">
	<img src="https://i.imgur.com/0WsmsVD.png">
	<img src="https://i.imgur.com/RIQBxge.png">
</p>

## Install & Get Started:

`pip install Ufd`

###### or

`git clone https://github.com/emboiko/Ufd.git` 

###### or

Download the .zip [here](https://github.com/emboiko/Ufd/archive/master.zip)

### Import:

`from Ufd import Ufd`

### Construct:
```
dialog = Ufd(**Kwargs)
result = dialog()
```

or specify a bunch of **options**:

```
dialog = Ufd(
    title="My Dialog",
    icon="path/to/some_icon.ico",
    show_hidden=True,
    multiselect=False
    select_dirs=False
)
result = dialog()
```

Ufd's full constructor signature looks like this:

```
def __init__(
    self,
    title:str="Universal File Dialog",
    icon:str="",
    show_hidden:bool=False,
    include_files:bool=True,
    multiselect:bool=True,
    select_dirs:bool=True,
    select_files:bool=True,
    unix_delimiter:bool=True,
    stdout:bool=False
):
```
`title`             : str: Window title

`icon`              : str: Path to your custom icon.ico file 

`show_hidden`       : bool: Include hidden file(s) or folder(s) in treeview

`include_files`     : bool: Include file(s) in treeview

`multiselect`       : bool: File-list multiselect support, returns a list either way

`select_dirs`       : bool: File-list shows directories (folder-browser)

`select_files`      : bool: File-list shows files (file-browser)

`unix_delimiter`    : bool: Return paths delimited with "/" or "\\"

`stdout`            : bool: Print a newline delimited list of the dialog selection to stdout before returning (Useful if you aren't calling the dialog from a Python)

Ufd still has several [boolean constructor parameters] options & behavioral tweaks in development that will optionally restrict / expand upon its behavior to match the context in which it is used. 

## Using Ufd without Python
Ufd.exe is a Windows binary compiled with PyInstaller for x64 systems. (`dist_win64/Ufd/Ufd.exe`)

```
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

int main(int argc, char *argv[]) {
    system("C:/Programming/Python/Projects/Ufd/dist/Ufd/ufd.exe stdout=True > paths.txt");
    std::ifstream inFile("paths.txt");

    std::vector<std::string> results;
    std::string result;

    while (getline(inFile, result)) results.push_back(result);

    inFile.close();
    std::remove("paths.txt");

    for (std::string path : results) std::cout << path << "\n";

    std::cin.ignore();
    return 0;
}
```

## Why should I use Ufd?
- It's easy
- No external dependencies
- Ufd doesn't care what kind of dialog it's serving as. You get to deal with any ambiguities in your own way. 

Want to select 3 directories and 2 files from the same dialog, and have their paths returned as a list? 

```
dialog = Ufd()
result = dialog()
>> result
>> ["C:some_dir/dir1", "C:some_dir/dir2", "C:some_dir/dir3", "C:some_dir/file1.ext", "C:some_dir/file2.ext"]
```

Or if you'd prefer to corral the user into selecting a single file:

```
dialog = Ufd(multiselect=False, select_dirs=False)
result = dialog()
>> result
>> ["C:some_dir/file1.ext"]
```

## Tips & Tricks:

- Drill through the treeview with `<Doubleclick>`, `<Enter>`, and/or ArrowKeys.
- Treeview supports single-select via `<Doubleclick>` or the submit button.
- Navigate the listbox on the right with the mouse or arrow keys. Multiselect is supported with `<Shift>` (span) & `<Ctrl>` (individuals), or by clicking + dragging the mouse. Select all with `<Ctrl+A>` as expected. Confirm selection in the listbox with `<Enter>` or the submit button.
- Cancelling via `<Ctrl-w>`, the cancel button, or the window manager will both return an empty list from the dialog.

---
##### Todo
- Tree only mode
- Treeview x_scroll 
- Listbox Filter
- Listbox Navigation
