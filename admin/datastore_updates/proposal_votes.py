import logging
from app.data.models import Vote
from app.services.BackerService import BackerService
from google.appengine.ext import deferred
from google.appengine.ext import db

BATCH_SIZE = 5  # ideal batch size may vary based on entity size.

def AddBackerToProposalVotes(cursor=None, num_updated=0):
    """
    Function finds all Votes where Vote.Backer is None (added post-production)
    and updates it with Backer based on Vote.userId value

    :rtype: None
    :type cursor: Query Cursor (used by subsequent cycle runs)
    :type num_updated: number of already updated records during previous cycles
    """
    query = Vote.all()

    if cursor:
        query.with_cursor(cursor)

    to_put = []

    for v in query.fetch(limit=BATCH_SIZE):
        if v.backer is None:
            _voteBacker = BackerService().GetBackerByEmail(v.userId)
            v.backer = _voteBacker
            to_put.append(v)

    if to_put:
        db.put(to_put)
        num_updated += len(to_put)
        logging.debug('Put %d entities to Datastore for a total of %d', len(to_put), num_updated)

        deferred.defer(AddBackerToProposalVotes, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug('AddBackerToProposalVotes complete with %d updates!', num_updated)



def RemoveVoteUserId(cursor=None, num_updated=0):
    """
    Function finds all Votes where Vote.Backer is not None (added post-production)
    and removed its userId property

    :rtype: None
    :type cursor: Query Cursor (used by subsequent cycle runs)
    :type num_updated: number of already updated records during previous cycles
    """
    query = Vote.all()

    if cursor:
        query.with_cursor(cursor)

    to_put = []

    for v in query.fetch(limit=BATCH_SIZE):
        if v.backer is not None:
            delattr(v, 'userId')
            to_put.append(v)
            pass

    if to_put:
        db.put(to_put)
        num_updated += len(to_put)
        logging.debug('Put %d entities to Datastore for a total of %d', len(to_put), num_updated)

        deferred.defer(RemoveVoteUserId, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug('RemoveVoteUserId complete with %d updates!', num_updated)
