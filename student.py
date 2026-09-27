import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


# ==================== COLOR PALETTE ====================
COLOR_YELLOW = "#facc15"
COLOR_YELLOW_DARK = "#ca8a04"
COLOR_PINK = "#ec4899"
COLOR_PINK_DARK = "#be185d"
COLOR_GREEN = "#22c55e"
COLOR_GREEN_DARK = "#15803d"
COLOR_BLUE = "#2563eb"
COLOR_BLUE_DARK = "#1d4ed8"
COLOR_ORANGE = "#f97316"
COLOR_ORANGE_DARK = "#c2410c"
COLOR_WHITE = "#ffffff"
COLOR_TEXT_DARK = "#1e293b"
COLOR_PAGE_BG = "#fff9ed"  # soft warm white background for the whole app
COLOR_ROW_ALT = "#fff4d6"  # light yellow stripe for alternating rows


def make_button(parent, text, command, bg, fg=COLOR_WHITE, hover=None):
    """Create a flat, modern-looking button with a hover effect."""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=bg,
        fg=fg,
        activebackground=hover or bg,
        activeforeground=fg,
        cursor="hand2",
        relief=tk.FLAT,
        bd=0,
        padx=10,
        pady=10,
    )
    hover_color = hover or bg

    def on_enter(_):
        btn.config(bg=hover_color)

    def on_leave(_):
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


