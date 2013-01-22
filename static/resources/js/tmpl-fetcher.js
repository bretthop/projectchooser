// TODO: Maybe move these to an app config file
var PROPOSALS_TMPL_URL = '/static/templates/proposalsTmpl.html';
var BACKER_TMPL_URL = '/static/templates/backerTmpl.html';

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