import os
import shutil
from pathlib import Path
from datetime import datetime

def get_valid_path():
    """Prompt user for a valid directory path (up to 3 attempts)."""
    attempts = 0
    while attempts < 3:
        path_input = input("Enter the full folder path to sort: ").strip()
        path = Path(path_input)
        if path.exists() and path.is_dir():
            print(f"✅ Path found: {path}")
            return path
        else:
            print("❌ Invalid path. Please try again.")
            attempts += 1
    print("⚠️ Too many invalid attempts. Exiting service.")
    exit(1)

def sort_files(base_path: Path):
    """Sort and organize files in the provided path."""
    files = [f for f in base_path.iterdir() if f.is_file()]
    if not files:
        print("No files found in this directory.")
        return

    # Define groups using the keyword 'sort_my'
    groups = {
        "sort_my_pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "sort_my_documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
        "sort_my_videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
        "sort_my_audio": [".mp3", ".wav", ".flac", ".aac"],
    }

    summary = {"sorted": 0, "moved": 0, "created_folders": []}
    lost_files_dir = base_path / "lost_files"
    unknown_files = []

    # Sort files by creation date
    files.sort(key=lambda f: f.stat().st_ctime)

    # Track which folders need to be created
    folders_to_create = set()

    for file in files:
        ext = file.suffix.lower()
        moved = False

        for folder, extensions in groups.items():
            if ext in extensions:
                folders_to_create.add(folder)
                moved = True
                break

        if not moved:
            unknown_files.append(file)

    # Create only necessary folders
    for folder in folders_to_create:
        folder_path = base_path / folder
        if not folder_path.exists():
            folder_path.mkdir()
            summary["created_folders"].append(folder)

    # Create lost_files folder only if needed
    if unknown_files:
        if not lost_files_dir.exists():
            lost_files_dir.mkdir()
            summary["created_folders"].append("lost_files")

    # Move files now
    for file in files:
        ext = file.suffix.lower()
        moved = False

        for folder, extensions in groups.items():
            if ext in extensions:
                dest_folder = base_path / folder
                shutil.move(str(file), dest_folder / file.name)
                summary["sorted"] += 1
                summary["moved"] += 1
                moved = True
                break

        if not moved:
            shutil.move(str(file), lost_files_dir / file.name)
            summary["sorted"] += 1
            summary["moved"] += 1

    # Final report
    print("\n📊 --- Sort Report ---")
    print(f"📁 Path sorted: {base_path}")
    print(f"🗂️  Total files sorted: {summary['sorted']}")
    print(f"📦  Total files moved: {summary['moved']}")
    print(f"🪄  Folders created: {', '.join(summary['created_folders']) if summary['created_folders'] else 'None'}")

    # Show final folder contents
    print("\n📄 --- Folder contents after sorting ---")
    for item in base_path.iterdir():
        if item.is_dir():
            print(f"\n📂 {item.name}:")
            for sub in item.iterdir():
                print(f"   - {sub.name}")

def main():
    print("🔧 Welcome to sort_my – your smart file organizer!\n")
    base_path = get_valid_path()
    sort_files(base_path)
    print("\n✅ Sorting complete. Have a great day!")

if __name__ == "__main__":
    main()
