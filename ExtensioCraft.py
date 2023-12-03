import os, shutil, platform, subprocess, tkinter as tk, threading
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# Create a list to store previously browsed directories
previous_directories = []
full_extension_list = {}  # Initialize as a dictionary

# Global variable to store selected extensions
selected_extensions_global = []

# Global variable to store the currently selected extension
current_selected_extension = ""

def generate_unique_file_name(destination_folder, file_name):
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    unique_file_name = file_name
    while os.path.exists(os.path.join(destination_folder, unique_file_name)):
        unique_file_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return unique_file_name

def generate_unique_folder_name(base_path, extension):
    folder_name = f"Copy_{extension}"
    counter = 1
    unique_folder_name = folder_name
    while os.path.exists(os.path.join(base_path, unique_folder_name)):
        unique_folder_name = f"{folder_name}_{counter}"
        counter += 1
    return unique_folder_name

def get_data_file_path(file_name="previous_directories.txt"):
    home = Path.home()
    if platform.system() == "Darwin":  # macOS
        data_dir = home / "Library" / "Application Support" / "YourAppName"
    elif platform.system() == "Windows":  # Windows
        data_dir = home / "AppData" / "Local" / "YourAppName"
    else:  # Linux and other OSes
        data_dir = home / ".your_app_name"  # Hidden directory in home

    data_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
    return data_dir / file_name

# Usage
data_file_path = get_data_file_path()

def save_path_to_file(path, file_name="previous_directories.txt"):
    with open(file_name, "a") as file:
        file.write(path + "\n")

def load_paths_from_file(file_name="previous_directories.txt"):
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r") as file:
        return [line.strip() for line in file if line.strip()]

previous_directories = load_paths_from_file()

def show_progress_bar():
    global progress_window  # Use a global variable to access the window later for closing
    progress_window = tk.Toplevel(window)
    progress_window.title("Loading")
    progress_window.geometry("300x100")  # Adjust the size as needed

    tk.Label(progress_window, text="Please wait...").pack(pady=20)
    progress = ttk.Progressbar(progress_window, orient="horizontal", mode="indeterminate")
    progress.pack(fill=tk.BOTH, expand=True, padx=20)
    progress.start(10)

    # Disable interaction with the main window
    progress_window.grab_set()

def browse_folder():
    global full_extension_list

    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder.set(folder_path)

        # Reset the progress bar
        progress_var.set(0)
        progress_bar["maximum"] = 100

        # Start the folder browsing operation in a new thread to keep the UI responsive
        threading.Thread(target=update_extension_listbox, daemon=True).start()

        # Update the previously browsed directories and save the new path
        if folder_path not in previous_directories:
            previous_directories.append(folder_path)
            folder_combobox['values'] = previous_directories
            save_path_to_file(folder_path)  # Save the new path to the file

    full_extension_list = {}  # Initialize as a dictionary

def reset_progress_bar():
    # Reset the progress bar after the operation is complete
    progress_var.set(0)
def close_progress_window():
    # Close the progress bar window
    progress_window.destroy()

def get_file_extensions(folder):
    extensions = set()
    for root, dirs, files in os.walk(folder):
        for file in files:
            _, ext = os.path.splitext(file)
            extensions.add(ext.lower())  # Add lowercase extension
    return extensions

def filter_extensions(extensions, filter_types):
    # Define all categories
    picture_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.psd', '.raw', '.heif', '.svg', '.webp',
        '.ico', '.dng', '.cr2', '.nef', '.orf', '.sr2', '.arw', '.eps', '.ai'
    }
    video_extensions = {
        '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v', '.mpg', '.mpeg', '.3gp', '.vob',
        '.swf', '.rm', '.webm', '.ogv', '.m2ts', '.ts', '.mxf', '.asf', '.dv', '.qt'
    }
    document_extensions = {
        '.txt', '.docx', '.pdf', '.xlsx', '.pptx', '.odt', '.ods', '.odp', '.rtf', '.csv',
        '.doc', '.xml', '.html', '.htm', '.epub', '.mobi', '.md', '.tex', '.json', '.log', '.msg'
    }
    compression_extensions = {
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tar.gz', '.tar.bz2', '.tar.xz',
        '.tgz', '.zipx', '.iso', '.lz', '.lzma', '.z', '.cab', '.arj', '.ace', '.apk'
    }
    software_extensions = {
        '.exe', '.msi', '.bat', '.sh', '.app', '.dmg', '.jar', '.py', '.pl', '.php', '.rb',
        '.vb', '.vbs', '.js', '.cmd', '.cpl', '.wsf', '.scr', '.deb', '.rpm'
    }

    filtered_extensions = set()
    for filter_type in filter_types:
        if filter_type == 'Pictures':
            filtered_extensions.update([ext for ext in extensions if ext.lower() in picture_extensions])
        elif filter_type == 'Videos':
            filtered_extensions.update([ext for ext in extensions if ext.lower() in video_extensions])
        elif filter_type == 'Document Files':
            filtered_extensions.update([ext for ext in extensions if ext.lower() in document_extensions])
        elif filter_type == 'Compression Files':
            filtered_extensions.update([ext for ext in extensions if ext.lower() in compression_extensions])
        elif filter_type == 'Software Files':
            filtered_extensions.update([ext for ext in extensions if ext.lower() in software_extensions])
        elif filter_type == 'Others':
            all_known_extensions = picture_extensions.union(video_extensions, document_extensions, compression_extensions, software_extensions)
            filtered_extensions.update([ext for ext in extensions if ext.lower() not in all_known_extensions])

    return filtered_extensions

