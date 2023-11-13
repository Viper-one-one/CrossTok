from cx_Freeze import build_exe, setup, Executable

build_exe_options = {
    "packages": ["socket", "sys", "threading"],
    "excludes": [],
    "includes": ["tabulate"]
}

setup(
    name = "CrossTok",
    version = "1.0",
    description = "A TCP Chat app",
    options = {"build_exe": build_exe_options},
    executables = [Executable(script="CrossTok.py")]
    )
