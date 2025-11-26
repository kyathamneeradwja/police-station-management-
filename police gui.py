from pymongo import MongoClient
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox, Listbox,filedialog
from tkcalendar import DateEntry
def add_rounded_corners(image_path, radius):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    rounded_mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(rounded_mask)
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
    image.putalpha(rounded_mask)
    return image

def only_numbers(char):
    return char.isdigit()

client = MongoClient("mongodb://localhost:27017/")
db = client["admin"]
collection = db["users"]

# Prevent image garbage collection
bg_images = {}
def upload_photo(file_path_var):
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        # Optional: Validate file extension
        if file_path.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            file_path_var.set(file_path)  # show full path in the text box
        else:
            messagebox.showwarning("Unsupported File", "Please select a valid PDF or image.")
def upload_video(file_path_var2):
    file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("Videos", "*.mp4")]
    )
    if file_path:
        # Optional: Validate file extension
        if file_path.lower().endswith(('.mp4')):
            file_path_var2.set(file_path)  # show full path in the text box
        else:
            messagebox.showwarning("Unsupported File", "Please select a valid PDF or image.")

def tile_background(canvas, img, width, height):
    """Tiles a PhotoImage on a Canvas with alternating blank images."""
    tile_width = img.width()
    tile_height = img.height()

    # Create a blank image of same size (transparent or white)
    blank = Image.new("RGBA", (tile_width, tile_height), (255, 255, 255, 0))  # Transparent
    blank_tk = ImageTk.PhotoImage(blank)

    # Keep references to avoid garbage collection
    bg_images["tile"] = img
    bg_images["blank"] = blank_tk

    for x in range(0, width, tile_width):
        for y in range(0, height, tile_height):
            tile_x = x // tile_width
            tile_y = y // tile_height
            if (tile_x + tile_y) % 2 == 0:
                canvas.create_image(x, y, image=img, anchor="nw")
            else:
                canvas.create_image(x, y, image=blank_tk, anchor="nw")

def save_fir(d_e1, d_e2, d_e3, d_e4,d_e5,d_e6,d_e7,date_entry, time_entry, date_entry2, time_entry2,file_path_var, file_path_var2):
    data={  "petitioner_name": d_e1.get(),
            "contact":d_e2.get(),
            "email":d_e3.get(),
            "address":d_e4.get(),
            "case_id": d_e5.get(),
            "case_description": d_e6.get("1.0", "end-1c"),
            "date_of_action": date_entry.get(),
            "time_of_action": time_entry.get(),
            "date_of_petition": date_entry2.get(),
            "time_of_petition": time_entry2.get(),
            "proof_items": d_e7.get(),
            "photo_path": file_path_var.get(),
            "video_path": file_path_var2.get()}
    collection.insert_one(data)
    messagebox.showinfo("Success", "FIR saved successfully!")
