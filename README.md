# Tkinter_T9
T-9 для Tkinter


```python
# В качестве дополнения
import Tk_t9
T9 = Text_T9(tkinter.Tk(), tkinter.Text(), 'ru')
T9.pack()
```

```python
# Независимая работа
import Tk_t9
import tkinter

Windows = tkinter.Tk()
Text = tkinter.scrolledtext.ScrolledText(Windows, width=1, height=7)
Text.pack(fill=tkinter.BOTH, expand=True)

T9 = Text_T9(Windows, Text, 'ru')
T9.pack()
Windows.mainloop()
```
