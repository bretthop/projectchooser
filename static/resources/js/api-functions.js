function addDomain()
{
    var valid = $('form#addDomain').validate().form();

    if (valid) {
        ajax.showAjaxLoader();

        var data = {
            title: $('#title').val(),
            description: $('#description').val()
        };

        ajax.req({method: 'post', url: '/api/domains', data: data, dataType: DataType.JSON, doneCallback: function() { loadDomains(); }});

        return true;
    }
    else {
        return false;
    }
}

function addProposal()
{
    var valid = $('form#addProposal').validate().form();

    if (valid) {
        ajax.showAjaxLoader();

        var data = {
            name: $('#name').val(),
            description: $('#description').val(),
            technologiesUsed: $('#technologiesUsed').val(),
            domain: {
                id: $('#domainId').val()
            }
        };

        ajax.req({method: 'post', url: '/api/proposals', data: data, dataType: DataType.JSON, doneCallback: function() { loadProposals(); }});

        return true;
    }
    else {
        return false;
    }
}

function withdraw(voteId)
{
    ajax.showAjaxLoader();

    ajax.req({method: 'delete', url: '/api/votes?voteId=' + voteId, doneCallback: function() { loadProposals(); }});
}

function vote(proposalId, weight)
{
    ajax.showAjaxLoader();

    ajax.req({method: 'post', url: '/api/votes?proposalId=' + proposalId + '&weight=' + weight, doneCallback: function() { loadProposals(); }});
}

function signUp()
{
    ajax.showAjaxLoader();
    $('#signUpFailText').hide();

    var user = {
        email: $('form#signUp #email').val(),
        username: $('form#signUp #username').val(),
        password: $('form#signUp #password').val()
    };

    var doneCallback = function(data)
    {
        session.setUser(data[0], user.password);

        window.location = '/';
    };

    var failCallback = function()
    {
        // TODO: Check for response code to make sure that this is the proper error (ATM this is the only error that can occur)
        ajax.hideAjaxLoader();

        $('#signUpFailText').show();
    };

    ajax.req({method: 'post', url: '/api/backers', authenticate: false, data: user, dataType: DataType.JSON, doneCallback: doneCallback, failCallback: failCallback});
}

function login(email, pass)
{
    ajax.showAjaxLoader();
    $('.loginResult').addClass('hidden');

    var successFunc = function(users) {
        var user = users[0];

        session.setUser(user, pass);

        ajax.hideAjaxLoader();

        $('.loginResult').html('Success!')
            .addClass('text-success')
            .removeClass('hidden');

        var loginCallback = globalVars.loginCallback;

        if (loginCallback) {
            loginCallback();
        }

        hideLoginModal();
    };

    var errorFunc = function() {
        session.clearUser();

        ajax.hideAjaxLoader();

        $('.loginResult')
            .html('Failed!')
            .addClass('text-error')
            .removeClass('hidden');
    };

    ajax.req({method: 'post', url: '/api/login', email: email, password: pass, doneCallback: successFunc, failCallback: errorFunc});
}

function logout()
{
    session.clearUser();
    window.location = '/';
}

function loadDomains()
{
    if (!session.isUserLoggedIn()) {
        globalVars.loginCallback = loadDomains;

        showLoginModal();

        return;
    }

    ajax.showAjaxLoader();

    resetAddDomainForm();

    loadAudits();

    loadWinningProposals();

    fetchTmpl(DASHBOARD_BACKER_TMPL_URL, function(tmpl) {
        var renderedHtml = _.template(tmpl, session.currentUser());
        $('.backerTmpl-rendered').html(renderedHtml);
    });

    ajax.req({method: 'get', url: '/api/domains?filter=Domain(*)~Proposal(name)', doneCallback: function(domains)
    {
        //TODO: Apply current backer information to the returned list of domains
        //applyCurrentBackerContext(domains, backer);

        //TODO: Sort the domains by total rating descending
        //domains.sort(function(a, b) { return a.rating < b.rating; });

        fetchTmpl(DOMAINS_TMPL_URL, function(tmpl) {
            var renderedHtml = _.template(tmpl, { domains: domains, currentBacker: null });
            $('.domainsTmpl-rendered').html(renderedHtml);

            ajax.hideAjaxLoader();
        });
    }});

}

