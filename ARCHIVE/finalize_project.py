import os
import shutil
import glob

def move_files():
    # 1. Create Directories
    folders = ["modules", "images", "docs", "ARCHIVE"]
    for f in folders:
        if not os.path.exists(f):
            os.makedirs(f)
            print(f"Created {f}/")

    # 2. Define moves
    # Scripts to modules (excluding roots)
    root_scripts = ["dashboard.py", "generate_report.py", "finalize_project.py"]
    scripts = glob.glob("*.py")
    for s in scripts:
        if s not in root_scripts:
            shutil.move(s, os.path.join("modules", s))
            print(f"Moved {s} -> modules/")
            
    # Images to images
    images = glob.glob("*.png") + glob.glob("*.gif")
    for img in images:
        shutil.move(img, os.path.join("images", img))
        print(f"Moved {img} -> images/")
        
    # Docs to docs (excluding README, FINAL_REPORT.md might be good in root? No, docs.)
    # User might want FINAL_REPORT.md in root. But "cleanup" implies moving it.
    # Let's keep README.md and QRS_Final_Report.html in root.
    docs = glob.glob("*.md") + glob.glob("*.txt")
    for d in docs:
        if d != "README.md":
            shutil.move(d, os.path.join("docs", d))
            print(f"Moved {d} -> docs/")

if __name__ == "__main__":
    move_files()
