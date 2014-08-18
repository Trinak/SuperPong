import sys
from cx_Freeze import setup, Executable

includefiles = [("D:\Python\lib\site-packages\pymunk\chipmunk.dll", "chipmunk.dll"),
                ("D:\Programming\Projects\Python\MyProjects\SuperPong\Assets", "Assets")]
zipIncludes = []
path = ["D:\Programming\Projects\Python\MyProjects\SuperPong"] + sys.path
packages = ['pyHopeEngine', "Mastermind"]

setup(  name = "SuperPong",
        version = "0.1",
        description = "SuperPongTest",
        options = {"build_exe": {"include_files": includefiles, 
                                 "zip_includes": zipIncludes, 
                                 "path": path, 
                                 "packages": packages,
                                 "include_msvcr": True}},
        executables = [Executable("pongApp.py", base = "Win32GUI")])