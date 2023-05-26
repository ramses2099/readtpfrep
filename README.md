# readtpfrep
Project read tpfrep file

## 1- Load file
## 2- Parse info
## 3 -Generate file with the report

## Resolve SSL
For me the problem was fixed by creating a folder pip, with a file: pip.ini in C:\Users\<username>\AppData\Roaming\ e.g:

C:\Users\<username>\AppData\Roaming\pip\pip.ini
Inside it I wrote:

[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
I restarted python, and then pip permanently trusted these sites, and used them to download packages from.

If you can't find the AppData Folder on windows, write %appdata% in file explorer and it should appear.