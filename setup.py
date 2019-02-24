"""
use "Process_Epilepsy_Docx" in terminal to run.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Epilepsy Surgery Text Data Analysis",
    version="0.1.0",
    author="Ali Alim-Marvasti",
    description="analysis of presurgical PDFs and word documents to predict"
                "Engel Class 1 outcomes post epilepsy surgery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['*tests']),
    install_requires=['argparse', 'PyYaml', 'PyPDF2', 'scikit-learn',
                      'json', 'copy', 'uuid', 'docx', 'os', 're', 'zipfile',
                      'pandas'],
    entry_points={
        'console_scripts': [
            'Process_Epilepsy_Docx = preprocessing.command:main_docx_preprocess'
        ]}
)
