import pickle


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def save_objects(objs, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        for obj in objs:
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)