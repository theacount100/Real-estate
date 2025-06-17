import subprocess
import pyperclip

# STEP 1: Run OmanReal Scraper
print("▶️ Running OmanReal Scraper...")
subprocess.run(["python", r"D:\Projects\realeastae\OmanRealScraper\omanreal_full_scraper.py"])

# STEP 2: Extract OmanReal Data
print("▶️ Extracting OmanReal Data...")
subprocess.run(["python", r"D:\Projects\realeastae\OmanRealScraper\Extract data and sort.py"])

# STEP 3: Run GoLands Scraper
print("▶️ Running GoLands Scraper...")
subprocess.run(["python", r"D:\Projects\realeastae\GoLandsScraper\golandsScraper.py"])

# STEP 4: Merge files
print("▶️ Merging files...")
subprocess.run(["python", r"D:\Projects\realeastae\OmanRealScraper\mergefiles.py"])

# STEP 5: Notify user to paste in ChatGPT
print("\n✅ All scripts finished.")
print("📁 New data saved to: D:\\Projects\\realeastae\\new_only_listings.xlsx")

# STEP 6: Load correction prompt from file and copy to clipboard
instruction_file = r"D:\Projects\realeastae\correction_instruction.txt"

try:
    with open(instruction_file, "r", encoding="utf-8") as f:
        instructions = f.read()
        pyperclip.copy(instructions)
        print("\n📎 The correction prompt has been copied to your clipboard.")
except FileNotFoundError:
    print("\n❌ ERROR: correction_instruction.txt not found at:")
    print(instruction_file)
    input("Press Enter to exit.")
    exit(1)

# STEP 7: Wait for the operator to finish ChatGPT correction
input("\n⏸️ After correcting in ChatGPT and saving as:\nD:\\Projects\\realeastae\\corrected_real_estate_listings.xlsx\n\nPress Enter to continue...")

# STEP 8: Run data cleanings
print("▶️ Cleaning Data...")
subprocess.run(["python", r"D:\Projects\realeastae\OmanRealScraper\Data Cleaning.py"])

# STEP 9: Keep terminal open until user closes it
input("\n✅ All done! Press Enter to close this window manually...")
