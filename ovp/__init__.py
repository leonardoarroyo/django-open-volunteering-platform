
def get_core_apps():
  """ Get core ovp apps list.

  Returns:
    list: A list with all ovp apps to be appended to INSTALLED_APPS on settings.py
  """
  CORE_APPS = [
    "ovp.apps.core"
  ]

  return CORE_APPS
