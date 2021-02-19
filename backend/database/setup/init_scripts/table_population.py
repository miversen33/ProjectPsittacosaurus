import shlex

from os.path import exists
from pathlib import Path
from subprocess import run
import subprocess

from flask import current_app as app

def populate_tables():
    '''
    Runs any script (except for sql files) that is in the 'DB_POPULATION_SCRIPTS_LOCATIONS' directory.

    When the script is run, it will be provided with a valid database URI in order to connect to the current database to populate.

    NOTE: This will not run the __init__.py, if that script exists
    '''
    _THREAD_LIMIT = 4
    _EXCLUSION_EXTENSIONS = ['.sql']
    
    db_uri = app.config.get('DATABASE_URI', '')
    if not db_uri:
        print('Unable to find database connection!')
        return
    db_uri = db_uri.replace('!', '\\!').replace('$', '\\\$')
    init_files_path: Path = app.config.get('DB_POPULATION_SCRIPTS_LOCATIONS', '')
    if not init_files_path:
        # TODO(Mike): Logging?
        print('No init files found')
        return
    if not isinstance(init_files_path, Path):
        print('Invalid init_files_path. Attempting manual conversion...')
        init_files_path = Path(init_files_path)
    if not exists(init_files_path.resolve()):
        print('init_files_path location not found')
        return
    scripts = list(init_files_path.glob('**/*'))
    if not scripts:
        print('No init scripts found')
        return

    for script in scripts:
        #TODO(Mike): Implement multithreading to make this go faster. No reason to have this be stuck in a single thread when the scripts are not dependent on each other
        if script.suffix in _EXCLUSION_EXTENSIONS and script.name != '__init__.py':
            continue
        cmd = f'/bin/sh -c "{script.resolve()} {db_uri}"'
        completed_process: subprocess.CompletedProcess = run(shlex.split(cmd))
        if completed_process.returncode != 0:
            # TODO(Mike): Logger
            print(f'Unable to complete {script.name}')