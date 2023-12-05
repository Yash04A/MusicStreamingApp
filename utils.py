import os

def uploadData(file, loc, file_name):
    if not os.path.exists(loc):
        os.makedirs(loc)
    new_file_path = os.path.join(loc, file_name)

    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    file.save(new_file_path)
    relative_path = os.path.relpath(new_file_path, start='static').replace(os.path.sep,'/')


    return relative_path


