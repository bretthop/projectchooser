/* Setup front end event handlers */
$.validator.setDefaults({
    errorPlacement: function(error, element) {
        //Override errorPlacement function (this stops the automatic 'This field is required' message from showing)
        return true;
    }
});

$('#addProposalModal').on('hide', function () {
    $('form#addProposal').validate().resetForm();
    $('#addProposalModal').find('input').val('');
});

$('#addDomainModal').on('hide', function () {
    $('form#addDomain').validate().resetForm();
    $('#addDomainModal').find('input').val('');
});

ajax.setAjaxLoaderSelector('.ajax-loader');

function showAddDomainModal()
{
    $('#addDomainModal').modal();
}
function handleAddDomainClick()
{
    var success = addDomain();

    if (success) {
        $('#addDomainModal').modal('hide');
    }
}

function showAddProposalModal()
{
    $('#addProposalModal').find('#domainId').val(globalVars.domainId);
    $('#addProposalModal').modal();
}

function handleAddProposalClick()
{
    var success = addProposal();

    if (success) {
        $('#addProposalModal').modal('hide');
    }
}

function handleSignUpClick()
{
    var formValid = $('form#signUp').validate().form();

    if (formValid) {
        signUp();
    }
}

function handleLoginClick()
{
    var formValid = $('form#login').validate().form();

    if (formValid) {
        var email    = $('#email').val();
        var password = $('#password').val();

        login(email, password)
    }
}

function resetAddDomainForm()
{
    $('#addDomainModal #title').val('');
    $('#addDomainModal #description').val('');
}

function resetAddProposalForm()
{
    $('#name').val('');
    $('#description').val('');
    $('#technologiesUsed').val('');
}

function showLoginModal()
{
    fetchTmpl(LOGIN_MODAL_TMPL_URL, function(tmpl)
    {
        if ($('#loginModalHolder').length == 0) {
            $('body').append($('<div id="loginModalHolder"></div>'));
        }

        // Set the login template into the dom
        $('#loginModalHolder').html(tmpl);

        $('#loginModal').modal();
    });
}

function hideLoginModal()
{
    $('#loginModal').modal('hide');
}