def civil():
            form_frame = tk.Frame(canvas, bg="white")
            canvas.create_window(600, 400, window=form_frame)

            button_frame = tk.Frame(form_frame, bg="white")
            button_frame.grid(row=0, column=0, columnspan=2, pady=10)

            tk.Button(button_frame, text="Crime", width=15).pack(side="left", padx=10)
            tk.Button(button_frame, text="Civil", width=15,command=civil()).pack(side="left", padx=10)

            tk.Label(form_frame, text='PETITIONER NAME', bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=5)
            d_e1 = tk.Entry(form_frame, width=50)
            d_e1.grid(row=1, column=1, padx=10, pady=5)
            gender_var = tk.StringVar(value="")  # holds selected gender
            # Gender Label
            gender_frame = tk.Frame(form_frame, bg="white")
            gender_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
            tk.Label(gender_frame, text='GENDER:', bg="white").pack(side="left",padx=2)
            # Male Radiobutton
            tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg="white").pack(side="left", padx=2)

            # Female Radiobutton
            tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg="white").pack(side="left", padx=2)

            # Other Radiobutton
            tk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other", bg="white").pack(side="left", padx=2)

            tk.Label(form_frame, text='CONTACT', bg="white").grid(row=3, column=0, sticky="e", padx=10, pady=5)
            d_e2 = tk.Entry(form_frame, width=50)
            d_e2.grid(row=3, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='EMAIL', bg="white").grid(row=4, column=0, sticky="e", padx=10, pady=5)
            d_e3 = tk.Entry(form_frame, width=50)
            d_e3.grid(row=4, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='ADDRESS', bg="white").grid(row=5, column=0, sticky="e", padx=10, pady=5)
            d_e4 = tk.Entry(form_frame, width=50)
            d_e4.grid(row=5, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='CASE ID', bg="white").grid(row=6, column=0, sticky="e", padx=10, pady=5)
            vcmd = root.register(only_numbers)
            d_e5 = tk.Entry(form_frame, width=50, validate="key", validatecommand=(vcmd, "%S"))
            d_e5.grid(row=6, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='CASE Id', bg="white").grid(row=7, column=0, sticky="e", padx=10, pady=5)
            vcmd = root.register(only_numbers)
            d_e6 = tk.Text(form_frame, width=60, height=10, font=("Arial", 12))
            d_e6.grid(row=7, column=1, padx=10, pady=5)
            # Main Label
            tk.Label(form_frame, text='DATE OF ACTION', bg="white").grid(row=8, column=0, sticky="e", padx=10, pady=5)

            # Frame for date + time
            datetime_frame = tk.Frame(form_frame, bg="white")
            datetime_frame.grid(row=8, column=1, sticky="w", padx=0, pady=5)

            # Date Entry
            date_entry = DateEntry(datetime_frame, width=16, background='darkblue',
                                   foreground='white', borderwidth=2, year=2025)
            date_entry.grid(row=0, column=0, padx=(0, 5))

            # Label for Time
            tk.Label(datetime_frame, text='TIME OF ACTION', bg="white").grid(row=0, column=1, sticky="e", padx=(100, 5))

            # Time Entry
            time_entry = tk.Entry(datetime_frame, width=10)
            time_entry.grid(row=0, column=2, padx=(5, 0))
            tk.Label(form_frame, text='DATE  OF PETITION', bg="white").grid(row=9, column=0, sticky="e", padx=10, pady=5)

            # Frame for date + time
            datetime_frame2 = tk.Frame(form_frame, bg="white")
            datetime_frame2.grid(row=9, column=1, sticky="w", padx=0, pady=5)

            # Date Entry
            date_entry2 = DateEntry(datetime_frame2, width=16, background='darkblue',
                                   foreground='white', borderwidth=2, year=2025)
            date_entry2.grid(row=0, column=0, padx=(0, 5))

            # Label for Time
            tk.Label(datetime_frame2, text='TIME OF PETITION', bg="white").grid(row=0, column=1, sticky="e", padx=(100, 5))

            # Time Entry
            time_entry2 = tk.Entry(datetime_frame2, width=10)
            time_entry2.grid(row=0, column=2, padx=(5, 0))
            separator = tk.Frame(form_frame, bg="black", height=2, bd=0)
            separator.grid(row=10, column=0, columnspan=4, sticky="we", pady=10)

            tk.Label(form_frame, text="PROOFS", bg="white", font=("Arial", 14, "bold")).grid(row=11, column=0, columnspan=4, padx=10, pady=5, sticky="n")
            tk.Label(form_frame, text='LIST OF ITEMS COLLECTED AS PROOF', bg="white").grid(row=12, column=0, sticky="e", padx=10, pady=5)
            d_e7 = tk.Entry(form_frame, width=50)
            d_e7.grid(row=12, column=1, padx=10, pady=5)
            file_path_var = tk.StringVar()
            tk.Label(form_frame, text='photos', bg="white").grid(row=13, column=0, sticky="e", padx=10, pady=5)
            # Entry to show selected file path
            file_path_var=tk.StringVar()
            file_entry = tk.Entry(form_frame, textvariable=file_path_var, width=50)
            file_entry.grid(row=13, column=1, padx=(0, 5), pady=5)

            # Upload button on the right
            upload_btn = tk.Button(form_frame, text="Upload File", command=lambda:upload_photo(file_path_var))
            upload_btn.grid(row=13, column=2, pady=5)
            file_path_var2=tk.StringVar()
            tk.Label(form_frame, text='videos', bg="white").grid(row=14, column=0, sticky="e", padx=10, pady=5)
            # Entry to show selected file path
            file_entry = tk.Entry(form_frame, textvariable=file_path_var2, width=50)
            file_entry.grid(row=14, column=1, padx=(0, 5), pady=5)

            # Upload button on the right
            upload_btn = tk.Button(form_frame, text="Upload File", command=lambda:upload_video(file_path_var2))
            upload_btn.grid(row=14, column=2, pady=5)
            submit_btn = tk.Button(form_frame, text="Submit", command=lambda:save_fir(d_e1, d_e2, d_e3,d_e4,d_e5,d_e6,d_e7, date_entry, time_entry, date_entry2, time_entry2, file_path_var, file_path_var2))
            submit_btn.grid(row=15, column=1, pady=5)

