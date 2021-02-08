# Bungee copy

Given a list of files stored in a directory, find the files that match the same filename but with differt extension. 

'Bungee Copy has the properties of both rubber and gum.'

## Copy files

Get the names of the files with `wav` extension in the `C:\Users\Teresa\Desktop\wav_audio` directory and find their corresponding annotation files (with `TextGrid` extension) in the `C:\Users\Teresa\Repository\textgrid_files`. If the corresponding TextGrid file of a wav file is found, copy it to the same directory of the wav file.  

On Windows:
```
python.exe cli-bungee_copy.py "C:\Users\Teresa\Desktop\wav_audio" -x "wav" -X "TextGrid" -r "C:\Users\Teresa\Repository\textgrid_files"
```
