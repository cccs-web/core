from .dev import *

SITE_TITLE = 'Local Cross-Cultural Consulting'
SITE_TAGLINE = None

# Overwrite AWS settings depending upon what I'm up to
# AWS_OVERRIDES is set in my secrets.py. It overrides
# AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY
# Can't do this in secrets.py because other settings set the values.
globals().update(AWS_OVERRIDES)