function loadAudits()
{
    fetchTmpl(AUDIT_TMPL_URL, function(tmpl) {
        ajax.req({method: 'get', url: 'api/audits?filter=Audit(message,dateCreated)', doneCallback: function(audits){
            var renderedHtml = _.template(tmpl, {audits: audits});
            $('.auditTmpl-rendered').html(renderedHtml);
        }});
    });
}

function loadWinningProposals()
{
    fetchTmpl(WINNING_PROPOSALS_TMPL_URL, function(tmpl) {
        ajax.req({method: 'get', url: 'api/proposals/winning?filter=Proposal(name,totalRating)', doneCallback: function(responseItems){
            var renderedHtml = _.template(tmpl, {proposals: responseItems});
            $('.winningProposalsTmpl-rendered').html(renderedHtml);
        }});
    });
}

function loadProposals()
{
    // Make sure the user is logged in
    if (!session.isUserLoggedIn()) {
        globalVars.loginCallback = loadProposals;

        showLoginModal();

        return;
    }

    ajax.showAjaxLoader();

    var searchParams = location.search.split('?')[1];
    globalVars.domainId = extractSearchParamValue(searchParams, 'domainId');

    resetAddProposalForm();

    loadAudits();

    var backer = session.currentUser();

    ajax.req({method: 'get', url: '/api/backerVotes', data: {backerId: backer.id}, doneCallback: function(remainingVotes) {
        backer.remainingVotes = remainingVotes;

        fetchTmpl(BACKER_TMPL_URL, function(tmpl) {
            var renderedHtml = _.template(tmpl, backer);
            $('.backerTmpl-rendered').html(renderedHtml);

            //Filter the requested data on only the fields we need
            var proposalsFilterQuery = 'filter=Proposal(*)~Vote(*)~VoteType(*)~Backer(username,email)';
            var proposalsData = searchParams + '&' + proposalsFilterQuery;

            ajax.req({method: 'get', url: '/api/proposals', data: proposalsData, doneCallback: function(proposals) {
                //Apply current backer information to the returned list of proposals
                applyCurrentBackerContext(proposals, backer);

                //Sort the proposals by rating descending
                proposals.sort(function(a, b) { return a.rating < b.rating; });

                fetchTmpl(PROPOSALS_TMPL_URL, function(tmpl) {
                    var renderedHtml = _.template(tmpl, { proposals: proposals, currentBacker: backer });
                    $('.proposalsTmpl-rendered').html(renderedHtml);

                    ajax.hideAjaxLoader();
                });
            }});
        });
    }});
}

/**
 * Adds context information to a list of proposals based on the currently logged in backer.
 *
 * It also sums up all the vote weights for each proposal
 *
 * @param proposals
 * @param currentBacker
 */
function applyCurrentBackerContext(proposals, currentBacker)
{
    for (var i = 0; i < proposals.length; i++) {
        var proposal = proposals[i];

        var rating = 0;
        var hasUserVoted = false;
        var userVote = null;

        for (var j = 0; j < proposal.votes.length; j++) {
            var vote = proposal.votes[j];

            rating += vote.voteType.weight;

            if (vote.backer && vote.backer.email == currentBacker.email) {
                hasUserVoted = true;
                userVote = vote;
            }
        }

        proposal.rating = rating;
        proposal.hasUserVoted = hasUserVoted;
        proposal.userVote = userVote;
    }
}

/**
 * Returns the number of votes that have a quantity greater than zero
 * @param votes
 * @return {Number}
 */
function countRemainingVotes(votes)
{
    return _.filter(votes, function(vote) {
        return vote.quantity > 0;
    }).length;
}

/**
 * Converts to start case. E.g. "GOLD" => "Gold", "gold" => "Gold"
 * @param str
 * @return {String}
 */
function toStartCase(str)
{
    return str.substr(0, 1) + str.toLowerCase().substring(1);
}

/**
 * Extracts URL search parameter value
 * @param searchParams all search key-value params (everything after '?')
 * @param paramKey parameter key
 * @return {String}
 */
function extractSearchParamValue(searchParams, paramKey)
{
    var result = '';
    searchParams = searchParams.split('&');

    for (var i=0; i<searchParams.length; i++)
    {
        if (searchParams[i].split('=')[0] == paramKey)
        {
            result = searchParams[i].split('=')[1];
        }
    }

    return result;
}