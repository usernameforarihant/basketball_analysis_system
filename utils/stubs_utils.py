import os
import pickle

def save_stubs(stub_path, obj):
    """
    Saves an object to a stub file.
    
    Args:
        stub_path (str): Path to the stub file.
        obj: The object to be saved.
    """
    if not stub_path:
        return  # Do nothing if no path is provided

    os.makedirs(os.path.dirname(stub_path), exist_ok=True)
    with open(stub_path, 'wb') as f:
        pickle.dump(obj, f)


def read_stubs(read_from_stub,stub_path):  
    if read_from_stub and stub_path is not None and os.path.exists(stub_path):
        with open(stub_path, 'rb') as f:
            object= pickle.load(f)
            return object
    return None