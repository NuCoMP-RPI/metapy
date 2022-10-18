# MetaPy
Python package to manage the Java Server and automated wrapping functions required for metamodel-driven APIs like MCNPy and Serpy.

# Usage
On its own, this package does very little. It manages basic utilities required for other packages. Thus, you will likely never invoke it directly.

# Dependencies
- `py4j`.
- `psutil`
- Java 8
- Everything else should come with a standard Python install

# How to Install
1. Clone the repository: `git clone https://github.rpi.edu/NuCoMP/metapy.git`.
2. Ensure you are running the desired Python environment.
    - Try `conda activate ENV_NAME` to switch.
3. Run `pip install /path/to/cloned/repo/dist/metapy-X.whl` where `X` is the version.
    - All dependencies *except* Java will be downloaded if needed.
4. Done!

# Building a New Wheel
1. Use `pip uninstall metapy` to uninstall current version.
2. Run `python /path/to/cloned/repo/setup.py` to build the wheel.

# Updating the Java Server
After any changes to the `EntryPoint.java` source file, you must recompile the Java server. From within `/path/to/cloned/repo/metapy`, run:
- `bash compile.sh`(Linux)
- `compile.bat` (Windows)