import os
import sys
from flask import Flask, render_template, redirect, url_for, request, abort, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
from models import db, setup_db, User, Job
from forms import NewJobForm


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')
    setup_db(app)
    CORS(app, supports_credentials=True)
    ckeditor = CKEditor(app)
    login_manager = LoginManager()
    login_manager.login_view = 'get_login'
    login_manager.login_message = 'Please sign back in to continue'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.get('/login')
    def get_login():
        return render_template('login.html')

    @app.post('/login')
    def process_login():
        username = request.form['username']
        password = request.form['password']

        if username and password:

            user = User.query.filter_by(username=username).one_or_none()

            if not user:
                flash(f'User not found. Try again.')
                return redirect(url_for('get_login'))
            elif password != password:
                flash(f'Incorrect password. Try again.')
                return redirect(url_for('get_login'))
            else:
                session['username'] = user.username
                session['privileges'] = user.privileges
                login_user(user, remember=True)
                return redirect(url_for('index'))
        else:
            flash(f'Please enter username and password.')
            return redirect(url_for('get_login'))

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        session.pop('privileges', None)
        logout_user()
        return redirect(url_for('index'))

    @app.get('/')
    def index():
        data = Job.query.filter_by(is_approved=True)

        jobs = [job.format() for job in data]
        return render_template('index.html', jobs=jobs, current_user=current_user, session=session)

    @app.get('/<company>/<job_name>')
    def get_job(company, job_name):
        job = Job.query.filter_by(company=company, job_title=job_name).first()
        return render_template('job.html', job=job, current_user=current_user, session=session)

    @app.get('/new-job')
    @login_required
    def get_job_form():
        form = NewJobForm()
        return render_template('newjob.html', form=form, current_user=current_user, session=session)

    @app.post('/new-job')
    def process_job_form():
        form = NewJobForm()

        if form.validate_on_submit():
            company_img = form.company_img.data
            filename = secure_filename(company_img.filename)

            file_path = os.path.join(app.config['COMPANY_IMGS'], filename)
            company_img.save(file_path)
            try:
                new_job = Job(
                    company=form.company.data,
                    company_img=file_path,
                    job_title=form.job_title.data,
                    job_description=form.job_description.data
                )
                new_job.insert()
                flash(f'Job opening submitted for review')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                print(sys.exc_info())
                flash(f'Something went wrong, try again.')
                return redirect(url_for('index'))
            finally:
                db.session.close()
        else:
            for field, message in form.errors.items():
                flash(field.replace('_', ' ').title() +
                      ' - ' + str(message), 'danger')
            return redirect(url_for('get_job_form'))

    @app.get('/job-submissions')
    def get_pending_jobs():
        data = Job.query.filter_by(is_approved=False)

        jobs = [job.format() for job in data]
        return render_template('pendingjobs.html', jobs=jobs, session=session, current_user=current_user)

    @app.get('/approve-job/<job_id>')
    def approve_job(job_id):
        job = Job.query.get(job_id)
        if job:
            try:
                job.is_approved = True

                job.update()
                flash(
                    f'{job.job_title.title()} by {job.company.title()} opening has been approved.')
                return redirect(url_for('get_pending_jobs'))
            except:
                db.session.rollback()
                flash(
                    f'Something went wrong could not approve {job.job_title.title()} by {job.company.title()}. Try again.')
                return redirect(url_for('get_pending_jobs'))
            finally:
                db.session.close
        return

    @app.get('/reject-job/<job_id>')
    def reject_job(job_id):
        job = Job.query.get(job_id)
        if job:
            try:
                job.delete()
                flash(
                    f'{job.job_title.title()} by {job.company.title()} opening has been rejected.')
                return redirect(url_for('get_pending_jobs'))
            except:
                db.session.rollback()
                flash(
                    f'Something went wrong could not reject {job.job_title.title()} by {job.company.title()}. Try again.')
                return redirect(url_for('get_pending_jobs'))
            finally:
                db.session.close
        return
    return app
