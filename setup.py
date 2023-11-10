from cx_Freeze import setup, Executable

setup(
    name = "CrossTok",
    version = "1.0",
    description = "A TCP Chat app",
    executables = [Executable(script="CrossTok.py")]
    )
