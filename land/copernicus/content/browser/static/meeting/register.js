$(document).ready(function() {
  (function(){
    var elem_choice = document.getElementById('choice');
    var elem_register = document.getElementById('form-register');

    var show_registration = function(preserve_history) {
      $("p.info-on-create-account").show();
      $("p.info-login-or-create").hide();
      $(elem_register).fadeIn();
      $(elem_choice).hide();
      var new_url = document.location.search ?
        document.location.href.split(document.location.search)[0] + '?form=register' :
        document.location.href + '?form=register';
      if (!preserve_history) {
        history.pushState(
          { action: 'show_registration' },
          'Show registration form.',
          new_url
        );
      }
    }

    var show_choice = function(preserve_history) {
      $("p.info-login-or-create").show();
      $("p.info-on-create-account").hide();
      $(elem_register).hide();
      $(elem_choice).fadeIn();
      var new_url = document.location.search ?
        document.location.href.split(document.location.search)[0] :
        document.location.href;
      if (!preserve_history){
        history.pushState(
          { action: 'show_choice' },
          'Show choice form.',
          new_url
        );
      }
    }

    var setup_pages = function() {
      window.addEventListener('popstate', function(evt) {
        evt.state ? ns[evt.state.action](true) : null;
      });

      if (document.location.search.indexOf('?form=register') !== -1) {
        show_registration();
      } else {
        show_choice();
      }
    }

    var widget_other = function(selector_choice, selector_other){
      var role = document.querySelector(selector_choice);
      var other = document.querySelector(selector_other);
      function update_other() {
        if (role.value === 'other') {
          other.style.display = '';
          other.setAttribute('required', 'required');
        }
        else {
          other.style.display = 'none';
          other.removeAttribute('required');
        }
      }
      update_other();
      role.addEventListener('change', update_other);
    }

    ns = {
      show_choice: show_choice,
      show_registration: show_registration,
      setup_pages: setup_pages,
      widget_other: widget_other,
    }

    window.meeting = ns;
  })()
  // Prevent multiple submitting of register form with multiple click on
  // button 'Register to this meeting' (submit.signup). Without this, duplicate
  // mail notification is sent to participant and contact person.
  $('form#form-signup').submit(function() {
    $(this).submit(function() {
      return false;
    });
    return true;
  });
});
