import os
import shutil
import glob

def refactor():
    # 1. create backend and frontend dirs
    os.makedirs('frontend', exist_ok=True)
    os.rename('app', 'backend')

    # 2. move static and templates to frontend
    if os.path.exists('backend/templates'):
        shutil.move('backend/templates', 'frontend/templates')
    if os.path.exists('backend/static'):
        shutil.move('backend/static', 'frontend/static')

    # 3. replace imports and paths in python files
    files_to_check = glob.glob('backend/**/*.py', recursive=True) + glob.glob('*.py') + glob.glob('*.bat')
    for filepath in files_to_check:
        if not os.path.isfile(filepath): continue
        if filepath.startswith('app_backup'): continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replacements
        new_content = content.replace('from backend.', 'from backend.')
        new_content = new_content.replace('from backend ', 'from backend ')
        new_content = new_content.replace('import backend.', 'import backend.')
        new_content = new_content.replace('frontend/templates', 'frontend/templates')
        new_content = new_content.replace('frontend/static', 'frontend/static')
        new_content = new_content.replace('backend.main:app', 'backend.main:app')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")

if __name__ == '__main__':
    refactor()
    print("Done")
