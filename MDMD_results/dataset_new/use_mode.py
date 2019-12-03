
USE_MODE = 'all'



mode = ['all', 'generate', 'use', 'evaluate']
if USE_MODE not in mode:
    raise Exception('Eorror! "mode" only has five options: {}.'.format(str(mode).strip('[').strip(']')))