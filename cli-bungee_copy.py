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

parser = argparse.ArgumentParser(prog = 'Copia bungee',
  description='Extrae archivos pareja de un repositorio. "La copia bungee tiene las propiedades de la goma y el caucho."',
  epilog = 'Escrito por Rolando Muñoz Aramburú (Feb-2021)',
  formatter_class = argparse.RawTextHelpFormatter
)

parser.add_argument('folder_path', help='Carpeta donde se encuentran los archivos de origen.')
parser.add_argument('-x', '--file-extension', default = None, help='Extensión de los archivos de origen.')
parser.add_argument('-f', '--filter-path-by', default = None, help='Filtrar directorios de los archivos de origen. Se usan comodines (wild cards).')
parser.add_argument('-r', '--repository-path', default = None, help = 'Dirección del repositorio de archivos.')
parser.add_argument('-X', '--target-extension', default = None, help='Extensión de los archivos pareja (los que se buscan).')
parser.add_argument('-d', '--dynamic-mode', action='store_true', help='La dirección del repositorio es relativa a la dirección de cada archivo de origen')

# Variables
args = parser.parse_args()
folder_path = args.folder_path
file_extension = args.file_extension
filter_path_by = args.filter_path_by
target_extension = args.target_extension
repository_path = args.repository_path
dynamic_mode = args.dynamic_mode

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
	raise NameError('La dirección de la carpeta de origen no existe:\n-{}'.format(folder_path))

print('-----------------Copia bungee-----------------')
print('')
print('Modo:\t{}\n'.format('Repositorio dinámico' if dynamic_mode else 'Normal'))
print('Origen:')
print('- Dirección: \t', folder_path)
print('- Extensión: \t', file_extension)
print('- Filtro:\t', filter_path_by)
print('\nRepositorio:')
print('- Dirección: \t', repository_path)
print('- Extensión buscada: \t', target_extension)
print()

if dynamic_mode:
	pull_files.dynamic_pull_files(folder_path, file_extension, filter_path_by, repository_path, target_extension)
else:
	if not os.path.isabs(repository_path):
		raw_repository_path = os.path.join(folder_path, repository_path)
		repository_path = os.path.normpath(raw_repository_path)

	# Validate directories
	if not os.path.isdir(repository_path):
		raise NameError('La dirección del repositorio no existe:\n-{}'.format(repository_path))
	pull_files.pull_files(folder_path, file_extension, filter_path_by, repository_path, target_extension)
print('__________________________Listo______________________')