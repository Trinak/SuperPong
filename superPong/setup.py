import sys
from cx_Freeze import setup, Executable

includefiles = [("D:\Programming\Python\Lib\site-packages\pymunk\chipmunk.dll", "chipmunk.dll"),
                ("D:\Programming\Projects\Python\MyProjects\superPong\Assets", "Assets")]
zipIncludes = []
path = ["D:\Programming\Projects\Python\MyProjects\superPong"] + sys.path
packages = ['pyHopeEngine', "Mastermind"]

setup(  name = "EmotiPong",
        version = "0.1",
        description = "EmotiPong",
        options = {"build_exe": {"include_files": includefiles, 
                                 "zip_includes": zipIncludes, 
                                 "path": path, 
                                 "packages": packages,
                                 "include_msvcr": True}},
        executables = [Executable("main\pongApp.py", base = "Win32GUI", targetName = "EmotiPong.exe")])