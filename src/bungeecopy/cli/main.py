import argparse
from pathlib import Path
from importlib.resources import files
import tomlkit
from bungeecopy.copy import pull_files

LOGO = '''

'''
def cli():
    """
    CLI for populating qual dirs.
    """
    # Build Parser
    parser = argparse.ArgumentParser(
        prog = 'bungee-copy',
        description= f'{LOGO}\nGiven a list of files stored in a directory,'
        ' find the files that match the same filename but with'
        ' different extension.'
        '"BungeeCopy has the properties'
        ' of both rubber and gum."',
        epilog = '(c) Rolando Muñoz Aramburú (2021-presente)',
        formatter_class = argparse.RawDescriptionHelpFormatter
    )

    # Parser
    src_group = parser.add_argument_group('Source', 'Source parameters')
    parser.add_argument('source_dir', type = Path, help='Origin folder')
    src_group.add_argument('-x', '--file-extension', type = str,
        help='origin extension'
    )
    src_group.add_argument('-f', '--filter-path-by', type = str,
        help='select specific path names using wild cards'
    )
    repo_group = parser.add_argument_group('Target', 'Target parameters')
    repo_group.add_argument('-r', '--repository-dir', type = Path,
        help = 'the folder path where target files are stored'
    )
    repo_group.add_argument('-X', '--target-extension', type = str,
        help='the extension of the target files.'
    )
    parser.add_argument('-d', '--dynamic-mode', action='store_true',
        help='if activated, the repository path becomes relative to the origin files'
    )
    parser.add_argument('-w', '--overwrite-mode', action='store_true',
        help='overwrite files in the origin folder'
    )

    # Verify
    config_path = files('bungeecopy.cli').joinpath('config.toml')
    config = tomlkit.parse(
        config_path.read_text('utf-8')
    )
    namespace = parser.parse_args()

    if namespace.file_extension is None:
        namespace.file_extension = config['file_extension']

    if namespace.target_extension is None:
        namespace.target_extension = config['target_extension']

    if namespace.repository_dir is None:
        namespace.repository_dir = Path(config['repository_dir'])

    dict_ = {
            'dir_in': namespace.source_dir.as_posix(),
            'file_extension': namespace.file_extension,
            #'filter_path_by': namespace.filter_path_by,
            'target_extension': namespace.target_extension,
            'repository_dir': namespace.repository_dir.as_posix(),
            'dynamic_mode': namespace.dynamic_mode,
            'overwrite_mode': namespace.overwrite_mode,
    }
    config_out_str = tomlkit.dumps(dict_)
    config_path.write_text(config_out_str, encoding = 'utf-8')
    info = f'''
    -----------------Bunee Copy-----------------
    Origin:
        - Path:                 {namespace.source_dir}
        - Extension:            {namespace.file_extension}
        - Filter path by:       {namespace.filter_path_by}
        - Overwrite files       {namespace.overwrite_mode}
    Repository:
        - Path:                 {namespace.repository_dir}
        - Target extension:     {namespace.target_extension}
    '''
    print(info)
    if namespace.dynamic_mode:
        pull_files.dynamic_pull_files(
            namespace.source_dir,
            namespace.file_extension,
            namespace.filter_path_by,
            namespace.repository_dir,
            namespace.target_extension,
            namespace.overwrite_mode
        )
    else:
        pull_files.pull_files(
            namespace.source_dir,
            namespace.file_extension,
            namespace.filter_path_by,
            namespace.repository_dir,
            namespace.target_extension,
            namespace.overwrite_mode
        )
    print('__________________________Done______________________')
