# utils/config_loader.py
import configparser

def load_metadata(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)
    metadata_dict = {}
    for section in config.sections():
        metadata_dict[section] = {
            'Title': config.get(section, 'Title', fallback=''),
            'Author': config.get(section, 'Author', fallback=''),
            'Subject': config.get(section, 'Subject', fallback=''),
            'Keywords': config.get(section, 'Keywords', fallback=''),
        }
    return metadata_dict
