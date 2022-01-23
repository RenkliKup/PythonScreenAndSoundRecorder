import logging
import filesAndFolders
def create_log_file(name,folder_name,log_path):
    filesAndFolders.create_log_folder()
    logger=logging.getLogger(name)
    formatter=logging.Formatter("%(asctime)s:%(lineno)d:%(threadName)s:%(name)s:%(message)s")
    fileHandler=logging.FileHandler(log_path+f"\\{folder_name}")
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    return logger