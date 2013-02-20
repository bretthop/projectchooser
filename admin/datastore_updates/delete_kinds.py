import logging
from app.data.models import *
from google.appengine.ext import deferred

BATCH_SIZE = 5  # ideal batch size may vary based on entity size.

def deleteAllForAuditKind(cursor=None, num_deleted=0, chained_func=None):
    """
    Deletes all entries for a given Kind. Once complete, it will
    call a callback if defined.

    :rtype: None
    :type cursor: Query Cursor (used by subsequent cycle runs)
    :type num_updated: number of already updated records during previous cycles
    """

    # TODO: Add a param called 'kind' to this function and use it instead of the following hardcoded Audit, then replace the 'clearDatabase' function with this
    query = Audit.all()

    if cursor:
        query.with_cursor(cursor)

    num_processed = 0

    for a in query.fetch(limit=BATCH_SIZE):
        num_processed += 1
        db.delete(a)

    if num_processed > 0:
        num_deleted += num_processed
        logging.info('Deleted %d Audits for a total of %d', num_processed, num_deleted)

        deferred.defer(deleteAllForAuditKind, cursor=query.cursor(), num_deleted=num_deleted, chained_func=chained_func)
    else:
        logging.info('deleteAllForKind complete with %d deletions!', num_deleted)

        if chained_func:
            deferred.defer(chained_func)