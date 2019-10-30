from multiprocessing.dummy import Pool as ThreadPool
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from ovp.apps.projects.models import Project
from ovp.apps.digest.emails import DigestEmail
from ovp.apps.digest.models import DigestLog
from ovp.apps.digest.models import DigestLogContent
from ovp.apps.digest.models import PROJECT
from ovp.apps.users.models import User
from ovp.apps.search.filters import UserSkillsCausesFilter
from ovp.apps.uploads import helpers
from django.db.models import Value, IntegerField

import math
import time


############
## Config ##
############
# TODO: Migrate this to django settings
config = {
  'interval': {
    'minimum': 60 * 60 * 24 * 6,
    'maximum': 0
  },
  'projects': {
    'minimum': 1,
    'maximum': 6,
    'max_age': 60 * 60 * 24 * 7 * 4,
  }

}

###############
## Querysets ##
###############




######################
## Generate content ##
######################


##############
## Triggers ##
##############
