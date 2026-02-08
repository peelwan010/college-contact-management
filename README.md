# College Contact Management System

This project is a Python-based college contact management system built to work with real-world institutional Excel data. It provides both a Command Line Interface (CLI) and a Tkinter-based Graphical User Interface (GUI), allowing users to view, search, sort, and filter student and contact information in a structured and user-friendly way.

The system is designed with a clean separation between data processing and user interfaces. All Excel reading, cleaning, and normalization logic is handled in a dedicated backend module, while the CLI and GUI act as independent frontends built on top of the same core logic.

---

## Key Features

- Dual interface support:
  - CLI for quick access, testing, and debugging
  - Tkinter GUI for interactive and visual usage
- Reads and processes Excel (.xlsx) files using Pandas
- Supports Excel files with multiple worksheets (branch/section-wise data)
- Search functionality across all visible columns in all datasets
- Sorting by student name (ascending or descending) for all datasets
- Filtering first-year student data based on Admission Category
- UI controls appear only when relevant to the selected dataset
- No hardcoded file paths; project is fully portable
- Clean, modular, and extensible project structure

---

## Datasets Supported

The project currently works with three categories of institutional data:

1. AKTU Roll List  
   - Displays registration number, roll number, student name, and father’s name  
   - Supports search and sorting by student name  

2. Second Year Student List  
   - Supports Excel files with multiple sheets representing different branches or sections  
   - Users can select the required sheet at runtime  
   - Supports search and sorting by student name  

3. First Year Student Contacts  
   - Includes student and parent contact information  
   - Supports search across all fields  
   - Supports filtering based on Admission Category  
   - Supports sorting by student name  

---

## Project Structure

college-contact-management/
├── cli_app.py          # Command Line Interface
├── gui_app.py          # Tkinter GUI application
├── loaders.py          # Excel loading, cleaning, and normalization logic
├── data/
│   ├── aktu_roll_list.xlsx
│   ├── second_year_students.xlsx
│   └── first_year_contacts.xlsx
├── requirements.txt
├── README.md
└── .gitignore

---

## Tech Stack

- Python
- Pandas
- Tkinter
- Excel (.xlsx)

---

## How to Run the Project

1. Install dependencies:

pip install -r requirements.txt

2. Run the CLI version:

python cli_app.py

3. Run the GUI version:

python gui_app.py

---

## Design and Implementation Notes

- All Excel files are loaded using relative paths to ensure portability.
- Column names from Excel files are normalized in the data loading layer to handle inconsistent or messy headers.
- The GUI never directly reads Excel files; it relies entirely on backend loader functions.
- Search, filter, and sort operations are applied only to the currently loaded dataset.
- Filter and sort controls are intentionally restricted to prevent invalid operations and improve usability.
- The project structure allows easy future expansion, such as adding new datasets or interfaces.

---

## Disclaimer

This project was developed as an academic and learning-focused exercise. The included Excel files represent institutional-style datasets and are used strictly for demonstration and educational purposes. The project is not intended for production deployment.

---

## Future Improvements

- Export filtered or sorted data to Excel
- Pagination support for very large datasets
- Detailed student information view on row selection
- Database backend (SQLite) instead of Excel files
- Enhanced GUI layout and theming