def delete_files_with_extension(folder, extensions, progress_var, file_paths):
    total_files = sum(1 for root, _, files in os.walk(folder) for file in files if os.path.splitext(file)[1].lower() in extensions)

    def delete_files():
        nonlocal file_paths
        progress = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    progress += 1
                    progress_var.set(int(progress / total_files * 100))
                    file_paths.append(file_path)
                    progress_frame.after(10, update_file_paths, file_paths)
                    yield

    delete_gen = delete_files()
    progress_frame.after(10, perform_file_operation, delete_gen)

def copy_files_with_extension(folder, extensions, destination_folder, progress_var, file_paths):
    total_files = sum(1 for root, _, files in os.walk(folder) for file in files if os.path.splitext(file)[1].lower() in extensions)
    progress = 0

    def copy_files():
        nonlocal progress
        for root, dirs, files in os.walk(folder):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in extensions:
                    source_file = os.path.join(root, file)
                    destination_file = os.path.join(destination_folder, file)
                    shutil.copy2(source_file, destination_file)
                    progress += 1
                    progress_var.set(int(progress / total_files * 100))
                    file_paths.append(destination_file)
                    progress_frame.after(10, update_file_paths, file_paths)
                    progress_frame.update()
                    yield

    def advance_generator():
        try:
            next(copy_gen)
            progress_frame.after(10, advance_generator)
        except StopIteration:
            show_copy_complete_message()

    copy_gen = copy_files()
    progress_frame.after(10, advance_generator)


def perform_file_operation(copy_gen):
    pass

def show_copy_complete_message():
    messagebox.showinfo("Copy Complete", "All files with selected extensions have been copied to the destination folder.")

def update_file_paths(file_paths):
    path_listbox.delete(0, tk.END)
    for path in file_paths:
        path_listbox.insert(tk.END, path)

def update_extension_listbox(event=None):
    global full_extension_list
    folder_path = selected_folder.get()

    if folder_path:
        # Check if the full extension list for the folder is already populated
        if not full_extension_list:
            extensions = get_file_extensions(folder_path)
            total_files = sum(1 for _, _, files in os.walk(folder_path) for _ in files)
            processed_files = 0

            # Reset the listboxes and progress bar
            extension_listbox.delete(0, tk.END)
            path_listbox.delete(0, tk.END)
            progress_var.set(0)

            for ext in extensions:
                count = sum(ext.lower() == os.path.splitext(file)[1].lower() for _, _, files in os.walk(folder_path) for file in files)
                processed_files += count
                progress_var.set((processed_files / total_files) * 100)  # Update progress bar
                if count > 0:
                    full_extension_list[ext] = count
                    extension_listbox.insert(tk.END, f"{ext} ({count})")
                    extension_listbox.update()  # Update the listbox in real-time

            # Reset progress bar after completion
            progress_var.set(0)

        # Apply filters if any
        filter_types = [filter_vars[var].get() for var in filter_vars if filter_vars[var].get()]
        if filter_types:
            apply_filters(filter_types)
        else:
            # If no filters are selected, display the full list
            display_full_extension_list()

def apply_filters(filter_types):
    filtered_extensions = filter_extensions(full_extension_list.keys(), filter_types)
    extension_listbox.delete(0, tk.END)
    for ext in filtered_extensions:
        count = full_extension_list.get(ext, 0)
        if count > 0:
            extension_listbox.insert(tk.END, f"{ext} ({count})")
def display_full_extension_list():
    extension_listbox.delete(0, tk.END)
    for ext, count in full_extension_list.items():
        if count > 0:
            extension_listbox.insert(tk.END, f"{ext} ({count})")