def open_dashboard(user_name):
    dashboard = tk.Toplevel()
    dashboard.geometry("800x600")
    dashboard.title(f"Dashboard - {user_name}")

    lb = Listbox(dashboard, width=40, height=25, font=("Arial", 10))
    lb.insert(1, 'file an fir')
    lb.insert(2, 'close the case')
    lb.insert(3, 'pending cases')
    lb.insert(4, 'solved cases')
    lb.pack(side="left", fill="y")

    canvas = tk.Canvas(dashboard, width=800, height=600)
    canvas.pack(side="right", expand=True, fill="both")

    tile_image = Image.open("telangana_police.jpg").resize((100, 100), Image.Resampling.LANCZOS)
    tile_tk = ImageTk.PhotoImage(tile_image)
    bg_images[canvas] = tile_tk  # prevent garbage collection
    tile_background(canvas, tile_tk, 2000, 5000)

    
    def on_item_select(event):
        selected_index = lb.curselection()
        if not selected_index:
            return
        option = lb.get(selected_index)

        if option == "file an fir":
            form_frame = tk.Frame(canvas, bg="white")
            canvas.create_window(600, 400, window=form_frame)

            button_frame = tk.Frame(form_frame, bg="white")
            button_frame.grid(row=0, column=0, columnspan=2, pady=10)

            tk.Button(button_frame, text="Crime", width=15).pack(side="left", padx=10)
            tk.Button(button_frame, text="Civil", width=15,command=civil()).pack(side="left", padx=10)

            tk.Label(form_frame, text='PETITIONER NAME', bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=5)
            d_e1 = tk.Entry(form_frame, width=50)
            d_e1.grid(row=1, column=1, padx=10, pady=5)
            gender_var = tk.StringVar(value="")  # holds selected gender
            # Gender Label
            gender_frame = tk.Frame(form_frame, bg="white")
            gender_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
            tk.Label(gender_frame, text='GENDER:', bg="white").pack(side="left",padx=2)
            # Male Radiobutton
            tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg="white").pack(side="left", padx=2)

            # Female Radiobutton
            tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg="white").pack(side="left", padx=2)

            # Other Radiobutton
            tk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other", bg="white").pack(side="left", padx=2)

            tk.Label(form_frame, text='CONTACT', bg="white").grid(row=3, column=0, sticky="e", padx=10, pady=5)
            d_e2 = tk.Entry(form_frame, width=50)
            d_e2.grid(row=3, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='EMAIL', bg="white").grid(row=4, column=0, sticky="e", padx=10, pady=5)
            d_e3 = tk.Entry(form_frame, width=50)
            d_e3.grid(row=4, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='ADDRESS', bg="white").grid(row=5, column=0, sticky="e", padx=10, pady=5)
            d_e4 = tk.Entry(form_frame, width=50)
            d_e4.grid(row=5, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='CASE ID', bg="white").grid(row=6, column=0, sticky="e", padx=10, pady=5)
            vcmd = root.register(only_numbers)
            d_e5 = tk.Entry(form_frame, width=50, validate="key", validatecommand=(vcmd, "%S"))
            d_e5.grid(row=6, column=1, padx=10, pady=5)
            tk.Label(form_frame, text='CASE DESCRIPTION', bg="white").grid(row=7, column=0, sticky="e", padx=10, pady=5)
            vcmd = root.register(only_numbers)
            d_e6 = tk.Text(form_frame, width=60, height=10, font=("Arial", 12))
            d_e6.grid(row=7, column=1, padx=10, pady=5)
            # Main Label
            tk.Label(form_frame, text='DATE OF ACTION', bg="white").grid(row=8, column=0, sticky="e", padx=10, pady=5)

            # Frame for date + time
            datetime_frame = tk.Frame(form_frame, bg="white")
            datetime_frame.grid(row=8, column=1, sticky="w", padx=0, pady=5)

            # Date Entry
            date_entry = DateEntry(datetime_frame, width=16, background='darkblue',
                                   foreground='white', borderwidth=2, year=2025)
            date_entry.grid(row=0, column=0, padx=(0, 5))

            # Label for Time
            tk.Label(datetime_frame, text='TIME OF ACTION', bg="white").grid(row=0, column=1, sticky="e", padx=(100, 5))

            # Time Entry
            time_entry = tk.Entry(datetime_frame, width=10)
            time_entry.grid(row=0, column=2, padx=(5, 0))
            tk.Label(form_frame, text='DATE  OF PETITION', bg="white").grid(row=9, column=0, sticky="e", padx=10, pady=5)

            # Frame for date + time
            datetime_frame2 = tk.Frame(form_frame, bg="white")
            datetime_frame2.grid(row=9, column=1, sticky="w", padx=0, pady=5)

            # Date Entry
            date_entry2 = DateEntry(datetime_frame2, width=16, background='darkblue',
                                   foreground='white', borderwidth=2, year=2025)
            date_entry2.grid(row=0, column=0, padx=(0, 5))

            # Label for Time
            tk.Label(datetime_frame2, text='TIME OF PETITION', bg="white").grid(row=0, column=1, sticky="e", padx=(100, 5))

            # Time Entry
            time_entry2 = tk.Entry(datetime_frame2, width=10)
            time_entry2.grid(row=0, column=2, padx=(5, 0))
            separator = tk.Frame(form_frame, bg="black", height=2, bd=0)
            separator.grid(row=10, column=0, columnspan=4, sticky="we", pady=10)

            tk.Label(form_frame, text="PROOFS", bg="white", font=("Arial", 14, "bold")).grid(row=11, column=0, columnspan=4, padx=10, pady=5, sticky="n")
            tk.Label(form_frame, text='LIST OF ITEMS COLLECTED AS PROOF', bg="white").grid(row=12, column=0, sticky="e", padx=10, pady=5)
            d_e7 = tk.Entry(form_frame, width=50)
            d_e7.grid(row=12, column=1, padx=10, pady=5)
            file_path_var = tk.StringVar()
            tk.Label(form_frame, text='photos', bg="white").grid(row=13, column=0, sticky="e", padx=10, pady=5)
            # Entry to show selected file path
            file_path_var=tk.StringVar()
            file_entry = tk.Entry(form_frame, textvariable=file_path_var, width=50)
            file_entry.grid(row=13, column=1, padx=(0, 5), pady=5)

            # Upload button on the right
            upload_btn = tk.Button(form_frame, text="Upload File", command=lambda:upload_photo(file_path_var))
            upload_btn.grid(row=13, column=2, pady=5)
            file_path_var2=tk.StringVar()
            tk.Label(form_frame, text='videos', bg="white").grid(row=14, column=0, sticky="e", padx=10, pady=5)
            # Entry to show selected file path
            file_entry = tk.Entry(form_frame, textvariable=file_path_var2, width=50)
            file_entry.grid(row=14, column=1, padx=(0, 5), pady=5)

            # Upload button on the right
            upload_btn = tk.Button(form_frame, text="Upload File", command=lambda:upload_video(file_path_var2))
            upload_btn.grid(row=14, column=2, pady=5)
            submit_btn = tk.Button(form_frame, text="Submit", command=lambda:save_fir(d_e1, d_e2, d_e3,d_e4,d_e5,d_e6,d_e7, date_entry, time_entry, date_entry2, time_entry2, file_path_var, file_path_var2))
            submit_btn.grid(row=15, column=1, pady=5)
        elif option == "close the case":
                form_frame = tk.Frame(canvas, bg="white")
                canvas.create_window(400, 300, window=form_frame)

                button_frame = tk.Frame(form_frame, bg="white")
                button_frame.grid(row=0, column=0, columnspan=2, pady=10)

                tk.Button(button_frame, text="Crime", width=15).pack(side="left", padx=10)
                tk.Button(button_frame, text="Civil", width=15).pack(side="left", padx=10)

                tk.Label(form_frame, text='NAME', bg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)
                d_e1 = tk.Entry(form_frame, width=50)
                d_e1.grid(row=1, column=1, padx=10, pady=5)

                tk.Label(form_frame, text='ID', bg="white").grid(row=2, column=0, sticky="e", padx=10, pady=5)
                vcmd = root.register(only_numbers)
                d_e2 = tk.Entry(form_frame, width=50, validate="key", validatecommand=(vcmd, "%S"))
                d_e2.grid(row=2, column=1, padx=10, pady=5)

    lb.bind("<<ListboxSelect>>", on_item_select)

