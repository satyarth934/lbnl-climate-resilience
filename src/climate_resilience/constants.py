CONST = {
    "pr": {
        "multiply": 86400,
        "add": 0
    },
    "tasmin": {
        "multiply": 1,
        "add": -273.15
    },
    "tasmax": {
        "multiply": 1,
        "add": -273.15
    },
    "pr_mean": {
        "multiply": 86400,
        "add": 0
    },
    "tasmin_mean": {
        "multiply": 1,
        "add": -273.15
    },
    "tasmax_mean": {
        "multiply": 1,
        "add": -273.15
    }
}


def geog_by_states(state: str) -> str:
    """Returns geographical region based on the input state code.
    
    Args:
        state (str): State code.
    
    Returns: 
        str: Corresponding geographical region.
        
    Raises:
        ValueError: In case the input state is not one of the valid state codes.
    """
    
    if state in ['CA','NV','AZ','NM','UT','CO']:
        return 'Southwest'
    elif state in ['WA', 'OR','ID']:
        return 'Northwest'
    elif state in ['MT','WY','ND','SD','NE']:
        return 'N. Great Plains'
    elif state in ['KS','OK','TX']:
        return 'S. Great Plains'
    elif state in ['LA','AR','TN','KY','MS','AL','GA','FL','SC','NC','VA']:
        return 'Southeast'
    elif state in ['MN','IA','MO','WI','IL','IN','MI','OH']:
        return 'Midwest'
    elif state in ['ME','VT','NH','MA','RI','CT','NJ','NY','PA','WV','MD','DE']:
        return 'Northeast'
    elif state in ['AK']:
        return 'Alaska'
    elif state in ['HI']:
        return 'Hawaii'
    elif state in ['PR', 'VI']:
        return 'Carribean'
    else:
        raise ValueError("Invalid State Code!")


def geog_by_states_code(state: str) -> int:
    """Returns geographical region code based on the input state code.
    
    Args:
        state (str): State code.
    
    Returns: 
        str: Corresponding geographical region code.
        
    Raises:
        ValueError: In case the input state is not one of the valid state codes.
    """
    
    if state in ['CA','NV','AZ','NM','UT','CO']:
        return 1
    elif state in ['WA', 'OR','ID']:
        return 2
    elif state in ['MT','WY','ND','SD','NE']:
        return 3
    elif state in ['KS','OK','TX']:
        return 4
    elif state in ['LA','AR','TN','KY','MS','AL','GA','FL','SC','NC','VA']:
        return 5
    elif state in ['MN','IA','MO','WI','IL','IN','MI','OH']:
        return 6
    elif state in ['ME','VT','NH','MA','RI','CT','NJ','NY','PA','WV','MD','DE']:
        return 7
    elif state in ['AK']:
        return 8
    elif state in ['HI']:
        return 10
    elif state in ['PR', 'VI']:
        return 9
    else:
        raise ValueError("Invalid State Code!")