"""
First-time onboarding screen for TriFlow app (Phase 2).

Features:
- Tkinter frame that appears before main GUI is shown.
- Shows a brief welcome message and a "Start Tour" or "Continue" button.
- Provides accessibility tips or a brief app walkthrough.
- On click, this window closes and launches main_gui.MainApp.

Structure:
- Class: OnboardingScreen(tk.Toplevel)
"""

import tkinter as tk
from tkinter import ttk
# from gui.main_gui import MainApp  # Uncomment when main_gui.py is implemented

class OnboardingScreen(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Welcome to TriFlow")
        self.geometry("400x250")
        ttk.Label(self, text="👋 Welcome to TriFlow!", font=("Arial", 16)).pack(pady=12)
        ttk.Label(self, text="TriFlow helps you manage tasks, budgets, and more.\nGet started with a quick tour!").pack(pady=6)
        ttk.Button(self, text="Start", command=self._start_main_app).pack(pady=18)
        # Optionally add more onboarding info here

    def _start_main_app(self):
        self.destroy()
        # MainApp().mainloop()  # Uncomment to launch main app after onboarding

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    onboarding = OnboardingScreen(root)
    onboarding.mainloop()