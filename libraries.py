import pkg_resources

def missing_libs():
  required = {'tkinter', 'datetime', 'sqlite3', 'hashlib', 'hmac', 'secrets', 'sys', 'subprocess', 'pkg_resources'}
  installed = {f"{pkg.key}=={pkg.version}" for pkg in pkg_resources.working_set}

  missing = required - installed

  return missing