def browse_specific_extension(event=None):
    specific_extension = specific_extension_entry.get()
    if specific_extension:
        folder_path = selected_folder.get()
        extensions = get_file_extensions(folder_path)
        # Filter extensions that start with the specified partial string
        filtered_extensions = [ext for ext in extensions if ext.lower().startswith(specific_extension.lower())]
        extension_listbox.delete(0, tk.END)
        for ext in filtered_extensions:
            extension_listbox.insert(tk.END, ext)
    else:
        update_extension_listbox()

def refresh_script():
    global full_extension_list
    folder_path = selected_folder.get()
    if folder_path:
        update_extension_listbox()
    full_extension_list = {}  # Initialize as a dictionary

def show_file_paths(event):
    global current_selected_extension
    selected_indices = extension_listbox.curselection()
    if selected_indices:
        current_selected_extension = extension_listbox.get(selected_indices[0]).split(" ")[0].lower()
        folder_path = selected_folder.get()
        path_listbox.delete(0, tk.END)  # Clear existing items
        displayed_dirs = set()
        for root, _, files in os.walk(folder_path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() == current_selected_extension and root not in displayed_dirs:
                    path_listbox.insert(tk.END, root)
                    displayed_dirs.add(root)

def open_file_in_explorer(file_path):
    system = platform.system()

    if system == "Darwin":  # macOS
        # Ensure the path is absolute and properly formatted
        absolute_path = os.path.abspath(file_path)
        subprocess.run(["open", "-R", absolute_path])
    elif system == "Windows":  # Windows
        subprocess.run(["explorer", "/select,", file_path])
    elif system == "Linux":  # Linux
        # Open the folder as Linux doesn't have a universal command for highlighting files
        folder_path = os.path.dirname(file_path)
        subprocess.run(["xdg-open", folder_path])

def delete_selected_extensions():
    global current_selected_extension
    selected_directories = [path_listbox.get(idx) for idx in path_listbox.curselection()]

    if not current_selected_extension:
        messagebox.showinfo("No Extension Selected", "Please select an extension first.")
        return

    if not selected_directories:
        messagebox.showinfo("No Folder Selected", "Please select at least one folder.")
        return

    if messagebox.askyesno("Confirmation", "Are you sure you want to delete all files with the selected extension in the selected folders?"):
        total_deleted = 0
        for directory in selected_directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    _, ext = os.path.splitext(file)
                    if ext.lower() == current_selected_extension:
                        try:
                            os.remove(os.path.join(root, file))
                            total_deleted += 1
                        except Exception as e:
                            print(f"Error deleting file {file}: {e}")
        messagebox.showinfo("Deletion Complete", f"All files with the selected extension have been deleted. Total files deleted: {total_deleted}.")

def copy_selected_extensions():
    global current_selected_extension
    selected_directories = [path_listbox.get(idx) for idx in path_listbox.curselection()]
    base_destination_folder = filedialog.askdirectory()

    if not current_selected_extension:
        messagebox.showinfo("No Extension Selected", "Please select an extension first.")
        return

    if not selected_directories:
        messagebox.showinfo("No Folder Selected", "Please select at least one folder.")
        return

    if not base_destination_folder:
        messagebox.showinfo("No Destination Selected", "Please select a destination folder.")
        return

    destination_folder = os.path.join(base_destination_folder, generate_unique_folder_name(base_destination_folder, current_selected_extension.strip('.')))
    os.makedirs(destination_folder, exist_ok=True)

    total_files_copied = 0
    for directory in selected_directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() == current_selected_extension:
                    source_file = os.path.join(root, file)
                    unique_file_name = generate_unique_file_name(destination_folder, os.path.basename(file))
                    destination_file = os.path.join(destination_folder, unique_file_name)
                    try:
                        shutil.copy2(source_file, destination_file)
                        total_files_copied += 1
                    except Exception as e:
                        print(f"Error copying file {file}: {e}")

    messagebox.showinfo("Copy Complete", f"All files with the selected extension have been copied to '{destination_folder}'. Total files copied: {total_files_copied}.")

def on_combobox_select(event):
    global full_extension_list
    folder_path = folder_combobox.get()

    if folder_path:
        selected_folder.set(folder_path)
        full_extension_list = {}  # Initialize as a dictionary
        progress_var.set(0)
        progress_bar["maximum"] = 100

        # Start the update in a new thread to keep the UI responsive
        threading.Thread(target=update_extension_listbox, daemon=True).start()

def open_folders_of_selected_files():
    selected_indices = path_listbox.curselection()

    for idx in selected_indices:
        file_path = path_listbox.get(idx)
        open_file_in_explorer(file_path)

def open_folder_in_explorer(folder_path):
    system = platform.system()

    if system == "Darwin":  # macOS
        subprocess.run(["open", folder_path])
    elif system == "Windows":  # Windows
        subprocess.run(["explorer", folder_path])
    elif system == "Linux":  # Linux
        subprocess.run(["xdg-open", folder_path])


# Create the main window
window = tk.Tk()
window.title("ExtensioCraft")
window.geometry('700x450')
window.resizable(False, False)

# Create a frame for the folder selection
folder_frame = tk.Frame(window)
folder_frame.pack(pady=10)

selected_folder = tk.StringVar()

folder_label = tk.Label(folder_frame, text="Select Folder:")
folder_label.pack(side=tk.LEFT)

folder_combobox = ttk.Combobox(folder_frame, textvariable=selected_folder, width=40)
folder_combobox.pack(side=tk.LEFT, padx=10)
folder_combobox['values'] = previous_directories
folder_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

refresh_button = tk.Button(folder_frame, text="Refresh", command=refresh_script)
refresh_button.pack(side=tk.LEFT)

# Create a frame for the progress bar
progress_frame = tk.Frame(window)
progress_frame.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.BOTH, expand=True)

