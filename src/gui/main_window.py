"""
Module for GUI main window creation.
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext
from typing import Union

import pandas as pd
from pandera.errors import SchemaError
from src.file_io import input_reader
from src.ors_helper.ors_helper import ORShelper

class MainWindow:
    """
    Main Window of the application.
    """
    def __init__(self, root):
        self.root = root
        root.geometry("800x600")
        self.root.title("Ors Matrix")
        self.input_file = pd.DataFrame()
        self.distance_matrix_car = pd.DataFrame()
        self.ors_helper = ORShelper.from_env_file()
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the widgets for the main window.
        """

        #Create input file button.
        self.open_file_button = tk.Button(
            self.root,
            text="Select input file",
            command=self.load_input_file
        )
        self.open_file_button.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

        # Create text_widget for input_file
        self.info_field = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            height=10,
            width=80)
        self.info_field.config(state=tk.DISABLED)

        self.info_field.pack(
            side=tk.BOTTOM,
            anchor=tk.W,
            padx=10,
            pady=10,
            fill=tk.X)



    def open_file_dialog(self) -> Union[str, None]:
        """
        Opens a file dialog to choose a file from computer.
        """

        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Excel file", "*.xlsx")]
        )

        return file_path


    def set_input_file(self, path: str) -> None:
        """
        Sets the input_file attribute.
        """
        file_df = input_reader.read_xlsx_input_file(path)
        self.input_file = file_df


    def load_input_file(self, file_path: Union[str, None] = None) -> None:
        """
        Opens a file dialog to choose a input *.xlsx file, loads the data as
        a pd.DataFrame and sets the input_file attribute to it.
        """

        if file_path is None:
            file_path = self.open_file_dialog()

        if file_path:
            try:
                self.set_input_file(file_path)
                self.update_info_field_text("Loading input file successful")
            except SchemaError as exc:
                error_message = (
                    f"Schema validation failesd\n"
                    f"Error message: {exc.args[0]}\n"
                    f"Failure cases:\n"
                    f"{exc.failure_cases}"
                )
                self.update_info_field_text(error_message)



    def update_info_field_text(self, text: str) -> None:
        """
        Updates info field text.

        Parameter
        ---------
        text : str
            Text to display in the input field.
        """

        self.info_field.config(state=tk.NORMAL)
        self.info_field.delete("1.0", tk.END)
        self.info_field.insert(tk.END, text)
        self.info_field.config(state=tk.DISABLED)
