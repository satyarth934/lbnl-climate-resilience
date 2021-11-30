import sys
import yaml


def parse_input_yaml(yaml_path: str) -> dict:
    """Returns the yaml file content as dictionary.
    
    Args:
        yaml_path (str): Path to the YAML configuration file.
    
    Returns:
        dict: Dictionary of all the YAML configuration parameters.
    """
    
    yaml_vals = yaml.load(open(yaml_path, "r"), Loader=yaml.FullLoader)
    return yaml_vals


def stall():
    """Can be used in a loop for debugging.
    Stalls the current iteration and requires a user input to either 
    continue to the next iteration or quit the loop.
    """
    
    inp = input("Enter to continue...")
    
    if inp.lower() == 'q':
        sys.exit(0)