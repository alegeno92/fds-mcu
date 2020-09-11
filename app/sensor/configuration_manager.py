import configparser
import logging


class ConfigurationManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.logger = logging.getLogger(__name__)

    def load(self, key='DEFAULT'):
        configs = configparser.ConfigParser()
        configs.read(self.config_file_path)
        return configs[key]

    def save(self, configurations=None):

        if configurations is None:
            configurations = {}

        configs = configparser.ConfigParser()
        for key in configurations.keys():
            configs['DEFAULT'][key] = str(configurations[key])

        # save to file
        self.logger.debug("save configurations to file {}".format(self.config_file_path))
        with open(self.config_file_path, 'w') as configfile:
            configs.write(configfile)
            configfile.flush()
