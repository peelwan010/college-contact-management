import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_aktu_roll_list():
    path = os.path.join(DATA_DIR, "aktu_roll_list.xlsx")

    df = pd.read_excel(path, header=1)

    
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("'", "")
    )

    
    df = df.rename(columns={
        "registration no": "registration_no",
        "roll no": "roll_no",
        "name": "student_name",
        "student name": "student_name",
        "fathers name": "father_name",
        "father name": "father_name"
    })

    required = ["registration_no", "roll_no", "student_name", "father_name"]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")

    return df[required]


def get_second_year_sheets():
    path = os.path.join(DATA_DIR, "second_year_students.xlsx")
    xls = pd.ExcelFile(path)
    return xls.sheet_names


def load_second_year_students(sheet_name):
    path = os.path.join(DATA_DIR, "second_year_students.xlsx")
    df = pd.read_excel(path, sheet_name=sheet_name)

    df = df.rename(columns={
        "AKTU Roll No": "roll_no",
        "Student Name": "student_name",
        "Section": "section"
    })

    return df


def load_first_year_contacts():
    path = os.path.join(DATA_DIR, "first_year_contacts.xlsx")
    df = pd.read_excel(path)

    # Normalize column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )

    # Clean student mobile
    if "student_mobile" in df.columns:
        df["student_mobile"] = (
            df["student_mobile"]
            .astype(str)
            .str.replace("`", "")
            .str.replace("+91-", "")
            .str.strip()
        )

    # Explicit renaming for clarity
    df = df.rename(columns={
        "admission_category": "admission_category",
        "father_mobile_no.": "parent_mobile",
        "father_email": "parent_email",
        "father_name": "father_name",
        "email": "email"
    })

    # Safety check
    if "admission_category" not in df.columns:
        raise ValueError(
            "Column 'Admission Category' not found in first_year_contacts.xlsx"
        )

    return df

