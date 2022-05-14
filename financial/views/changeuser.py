from flask import render_template, session
from flask_login import login_required
from werkzeug.security import generate_password_hash

from financial.service.users import update_user
from financial.views import financial, WTForm


@financial.route("/change", methods=["POST", "GET"])
@login_required
def change():
    if not session['superuser']:
        return render_template('404.html')
    return render_template('change.html', user=session["user"], superuser=session["superuser"]
                           )


@financial.route('/users/edit/<string:UUID>', methods=['GET', "POST"])
@login_required
def edit_employee(UUID):
    """
    This function represents the logic on /employees/edit address
    :return: the rendered employee.html template to edit an existing employee
    """

    # load employee.html template
    if not session['superuser']:
        return render_template('404.html')
    else:
        form = WTForm.Register()
        if form.validate_on_submit():
            update_user(UUID, form.username.data, generate_password_hash(form.password.data))
            return render_template('change.html', user=session["user"], superuser=session["superuser"]
                                   )

    return render_template('user.html', form=form, user=session["user"], superuser=session["superuser"]
                           )
