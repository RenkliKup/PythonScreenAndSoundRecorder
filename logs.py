import logging
import filesAndFolders
def create_log_file(folder_name,log_path):
    filesAndFolders.create_log_folder()
    logger=logging.getLogger(__name__)
    formatter=logging.Formatter("%(lineno)d:%(asctime)s:%(levelname)s")
    fileHandler=logging.FileHandler(log_path+f"\\{folder_name}")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger