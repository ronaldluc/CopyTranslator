import pyperclip

s = pyperclip.paste()
s += ' it WORKED!'
pyperclip.copy(s)