class StudentManagementSystem:

  def __init__(self, root):
    self.root = root
    self.root.title("Student Record Management System")

    # Window geometry and main background
    self.root.geometry("1300x750+40+40")
    self.root.config(bg=COLOR_PAGE_BG)

    # --- Database Initialization ---
    self.create_database()

    # --- Variables for Form Inputs ---
    self.roll_var = tk.StringVar()
    self.name_var = tk.StringVar()
    self.email_var = tk.StringVar()
    self.gender_var = tk.StringVar()
    self.contact_var = tk.StringVar()
    self.search_by_var = tk.StringVar()
    self.search_txt_var = tk.StringVar()

    # ==================== TTK STYLING ====================
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=COLOR_WHITE,
        fieldbackground=COLOR_WHITE,
        foreground=COLOR_TEXT_DARK,
        rowheight=30,
        font=("Segoe UI", 10),
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", COLOR_ORANGE)], foreground=[("selected", COLOR_WHITE)])

    style.configure(
        "Treeview.Heading",
        background=COLOR_BLUE_DARK,
        foreground=COLOR_WHITE,
        font=("Segoe UI", 10, "bold"),
        relief=tk.FLAT,
        padding=8,
    )
    style.map("Treeview.Heading", background=[("active", COLOR_BLUE)])

    style.configure(
        "TCombobox",
        fieldbackground=COLOR_WHITE,
        background=COLOR_WHITE,
        foreground=COLOR_TEXT_DARK,
        padding=6,
    )

    # ==================== TITLE BAR (Blue -> Orange gradient feel via two labels) ====================
    header_frame = tk.Frame(self.root, bg=COLOR_BLUE_DARK)
    header_frame.pack(side=tk.TOP, fill=tk.X)

    title_label = tk.Label(
        header_frame,
        text="🎓  STUDENT RECORD MANAGEMENT SYSTEM",
        font=("Segoe UI", 22, "bold"),
        bg=COLOR_BLUE_DARK,
        fg=COLOR_WHITE,
        pady=18,
    )
    title_label.pack(side=tk.LEFT, padx=25)

    accent_strip = tk.Frame(self.root, bg=COLOR_ORANGE, height=6)
    accent_strip.pack(side=tk.TOP, fill=tk.X)

    # ==================== MAIN CONTAINER ====================
    main_frame = tk.Frame(self.root, bg=COLOR_PAGE_BG)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # ---------------- Left Frame: Manage / Form ----------------
    manage_outer = tk.Frame(main_frame, bg=COLOR_BLUE, padx=2, pady=2)
    manage_outer.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

    manage_frame = tk.LabelFrame(
        manage_outer,
        text="  Student Details Form  ",
        font=("Segoe UI", 13, "bold"),
        bg=COLOR_WHITE,
        fg=COLOR_BLUE_DARK,
        bd=0,
        relief=tk.FLAT,
        labelanchor="n",
    )
    manage_frame.pack(fill=tk.BOTH, expand=True, ipady=10)
    manage_frame.config(width=450)

    # Inner form container to keep fields aligned
    form_container = tk.Frame(manage_frame, bg=COLOR_WHITE)
    form_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

    # Form Fields setup, each with its own accent color on the left label
    fields = [
        ("Roll No:", self.roll_var, COLOR_BLUE_DARK),
        ("Name:", self.name_var, COLOR_GREEN_DARK),
        ("Email:", self.email_var, COLOR_PINK_DARK),
        ("Contact:", self.contact_var, COLOR_ORANGE_DARK),
    ]

    for idx, (label_text, var, accent) in enumerate(fields):
      lbl = tk.Label(
          form_container,
          text=label_text,
          font=("Segoe UI", 11, "bold"),
          bg=COLOR_WHITE,
          fg=accent,
          anchor="w",
      )
      lbl.grid(row=idx, column=0, sticky="w", pady=12)

      txt = tk.Entry(
          form_container,
          textvariable=var,
          font=("Segoe UI", 11),
          bd=1,
          relief=tk.SOLID,
          bg=COLOR_WHITE,
          fg=COLOR_TEXT_DARK,
          highlightthickness=1,
          highlightbackground="#e2e8f0",
          highlightcolor=accent,
      )
      txt.grid(row=idx, column=1, sticky="ew", pady=12, padx=(15, 0), ipady=5)

    # Gender Dropdown row
    lbl_gender = tk.Label(
        form_container,
        text="Gender:",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_WHITE,
        fg=COLOR_YELLOW_DARK,
        anchor="w",
    )
    lbl_gender.grid(row=4, column=0, sticky="w", pady=12)

    self.combo_gender = ttk.Combobox(
        form_container,
        textvariable=self.gender_var,
        font=("Segoe UI", 11),
        state="readonly",
    )
    self.combo_gender["values"] = ("Male", "Female", "Other")
    self.combo_gender.grid(
        row=4, column=1, sticky="ew", pady=12, padx=(15, 0), ipady=4
    )

    # Address Field row
    lbl_address = tk.Label(
        form_container,
        text="Address:",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_WHITE,
        fg=COLOR_BLUE_DARK,
        anchor="nw",
    )
    lbl_address.grid(row=5, column=0, sticky="nw", pady=12)

    self.txt_address = tk.Text(
        form_container,
        font=("Segoe UI", 11),
        bd=1,
        relief=tk.SOLID,
        width=20,
        height=4,
        bg=COLOR_WHITE,
        fg=COLOR_TEXT_DARK,
        highlightthickness=1,
        highlightbackground="#e2e8f0",
        highlightcolor=COLOR_BLUE_DARK,
    )
    self.txt_address.grid(row=5, column=1, sticky="ew", pady=12, padx=(15, 0))

    form_container.columnconfigure(1, weight=1)

    # Divider
    tk.Frame(manage_frame, bg="#e2e8f0", height=1).pack(fill=tk.X, padx=20, pady=(0, 5))

    # Button Frame inside Left Panel (Green, Blue, Pink, Yellow)
    btn_frame = tk.Frame(manage_frame, bg=COLOR_WHITE)
    btn_frame.pack(fill=tk.X, padx=20, pady=15)

    make_button(btn_frame, "➕ Add", self.add_student, COLOR_GREEN, hover=COLOR_GREEN_DARK).grid(
        row=0, column=0, padx=4, sticky="ew"
    )
    make_button(btn_frame, "✎ Update", self.update_student, COLOR_BLUE, hover=COLOR_BLUE_DARK).grid(
        row=0, column=1, padx=4, sticky="ew"
    )
    make_button(btn_frame, "🗑 Delete", self.delete_student, COLOR_YELLOW_DARK, hover=COLOR_PINK_DARK).grid(
        row=0, column=2, padx=4, sticky="ew"
    )
    make_button(
        btn_frame, "↺ Clear", self.clear_fields, COLOR_YELLOW, fg=COLOR_TEXT_DARK, hover=COLOR_YELLOW_DARK
    ).grid(row=0, column=3, padx=4, sticky="ew")

    for i in range(4):
      btn_frame.columnconfigure(i, weight=1)

    # ---------------- Right Frame: View & Search Table ----------------
    detail_outer = tk.Frame(main_frame, bg=COLOR_ORANGE, padx=2, pady=2)
    detail_outer.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    detail_frame = tk.LabelFrame(
        detail_outer,
        text="  Student Records Database  ",
        font=("Segoe UI", 13, "bold"),
        bg=COLOR_WHITE,
        fg=COLOR_ORANGE_DARK,
        bd=0,
        relief=tk.FLAT,
        labelanchor="n",
    )
    detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Search Bar Frame
    search_frame = tk.Frame(detail_frame, bg=COLOR_WHITE)
    search_frame.pack(fill=tk.X, padx=20, pady=20)

    tk.Label(
        search_frame,
        text="Search By:",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_WHITE,
        fg=COLOR_TEXT_DARK,
    ).pack(side=tk.LEFT, padx=(0, 8))

    combo_search = ttk.Combobox(
        search_frame,
        textvariable=self.search_by_var,
        font=("Segoe UI", 11),
        state="readonly",
        width=12,
    )
    combo_search["values"] = ("roll", "name", "contact")
    combo_search.pack(side=tk.LEFT, padx=8)
    combo_search.current(0)

    txt_search = tk.Entry(
        search_frame,
        textvariable=self.search_txt_var,
        font=("Segoe UI", 11),
        bd=1,
        relief=tk.SOLID,
        width=18,
        highlightthickness=1,
        highlightbackground="#e2e8f0",
        highlightcolor=COLOR_ORANGE_DARK,
    )
    txt_search.pack(side=tk.LEFT, padx=8, ipady=4)

    make_button(
        search_frame, "🔍 Search", self.search_data, COLOR_ORANGE, hover=COLOR_ORANGE_DARK
    ).pack(side=tk.LEFT, padx=8)

    make_button(
        search_frame, "📋 Show All", self.fetch_data, COLOR_YELLOW, fg=COLOR_TEXT_DARK, hover=COLOR_YELLOW_DARK
    ).pack(side=tk.LEFT, padx=8)

    # Table Frame (Treeview with Scrollbars)
    table_frame = tk.Frame(detail_frame, bg=COLOR_WHITE)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
    scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

    self.student_table = ttk.Treeview(
        table_frame,
        columns=("roll", "name", "email", "gender", "contact", "address"),
        xscrollcommand=scroll_x.set,
        yscrollcommand=scroll_y.set,
    )

    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    scroll_x.config(command=self.student_table.xview)
    scroll_y.config(command=self.student_table.yview)

    self.student_table.heading("roll", text="Roll No")
    self.student_table.heading("name", text="Name")
    self.student_table.heading("email", text="Email")
    self.student_table.heading("gender", text="Gender")
    self.student_table.heading("contact", text="Contact")
    self.student_table.heading("address", text="Address")

    self.student_table["show"] = "headings"

    self.student_table.column("roll", width=90, anchor="w")
    self.student_table.column("name", width=140, anchor="w")
    self.student_table.column("email", width=180, anchor="w")
    self.student_table.column("gender", width=80, anchor="center")
    self.student_table.column("contact", width=120, anchor="w")
    self.student_table.column("address", width=200, anchor="w")

    # Alternating row stripes for readability
    self.student_table.tag_configure("oddrow", background=COLOR_ROW_ALT)
    self.student_table.tag_configure("evenrow", background=COLOR_WHITE)

    self.student_table.pack(fill=tk.BOTH, expand=True)
    self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

    # Load initial data into table
    self.fetch_data()

  # ==================== DATABASE FUNCTIONS ====================
  def create_database(self):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                address TEXT
            )
        """)
    conn.commit()
    conn.close()

  def add_student(self):
    if (
        self.roll_var.get() == ""
        or self.name_var.get() == ""
        or self.contact_var.get() == ""
    ):
      messagebox.showerror(
          "Error", "Roll No, Name, and Contact fields are required!"
      )
      return

    try:
      conn = sqlite3.connect("student_management.db")
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
          (
              self.roll_var.get(),
              self.name_var.get(),
              self.email_var.get(),
              self.gender_var.get(),
              self.contact_var.get(),
              self.txt_address.get("1.0", tk.END).strip(),
          ),
      )
      conn.commit()
      conn.close()
      self.fetch_data()
      self.clear_fields()
      messagebox.showinfo("Success", "Student record added successfully!")
    except sqlite3.IntegrityError:
      messagebox.showerror("Error", "Student with this Roll No already exists!")

  def fetch_data(self):
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    self.student_table.delete(*self.student_table.get_children())
    for i, row in enumerate(rows):
      tag = "evenrow" if i % 2 == 0 else "oddrow"
      self.student_table.insert("", tk.END, values=row, tags=(tag,))
    conn.close()

  def clear_fields(self):
    self.roll_var.set("")
    self.name_var.set("")
    self.email_var.set("")
    self.gender_var.set("")
    self.contact_var.set("")
    self.txt_address.delete("1.0", tk.END)

  def get_cursor(self, event):
    cursor_row = self.student_table.focus()
    contents = self.student_table.item(cursor_row)
    row = contents["values"]
    if row:
      self.roll_var.set(row[0])
      self.name_var.set(row[1])
      self.email_var.set(row[2])
      self.gender_var.set(row[3])
      self.contact_var.set(row[4])
      self.txt_address.delete("1.0", tk.END)
      self.txt_address.insert(tk.END, row[5])

  def update_student(self):
    if self.roll_var.get() == "":
      messagebox.showerror("Error", "Please select a student record to update.")
      return

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute(
        """
            UPDATE students SET name=?, email=?, gender=?, contact=?, address=? WHERE roll=?
        """,
        (
            self.name_var.get(),
            self.email_var.get(),
            self.gender_var.get(),
            self.contact_var.get(),
            self.txt_address.get("1.0", tk.END).strip(),
            self.roll_var.get(),
        ),
    )
    conn.commit()
    conn.close()
    self.fetch_data()
    self.clear_fields()
    messagebox.showinfo("Success", "Student record updated successfully!")

  def delete_student(self):
    if self.roll_var.get() == "":
      messagebox.showerror("Error", "Please select a student record to delete.")
      return

    confirm = messagebox.askyesno(
        "Confirm", "Are you sure you want to delete this record?"
    )
    if confirm:
      conn = sqlite3.connect("student_management.db")
      cursor = conn.cursor()
      cursor.execute("DELETE FROM students WHERE roll=?", (self.roll_var.get(),))
      conn.commit()
      conn.close()
      self.fetch_data()
      self.clear_fields()
      messagebox.showinfo("Success", "Student record deleted successfully!")

  def search_data(self):
    if (
        self.search_txt_var.get() == ""
        or self.search_by_var.get() == ""
    ):
      messagebox.showerror("Error", "Please enter search criteria.")
      return

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM students WHERE {self.search_by_var.get()} LIKE ?"
    cursor.execute(query, ("%" + self.search_txt_var.get() + "%",))
    rows = cursor.fetchall()
    if len(rows) != 0:
      self.student_table.delete(*self.student_table.get_children())
      for i, row in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        self.student_table.insert("", tk.END, values=row, tags=(tag,))
    else:
      messagebox.showinfo("Not Found", "No matching records found.")
    conn.close()


# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
  root = tk.Tk()
  app = StudentManagementSystem(root)
  root.mainloop()