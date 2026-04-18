import sqlite3
import json
import os

os.chdir(r'C:\Users\SERVER PC\Downloads\NEXUS GPT')

db_path = r'server/nexus_gpt.db'
print('Database path:', os.path.abspath(db_path))
print('DB exists:', os.path.exists(db_path))

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row['name'] for row in cursor.fetchall()]
    print('\nTables:', tables)
    
    # Check users
    if 'users' in tables:
        cursor.execute('SELECT username, role, email FROM users')
        users = cursor.fetchall()
        print('\nUsers:')
        for u in users:
            print(f'  - {u["username"]} ({u["role"]}) - {u["email"]}')
    
    # Check history entries in storage
    if 'storage' in tables:
        cursor.execute("SELECT username, key_name, LENGTH(value_data) as size FROM storage WHERE key_name LIKE 'nexus_history_%'")
        history = cursor.fetchall()
        print(f'\nHistory entries found: {len(history)}')
        for h in history:
            print(f'  - User: {h["username"]}, Key: {h["key_name"]}, Size: {h["size"]} bytes')
        
        # Sample history content
        if history:
            first_user = history[0]['username']
            cursor.execute('SELECT value_data FROM storage WHERE username=? AND key_name=?', 
                         [first_user, f'nexus_history_{first_user}'])
            data = cursor.fetchone()
            if data:
                try:
                    parsed = json.loads(data['value_data'])
                    print(f'\nSample history for {first_user}: {len(parsed)} sessions')
                    for sid in list(parsed.keys())[:3]:
                        print(f'  - Session: {sid[:30]}...')
                except Exception as e:
                    print(f'Could not parse history JSON: {e}')
    
    conn.close()
else:
    print('Database file not found!')
