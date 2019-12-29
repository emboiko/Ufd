# Universal File Dialog

Import:

`from Ufd import Ufd`

Construct:
```
dialog = Ufd(**Kwargs)`
result = dialog()
```

Or

```
dialog = Ufd(
show_hidden_files=True,
include_files=True,
tree_xscroll=True,
multiselect=False
)

```

Ufd still has several [boolean constructor parameters] options & behavioral tweaks in development that will optionally restrict / expand upon its behavior to match the context in which it is used. 

<img  src="https://i.imgur.com/1X8c48Y.png">
<img  src="https://i.imgur.com/XLXe8Nc.png">