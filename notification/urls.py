from django.conf.urls.defaults import *
from notification import NOTIFICATION_FEEDS

from notification.views import notices, mark_all_seen, single, archive, delete, delete_all

urlpatterns = patterns('',
    url(r'^$', notices, name="notification_notices"),
    url(r'^(?P<id>\d+)/$', single, name="notification_notice"),
    url(r'^mark_all_seen/$', mark_all_seen, name="notification_mark_all_seen"),
    url(r'^delete_all/$', delete_all, name="notification_delete_all"),
    url(r'^archive/(?P<noticeid>\d+)/$', archive, name="notification_archive"),
    url(r'^delete/(?P<noticeid>\d+)/$', delete, name="notification_delete"),
)

if NOTIFICATION_FEEDS:
    from notification.views import feed_for_user
    urlpatterns.append(url(r'^feed/$', feed_for_user, name="notification_feed_for_user"))
