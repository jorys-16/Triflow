"""
Firebase login/signup screen for TriFlow app (Phase 2).

Features:
- Tkinter-based login form with Email + Password fields.
- Buttons: "Login", "Sign Up", "Continue as Guest"
- On success, launches main_gui.MainApp with current user token.
- Shows error dialogs for failed login.

Structure:
- Class: LoginScreen(tk.Tk or tk.Frame)
- Uses requests to call Firebase REST endpoint (Firebase Auth API)
- Save user session/token securely (optional: encrypted local JSON)
"""

import tkinter as tk
from tkinter import ttk, messagebox
# import requests  # For Firebase REST API
# from gui.main_gui import MainApp  # Uncomment when main_gui.py is implemented

class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TriFlow Login")
        self.geometry("350x250")
        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(self, text="Login to TriFlow", font=("Arial", 14)).pack(pady=10)
        self.email_var = tk.StringVar()
        self.pw_var = tk.StringVar()
        ttk.Label(self, text="Email:").pack()
        ttk.Entry(self, textvariable=self.email_var).pack(fill="x", padx=30)
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.pw_var, show="*").pack(fill="x", padx=30)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text="Login", command=self._login).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Sign Up", command=self._signup).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Continue as Guest", command=self._guest).grid(row=1, column=0, columnspan=2, pady=5)

    def _login(self):
        email = self.email_var.get()
        password = self.pw_var.get()
        # TODO: Implement Firebase login logic here using requests
        messagebox.showinfo("Login", f"Logging in as {email} (not implemented)")
        # On success: self.destroy(); MainApp(user=email).mainloop()

    def _signup(self):
        messagebox.showinfo("Sign Up", "Sign up not implemented yet.")

    def _guest(self):
        self.destroy()
        # MainApp(user=None).mainloop()  # Uncomment to launch main app as guest

if __name__ == "__main__":
    LoginScreen().mainloop()