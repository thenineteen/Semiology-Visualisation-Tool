"""
use "MEGA_ANALYSIS_CONSOLE" in terminal to run.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    requirements = fh.readlines()

setup(
    name="mega_analysis",
    version="0.1.0",
    author="Ali Alim-Marvasti",
    description="Epilepsy Semiology Visualisation Tool: "
                "Thousands of patient level semiology data from journal"
                "publications with localisation and lateralisation numbers"
                "collected based on post-operative seizure freedom,"
                "imaging and EEG concordance, and sEEG/stimulation studies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['*tests']),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'MEGA_ANALYSIS_CONSOLE = scripts.command_console:process_pdfs',
            'make-scores = mega_analysis.cli:main',
        ]}
)
