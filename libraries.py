from subprocess import PIPE, STDOUT, run
import pkg_resources

def missing_libs():
  required = {'tkinter', 'datetime', 'sqlite3', 'hashlib', 'hmac', 'secrets', 'sys', 'subprocess', 'pkg_resources'}
  installed = {f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set}

  missing = required - installed
  print('Checking missing libraries ...')

  if missing is True:
    print(f"Installing missing libraries {required}")
    run(f'pip install --ignore-installed {" ".join([*missing])}', stdout=PIPE, stderr=STDOUT, shell=True, text=True)
  
  print('All libraries installed ...')

  return missing