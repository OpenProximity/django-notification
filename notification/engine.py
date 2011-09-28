
import sys
import time
import logging
import traceback

try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.core.mail import mail_admins
from django.contrib.auth.models import User

from notification import NOTIFICATION_USE_SITE, NOTIFICATION_DEFAULT_SITE_NAME, NOTIFICATION_LOCK_WAIT_TIMEOUT

if NOTIFICATION_USE_SITE:
    from django.contrib.sites.models import Site
else:
    Site = None

from lockfile import FileLock, AlreadyLocked, LockTimeout

from notification.models import NoticeQueueBatch
from notification import models as notification

def send_all():
    lock = FileLock("send_notices")

    logging.debug("acquiring lock...")
    try:
        lock.acquire(NOTIFICATION_LOCK_WAIT_TIMEOUT)
    except AlreadyLocked:
        logging.debug("lock already in place. quitting.")
        return
    except LockTimeout:
        logging.debug("waiting for the lock timed out. quitting.")
        return
    logging.debug("acquired.")

    batches, sent = 0, 0
    start_time = time.time()

    try:
        # nesting the try statement to be Python 2.4
        try:
            for queued_batch in NoticeQueueBatch.objects.all():
                notices = pickle.loads(str(queued_batch.pickled_data).decode("base64"))
                for user, label, extra_context, on_site in notices:
                    user = User.objects.get(pk=user)
                    logging.info("emitting notice to %s" % user)
                    # call this once per user to be atomic and allow for logging to
                    # accurately show how long each takes.
                    notification.send_now([user], label, extra_context, on_site)
                    sent += 1
                queued_batch.delete()
                batches += 1
        except:
            # get the exception
            exc_class, e, t = sys.exc_info()
            # email people
            
            if NOTIFICATION_USE_SITE:
               name = Site.objects.get_current().name
           elif NOTIFICATION_DEFAULT_SITE_NAME:
               name = NOTIFICATION_DEFAULT_SITE_NAME
           else:
               # don't display None, display just a space
               name = ""

           subject = "[%s emit_notices] %r" % (name, e)
               
            message = "%s" % ("\n".join(traceback.format_exception(*sys.exc_info())),)
            mail_admins(subject, message, fail_silently=True)
            # log it as critical
            logging.critical("an exception occurred: %r" % e)
    finally:
        logging.debug("releasing lock...")
        lock.release()
        logging.debug("released.")
    
    logging.info("")
    logging.info("%s batches, %s sent" % (batches, sent,))
    logging.info("done in %.2f seconds" % (time.time() - start_time))
