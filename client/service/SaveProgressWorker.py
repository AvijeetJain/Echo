import logging
import pickle
import time
from pathlib import Path
from typing import Any
from PyQt5.QtCore import QObject

# Import utilities
from utils.types import ProgressBarData, TransferStatus


class SaveProgressWorker(QObject):
    """A worker that periodically saves the download progress and statuses to a file

    Methods
    -------
    dump_progress_data()
        Stores the current download progress and statuses of all files and folders to a file
    run()
        Runs the dump_progress_data function every 10 seconds
    """

    def dump_progress_data(self) -> None:
        """Pickles the transfer_progress, dir_progress and progress_widgets dictionaries into 3 files"""
        global transfer_progress
        global dir_progress
        global progress_widgets

        for path in transfer_progress.keys():
            if transfer_progress[path]["status"] in [
                TransferStatus.DOWNLOADING,
                TransferStatus.NEVER_STARTED,
            ]:
                transfer_progress[path]["status"] = TransferStatus.PAUSED

        # Pickle the transfer_progress dictionary
        with (Path.home() / ".Echo/db/transfer_progress.pkl").open(mode="wb") as transfer_progress_dump:
            logging.debug(msg="Created transfer progress dump")
            pickle.dump(transfer_progress, transfer_progress_dump)

        # Pickle the dir_progress dictionary
        with (Path.home() / ".Echo/db/dir_progress.pkl").open(mode="wb") as dir_progress_dump:
            logging.debug(msg="Created dir progress dump")
            dir_progress_writeable: dict[Path, Any] = {}
            for path in dir_progress.keys():
                dir_progress[path]["mutex"].lock()
                dir_progress_writeable[path] = {
                    "current": dir_progress[path]["current"],
                    "total": dir_progress[path]["total"],
                    "status": dir_progress[path]["status"],
                }
                dir_progress[path]["mutex"].unlock()
            pickle.dump(dir_progress_writeable, dir_progress_dump)

        # Pickle the progress_widgets dictionary
        with (Path.home() / ".Echo/db/progress_widgets.pkl").open(mode="wb") as progress_widgets_dump:
            progress_widgets_writeable: dict[Path, ProgressBarData] = {}
            for path, widget in progress_widgets.items():
                progress_widgets_writeable[path] = {
                    "current": widget.ui.progressBar.value(),
                    "total": widget.ui.total,
                }
            pickle.dump(progress_widgets_writeable, progress_widgets_dump)

    def run(self):
        """Runs the dump_progress_data periodically"""
        global transfer_progress
        global dir_progress
        global progress_widgets

        # Save the progress data every 10 seconds
        while True:
            self.dump_progress_data()
            time.sleep(10)