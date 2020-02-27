# Universal File Dialog

<p align="center">
	<img src="https://i.imgur.com/yzIXiTs.png">
</p>

Import:

`from Ufd import Ufd`

Construct:
```
dialog = Ufd(**Kwargs)
result = dialog()
```

or specify a bunch of options:

```
dialog = Ufd(
    title="My Dialog"
    show_hidden=True,
    include_files=True,
    tree_xscroll=True,
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
    show_hidden:bool=False,
    include_files:bool=True,
    tree_xscroll:bool=False,
    multiselect:bool=True,
    select_dirs:bool=True,
    select_files:bool=True,
    unix_delimiter:bool=True,
):
```
`title`             : str: Window title

`show_hidden`       : bool: Include hidden file(s) or folder(s) in treeview

`include_files`     : bool: Include file(s) in treeview

`tree_xscroll`      : bool: Enable a hardcoded horizontal scroll for treeview 

`multiselect`       : bool: File-list multiselect support, returns a list either way

`select_dirs`       : bool: File-list shows directories (folder-browser)

`select_files`      : bool: File-list shows files (file-browser)

`unix_delimiter`    : bool: Return paths delimited with "/" or "\"

Ufd still has several [boolean constructor parameters] options & behavioral tweaks in development that will optionally restrict / expand upon its behavior to match the context in which it is used. 

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
