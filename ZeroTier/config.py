from pydantic import BaseModel
import yaml


class Device(BaseModel):
    """Device config class"""
    name: str
    network_id: str
    node_id: str


class Config(BaseModel):
    """Config class"""
    interval: int
    token: str
    devices: list[Device]


def __load_yml_config__(path: str):
    """Classmethod returns YAML config"""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError as error:
        message = "Error: yml config file not found."
        raise FileNotFoundError(error, message) from error
    except yaml.YAMLError as error:
        message = "Error: yml config file is not valid."
        raise yaml.YAMLError(error, message) from error
    except Exception as error:
        message = "Error: yml config file is not valid."
        raise Exception(error, message) from error
    
def getConfig(config_file: str) -> Config:
    """Function to load YAML config file"""
    def _load_yml_config(path: str):
        return __load_yml_config__(path)
    
    # Return the parsed config
    return Config(**_load_yml_config(config_file))
    