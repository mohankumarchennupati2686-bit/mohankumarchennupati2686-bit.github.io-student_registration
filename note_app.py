import tkinter as tk
from tkinter import messagebox, ttk
import os
import smtplib
from email.message import EmailMessage


class StudentPortalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Student Management System")
        self.root.geometry("550x850")

        # Data Files
        self.db_file = "user_credentials.txt"
        self.reg_file = "registrations.txt"

        # Admin, Email & Payment Details
        self.admin_email = "chennupatimohankumar8@gmail.com"
        self.app_password = "nwwz jsgs mkck cywy"
        self.upi_id = "mohankumarchennupati2686@okicici"
        self.mobile = "9398756203"

        # Special Admin Login Credentials
        self.ADMIN_USER = "admin"
        self.ADMIN_PASS = "admin123"

        # Initialize Files
        for f in [self.db_file, self.reg_file]:
            if not os.path.exists(f):
                with open(f, "w") as file: pass

        self.dark_mode = False
        self.show_login_screen()

    # --- EMAIL SENDER ---
    def send_email_receipt(self, student_email, program, utr, s1_name, s2_name):
        try:
            msg = EmailMessage()
            msg['Subject'] = f"Registration Received: {program}"
            msg['From'] = self.admin_email
            msg['To'] = student_email
            content = f"Hello {s1_name},\n\nPayment for {program} (â‚¹200) has been received. \nUTR: {utr}\nStatus: Under Verification by Admin."
            msg.set_content(content)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.admin_email, self.app_password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False

    # --- ADMIN DASHBOARD ---
    def show_admin_page(self):
        self.clear_screen()
        self.root.configure(bg="#f4f4f4")
        tk.Label(self.root, text="Admin: Payment Verification", font=("Arial", 18, "bold"), bg="#f4f4f4",
                 fg="#d32f2f").pack(pady=20)

        # Table
        columns = ("User", "UTR", "Program", "Student 1", "Status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True, padx=20)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f4f4f4")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="APPROVE PAYMENT", bg="#2e7d32", fg="white", width=20, font=("Arial", 10, "bold"),
                  command=self.verify_selected_payment).pack(side="left", padx=10)
        tk.Button(btn_frame, text="LOGOUT", bg="#555", fg="white", command=self.show_login_screen).pack(side="left",
                                                                                                        padx=10)
        self.refresh_admin_table()

    def refresh_admin_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        with open(self.reg_file, "r") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) >= 6:
                    self.tree.insert("", "end", values=(
                    parts[1].split(": ")[1], parts[2].split(": ")[1], parts[3].split(": ")[1], parts[4].split(": ")[1],
                    parts[0].split(": ")[1]))

    def verify_selected_payment(self):
        selected = self.tree.selection()
        if not selected: return messagebox.showwarning("Admin", "Select a record!")
        utr_to_verify = str(self.tree.item(selected)['values'][1])
        new_lines = []
        with open(self.reg_file, "r") as f:
            for line in f:
                new_lines.append(line.replace("STATUS: PAID", "STATUS: VERIFIED âœ…") if utr_to_verify in line else line)
        with open(self.reg_file, "w") as f:
            f.writelines(new_lines)
        messagebox.showinfo("Success", f"UTR {utr_to_verify} Verified!")
        self.refresh_admin_table()

    # --- STUDENT DASHBOARD & REGISTRATION ---
    def show_notes_screen(self, username):
        self.current_user = username
        self.clear_screen()
        header = tk.Frame(self.root, bg="#d32f2f", pady=10);
        header.pack(fill="x")
        tk.Label(header, text=f"Welcome, {username}", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        tk.Button(header, text="Logout", command=self.show_login_screen).pack(side="right", padx=10)

        # Event Buttons
        reg_frame = tk.LabelFrame(self.root, text="Register for Events (â‚¹200)");
        reg_frame.pack(fill="x", padx=20, pady=10)
        for p in ["PPT", "Quiz", "Dance"]:
            tk.Button(reg_frame, text=p, width=10, command=lambda n=p: self.open_reg_form(n)).pack(side="left", padx=10,
                                                                                                   pady=10)

        # My Receipts Button
        tk.Button(self.root, text="View My Receipts", bg="#2196F3", fg="white", command=self.show_my_receipts).pack(
            pady=5)

        # Notebook
        tk.Label(self.root, text="Personal Notebook", font=("Arial", 11, "bold")).pack()
        self.text_area = tk.Text(self.root, height=15);
        self.text_area.pack(fill="both", expand=True, padx=20, pady=10)

        note_path = f"note_{username}.txt"
        if os.path.exists(note_path):
            with open(note_path, "r") as f: self.text_area.insert("1.0", f.read())

        tk.Button(self.root, text="SAVE NOTES", bg="#d32f2f", fg="white", font=("Arial", 12, "bold"),
                  command=self.save_notes).pack(fill="x", padx=20, pady=10)

    def open_reg_form(self, program):
        reg_win = tk.Toplevel(self.root);
        reg_win.geometry("400x650")
        entries = {}

        def create_form(title, pfx):
            tk.Label(reg_win, text=title, font=("Arial", 11, "bold"), fg="#d32f2f").pack(pady=5)
            for f in ["Name", "Gmail", "College", "Roll No"]:
                tk.Label(reg_win, text=f).pack()
                e = tk.Entry(reg_win);
                e.pack(padx=40, fill="x")
                entries[f"{pfx}_{f.lower()}"] = e

        create_form("Student 1 (Recipient)", "s1");
        create_form("Student 2 Details", "s2")
        tk.Button(reg_win, text="Proceed to Payment", bg="#d32f2f", fg="white",
                  command=lambda: [self.open_payment_window(program, {k: v.get() for k, v in entries.items()}),
                                   reg_win.destroy()]).pack(pady=20)

    def open_payment_window(self, program, data):
        pay_win = tk.Toplevel(self.root);
        pay_win.geometry("450x650");
        pay_win.configure(bg="white")
        tk.Label(pay_win, text=f"Pay â‚¹200 to {self.mobile}", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
        try:
            self.qr_img = tk.PhotoImage(file="qr.png")
            tk.Label(pay_win, image=self.qr_img, bg="white").pack()
        except:
            tk.Label(pay_win, text="[QR Image missing: qr.png]", bg="#eee", width=20, height=8).pack()

        tk.Label(pay_win, text="Enter 12-Digit UTR Number:", bg="white").pack(pady=10)
        utr_ent = tk.Entry(pay_win, font=("Arial", 14), justify="center");
        utr_ent.pack(padx=50, fill="x")

        def finalize():
            utr = utr_ent.get().strip()
            if len(utr) < 12: return messagebox.showerror("Error", "Invalid UTR")
            with open(self.reg_file, "a") as f:
                f.write(
                    f"STATUS: PAID | USER: {self.current_user} | UTR: {utr} | PROG: {program} | S1: {data['s1_name']} | S2: {data['s2_name']}\n")
            self.send_email_receipt(data['s1_gmail'], program, utr, data['s1_name'], data['s2_name'])
            messagebox.showinfo("Success", "Payment Submitted! Check Email for Receipt.")
            pay_win.destroy()

        tk.Button(pay_win, text="SUBMIT & SEND EMAIL", bg="#2e7d32", fg="white", font=("Arial", 12, "bold"),
                  command=finalize).pack(pady=20)

    def show_my_receipts(self):
        rec_win = tk.Toplevel(self.root);
        rec_win.geometry("400x500");
        tk.Label(rec_win, text="My Registrations", font=("Arial", 14, "bold")).pack(pady=10)
        with open(self.reg_file, "r") as f:
            for line in f:
                if f"USER: {self.current_user}" in line:
                    tk.Label(rec_win, text=line.replace(" | ", "\n"), bg="white", relief="groove", pady=5, padx=5).pack(
                        fill="x", padx=20, pady=5)

    # --- LOGIN / SIGNUP ---
    def handle_login(self):
        u, p = self.u_ent.get().strip(), self.p_ent.get().strip()
        if u == self.ADMIN_USER and p == self.ADMIN_PASS: return self.show_admin_page()
        with open(self.db_file, "r") as f:
            for line in f:
                if f"{u},{p}" == line.strip(): return self.show_notes_screen(u)
        messagebox.showerror("Error", "Login Failed")

    def show_login_screen(self):
        self.clear_screen()
        self.root.configure(bg="white")
        tk.Label(self.root, text="Student Portal", font=("Arial", 24, "bold"), fg="#d32f2f", bg="white").pack(pady=50)
        self.u_ent = tk.Entry(self.root, font=("Arial", 12));
        self.u_ent.pack(pady=5)
        self.p_ent = tk.Entry(self.root, show="*", font=("Arial", 12));
        self.p_ent.pack(pady=5)
        tk.Button(self.root, text="Login", bg="#d32f2f", fg="white", width=15, command=self.handle_login).pack(pady=20)
        tk.Button(self.root, text="Create Account", command=self.show_signup_screen, bd=0).pack()

    def show_signup_screen(self):
        self.clear_screen();
        tk.Label(self.root, text="Sign Up").pack(pady=20)
        self.nu = tk.Entry(self.root);
        self.nu.pack();
        self.np = tk.Entry(self.root, show="*");
        self.np.pack()
        tk.Button(self.root, text="Register", command=self.handle_signup).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_login_screen).pack()

    def handle_signup(self):
        if self.nu.get() and self.np.get():
            with open(self.db_file, "a") as f: f.write(f"{self.nu.get()},{self.np.get()}\n")
            messagebox.showinfo("Success", "Account Created!");
            self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children(): widget.destroy()

    def save_notes(self):
        with open(f"note_{self.current_user}.txt", "w") as f: f.write(self.text_area.get("1.0", tk.END))
        messagebox.showinfo("Saved", "Notes Saved")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPortalApp(root)
    root.mainloop()
