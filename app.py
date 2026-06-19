import os
import json
import hashlib
import secrets
import string
import datetime
import numpy as np
from flask import Flask, request, jsonify, session
from flask_cors import CORS

# ==========================================
# LOAD .env FILE (if present)
# ==========================================
def load_env_file():
    """Load key=value pairs from .env file into os.environ."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        return
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip()
            if key and value and value != 'PASTE_YOUR_16_CHAR_APP_PASSWORD_HERE':
                os.environ[key] = value   # force-set every time

load_env_file()

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'fet2snn-super-secret-key-2024-change-in-production')
CORS(app, supports_credentials=True, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])


# ==========================================
# DATABASE HELPERS (JSON file-based)
# ==========================================
DB_FILE = os.path.join(os.path.dirname(__file__), 'auth_db.json')

def load_db():
    """Load the auth database from disk."""
    if not os.path.exists(DB_FILE):
        data = {"users": {}, "sessions": {}, "reset_tokens": {}}
        save_db(data)
        return data
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    """Persist the auth database to disk."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def hash_password(password: str) -> str:
    """Hash a password with a random salt using SHA-256."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash."""
    try:
        salt, hashed = stored_hash.split(':', 1)
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
    except Exception:
        return False

def generate_token(length=32) -> str:
    """Generate a secure random token."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ==========================================
# SEED DEFAULT DEMO ACCOUNTS ON FIRST RUN
# ==========================================
def seed_demo_users():
    db = load_db()
    if not db['users']:
        demo_accounts = [
            {
                'email': 'demo@fet2snn.com',
                'password': 'manoj123',
                'fullName': 'Demo User',
                'firstName': 'Demo',
                'role': 'Guest Researcher',
                'institution': 'FET2SNN Platform',
                'stats': {'projects': 3, 'inferences': 15, 'collaborators': 4},
                'joinDate': 'June 2024',
            },
            {
                'email': 'dr.sarah@mit.edu',
                'password': 'manoj123',
                'fullName': 'Dr. Sarah Chen',
                'firstName': 'Sarah',
                'role': 'Lead Researcher',
                'institution': 'MIT - Semiconductor Lab',
                'stats': {'projects': 12, 'inferences': 47, 'collaborators': 8},
                'joinDate': 'March 2024',
            },
        ]
        for acc in demo_accounts:
            pw = acc.pop('password')
            acc['password_hash'] = hash_password(pw)
            acc['created_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
            db['users'][acc['email']] = acc
        save_db(db)
        print("[AUTH] Seeded demo users.")

seed_demo_users()

# ==========================================
# STATIC PAGES
# ==========================================
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
def login_page():
    return app.send_static_file('login.html')

# ==========================================
# AUTH API - LOGIN
# ==========================================
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required.'}), 400

    db = load_db()
    user = db['users'].get(email)

    if not user:
        return jsonify({'status': 'error', 'message': 'No account found with this email. Please sign up.'}), 401

    if not verify_password(password, user.get('password_hash', '')):
        return jsonify({'status': 'error', 'message': 'Incorrect password. Please try again.'}), 401

    # Create session token
    token = generate_token(48)
    expires = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'
    if 'sessions' not in db:
        db['sessions'] = {}
    db['sessions'][token] = {'email': email, 'expires': expires}
    save_db(db)

    # Return safe user profile (no password hash)
    profile = {k: v for k, v in user.items() if k != 'password_hash'}
    profile['email'] = email

    return jsonify({
        'status': 'success',
        'message': f"Welcome back, {user.get('firstName', 'Researcher')}!",
        'token': token,
        'user': profile
    })


# ==========================================
# EMAIL HELPER
# ==========================================
def send_email(to_email: str, subject: str, html_body: str, text_body: str = ''):
    """Send an email via Gmail SMTP. Raises on failure."""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    load_env_file()
    smtp_email = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    if not smtp_email or not smtp_password:
        print(f"[EMAIL] SMTP not configured — skipping email to {to_email}")
        return False

    msg = MIMEMultipart('alternative')
    msg['From'] = f"FET2SNN Platform <{smtp_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Reply-To'] = smtp_email

    if text_body:
        msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_email, smtp_password)
    server.sendmail(smtp_email, [to_email], msg.as_string())
    server.quit()
    print(f"[EMAIL] Sent '{subject}' to {to_email}")
    return True


def send_welcome_email(email: str, first_name: str, role: str, institution: str):
    """Send a beautiful welcome email after signup."""
    subject = f"🎉 Welcome to FET2SNN, {first_name}!"
    login_url = "http://localhost:5000/login"

    html = f"""
    <html>
    <body style="margin:0;padding:0;background:#0a1628;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a1628;">
      <tr><td align="center" style="padding:40px 20px;">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#0d1f3c;border-radius:16px;border:1px solid rgba(0,212,255,0.15);overflow:hidden;font-family:Arial,sans-serif;">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#0d2b4a,#0a1628);padding:36px 40px;text-align:center;border-bottom:1px solid rgba(0,212,255,0.1);">
              <div style="font-size:28px;font-weight:800;color:#f0f4f8;letter-spacing:-0.5px;">FET2<span style="color:#00d4ff;">SNN</span></div>
              <div style="font-size:11px;color:rgba(0,212,255,0.5);letter-spacing:0.2em;text-transform:uppercase;margin-top:6px;">OneClick · One Inference</div>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:40px;">
              <p style="font-size:24px;font-weight:700;color:#f0f4f8;margin:0 0 8px;">🎉 Welcome aboard, {first_name}!</p>
              <p style="font-size:14px;color:rgba(240,244,248,0.6);margin:0 0 28px;line-height:1.6;">
                Your FET2SNN account has been created successfully. You're now part of the world's leading 
                TCAD-to-SNN research ecosystem.
              </p>
              <!-- Account Info Card -->
              <table width="100%" cellpadding="0" cellspacing="0" style="background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.12);border-radius:12px;margin-bottom:28px;">
                <tr><td style="padding:20px 24px;">
                  <p style="font-size:11px;font-weight:700;color:rgba(0,212,255,0.6);text-transform:uppercase;letter-spacing:0.1em;margin:0 0 14px;">Your Account Details</p>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="padding:6px 0;font-size:13px;color:rgba(240,244,248,0.5);width:120px;">Email</td>
                      <td style="padding:6px 0;font-size:13px;color:#f0f4f8;font-weight:600;">{email}</td>
                    </tr>
                    <tr>
                      <td style="padding:6px 0;font-size:13px;color:rgba(240,244,248,0.5);">Role</td>
                      <td style="padding:6px 0;font-size:13px;color:#f0f4f8;font-weight:600;">{role}</td>
                    </tr>
                    <tr>
                      <td style="padding:6px 0;font-size:13px;color:rgba(240,244,248,0.5);">Institution</td>
                      <td style="padding:6px 0;font-size:13px;color:#f0f4f8;font-weight:600;">{institution}</td>
                    </tr>
                  </table>
                </td></tr>
              </table>
              <!-- Features -->
              <p style="font-size:14px;color:rgba(240,244,248,0.6);margin:0 0 16px;">What you can do with FET2SNN:</p>
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                {"".join([f'<tr><td style="padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);"><span style="color:#00d4ff;font-size:16px;">{icon}</span> <span style="font-size:13px;color:rgba(240,244,248,0.7);vertical-align:middle;"> {text}</span></td></tr>' for icon, text in [('⚡', 'OneClick inference from TCAD device to SNN'), ('🔬', 'TCAD visualization & parameter sweep'), ('🧠', 'Spiking Neural Network simulation'), ('📊', 'Model comparison & validation tools'), ('🤝', 'Collaborate with researchers worldwide')]])}
              </table>
              <!-- CTA -->
              <table cellpadding="0" cellspacing="0" style="margin:0 auto 32px;">
                <tr>
                  <td style="background:linear-gradient(135deg,#00d4ff,#0ea5e9);border-radius:10px;">
                    <a href="{login_url}" style="display:block;padding:14px 40px;font-size:15px;font-weight:700;color:#0a1628;text-decoration:none;border-radius:10px;">
                      Start Researching →
                    </a>
                  </td>
                </tr>
              </table>
              <p style="font-size:12px;color:rgba(240,244,248,0.3);text-align:center;margin:0;line-height:1.5;">
                If you didn't create this account, please ignore this email.
              </p>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="background:rgba(0,0,0,0.3);padding:20px 40px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
              <p style="font-size:11px;color:rgba(240,244,248,0.2);margin:0;">© 2024 FET2SNN Platform · TCAD to SNN Research Ecosystem</p>
            </td>
          </tr>
        </table>
      </td></tr>
    </table>
    </body></html>
    """

    text = f"""Welcome to FET2SNN, {first_name}!

