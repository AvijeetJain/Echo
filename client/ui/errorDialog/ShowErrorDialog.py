from PyQt5.QtWidgets import QDialog
from ui.errorDialog.ErrorDialog import Ui_ErrorDialog

def show_error_dialog(error_msg: str, show_settings: bool = False) -> None:
    """Displays an error dialog with the given message

    Parameters
    ----------
    error_msg : str
        The error message to be displayed in the dialog
    show_settings : bool, optional
        A flag used to indicate whether or not to display the settings button (default is False)
    """

    global user_settings
    global error_dialog_is_open

    error_dialog = QDialog()
    error_dialog.ui = Ui_ErrorDialog(error_dialog, error_msg, user_settings if show_settings else None)

    # Don't display dialog if another dialog is already open
    if not error_dialog_is_open:
        error_dialog_is_open = True
        error_dialog.exec()
        error_dialog_is_open = False