import argparse
import os
import sys
import configparser
import pull_files

_CONFIG_FILE = 'config.ini'

def find_data_file(filename):
  if getattr(sys, "frozen", False):
    # The application is frozen
    datadir = os.path.dirname(sys.executable)
  else:
    # The application is not frozen
    # Change this bit to match where you store your data files:
    datadir = os.path.dirname(__file__)
  return os.path.join(datadir, filename)

config_file = find_data_file(_CONFIG_FILE)

parser = argparse.ArgumentParser(prog = 'Bungee copy',
  description='Given a list of files stored in a directory, find the files that match the same filename but with differt extension.\n"Bungee Copy has the properties of both rubber and gum."',
  epilog = 'Written by Rolando Muñoz Aramburú (Feb-2021)',
  formatter_class = argparse.RawTextHelpFormatter
)

parser.add_argument('folder_path', help='Origin folder')
parser.add_argument('-x', '--file-extension', default = None, help='Origin extension')
parser.add_argument('-f', '--filter-path-by', default = None, help='Select specific path names using wild cards.')
parser.add_argument('-r', '--repository-path', default = None, help = 'The folder path where target files are stored.')
parser.add_argument('-X', '--target-extension', default = None, help='The extension of the target files.')
parser.add_argument('-d', '--dynamic-mode', action='store_true', help='If activated, the repository path becomes relative to the origin files')
parser.add_argument('-w', '--overwrite-mode', action='store_true', help='overwrite files in the origin folder')
# Variables
args = parser.parse_args()
folder_path = args.folder_path
file_extension = args.file_extension
filter_path_by = args.filter_path_by
target_extension = args.target_extension
repository_path = args.repository_path
dynamic_mode = args.dynamic_mode
overwrite_mode = args.overwrite_mode

# Executable path
config = configparser.ConfigParser()
config.read(config_file)

save = False
if file_extension == None:
  file_extension = config['General']['file_extension']
else:
	config['General']['file_extension'] = file_extension
	save = True

if target_extension == None:
  target_extension = config['General']['target_extension']
else:
	config['General']['target_extension'] = target_extension
	save = True

if repository_path == None:
  repository_path = config['General']['repository_path']
else:
	config['General']['repository_path'] = repository_path
	save = True

if save:
	with open(config_file, 'w') as configfile:
		config.write(configfile)

if not os.path.isdir(folder_path):
	raise NameError('Origin folder does not exist:\n-{}'.format(folder_path))

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
		raise NameError('The repository path does not exist:\n-{}'.format(repository_path))
	pull_files.pull_files(folder_path, file_extension, filter_path_by, repository_path, target_extension, overwrite_mode)
print('__________________________Done______________________')