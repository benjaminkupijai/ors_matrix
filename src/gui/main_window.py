"""
Module for GUI main window creation.
"""

from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext
from typing import Union

import pandas as pd
from pandera.errors import SchemaError
from src.file_io import input_reader
from src.ors_helper.ors_helper import ORShelper

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

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
        self.distance_matrix_hgv = pd.DataFrame()
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

        self.get_distance_matrix_car_button = tk.Button(
            self.root,
            text="Get Distance Matrix Car",
            command=self.get_distance_matrix_car
        )

        #Buttons to create distance matrices
        self.get_distance_matrix_car_button.pack(
            side=tk.TOP,
            anchor=tk.W,
            padx=10,
            pady=10
        )

        self.get_distance_matrix_car_button = tk.Button(
            self.root,
            text="Get Distance Matrix HGV",
            command=self.get_distance_matrix_hgv
        )
        self.get_distance_matrix_car_button.pack(
            side=tk.TOP,
            anchor=tk.W,
            padx=10,
            pady=10
        )


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

        #Save File button
        self.save_result_button = tk.Button(
            self.root,
            text="Save Result",
            command=self.save_result
        )
        self.save_result_button.pack(
            side=tk.BOTTOM,
            anchor=tk.E,
            padx=10,
            pady=10
        )


    def open_file_dialog(self) -> Union[str, None]:
        """
        Opens a file dialog to choose a file from computer.
        """

        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Excel file", "*.xlsx")]
        )

        return file_path
    
    def open_save_file_dialog(self) -> Union[str, None]:
        """
        Opens a file dialog to to get a path to the desired save file location.
        """

        date = datetime.now().strftime("%y%m%d_%H%M")
        default_name = f"{date}_distance_matrix.xlsx"

        file_path = filedialog.asksaveasfilename(
            title="Save as",
            initialdir=CURRENT_DIR,
            initialfile=default_name,
            defaultextension=".xlsx",
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
                    f"Schema validation failed\n"
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


    def get_distance_matrix(self, profile: str) -> pd.DataFrame:
        """
        Gets distance matrix from openrouteservice with the progile 'car' or 'hgv.
        """

        if self.input_file.empty:
            self.update_info_field_text("Select input file first!")
            return pd.DataFrame()

        return self.ors_helper.get_distance_matrix(
            locations=self.input_file,
            profile=profile
        )

    def get_distance_matrix_car(self) -> None:
        """
        Executes get_distance_matrix with attribut car
        """
        self.distance_matrix_car = self.get_distance_matrix("car")
        if not self.distance_matrix_car.empty:
            self.update_info_field_text(str(self.distance_matrix_car.head(2)))

    def get_distance_matrix_hgv(self) -> None:
        """
        Executes get_distance_matrix with attribut car
        """
        self.distance_matrix_hgv = self.get_distance_matrix("hgv")
        if not self.distance_matrix_hgv.empty:
            self.update_info_field_text(str(self.distance_matrix_hgv.head(2)))

    def save_result(self, file_path: Union[str, None] = None) -> None:
        """
        Saves the results to an excel file
        """

        #TODO: Implement check if any results are available

        if file_path is None:
            file_path = self.open_save_file_dialog()

        if file_path is not None:
            writer = pd.ExcelWriter(file_path, engine="xlsxwriter")

            self.input_file.to_excel(
                writer, sheet_name="locations", index=False
            )

            if not self.distance_matrix_car.empty:
                self.distance_matrix_car.to_excel(
                    writer, sheet_name="matrix_car", index=False
                )
            if not self.distance_matrix_hgv.empty:
                self.distance_matrix_hgv.to_excel(
                    writer, sheet_name="matrix_hgv", index=False
                )

            writer.close()
