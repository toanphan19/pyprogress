from __future__ import annotations

import sys
import time

from . import writer
from .theme import Theme

class ProgressBar:
    """A class for representing the state of the progressbar.
    """

    def __init__(self, 
                 max_value: int = 100, 
                 terminal_width: int = 61,
                 theme: Theme = None) -> ProgressBar:
        self.current_value = 0
        self.max_value = max_value
        self.width = terminal_width
        self.theme = theme if theme is not None else Theme()
        self.start_time = time.time()

        self._render()
    
    def increase(self, value: int) -> None:
        self._increase(value)
        self._render()

    def _increase(self, value: int) -> None:
        self.current_value += value

    def set_progress(self, value: int) -> None:
        self._set_progress(value)
        self._render()

    def _set_progress(self, value: int) -> None:
        self.current_value = value

    @property 
    def current_percent(self) -> float:
        return min(100, int(100 * self.current_value / self.max_value))

    @property
    def time_elapsed_secs(self) -> int:
        return int(time.time() - self.start_time)


    def _render(self) -> str:
        NON_PROGRESS_LENGTH = 15
        bar_width = self.width - NON_PROGRESS_LENGTH

        progress_length = int(bar_width * self.current_percent / 100)
        padding_length = bar_width - progress_length        
    
        line = ' {}% |{}{}| [{}s]'.format(
            self.current_percent,
            self.theme.progress_char * progress_length,
            self.theme.padding_char * padding_length,
            self.time_elapsed_secs
        )
        writer.overwrite(sys.stdout, line)

        if self.current_percent == 100:
            sys.stdout.write('  Done.\n')
