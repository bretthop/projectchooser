import logging
from app.data.models import *
from app.services.AuditService import AuditService
from google.appengine.ext import deferred

BATCH_SIZE = 5  # ideal batch size may vary based on entity size.

def forDomains(cursor=None, num_updated=0):
    """
    Finds all Domains and adds auditing information for them

    :rtype: None
    :type cursor: Query Cursor (used by subsequent cycle runs)
    :type num_updated: number of already updated records during previous cycles
    """
    _auditService = AuditService()
    query = Domain.all()

    if cursor:
        query.with_cursor(cursor)

    num_processed = 0

    for d in query.fetch(limit=BATCH_SIZE):
        num_processed += 1
        _auditService.AuditAddDomain(d)

    if num_processed > 0:
        num_updated += num_processed
        logging.debug('Audited %d Domains for a total of %d', num_processed, num_updated)

        deferred.defer(forDomains, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug('initAuditingForDomains complete with %d updates!', num_updated)

def forProposals(cursor=None, num_updated=0):
    """
    Finds all Proposals and adds auditing information for them

    :rtype: None
    :type cursor: Query Cursor (used by subsequent cycle runs)
    :type num_updated: number of already updated records during previous cycles
    """
    _auditService = AuditService()
    query = Proposal.all()

    if cursor:
        query.with_cursor(cursor)

    num_processed = 0

    for p in query.fetch(limit=BATCH_SIZE):
        num_processed += 1
        _auditService.AuditAddProposal(p)

    if num_processed > 0:
        num_updated += num_processed
        logging.debug('Audited %d Proposals for a total of %d', num_processed, num_updated)

        deferred.defer(forProposals, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug('initAuditingForProposals complete with %d updates!', num_updated)