def get_file_type_from_extension(ext):
    ext_to_file = {
        'py': 'python',
        'c': 'c',
        'cs': 'csharp',
    }
    return ext_to_file.get(ext)

