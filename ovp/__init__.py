
def get_core_apps():
  """ Get core ovp apps list.

  Returns:
    list: A list with all ovp apps to be appended to INSTALLED_APPS on settings.py
  """
  CORE_APPS = [
    # External essentials
    "haystack",
    "vinaigrette",
    "corsheaders",
    'jet',
    'jet.dashboard',

    # OVP
    "ovp.apps.core",
    "ovp.apps.uploads",
    "ovp.apps.users",
    "ovp.apps.projects",
    "ovp.apps.organizations",
    "ovp.apps.faq",
    "ovp.apps.search",
    "ovp.apps.channels",
    "ovp.apps.catalogue",
  ]

  return CORE_APPS