# Create a frame for the filter checkboxes
filter_frame = tk.Frame(window)
filter_frame.pack(pady=10)

filter_vars = {
    'Pictures': tk.StringVar(),
    'Videos': tk.StringVar(),
    'Document Files': tk.StringVar(),
    'Compression Files': tk.StringVar(),
    'Software Files': tk.StringVar(),
    'Others': tk.StringVar(),
}

pictures_checkbox = tk.Checkbutton(filter_frame, text="Pictures", variable=filter_vars['Pictures'], onvalue="Pictures", offvalue="", command=update_extension_listbox)
pictures_checkbox.pack(side=tk.LEFT)

videos_checkbox = tk.Checkbutton(filter_frame, text="Videos", variable=filter_vars['Videos'], onvalue="Videos", offvalue="", command=update_extension_listbox)
videos_checkbox.pack(side=tk.LEFT)

document_files_checkbox = tk.Checkbutton(filter_frame, text="Document Files", variable=filter_vars['Document Files'], onvalue="Document Files", offvalue="", command=update_extension_listbox)
document_files_checkbox.pack(side=tk.LEFT)

compression_files_checkbox = tk.Checkbutton(filter_frame, text="Compression Files", variable=filter_vars['Compression Files'], onvalue="Compression Files", offvalue="", command=update_extension_listbox)
compression_files_checkbox.pack(side=tk.LEFT)

software_files_checkbox = tk.Checkbutton(filter_frame, text="Software Files", variable=filter_vars['Software Files'], onvalue="Software Files", offvalue="", command=update_extension_listbox)
software_files_checkbox.pack(side=tk.LEFT)

others_checkbox = tk.Checkbutton(filter_frame, text="Others", variable=filter_vars['Others'], onvalue="Others", offvalue="", command=update_extension_listbox)
others_checkbox.pack(side=tk.LEFT)

# Create a frame for the specific extension entry
specific_extension_frame = tk.Frame(window)
specific_extension_frame.pack(pady=10)

specific_extension_label = tk.Label(specific_extension_frame, text="Specific Extension:")
specific_extension_label.pack(side=tk.LEFT)

specific_extension_entry = tk.Entry(specific_extension_frame, width=10)
specific_extension_entry.bind("<Return>", browse_specific_extension)
specific_extension_entry.pack(side=tk.LEFT)

browse_specific_button = tk.Button(specific_extension_frame, text="Browse", command=browse_specific_extension)
browse_specific_button.pack(side=tk.LEFT)

# Create a frame for the extension listboxes
extension_frame = tk.Frame(window)
extension_frame.pack(pady=10)

extension_listbox = tk.Listbox(extension_frame, width=20, height=10, selectmode="extended")
extension_listbox.pack(side=tk.LEFT)

path_listbox = tk.Listbox(extension_frame, width=40, height=10, selectmode="extended")
path_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Bind selection event to show file paths
extension_listbox.bind("<<ListboxSelect>>", show_file_paths)

# Create a frame for the action buttons
action_frame = tk.Frame(window)
action_frame.pack(pady=10)

delete_button = tk.Button(action_frame, text="Delete Selected Extensions", command=delete_selected_extensions)
delete_button.pack(side=tk.LEFT, padx=5, pady=10)

copy_button = tk.Button(action_frame, text="Copy Selected Extensions", command=copy_selected_extensions)
copy_button.pack(side=tk.LEFT, padx=5, pady=10)

go_to_folder_button = tk.Button(action_frame, text="Go to Folder", command=open_folders_of_selected_files)
go_to_folder_button.pack(side=tk.LEFT, padx=5, pady=10)

# Add a list to store the copied or deleted file paths
file_paths = []

window.mainloop()
