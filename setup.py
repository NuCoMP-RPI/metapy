from setuptools import setup
NAME = 'metapy'

setup(
    name=NAME,
    version='0.0.1',
    packages=[NAME],
    include_package_data=True,
    setup_requires=['setuptools_scm'],
    author='Peter Kowal',
    author_email='kowalp@rpi.edu',
    description='Metamodel-Driven Java Server',
    license='MIT',
    install_requires=['py4j', 'psutil', 'h5py'],
    platforms=['Windows', 'Linux']
)