#!/usr/bin/env python
import datetime
import os
import sys
from Tkinter import *
from core import ToDo


def main():
    data_path = os.path.join('~', '.todone')
    todo = ToDo(data_path)
    
    root = Tk()
    
    # DRL_TODO: Add widgets here.
    
    root.mainloop()


if __name__ == '__main__':
    main()
