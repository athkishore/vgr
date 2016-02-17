from flask import render_template, redirect, request, url_for, flash
#from flask.ext.login import login_user, logout_user, login_required, \
#    current_user
from . import gis
from .. import db
from flask import json
import urllib2
#from ..models import User
#from ..email import send_email
from .forms import PaddyPlotForm
#from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
#    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

@gis.route('/proxy')
def proxy():  
  allowedHosts = ['localhost:8080', '188.166.179.117:8080', 'www.openlayers.org']
  url = request.args.get('url')
  if url == "" or url is None:
    url = "http://www.openlayers.org"
      
  host = url.split("/")[2]
  if host in allowedHosts:
    response = urllib2.urlopen(url)
    feature_info = response.read()
    response.close()
    return feature_info
  else:
    print host
    return "Host not allowed"

@gis.route('/kannolichira')
def kannolichira():
  f = open('plots.csv','r')
  attr = []
  s = f.readline()
  for i in range(243):
    s = f.readline()
    t = s.split(',')
    print t[17][0]
    d = {'Id':int(t[0]),\
        'SurveyNo': t[1],
        'SubDivNo': t[2],
        'RentRoll': t[3],
        'Owner': t[4],
        'DBSvNo': t[5],
        'DBRentRoll': t[6],
        'DBOwner': t[7],
        'DBStatus': t[8],
        'Farming': int(t[9]),
        'Lease': int(t[10]),
        'Lessee': t[11],
        'LastCult': t[12],
        'NoConsent': int(t[13]),
        'Threat': int(t[14]),
        'Organic': int(t[15]),
        'Heirloom': t[16],
        'FallowBlock': int(t[17][0:len(t[17])-1])}        
    attr.append(json.dumps(t))
  f.close()
  return render_template('gis/kannolichira.html', attr=attr)  

  
@gis.route('/kannolichira_edit', methods=['GET','POST'])
def kannolichira_edit():
  f = open('plots.csv','r')
  attr = []
  lines = []
  s = f.readline()
  for i in range(243):
    s = f.readline()
    lines.append(s)
    t = s.split(',')
    print t[17][0]
    d = {'Id':int(t[0]),\
        'SurveyNo': t[1],
        'SubDivNo': t[2],
        'RentRoll': t[3],
        'Owner': t[4],
        'DBSvNo': t[5],
        'DBRentRoll': t[6],
        'DBOwner': t[7],
        'DBStatus': t[8],
        'Farming': int(t[9]),
        'Lease': int(t[10]),
        'Lessee': t[11],
        'LastCult': t[12],
        'NoConsent': int(t[13]),
        'Threat': int(t[14]),
        'Organic': int(t[15]),
        'Heirloom': t[16],
        #'FallowBlock': int(t[17][0:len(t[17])-1])}        
        'FallowBlock': int(t[17][0])}
    attr.append(json.dumps(t))
  f.close()
  form = PaddyPlotForm()
  if form.validate_on_submit():
    Id = form.Id.data
    SurveyNo = form.SurveyNo.data
    SubDivNo = form.SubDivNo.data
    RentRoll = form.RentRoll.data
    Owner = form.Owner.data
    DBSvNo = form.DBSvNo.data
    DBRentRoll = form.DBRentRoll.data
    DBOwner = form.DBOwner.data
    DBStatus = form.DBStatus.data
    Farming = form.Farming.data
    Lease = form.Lease.data
    Lessee = form.Lessee.data
    LastCult = form.LastCult.data
    DenyConsent = form.DenyConsent.data
    Threat = form.Threat.data
    Organic = form.Organic.data
    Heirloom = form.Heirloom.data
    FallowBlock = form.FallowBlock.data
    f = open('plots.csv','w')
    f.write('Id,SurveyNo,SubDivNo,RentRoll,Owner,DBSvNo,DBRentRoll,DBOwner,DBStatus,Farming,Lease,Lessee,LastCult,DenyConsent,Threat,Organic,Heirloom,FallowBlock\n')
    for i in range(int(Id)-1):
      f.write(lines[i])
    f.write(Id+','+SurveyNo+','+SubDivNo+','+RentRoll+','+Owner+','+DBSvNo+','+DBRentRoll+','+DBOwner+','+DBStatus+','+str(Farming)+','+str(Lease)+','+Lessee+','+LastCult+','+str(DenyConsent)+','+str(Threat)+','+str(Organic)+','+Heirloom+','+str(FallowBlock)+'\n')
    for i in range(int(Id),243):
      f.write(lines[i])
    f.close()
    flash('Data successfully saved')
    return redirect(url_for('gis.kannolichira_edit'))
  return render_template('gis/kannolichira_edit.html', form=form, attr=attr)


'''
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
'''

