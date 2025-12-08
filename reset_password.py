
import argparse
import sqlite3
import os
import shutil
import sys
import base64
import hashlib
import datetime

try:
    from werkzeug.security import generate_password_hash
    _HAS_WERKZEUG = True
except Exception:
    _HAS_WERKZEUG = False


def generate_hash(password, iterations=260000):
    if _HAS_WERKZEUG:
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    # fallback implementation compatible with werkzeug format
    salt_bytes = os.urandom(16)
    salt = base64.b64encode(salt_bytes).decode('utf-8').rstrip('=')
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, iterations)
    hash_b64 = base64.b64encode(dk).decode('utf-8').rstrip('=')
    return f'pbkdf2:sha256:{iterations}${salt}${hash_b64}'


def find_user_table(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    candidates = []
    for t in tables:
        try:
            cur.execute(f"PRAGMA table_info('{t}')")
            cols = [r[1].lower() for r in cur.fetchall()]
            if 'email' in cols and any(c in cols for c in ('password','passwd','pass')):
                return t, cols
            if 'email' in cols:
                candidates.append((t, cols))
        except Exception:
            continue
    if candidates:
        return candidates[0]
    return None, None


def backup_db(db_path):
    head, tail = os.path.split(db_path)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bak = db_path + f'.bak_{stamp}'
    shutil.copy2(db_path, bak)
    return bak


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', required=True)
    p.add_argument('--email', required=True)
    p.add_argument('--password', required=True)
    args = p.parse_args()

    db_path = os.path.abspath(args.db)
    if not os.path.exists(db_path):
        print('DB not found:', db_path, file=sys.stderr)
        sys.exit(2)

    bak = backup_db(db_path)
    print('Backup created:', bak)

    conn = sqlite3.connect(db_path)
    table, cols = find_user_table(conn)
    if not table:
        print('Could not find a users table with email+password columns.', file=sys.stderr)
        conn.close()
        sys.exit(3)

    print('Using table:', table)
    pwd_col = None
    for c in ('password','passwd','pass'):
        if c in cols:
            pwd_col = c
            break
    if not pwd_col:
        # choose any col that contains 'pass'
        for c in cols:
            if 'pass' in c:
                pwd_col = c
                break
    if not pwd_col:
        print('No password column found in table', table, 'columns:', cols, file=sys.stderr)
        conn.close()
        sys.exit(4)

    # build hash
    new_hash = generate_hash(args.password)

    cur = conn.cursor()
    cur.execute(f"UPDATE {table} SET {pwd_col} = ? WHERE email = ?", (new_hash, args.email))
    conn.commit()
    if cur.rowcount == 0:
        print('No rows updated. User with email not found:', args.email, file=sys.stderr)
        conn.close()
        sys.exit(5)
    print('Password updated for', args.email)
    conn.close()

if __name__ == '__main__':
    main()
