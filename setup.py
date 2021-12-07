import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['config.ini', 'LICENSE', 'README.md']
packages = ['os', 'argparse', 'configparser', 'shutil', 'fnmatch', 'sys']
build_exe_options = {"packages": packages, "include_files":includefiles}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#if sys.platform == "win32":
#  base = "Win32GUI"

setup(name = 'BungeeCopy',
  version = "1.0",
  description = 'Copy files',
  options = {'build_exe': build_exe_options, 'bdist_msi': {}},
  executables = [Executable('cli-bungee_copy.py', base=base, target_name ='BungeeCopy', icon='bungee_copy.ico')])