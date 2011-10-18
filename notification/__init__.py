VERSION = (0, 1, 5, "final")

def get_version():
    if VERSION[3] != "final":
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])
    else:
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()

try:
    from django.conf import settings

    # default configuration
    NOTIFICATION_DEFAULT_SITE_NAME = getattr(settings, 
                                             'NOTIFICATION_DEFAULT_SITE_NAME', 
                                             'Django Notifications')
    NOTIFICATION_USE_SITE = getattr(settings, 'NOTIFICATION_USE_SITE', False)
    NOTIFICATION_QUEUE_ALL = getattr(settings, "NOTIFICATION_QUEUE_ALL", False)
    NOTIFICATION_LANGUAGE_MODULE = getattr(settings, 
                                           'NOTIFICATION_LANGUAGE_MODULE', False)
    NOTIFICATION_FEEDS = getattr(settings, "NOTIFICATION_FEEDS", False)
    NOTIFICATION_LOCK_WAIT_TIMEOUT = getattr(settings, 
                                             "NOTIFICATION_LOCK_WAIT_TIMEOUT", 
                                             -1)
    NOTIFICATION_ITEMS_PER_FEED = getattr(settings, 
                                          'NOTIFICATION_ITEMS_PER_FEED', 20)
    DEFAULT_HTTP_PROTOCOL = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
except:
    pass



