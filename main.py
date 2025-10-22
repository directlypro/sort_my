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

    # Common categories with keyword 'sort_my'
    groups = {
        "sort_my_pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
        "sort_my_documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
        "sort_my_videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
        "sort_my_audio": [".mp3", ".wav", ".flac", ".aac"],
    }

    lost_files_dir = base_path / "lost_files"
    summary = {"sorted": 0, "moved": 0, "created_folders": []}

    # Create folders if they don’t exist
    for folder in groups.keys():
        folder_path = base_path / folder
        if not folder_path.exists():
            folder_path.mkdir()
            summary["created_folders"].append(folder)

    if not lost_files_dir.exists():
        lost_files_dir.mkdir()
        summary["created_folders"].append("lost_files")

    # Sort files by creation date
    files.sort(key=lambda f: f.stat().st_ctime)

    for file in files:
        ext = file.suffix.lower()
        moved = False

        # Check which group it belongs to
        for folder, extensions in groups.items():
            if ext in extensions:
                dest_folder = base_path / folder
                shutil.move(str(file), dest_folder / file.name)
                summary["sorted"] += 1
                summary["moved"] += 1
                moved = True
                break

        # Handle uncommon files
        if not moved:
            shutil.move(str(file), lost_files_dir / file.name)
            summary["sorted"] += 1
            summary["moved"] += 1

    # Print report
    print("\n📊 --- Sort Report ---")
    print(f"📁 Path sorted: {base_path}")
    print(f"🗂️  Total files sorted: {summary['sorted']}")
    print(f"📦  Total files moved: {summary['moved']}")
    print(f"🪄  Folders created: {', '.join(summary['created_folders']) if summary['created_folders'] else 'None'}")

    # List resulting folders and contents
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

