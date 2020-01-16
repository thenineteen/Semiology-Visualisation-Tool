import os
import shutil

def copy_all_pdfs_to_single_folder(source_folder='L:\\PDF\\Original Copy',
                                    destination_folder='L:\\PDF\\All_PDFs'):
    """
    Copy all PDFs from lots of subfolders and mixtures of some non-pdf files (e.g. EEG neurophys files)
    to a single target directory for subsequent XFA/XML data extraction using Greg Scott's Matlab/Java tools.

    Ali Alim-Marvasti 2019
    """


    for root, dirs, files in os.walk(source_folder):  # replace with your starting directory
        for file in files:
            path_file = os.path.join(root, file)
            
            if path_file.split('\\')[-1][-4:] == ".pdf":

                try:
                    shutil.copy2(path_file, destination_folder) # change your destination dir
                except PermissionError:
                    print(path_file, "Permission Error, Skipped.")
                    continue