def verify_user():
    user_id = e2.get().strip()
    user_name = e1.get().strip()
    user = collection.find_one({"id": user_id, "name": user_name})
    if user:
        messagebox.showinfo("Success", "Login Successful")
        root.withdraw()
        open_dashboard(user_name)
    else:
        messagebox.showerror("Error", "Invalid Name or ID")

# --- Main Login Window ---
root = tk.Tk()
root.geometry("800x600")
root.title("TELANGANA POLICE DEPARTMENT")
icon=tk.PhotoImage(file='telangana_police_logo.png')
root.iconphoto(True,icon)
header = tk.Frame(root, bg="steelblue", height=110)
header.pack(fill="x")
header_label = tk.Label(header, text="TELANGANA POLICE DEPARTMENT", bg="steelblue", fg="white", font=("Arial", 16, "bold"))
header_label.pack(pady=50)

# Profile Image with Rounded Corners
rounded_img = add_rounded_corners("telangana_police_logo.png", radius=10000)
rounded_img = rounded_img.resize((100, 100), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(rounded_img)

label = tk.Label(root, image=photo, bg="steelblue")
label.place(x=0, y=0)

# Login Form (centered)
border_frame = tk.Frame(root, bg="red", padx=2, pady=2)
border_frame.place(relx=0.5, rely=0.5, anchor="center")

form_frame = tk.Frame(border_frame, bg="white")
form_frame.pack()

tk.Label(form_frame, text='NAME', bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
tk.Label(form_frame, text='ID', bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)

e1 = tk.Entry(form_frame, width=30)
vcmd = root.register(only_numbers)
e2 = tk.Entry(form_frame, width=30, validate="key", validatecommand=(vcmd, "%S"))

e1.grid(row=0, column=1, padx=10, pady=5)
e2.grid(row=1, column=1, padx=10, pady=5)

tk.Button(form_frame, text='LOG IN', width=25, command=verify_user).grid(columnspan=2, pady=10)

root.mainloop()
