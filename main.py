
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import customtkinter as ctk

from university_api import search_universities


# --------------------------------------------------
# APPLICATION THEME
# --------------------------------------------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class UniFinderApp:

    def __init__(self, root):
        self.root = root

        self.root.title("UniFinder | University Search")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(fg_color="#F4F7FB")

        self.create_interface()

    # --------------------------------------------------
    # MAIN INTERFACE
    # --------------------------------------------------

    def create_interface(self):

        # Header
        header = ctk.CTkFrame(
            self.root,
            fg_color="#14213D",
            corner_radius=0,
            height=130
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="UniFinder",
            font=("Arial", 32, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            header,
            text="Discover universities around the world",
            font=("Arial", 15),
            text_color="#DCE6F5"
        ).pack()

        # Main content container
        content = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=30
        )

        # Search card
        search_card = ctk.CTkFrame(
            content,
            fg_color="#FFFFFF",
            corner_radius=18,
            border_width=1,
            border_color="#E2E8F0"
        )
        search_card.pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(
            search_card,
            text="Find Your University",
            font=("Arial", 22, "bold"),
            text_color="#14213D"
        ).pack(anchor="w", padx=25, pady=(22, 15))

        # Input fields
        input_frame = ctk.CTkFrame(
            search_card,
            fg_color="transparent"
        )
        input_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)

        # University name
        name_frame = ctk.CTkFrame(
            input_frame,
            fg_color="transparent"
        )
        name_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 12)
        )

        ctk.CTkLabel(
            name_frame,
            text="University Name",
            font=("Arial", 14, "bold"),
            text_color="#334155"
        ).pack(anchor="w", pady=(0, 8))

        self.name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="e.g. Oxford, Harvard...",
            height=45,
            corner_radius=10,
            border_color="#CBD5E1",
            text_color="#14213D",
            font=("Arial", 14)
        )
        self.name_entry.pack(fill="x")

        # Country
        country_frame = ctk.CTkFrame(
            input_frame,
            fg_color="transparent"
        )
        country_frame.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(12, 0)
        )

        ctk.CTkLabel(
            country_frame,
            text="Country",
            font=("Arial", 14, "bold"),
            text_color="#334155"
        ).pack(anchor="w", pady=(0, 8))

        self.country_entry = ctk.CTkEntry(
            country_frame,
            placeholder_text="e.g. Pakistan, United States...",
            height=45,
            corner_radius=10,
            border_color="#CBD5E1",
            text_color="#14213D",
            font=("Arial", 14)
        )
        self.country_entry.pack(fill="x")

        # Buttons
        button_frame = ctk.CTkFrame(
            search_card,
            fg_color="transparent"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 22)
        )

        self.search_button = ctk.CTkButton(
            button_frame,
            text="Search Universities",
            height=43,
            width=190,
            corner_radius=10,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            font=("Arial", 14, "bold"),
            command=self.start_search
        )
        self.search_button.pack(side="left")

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            height=43,
            width=100,
            corner_radius=10,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#14213D",
            font=("Arial", 14, "bold"),
            command=self.clear_fields
        )
        self.clear_button.pack(side="left", padx=12)

        # Results section
        results_card = ctk.CTkFrame(
            content,
            fg_color="#FFFFFF",
            corner_radius=18,
            border_width=1,
            border_color="#E2E8F0"
        )
        results_card.pack(
            fill="both",
            expand=True
        )

        results_header = ctk.CTkFrame(
            results_card,
            fg_color="transparent"
        )
        results_header.pack(
            fill="x",
            padx=25,
            pady=(20, 12)
        )

        ctk.CTkLabel(
            results_header,
            text="Search Results",
            font=("Arial", 21, "bold"),
            text_color="#14213D"
        ).pack(side="left")

        self.result_count = ctk.CTkLabel(
            results_header,
            text="0 universities found",
            font=("Arial", 13),
            text_color="#64748B"
        )
        self.result_count.pack(side="right")

        # Table container
        table_frame = ctk.CTkFrame(
            results_card,
            fg_color="transparent"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )

        # Treeview styling
        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#334155",
            fieldbackground="#FFFFFF",
            rowheight=55,
            font=("Arial", 15),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#EFF3F8",
            foreground="#334155",
            font=("Arial", 13, "bold"),
            relief="flat",
            padding=14,
            anchor="center"
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#14213D")]
        )

        # University results table
        self.results_table = ttk.Treeview(
            table_frame,
            columns=("name", "country", "website"),
            show="headings"
        )

        self.results_table.heading(
            "name",
            text="University Name"
        )

        self.results_table.heading(
            "country",
            text="Country"
        )

        self.results_table.heading(
            "website",
            text="Website"
        )

        # Centered columns and larger widths
        self.results_table.column(
            "name",
            width=420,
            minwidth=250,
            anchor="center"
        )

        self.results_table.column(
            "country",
            width=220,
            minwidth=150,
            anchor="center"
        )

        self.results_table.column(
            "website",
            width=400,
            minwidth=200,
            anchor="center"
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.results_table.yview
        )

        self.results_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.results_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Double-click to open university website
        self.results_table.bind(
            "<Double-1>",
            self.open_university_website
        )

        # Status bar
        self.status_label = ctk.CTkLabel(
            results_card,
            text="Ready to search for universities.",
            font=("Arial", 12),
            text_color="#64748B"
        )
        self.status_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

    # --------------------------------------------------
    # SEARCH FUNCTIONALITY
    # --------------------------------------------------

    def start_search(self):

        name = self.name_entry.get().strip()
        country = self.country_entry.get().strip()

        if not name and not country:
            messagebox.showwarning(
                "Search Required",
                "Please enter a university name or country."
            )
            return

        # Clear previous results
        for item in self.results_table.get_children():
            self.results_table.delete(item)

        self.search_button.configure(
            state="disabled",
            text="Searching..."
        )

        self.status_label.configure(
            text="Connecting to university database..."
        )

        self.result_count.configure(
            text="Searching..."
        )

        # Run API request in background
        search_thread = threading.Thread(
            target=self.search_worker,
            args=(name, country),
            daemon=True
        )

        search_thread.start()

    def search_worker(self, name, country):

        try:
            universities = search_universities(
                name=name or None,
                country=country or None
            )

            self.root.after(
                0,
                lambda: self.display_results(universities)
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.show_error(str(error))
            )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    
    def display_results(self, universities):

        self.search_button.configure(
            state="normal",
            text="Search Universities"
        )

        if not universities:

            self.result_count.configure(
                text="0 universities found"
            )

            self.status_label.configure(
                text="No matching universities found."
            )

            messagebox.showinfo(
                "No Universities Found",
                "Sorry! No universities match your search.\n\n"
                "Please try another university name or country."
            )

            return

        for university in universities:

            name = university.get("name", "Unknown")
            country = university.get("country", "Unknown")

            websites = university.get("web_pages", [])

            website = (
                websites[0]
                if websites
                else "Not available"
            )

            self.results_table.insert(
                "",
                "end",
                values=(name, country, website)
            )

        total = len(universities)

        self.result_count.configure(
            text=f"{total} universities found"
        )

        self.status_label.configure(
            text="Search completed successfully. "
                "Double-click a result to open its website."
        )


    # --------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------

    def show_error(self, error_message):

        self.search_button.configure(
            state="normal",
            text="Search Universities"
        )

        self.result_count.configure(
            text="Search failed"
        )

        self.status_label.configure(
            text="Unable to retrieve university data."
        )

        messagebox.showerror(
            "Search Error",
            f"Something went wrong while searching:\n\n{error_message}"
        )

    # --------------------------------------------------
    # CLEAR FUNCTIONALITY
    # --------------------------------------------------

    def clear_fields(self):

        self.name_entry.delete(0, "end")
        self.country_entry.delete(0, "end")

        for item in self.results_table.get_children():
            self.results_table.delete(item)

        self.result_count.configure(
            text="0 universities found"
        )

        self.status_label.configure(
            text="Ready to search for universities."
        )

    # --------------------------------------------------
    # OPEN UNIVERSITY WEBSITE
    # --------------------------------------------------

    def open_university_website(self, event):

        selected_item = self.results_table.selection()

        if not selected_item:
            return

        item = self.results_table.item(
            selected_item[0]
        )

        website = item["values"][2]

        if website and website != "Not available":

            webbrowser.open(website)

        else:

            messagebox.showinfo(
                "Website Unavailable",
                "No website is available for this university."
            )


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    root = ctk.CTk()

    app = UniFinderApp(root)

    root.mainloop()