Your account has been created successfully.

Email: {email}
Role: {role}
Institution: {institution}

Start researching: {login_url}

— The FET2SNN Team
"""
    return send_email(email, subject, html, text)


# ==========================================
# AUTH CONFIG
# ==========================================
@app.route('/api/auth/config', methods=['GET'])
def api_auth_config():
    load_env_file()
    return jsonify({
        'google_client_id': os.environ.get('GOOGLE_CLIENT_ID', '')
    })


# ==========================================
# AUTH API - GOOGLE OAUTH
# ==========================================
@app.route('/api/auth/google', methods=['POST'])
def api_google_auth():
    """Verify a Google ID token and login or create the user."""
    import urllib.request as ureq

    data = request.get_json(silent=True) or {}
    credential = data.get('credential') or ''

    if not credential:
        return jsonify({'status': 'error', 'message': 'No Google credential provided.'}), 400

    # Verify token with Google's tokeninfo endpoint
    try:
        verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={credential}"
        req = ureq.Request(verify_url)
        resp = ureq.urlopen(req, timeout=10)
        google_data = json.loads(resp.read().decode())
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Google token verification failed: {str(e)}'}), 401

    # Check token is valid
    if google_data.get('error_description') or not google_data.get('email'):
        return jsonify({'status': 'error', 'message': 'Invalid Google token.'}), 401

    # Check audience (client ID) if GOOGLE_CLIENT_ID is set
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    load_env_file()
    google_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    if google_client_id and google_data.get('aud') != google_client_id:
        return jsonify({'status': 'error', 'message': 'Google token audience mismatch.'}), 401

    email = google_data.get('email', '').lower()
    full_name = google_data.get('name', email.split('@')[0])
    first_name = google_data.get('given_name', full_name.split()[0])
    picture = google_data.get('picture', '')
    google_id = google_data.get('sub', '')

    db = load_db()
    is_new_user = email not in db['users']

    if is_new_user:
        join_date = datetime.datetime.utcnow().strftime('%B %Y')
        db['users'][email] = {
            'password_hash': '',   # Google users don't have a password
            'fullName': full_name,
            'firstName': first_name,
            'role': 'Researcher',
            'institution': 'Not specified',
            'stats': {'projects': 0, 'inferences': 0, 'collaborators': 0},
            'joinDate': join_date,
            'created_at': datetime.datetime.utcnow().isoformat() + 'Z',
            'email': email,
            'google_id': google_id,
            'picture': picture,
            'auth_provider': 'google',
        }
        save_db(db)
        print(f"[GOOGLE AUTH] New user created: {email}")

        # Send welcome email
        try:
            send_welcome_email(email, first_name, 'Researcher', 'Not specified (Google Sign-In)')
        except Exception as e:
            print(f"[EMAIL] Google welcome email failed: {e}")
    else:
        # Update picture/google_id if returning Google user
        db['users'][email]['google_id'] = google_id
        if picture:
            db['users'][email]['picture'] = picture
        if not db['users'][email].get('auth_provider'):
            db['users'][email]['auth_provider'] = 'google'
        save_db(db)

    # Create session
    token = generate_token(48)
    expires = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'
    if 'sessions' not in db:
        db['sessions'] = {}
    db['sessions'][token] = {'email': email, 'expires': expires}
    save_db(db)

    user = db['users'][email]
    profile = {k: v for k, v in user.items() if k != 'password_hash'}

    action = 'created' if is_new_user else 'login'
    return jsonify({
        'status': 'success',
        'message': f"Welcome{'to FET2SNN' if is_new_user else ' back'}, {first_name}!",
        'token': token,
        'user': profile,
        'action': action
    })


# ==========================================
# AUTH API - SIGNUP
# ==========================================
@app.route('/api/auth/signup', methods=['POST'])
def api_signup():

    data = request.get_json(silent=True) or {}
    name = (data.get('fullName') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    institution = (data.get('institution') or '').strip()
    role = (data.get('role') or '').strip()

    if not all([name, email, password, institution, role]):
        return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400

    if len(password) < 6:
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters.'}), 400

    db = load_db()
    if email in db['users']:
        return jsonify({'status': 'error', 'message': 'An account with this email already exists.'}), 409

    first_name = name.split()[0] if name else 'User'
    join_date = datetime.datetime.utcnow().strftime('%B %Y')

    new_user = {
        'password_hash': hash_password(password),
        'fullName': name,
        'firstName': first_name,
        'role': role,
        'institution': institution,
        'stats': {'projects': 0, 'inferences': 0, 'collaborators': 0},
        'joinDate': join_date,
        'created_at': datetime.datetime.utcnow().isoformat() + 'Z',
        'email': email,
    }
    db['users'][email] = new_user
    save_db(db)

    # Auto-login: create session
    token = generate_token(48)
    expires = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'
    if 'sessions' not in db:
        db['sessions'] = {}
    db['sessions'][token] = {'email': email, 'expires': expires}
    save_db(db)

    profile = {k: v for k, v in new_user.items() if k != 'password_hash'}

    # Send welcome email (non-blocking - don't fail signup if email fails)
    try:
        send_welcome_email(email, first_name, role, institution)
    except Exception as e:
        print(f"[EMAIL] Welcome email failed (non-critical): {e}")

    return jsonify({
        'status': 'success',
        'message': f"Welcome to FET2SNN, {first_name}! A welcome email has been sent.",
        'token': token,
        'user': profile
    }), 201

# ==========================================
# AUTH API - LOGOUT
# ==========================================
@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    data = request.get_json(silent=True) or {}
    token = data.get('token') or request.headers.get('Authorization', '').replace('Bearer ', '')
    if token:
        db = load_db()
        db.get('sessions', {}).pop(token, None)
        save_db(db)
    return jsonify({'status': 'success', 'message': 'Logged out successfully.'})

# ==========================================
# AUTH API - VERIFY SESSION
# ==========================================
@app.route('/api/auth/verify', methods=['GET'])
def api_verify():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({'status': 'error', 'message': 'No token provided.'}), 401

    db = load_db()
    sess = db.get('sessions', {}).get(token)
    if not sess:
        return jsonify({'status': 'error', 'message': 'Invalid or expired session.'}), 401

    # Check expiry
    try:
        expires = datetime.datetime.fromisoformat(sess['expires'].replace('Z', '+00:00'))
        if datetime.datetime.now(datetime.timezone.utc) > expires:
            db['sessions'].pop(token, None)
            save_db(db)
            return jsonify({'status': 'error', 'message': 'Session expired. Please log in again.'}), 401
    except Exception:
        pass

    email = sess['email']
    user = db['users'].get(email, {})
    profile = {k: v for k, v in user.items() if k != 'password_hash'}
    profile['email'] = email

    return jsonify({'status': 'success', 'user': profile})

# ==========================================
# AUTH API - FORGOT PASSWORD (Email Reset)
# ==========================================
@app.route('/api/auth/forgot-password', methods=['POST'])
def api_forgot_password():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()

    if not email:
        return jsonify({'status': 'error', 'message': 'Email address is required.'}), 400

    db = load_db()
    user = db['users'].get(email)

    if not user:
        # Security: don't reveal if email exists
        return jsonify({
            'status': 'success',
            'message': 'If an account exists with this email, a reset link has been sent.'
        })

    # Generate reset token (expires in 1 hour)
    reset_token = generate_token(48)
    reset_expires = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z'

    if 'reset_tokens' not in db:
        db['reset_tokens'] = {}
    db['reset_tokens'][reset_token] = {'email': email, 'expires': reset_expires}
    save_db(db)

    reset_link = f"http://localhost:5000/reset-password?token={reset_token}"

    # Send email if SMTP is configured
    load_env_file()  # reload fresh from .env every request
    smtp_email = os.environ.get('SMTP_EMAIL')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    if not smtp_email or not smtp_password:
        # Dev mode: return the link directly so user can test
        print(f"[DEV] No SMTP configured. Reset link: {reset_link}")
        return jsonify({
            'status': 'success',
            'message': 'Reset link generated (SMTP not configured — see server console).',
            'dev_reset_link': reset_link
        })

    # --- Send real email via Gmail SMTP ---
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    body_html = f"""
    <html>
    <body style="margin:0;padding:0;background:#0a1628;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a1628;min-height:100vh;">
      <tr><td align="center" style="padding:40px 20px;">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#0d1f3c;border-radius:16px;border:1px solid rgba(0,212,255,0.15);overflow:hidden;">
          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#0d2b4a,#0a1628);padding:32px 40px;text-align:center;border-bottom:1px solid rgba(0,212,255,0.1);">
              <div style="font-family:Arial,sans-serif;font-size:26px;font-weight:800;color:#f0f4f8;letter-spacing:-0.5px;">
                FET2<span style="color:#00d4ff;">SNN</span>
              </div>
              <div style="font-family:Arial,sans-serif;font-size:11px;color:rgba(0,212,255,0.5);letter-spacing:0.2em;text-transform:uppercase;margin-top:6px;">
                OneClick · One Inference
              </div>
            </td>
          </tr>
          <!-- Body -->
          <tr>
            <td style="padding:40px;">
              <p style="font-family:Arial,sans-serif;font-size:22px;font-weight:700;color:#f0f4f8;margin:0 0 16px;">
                🔐 Password Reset Request
              </p>
              <p style="font-family:Arial,sans-serif;font-size:15px;color:rgba(240,244,248,0.7);margin:0 0 24px;line-height:1.6;">
                Hello <strong style="color:#f0f4f8;">{user.get('firstName', 'Researcher')}</strong>,<br><br>
                We received a request to reset your FET2SNN account password. 
                Click the button below to set a new password. This link will expire in <strong style="color:#00d4ff;">1 hour</strong>.
              </p>
              <!-- CTA Button -->
              <table cellpadding="0" cellspacing="0" style="margin:0 auto 32px;">
                <tr>
                  <td style="background:linear-gradient(135deg,#00d4ff,#0ea5e9);border-radius:10px;">
                    <a href="{reset_link}"
                       style="display:block;padding:14px 36px;font-family:Arial,sans-serif;font-size:15px;font-weight:700;color:#0a1628;text-decoration:none;border-radius:10px;">
                      Reset My Password →
                    </a>
                  </td>
                </tr>
              </table>
              <!-- Fallback link -->
              <p style="font-family:Arial,sans-serif;font-size:12px;color:rgba(240,244,248,0.4);margin:0 0 8px;">
                If the button doesn't work, copy and paste this link:
              </p>
              <p style="font-family:monospace;font-size:11px;color:rgba(0,212,255,0.6);word-break:break-all;margin:0 0 24px;padding:10px;background:rgba(0,0,0,0.3);border-radius:6px;">
                {reset_link}
              </p>
              <!-- Warning -->
              <p style="font-family:Arial,sans-serif;font-size:12px;color:rgba(240,244,248,0.35);margin:0;line-height:1.5;">
                If you did not request a password reset, you can safely ignore this email. 
                Your password will remain unchanged.
              </p>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="background:rgba(0,0,0,0.3);padding:20px 40px;text-align:center;border-top:1px solid rgba(255,255,255,0.05);">
              <p style="font-family:Arial,sans-serif;font-size:11px;color:rgba(240,244,248,0.25);margin:0;">
                © 2024 FET2SNN Platform · TCAD to SNN Research Ecosystem
              </p>
            </td>
          </tr>
        </table>
      </td></tr>
    </table>
    </body>
    </html>
    """

    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"FET2SNN Platform <{smtp_email}>"
        msg['To'] = email
        msg['Subject'] = '🔐 FET2SNN — Password Reset Request'
        msg['Reply-To'] = smtp_email

        # Plain text fallback
        body_text = f"""FET2SNN Password Reset

