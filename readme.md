# Universal File Dialog

Import:

`from Ufd import Ufd`

Construct:
```
dialog = Ufd(**Kwargs)
result = dialog()
```

```
dialog = Ufd(
show_hidden_files=True,
include_files=True,
tree_xscroll=True,
multiselect=False
)
```

Ufd's actual constructor looks like this:

```
def __init__(
    self,
    show_hidden_files=False,
    include_files=False,
    tree_xscroll=False,
    multiselect=True,
    select_dirs=True,
    select_files=True,
):
```

`show_hidden_files` : Include hidden file(s) or folder(s) in treeview

`include_files`     : Include file(s) in treeview

`tree_xscroll`      : Enable a hardcoded horizontal scroll for treeview 

`multiselect`       : File-list multiselect support, returns a list either way

`select_dirs`       : File-list shows directories (folder-browser)

`select_files`      : File-list shows files (file-browser)

Ufd still has several [boolean constructor parameters] options & behavioral tweaks in development that will optionally restrict / expand upon its behavior to match the context in which it is used. 

## Why should I use Ufd?
- No dependencies
- It's easy
- Ufd doesn't care what kind of dialog it's serving as. 

Want to select 3 directories and 2 files from the same dialog, and have their paths returned as a list? 

```
dialog = Ufd()
result = dialog()
>> result
>> ["C:some_dir/dir1", "C:some_dir/dir2", "C:some_dir/dir3", "C:some_dir/file1.ext", "C:some_dir/file2.ext"]
```


<img  src="https://i.imgur.com/1X8c48Y.png">
<img  src="https://i.imgur.com/XLXe8Nc.png">