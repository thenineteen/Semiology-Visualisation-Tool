"""
use "Process_Epilepsy_Docx" in terminal to run.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mega_analysis",
    version="0.1.0",
    author="Ali Alim-Marvasti",
    description="analysis of presurgical PDFs and word documents to predict"
                "Engel Class 1 outcomes post epilepsy surgery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['*tests']),
    install_requires=[
        'click',
        'docx',
        'matplotlib',
        'matplotlib-venn',
        'pandas',
        'PyPDF2',
        'PyYaml',
        'scikit-learn',
        'seaborn',
        'uuid',
        'xlrd',
    ],
    entry_points={
        'console_scripts': [
            'Process_Epilepsy_Docx = mega_analysis.preprocessing.command:main_docx_preprocess',
            'make-scores = mega_analysis.cli:main',
        ]}
)
