import argparse
from pathlib import Path
import tomlkit
import pull_files

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
    parser.add_argument('folder_path', help='Origin folder', type = Path)
    parser.add_argument('-x', '--file-extension', type = str,
        help='origin extension'
    )
    parser.add_argument('-f', '--filter-path-by', type = str,
        help='select specific path names using wild cards'
    )
    parser.add_argument('-r', '--repository-path', type = Path,
        help = 'the folder path where target files are stored'
    )
    parser.add_argument('-X', '--target-extension', type = str,
        help='the extension of the target files.'
    )
    parser.add_argument('-d', '--dynamic-mode', action='store_true',
        help='if activated, the repository path becomes relative to the origin files'
    )
    parser.add_argument('-w', '--overwrite-mode', action='store_true',
        help='overwrite files in the origin folder'
    )

    # Verify
    namespace = parser.parse_namespace()
    print(namespace)
    exit()
    #namespace.folder_path
    #namespace.file_extension
    #namespace.filter_path_by
    #namespace.target_extension
    #namespace.repository_path
    #namespace.dynamic_mode
    #namespace.overwrite_mode

# Executable path

save = False
if file_extension is None:
    file_extension = config['General']['file_extension']
else:
    config['General']['file_extension'] = file_extension
    save = True

if target_extension is None:
    target_extension = config['General']['target_extension']
else:
    config['General']['target_extension'] = target_extension
    save = True

if repository_path is None:
    repository_path = config['General']['repository_path']
else:
    config['General']['repository_path'] = repository_path
    save = True

if save:
    with open(config_file, 'w', encoding = 'utf-8') as configfile:
        config.write(configfile)

if not os.path.isdir(folder_path):
    raise NameError(f'Origin folder does not exist:\n-{folder_path}')

print('-----------------Copia bungee-----------------')
print('')
print('Mode:\t{}\n'.format('Dynamic repository' if dynamic_mode else 'Fixed repository'))
print('Origin:')
print('  - Path:          \t', folder_path)
print('  - Extension:     \t', file_extension)
print('  - Filter path by:\t', filter_path_by)
print('  - Overwrite files\t', overwrite_mode)
print('\nRepository:')
print('  - Path:            \t', repository_path)
print('  - Target extension:\t', target_extension)
print()

if dynamic_mode:
    pull_files.dynamic_pull_files(folder_path, file_extension, filter_path_by, repository_path, target_extension, overwrite_mode)
else:
    if not os.path.isabs(repository_path):
        raw_repository_path = os.path.join(folder_path, repository_path)
        repository_path = os.path.normpath(raw_repository_path)

    # Validate directories
    if not os.path.isdir(repository_path):
        raise NameError(f'The repository path does not exist:\n-{repository_path}')
    pull_files.pull_files(folder_path, file_extension, filter_path_by, repository_path, target_extension, overwrite_mode)
print('__________________________Done______________________')
