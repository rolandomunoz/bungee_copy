import sys
from pathlib import Path
package_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(package_dir))
from bungeecopy.copy import search

filename = '000000000023090.2190096863 - 06.03.2018 at 08.28.42.376-1.wav'
dir_ = Path(r'C:\Users\lab\OneDrive\Documents\OPERIT\casos\2020_122s-suprema_cb\investigados')
matches = search.find_file(filename, dir_, True)
print(matches)
