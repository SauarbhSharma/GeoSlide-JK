import os

FORBIDDEN = [
    'Full J&K UT Interactive View',
    'Model Version: XGBoost v0.1.0-prototype',
    'Target ROC-AUC',
    'Target PR-AUC',
    '0 Missing',
    'VERIFIED (5 Tiles)',
    'Copernicus DEM Derived'
]

PROJECT_DIR = r"D:\Projects\GeoSlide_JK"

def audit():
    matches = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        if '.git' in dirs: dirs.remove('.git')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        if '.next' in dirs: dirs.remove('.next')
        for f in files:
            if f.endswith(('.ts', '.tsx', '.js', '.py', '.json', '.md', '.yaml', '.yml')):
                fp = os.path.join(root, f)
                try:
                    content = open(fp, encoding='utf-8', errors='ignore').read()
                    for term in FORBIDDEN:
                        if term in content:
                            matches.append((fp, term))
                except Exception:
                    pass
    print(f"Found {len(matches)} occurrences of forbidden terms:")
    for fp, term in matches:
        print(f"  - {fp}: '{term}'")
    return len(matches)

if __name__ == "__main__":
    audit()
