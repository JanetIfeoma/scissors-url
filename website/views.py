from flask import Blueprint,redirect,render_template,request,flash,url_for, send_file
from flask_login import login_required,current_user
from .models import Link
from . import db
from qrcode import make as make_qrcode
import io

views= Blueprint("views", __name__)

@views.route("/", methods=['GET', 'POST'])
@views.route("/home")
@login_required
def home():
    link = None  # Initialize the variable to None
    if request.method == 'POST':
        # Handle the form submission and create the link
        link_url = request.form.get('link')
        if len(link_url) < 1:
            flash("Link is too short!", category="error")
        else:
            new_link = Link(data=link_url, user_id=current_user.id)
            db.session.add(new_link)
            db.session.commit()
            flash("Link added!", category="success")
            link = new_link  # Assign the created link to the variable
    
    qr_code_url = url_for("views.generate_qr_code", short_url="your_short_url_here")
    return render_template("home.html", user=current_user, qr_code_url=qr_code_url, link=link)


@views.route('/<short_url>')
def redirect_to_url(short_url):
    link=Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits= link.visits +1
    db.session.commit()

    return redirect(link.original_url)

@views.route('/add_link', methods=['POST'])
@login_required
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url, user_id=current_user.id)
    db.session.add(link)
    db.session.commit()
    return render_template('link_added.html', user=current_user, new_link=link.short_url, original_url=link.original_url)


@views.route('/generate_qr/<short_url>')
def generate_qr_code(short_url):    
    link = Link.query.filter_by(short_url=short_url, user_id=current_user.id).first()
    if link:
        # Generate the QR code image
        qr_code = make_qrcode(short_url)
        
        # Create an in-memory stream to store the image data
        img_stream = io.BytesIO()
        
        # Save the QR code image to the stream
        qr_code.save(img_stream, "PNG")
        
        # Set the stream position to the beginning
        img_stream.seek(0)
        
        # Return the image file as a response
        return send_file(img_stream, mimetype="image/png")
    else:
        return "Short URL not found"


@views.route('/stats')
@login_required
def stats():
    links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('stats.html', links=links, user=current_user)


@views.route('/link_history')
@login_required
def link_history():
    links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('link_history.html', links=links, user=current_user)



@views.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', user=current_user), 404
