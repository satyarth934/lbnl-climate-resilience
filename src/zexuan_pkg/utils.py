import sys
import yaml
import time


#########################
# GENERAL PURPOSE UTILS #
#########################

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
    
    inp = input("Press [q|Q] to quit OR Enter to continue... ")
    
    if inp.lower() == 'q':
        sys.exit(0)

    
class ExecTimeCM(object):
    """Context manager to be used with the 'with' clause 
    to get the execution time of a code block.
    
    Example Usage:
        with ExecTimeCM() as st:
            print("sample code block.")
    """
    
    def __init__(self, txt="", verbose=True):
        self.txt = txt
        self.verbose = verbose
        self.description = f"EXECUTION TIME for {self.txt}"
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.exec_time = time.time() - self.start
        if self.verbose:
            print(f"{self.description}: {self.exec_time} seconds")

        
def warning_format(msg, *args, **kwargs):
    """Used to generate warnings within code.
    Prints the warning in the following format:
    <script>:<n>: <type of warning>: <warning msg>
    
    'n' is the line number of initiated warning command within the script
    
    Example Usage:
        import warnings
        warnings.formatwarning = warning_format
        warnings.warn("<Warning msg>")
    """
    
    return f"{args[1]}:{args[2]}: {args[0].__name__}: {str(msg)}\n"
    
    
