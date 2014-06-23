"""
warc
~~~~

Python library to work with WARC files.

:copyright: (c) 2012 Internet Archive
"""

from .arc import ARCFile, ARCRecord, ARCHeader
from .warc import WARCFile, WARCRecord, WARCHeader, WARCReader


def _detect_format(filename):
    """
    Attempt to detect the type of the file based on file extension.

    Args:
        filename: The name of the WARC or ARC file.

    Returns:
        "warc" for WARC files.
        "arc" for ARC files.
        file extension if the type cannot be detected.

    Note: Detection is based simply on if the filename ends with ``.warc``,
    ``.warc.gz``, ``.arc``, or ``.arc.gz``.
    """

    if filename.endswith(".warc") or filename.endswith(".warc.gz"):
        return "warc"
    elif filename.endswith(".arc") or filename.endswith(".arc.gz"):
        return "arc"
    else:
        return "".join(filename.rpartition(".")[1:])

def _detect_compression(filename):
    """
    Detect compression based on filename.

    Args:
        filename: The name of the WARC or ARC file.

    Returns:
        True if the file is compressed; otherwise returns false.

    Note:
        Detection simply looks to see if the filename ends with ``.gz``.
    """

    return filename.endswith(".gz")

def open(filename, mode="rb"):
    """
    Shorthand for WARCFile(filename, mode, ...) with auto-detection of file type
    (ARC, WARC) and compression.

    Args:
        filename: The name of the file to be opened.
        mode: The open mode (see Python open()); defaults to "rb".  Use "wb"
              or "ab" for writing and appending.

    Returns:
        An open file.

    Raises:
        IOError: If file type detection or opening the file fails.
    """
    format = _detect_format(filename)
    compress = _detect_compression(filename)

    if format == "warc":
        return WARCFile(filename, mode, compress=compress)
    elif format == "arc":
        return ARCFile(filename, mode, compress=compress)
    else:
        raise IOError("Don't know how to open '%s' files" % format)
