"""
Unit tests for MainWindow class.
"""

import tkinter as tk
from tkinter import scrolledtext
from os import path

import pandas as pd
from src.gui.main_window import MainWindow


def test_main_window_geometry():
    """
    Tests for the correct size of MainWindow after initialization
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    assert main_window.root.geometry().split("+")[0] == "800x600"
    root.destroy()


def test_main_window_title():
    """
    Tests for the correct title of the main window.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    assert main_window.root.title() == "Ors Matrix"
    root.destroy()


def test_main_window_input_file_init():
    """
    Tests for the correct initialization of input_file attribute of main_window.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    expected_input_file = pd.DataFrame()

    pd.testing.assert_frame_equal(main_window.input_file, expected_input_file)
    root.destroy()


def test_main_window_init_info_field():
    """
    Tests for the correct initialization of the info_field in main_window.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()
    info_field = main_window.info_field

    assert isinstance(info_field, scrolledtext.ScrolledText)
    root.destroy()


def test_init_open_file_button():
    """
    Tests for the correct initialization of the open_file_button.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    open_file_button = main_window.open_file_button

    assert isinstance(open_file_button, tk.Button)
    assert open_file_button.cget("text") == "Select input file"
    root.destroy()


def test_set_input_file():
    """
    Tests for the correct 
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    test_path = path.join(".", "tests", "test_files", "test.xlsx")
    main_window.set_input_file(test_path)

    expected_input_file = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [2, 3, 4]
    })

    pd.testing.assert_frame_equal(main_window.input_file, expected_input_file)
    root.destroy()


def test_load_input_file():
    """
    Tests for the correct loading of an input file.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    test_path = path.join(".", "tests", "test_files", "test.xlsx")
    main_window.load_input_file(test_path)

    expected_input_file = pd.DataFrame({
        "A": [1, 2, 3],
        "B": [2, 3, 4]
    })

    pd.testing.assert_frame_equal(main_window.input_file, expected_input_file)


def test_load_input_file_success_message():
    """
    Tests for the correct display of info after succesful loading of the input
    file.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    test_path = path.join(".", "tests", "test_files", "test.xlsx")
    main_window.load_input_file(test_path)

    info_text = main_window.info_field.get("1.0", tk.END)
    expected_info_text = "Loading input file successful\n"

    assert info_text == expected_info_text


def test_update_info_field():
    """
    Tests for correct update of the info field in main_window.
    """

    root = tk.Tk()
    main_window = MainWindow(root)

    root.update_idletasks()

    info_text = "This is a info field update"
    main_window.update_info_field_text(info_text)

    assert main_window.info_field.get("1.0", tk.END) == "This is a info field update\n"
