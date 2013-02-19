// TODO: Maybe move these to an app config file
var DOMAINS_TMPL_URL = '/static/templates/domainsTmpl.html';
var PROPOSALS_TMPL_URL = '/static/templates/proposalsTmpl.html';
var BACKER_TMPL_URL = '/static/templates/backerTmpl.html';
var LOGIN_MODAL_TMPL_URL = '/static/templates/loginTmpl.html';
var DASHBOARD_BACKER_TMPL_URL = '/static/templates/dash_backerTmpl.html';
var AUDIT_TMPL_URL = '/static/templates/auditTmpl.html';

tmplCache = {};

function fetchTmpl(url, callback)
{
    if (tmplCache[url] != undefined) {
        callback(tmplCache[url]);

        return;
    }

    $.get(url, function(tmpl) {
        tmplCache[url] = tmpl;

        callback(tmpl);
    });
}