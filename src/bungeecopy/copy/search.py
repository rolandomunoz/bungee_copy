"""
Copy files.
"""
def search_filepairs(src_dir, recursive, extension, new_extensions, search_dir):
    """
    Search files with .
    
    Parameters
    ----------
    src_dir : :class:`pathlib.Path`
        A folder containinig the base files.
    recursive : bool
        If `True`, search base files in subfolders under the `src_dir` as well.
    extension : str
        The extension of the base files.
    new_extensions : list or tuple
        The extensions for the target filenames.
    search_dir : :class:`pathlib.Path`
        
    """
    dict_ = {}
    for base_path in iterdirfiles(src_dir, extension, recursive):
        if not base_path.is_file():
            continue
        dict_[base_path] = None
        for new_extension in new_extensions:
            new_filename = base_path.with_suffix(new_extension).name                
            match = find_file(new_filename, search_dir, True)
            if match is None:
                continue
            dict_[base_path] = {
                new_extension: match
            }
    return dict_
            
def find_file(filename, root_dir, recursive):
    """
    Report all the occurrences of a filename in a directory.
    
    Parameters
    ----------
    filename : str
        The filename to search into a specific folder.
    root_dir : :class:`pathlib.Path`
        The folder where a files is searched.
    recursive : bool
        If True, search files inside subfolders as well. When it is False,
        search the files only under the root directory.
    """
    if recursive:
        return tuple(root_dir.rglob(filename))
    return tuple(root_dir.glob(filename))

def iterdirfiles(dir_, pattern, recursive = False):
    """
    Iter through files that match an extension and are under a directory.
    """
    if recursive:
        return dir_.rglob(f'*{pattern}')
    return dir_.glob(f'*{pattern}')