Hello {user.get('firstName', 'Researcher')},

Click the link below to reset your password (expires in 1 hour):
{reset_link}

If you did not request this, please ignore this email.

— The FET2SNN Team
"""
        msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, [email], msg.as_string())
        server.quit()

        print(f"[SMTP] Reset email sent successfully to {email}")
        return jsonify({
            'status': 'success',
            'message': f'Password reset email sent to {email}. Please check your inbox (and spam folder).'
        })

    except smtplib.SMTPAuthenticationError:
        print(f"[SMTP ERROR] Authentication failed. Make sure you are using a Gmail App Password, not your regular password.")
        print(f"[SMTP] Get App Password: https://myaccount.google.com/apppasswords")
        return jsonify({
            'status': 'error',
            'message': 'Email authentication failed. The SMTP password in .env must be a Gmail App Password (16 characters), not your regular Gmail password.'
        }), 500

    except smtplib.SMTPException as e:
        print(f"[SMTP ERROR] {e}")
        return jsonify({
            'status': 'error',
            'message': f'Failed to send email: {str(e)}'
        }), 500

    except Exception as e:
        print(f"[SMTP ERROR] Unexpected: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Could not send reset email. Check server logs for details.'
        }), 500


# ==========================================
# AUTH API - RESET PASSWORD (token-based)
# ==========================================
@app.route('/api/auth/reset-password', methods=['POST'])
def api_reset_password():
    data = request.get_json(silent=True) or {}
    token = data.get('token') or ''
    new_password = data.get('password') or ''

    if not token or not new_password:
        return jsonify({'status': 'error', 'message': 'Token and new password are required.'}), 400

    if len(new_password) < 6:
        return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters.'}), 400

    db = load_db()
    reset_info = db.get('reset_tokens', {}).get(token)

    if not reset_info:
        return jsonify({'status': 'error', 'message': 'Invalid or expired reset token.'}), 400

    try:
        expires = datetime.datetime.fromisoformat(reset_info['expires'].replace('Z', '+00:00'))
        if datetime.datetime.now(datetime.timezone.utc) > expires:
            db['reset_tokens'].pop(token, None)
            save_db(db)
            return jsonify({'status': 'error', 'message': 'Reset link has expired. Please request a new one.'}), 400
    except Exception:
        pass

    email = reset_info['email']
    if email not in db['users']:
        return jsonify({'status': 'error', 'message': 'User not found.'}), 404

    db['users'][email]['password_hash'] = hash_password(new_password)
    db['reset_tokens'].pop(token, None)
    save_db(db)

    return jsonify({'status': 'success', 'message': 'Password reset successfully! You can now log in.'})

# ==========================================
# RESET PASSWORD PAGE
# ==========================================
@app.route('/reset-password')
def reset_password_page():
    return app.send_static_file('reset_password.html')

# ==========================================
# EXISTING ML PREDICTION ROUTE
# ==========================================
print("Starting FET2SNN Backend Server...")

def simulate_mlfompy_prediction(params):
    Lg = float(params.get('Lg', 12))
    Wns = float(params.get('Wns', 20))
    Nstacks = float(params.get('Nstacks', 3))
    T_k = float(params.get('T', 298.15))
    T_c = T_k - 273.15
    Vdd = float(params.get('Vdd', 0.7))
    Nch = float(params.get('Nch', 1e16))

    q = 1.6e-19
    kT = 1.38e-23 * T_k
    Vt = kT / q

    Vth = 0.35 - 0.001 * (T_c - 25) - 0.01 * (Lg - 12) + 0.005 * np.log10(Nch/1e16)
    SS = 60 * (T_k / 300) * (1 + 10 / Lg)
    DIBL = 20 * (12 / Lg)

    # 80 points resolution for transfer characteristic curves
    vgs_array = np.linspace(0, Vdd, 80)
    id_transfer = []
    for vgs in vgs_array:
        if vgs < Vth:
            current = 1e-12 * 10 ** ((vgs - Vth) / (SS / 1000))
        else:
            current = 1e-4 * (Wns / Lg) * Nstacks * ((vgs - Vth) ** 1.5)
        id_transfer.append(float(current))

    Ion = id_transfer[-1]
    Ioff = id_transfer[0]

    # 60 points resolution for output characteristic curves
    vds_array = np.linspace(0, Vdd, 60)
    output_curves = {}
    for vg_bias in [0.4, 0.5, 0.6, 0.7]:
        id_out = []
        if vg_bias < Vth:
            ion_bias = 1e-12 * 10 ** ((vg_bias - Vth) / (SS / 1000))
        else:
            ion_bias = 1e-4 * (Wns / Lg) * Nstacks * ((vg_bias - Vth) ** 1.5)
        for vds in vds_array:
            current = ion_bias * (1 - np.exp(-vds / 0.1)) * (1 + 0.05 * vds)
            id_out.append(float(current))
        output_curves[f"vgs_{vg_bias:.1f}"] = id_out

    return {
        "foms": {
            "Vth": float(Vth), "SS": float(SS), "DIBL": float(DIBL),
            "Ion": float(Ion), "Ioff": float(Ioff),
            "muEff": 250.0 - 0.5 * (T_c - 25)
        },
        "curves": {
            "transfer": {"vgs": vgs_array.tolist(), "id": id_transfer},
            "output": {"vds": vds_array.tolist(), "curves": output_curves}
        }
    }

@app.route('/api/predict', methods=['POST'])
def predict():
    params = request.json
    try:
        result = simulate_mlfompy_prediction(params)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

CONTACT_DB_FILE = os.path.join(os.path.dirname(__file__), 'contact_inquiries.json')

@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    subject = (data.get('subject') or '').strip()
    message = (data.get('message') or '').strip()
    
    if not name or not email:
        return jsonify({'status': 'error', 'message': 'Name and Email are required.'}), 400
        
    inquiry = {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    
    try:
        inquiries = []
        if os.path.exists(CONTACT_DB_FILE):
            with open(CONTACT_DB_FILE, 'r', encoding='utf-8') as f:
                inquiries = json.load(f)
        inquiries.append(inquiry)
        with open(CONTACT_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(inquiries, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to save inquiry: {str(e)}'}), 500
        
    return jsonify({'status': 'success', 'message': 'Neural information successfully transmitted!'})

# ==========================================
# LEGACY RESET PASSWORD ROUTE (kept for compat)
# ==========================================
@app.route('/api/reset-password', methods=['POST'])
def reset_password_legacy():
    return api_forgot_password()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

