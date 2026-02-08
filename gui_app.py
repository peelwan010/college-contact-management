import tkinter as tk
from tkinter import ttk, messagebox

from loaders import (
    load_aktu_roll_list,
    get_second_year_sheets,
    load_second_year_students,
    load_first_year_contacts
)

# ---------------- Window ----------------

root = tk.Tk()
root.title("College Contact Management System")
root.geometry("1200x650")

# ---------------- Style ----------------

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    rowheight=30,
    borderwidth=1,
    relief="solid"
)

style.configure(
    "Treeview.Heading",
    anchor="center",
    borderwidth=1,
    relief="solid"
)

# ---------------- Global State ----------------

current_df = None
original_df = None
current_mode = None   # "aktu", "second_year", "first_year"

# ---------------- Table ----------------

table = ttk.Treeview(root, show="headings")
table.pack(fill=tk.BOTH, expand=True)

def show_dataframe(df):
    global current_df, original_df
    current_df = df.copy()
    original_df = df.copy()

    table.delete(*table.get_children())
    table["columns"] = list(df.columns)

    for col in df.columns:
        table.heading(col, text=col, anchor="center")
        table.column(col, width=150, anchor="center")

    for _, row in df.iterrows():
        table.insert("", tk.END, values=list(row))

# ---------------- Controls ----------------

controls = tk.Frame(root)
controls.pack(fill=tk.X, pady=8)

# ---------------- Utility ----------------

def clear_dynamic_controls():
    search_frame.pack_forget()
    filter_frame.pack_forget()
    sort_frame.pack_forget()

def reset_view():
    if original_df is not None:
        show_dataframe(original_df)

# ---------------- SEARCH (ALL DATASETS) ----------------

search_frame = tk.Frame(controls)

search_var = tk.StringVar()

tk.Entry(
    search_frame,
    textvariable=search_var,
    width=20
).pack(side=tk.LEFT, padx=5)

def apply_search():
    if current_df is None:
        return

    keyword = search_var.get().strip().lower()
    if not keyword:
        show_dataframe(original_df)
        return

    filtered = current_df[
        current_df.astype(str)
        .apply(lambda r: r.str.lower().str.contains(keyword).any(), axis=1)
    ]

    show_dataframe(filtered)

tk.Button(
    search_frame,
    text="Search",
    command=apply_search
).pack(side=tk.LEFT, padx=5)

# ---------------- Load AKTU ----------------

def load_aktu():
    global current_mode
    clear_dynamic_controls()
    current_mode = "aktu"

    show_dataframe(load_aktu_roll_list())

    search_frame.pack(side=tk.LEFT, padx=10)
    sort_frame.pack(side=tk.LEFT, padx=10)

tk.Button(
    controls,
    text="AKTU Roll List",
    command=load_aktu
).pack(side=tk.LEFT, padx=5)

# ---------------- Load First Year ----------------

def load_first_year():
    global current_mode
    clear_dynamic_controls()
    current_mode = "first_year"

    df = load_first_year_contacts()
    show_dataframe(df)

    # Admission Category filter
    categories = sorted(df["admission_category"].dropna().unique().tolist())
    filter_value_box["values"] = categories
    filter_value_box.set("Select Category")

    search_frame.pack(side=tk.LEFT, padx=10)
    filter_frame.pack(side=tk.LEFT, padx=10)
    sort_frame.pack(side=tk.LEFT, padx=10)

tk.Button(
    controls,
    text="First Year Contacts",
    command=load_first_year
).pack(side=tk.LEFT, padx=5)

# ---------------- Second Year ----------------

sheet_var = tk.StringVar()

sheet_box = ttk.Combobox(
    controls,
    textvariable=sheet_var,
    values=get_second_year_sheets(),
    state="readonly",
    width=18
)
sheet_box.set("Select Section")
sheet_box.pack(side=tk.LEFT, padx=5)

def load_second_year():
    global current_mode
    if sheet_var.get() == "Select Section":
        messagebox.showerror("Error", "Select a section")
        return

    clear_dynamic_controls()
    current_mode = "second_year"

    show_dataframe(load_second_year_students(sheet_var.get()))

    search_frame.pack(side=tk.LEFT, padx=10)
    sort_frame.pack(side=tk.LEFT, padx=10)

tk.Button(
    controls,
    text="Load Second Year",
    command=load_second_year
).pack(side=tk.LEFT, padx=5)

# ---------------- FILTER (First Year ONLY) ----------------

filter_frame = tk.Frame(controls)

filter_value_var = tk.StringVar()

filter_value_box = ttk.Combobox(
    filter_frame,
    textvariable=filter_value_var,
    state="readonly",
    width=18
)
filter_value_box.pack(side=tk.LEFT, padx=5)

def apply_filter():
    if current_mode != "first_year":
        return

    val = filter_value_var.get()
    if not val or val == "Select Category":
        messagebox.showerror("Error", "Select admission category")
        return

    filtered = original_df[
        original_df["admission_category"].astype(str) == val
    ]
    show_dataframe(filtered)

tk.Button(
    filter_frame,
    text="Filter",
    command=apply_filter
).pack(side=tk.LEFT, padx=5)

# ---------------- SORT (ALL DATASETS – Name ONLY) ----------------

sort_frame = tk.Frame(controls)

sort_order_var = tk.StringVar(value="Ascending")

sort_order_box = ttk.Combobox(
    sort_frame,
    textvariable=sort_order_var,
    values=["Ascending", "Descending"],
    state="readonly",
    width=12
)
sort_order_box.pack(side=tk.LEFT, padx=5)

def apply_sort():
    if current_df is None:
        return

    if "student_name" not in current_df.columns:
        messagebox.showerror("Error", "Name column not available")
        return

    ascending = sort_order_var.get() == "Ascending"
    sorted_df = current_df.sort_values(
        by="student_name",
        ascending=ascending
    )
    show_dataframe(sorted_df)

tk.Button(
    sort_frame,
    text="Sort by Name",
    command=apply_sort
).pack(side=tk.LEFT, padx=5)

# ---------------- Reset ----------------

tk.Button(
    controls,
    text="Reset",
    command=reset_view
).pack(side=tk.LEFT, padx=10)

# ---------------- Start ----------------

root.mainloop()
