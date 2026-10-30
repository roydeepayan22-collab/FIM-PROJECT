import tkinter as tk
from db.db_manager import DBManager
from core.fim_engine import FIMEngine
from gui.main_window import MainWindow

def main():
    root = tk.Tk()
    root.title("Endpoint File Integrity Monitor (FIM)")
    root.geometry("1000x650")

    # Wire together dependencies smoothly
    db_manager = DBManager()
    fim_engine = FIMEngine(db_manager)

    # Initialize the main UI component view matching your layout
    MainWindow(root, fim_engine, db_manager)

    root.mainloop()

if __name__ == "__main__":
    main()
