as ovp is able to serve multiple websites through channel, settings are mostly defined on the database with ChannelSetting model.
If there is no setting with a given key for a channel, ovp will attempt to read it from settings.py, if it's not declared on settings.py, the default setting will be used.

The model
----------
It's a simple key/value model. Keys are not unique, therefore there may be multiple value. Some settings make sense to have multiple value and some may not, if the setting does not support multiple values, the latest record for the channel will be used.


Common settings
-----------------
cors_origin_whitelist
=====================
Enable cors for a domain and channel pair.

Type: multi
Example: [(cors_origin_whitelist, 'domain.com'), (cors_origin_whitelist, 'www.domain.com')]
Default: []


LANGUAGE_CODE:
Used on: emails.
Todo: use language defined on default django setting

CLIENT_URL:
Used on: emails
Todo: move to channelsetting

OVP_EMAILS:
Used to: determine if email is enabled or disabled, determine email subject

ADDRESS_MODEL:
ADDRESS_SERIALIZER_TUPLE:
Used to switch between address model and serializer

MAPS_API_LANGUAGE
Used to: set maps api language

EXPIRE_PASSWORD_IN
Amount of seconds before a password expires and user has to update it.
0 should disable

USER_SEARCH_SERIALIZER
Path to user search serializer!

PROFILE_SERIALIZER_TUPLE
Path to user profile matching (ProfileCreateUpdateSerializer, ProfileRetrieveSerializer, ProfileSearchSerializer)

PROFILE_MODEL
Path to profile model

CANT_REUSE_LAST_PASSWORDS
Disable reuse of last N passwords.
0 should disable

ADMIN_MAIL
Admin email.

UNAUTHENTICATED_APPLY
Allows unauthenticated apply

CAN_CREATE_PROJECTS_IN_ANY_ORGANIZATION
Allows creating projects in any organization

CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION
Allows creating projects without organization

FILTER_OUT
Remove organization or project form search module

DEFAULT_INCLUDE_CLOSED
Include closed projects
