import auro.filename
import vim

class Filename(auro.filename.Filename):
    """
    Uses the user provided basname and dirname info dictionaries to provide meta information about the given path.

    If constructed without fn -> vim.current.buffer is used and the vim_filetype is detected not only on filename extension

    TODO: this should be independent of vim?
    """
    def __init__(self, fn = None, ft = None):
        if not fn:
            fn = vim.current.buffer.name
        super().__init__(fn, ft)
