from gui import TaskManagerGUI
import tkinter as tk

def main():
    # Start the GUI
    root = tk.Tk()
    gui = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
