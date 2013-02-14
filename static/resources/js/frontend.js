/* Setup front end event handlers */
var addProposalValidator = $("form").validate({
    errorPlacement: function(error, element) {
        //Override errorPlacement function (this stops the automatic 'This field is required' message from showing)
        return true;
    }
});

var signUpValidator = $("form#signUp").validate({
    errorPlacement: function(error, element) {
        //Override errorPlacement function (this stops the automatic 'This field is required' message from showing)
        return true;
    }
});

$('#addProposalModal').on('hide', function () {
    addProposalValidator.resetForm();
    $('#addProposalModal').find('input').val('');
});

var addDomainValidator = $("form").validate({
    errorPlacement: function(error, element) {
        //Override errorPlacement function (this stops the automatic 'This field is required' message from showing)
        return true;
    }
});
$('#addDomainModal').on('hide', function () {
    addDomainValidator.resetForm();
    $('#addDomainModal').find('input').val('');
});

ajax.setAjaxLoader($('.ajax-loader'));

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
    var formValid = signUpValidator.form();

    if (formValid) {
        signUp();
    }
}

function handleLoginClick()
{
    var email    = $('#email').val();
    var password = $('#password').val();

    login(email, password)
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