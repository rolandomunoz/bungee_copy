import sys
from pathlib import Path
package_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(package_dir))
from bungeecopy.copy import search

src_dir = Path(r'C:\Users\lab\OneDrive\Documents\OPERIT\casos\2020_122s-suprema_cb\investigados\03_fernando_alejandro_seminario_arteta\muestra_dubitada\audios')
recursive = False
extension = '.wav'
new_extensions = ['.TextGrid']
search_dir = Path(r'C:\Users\lab\OneDrive\Documents\OPERIT\casos\2020_122s-suprema_cb\investigados')

dict_ = search.search_filepairs(src_dir, recursive, extension, new_extensions, search_dir)
print(dict_)
