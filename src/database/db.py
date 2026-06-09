import pandas as pd
from src.database.config import supabase


# ══════════════════════════════════════════════
# AUTH — USERS
# ══════════════════════════════════════════════

def get_user(username: str) -> dict | None:
    """Fetch user by username. Returns dict or None."""
    try:
        res = supabase.table("users") \
            .select("*") \
            .eq("username", username) \
            .single() \
            .execute()
        return res.data if res.data else None
    except Exception:
        return None


def create_user(username: str, hashed_password: str, role: str = "user") -> bool:
    """Insert new user. Returns True on success."""
    try:
        res = supabase.table("users").insert({
            "username": username,
            "password": hashed_password,
            "role":     role,
        }).execute()
        return bool(res.data)
    except Exception as e:
        print(f"[DB ERROR] create_user: {e}")
        return False


# ══════════════════════════════════════════════
# VEHICLE REGISTRY
# ══════════════════════════════════════════════

def get_all_vehicles(user_id: str = None, role: str = "user") -> list[str]:
    """
    admin  → returns ALL vehicles
    user   → returns only vehicles created by that user_id
    """
    try:
        query = supabase.table("vehicles").select("bus_number").order("created_at")
        if role != "admin" and user_id:
            query = query.eq("created_by", user_id)
        res = query.execute()
        return [row["bus_number"] for row in res.data] if res.data else []
    except Exception as e:
        print(f"[DB ERROR] get_all_vehicles: {e}")
        return []


def delete_vehicle(bus_number: str) -> bool:
    """
    Delete vehicle and all its related records.
    Returns True on success.
    """
    try:
        # Delete all related data first (foreign key order)
        supabase.table("vehicle_records").delete().eq("bus_number", bus_number).execute()
        supabase.table("vehicle_expenses").delete().eq("bus_number", bus_number).execute()
        # Delete from vehicles table
        supabase.table("vehicles").delete().eq("bus_number", bus_number).execute()
        return True
    except Exception as e:
        print(f"[DB ERROR] delete_vehicle: {e}")
        return False


def create_vehicle(bus_number: str, created_by: str = None) -> bool:
    """Insert new vehicle with owner. Returns True on success."""
    try:
        res = supabase.table("vehicles").insert({
            "bus_number":  bus_number,
            "created_by":  created_by,
        }).execute()
        return bool(res.data)
    except Exception as e:
        print(f"[DB ERROR] create_vehicle: {e}")
        return False


# ══════════════════════════════════════════════
# VEHICLE RECORDS
# ══════════════════════════════════════════════

def save_vehicle_records(bus_number: str, df: pd.DataFrame) -> None:
    rows = []
    for _, row in df.iterrows():
        rows.append({
            "bus_number":     bus_number,
            "date":           str(row["Date"]),
            "driver_name":    row["Driver Name"],
            "conductor_name": row["Conductor Name"],
            "scheduled_km":   row["Scheduled KM"],
            "actual_km":      row["Actual KM"],
            "diesel":         row["Diesel"],
        })

    edited_dates = df["Date"].astype(str).unique().tolist()
    supabase.table("vehicle_records") \
        .delete() \
        .eq("bus_number", bus_number) \
        .in_("date", edited_dates) \
        .execute()
    supabase.table("vehicle_records").insert(rows).execute()


def get_vehicle_records(bus_number: str) -> pd.DataFrame:
    res = supabase.table("vehicle_records") \
        .select("*") \
        .eq("bus_number", bus_number) \
        .order("date", desc=True) \
        .execute()

    if not res.data:
        return pd.DataFrame(columns=["Date", "Driver Name", "Conductor Name", "Scheduled KM", "Actual KM", "Diesel"])

    df = pd.DataFrame(res.data)
    df = df.rename(columns={
        "date":           "Date",
        "driver_name":    "Driver Name",
        "conductor_name": "Conductor Name",
        "scheduled_km":   "Scheduled KM",
        "actual_km":      "Actual KM",
        "diesel":         "Diesel",
    })
    return df[["Date", "Driver Name", "Conductor Name", "Scheduled KM", "Actual KM", "Diesel"]]


# ══════════════════════════════════════════════
# DRIVER SALARY
# ══════════════════════════════════════════════

def save_driver_salary(df: pd.DataFrame) -> None:
    records = [
        {
            "driver_name": row["Driver Name"],
            "date":        str(row["Date"]),
            "salary":      float(row["Salary"] or 0),
            "transaction": row["Transaction"] or "",
        }
        for _, row in df.iterrows()
    ]

    edited_dates = df["Date"].astype(str).unique().tolist()
    supabase.table("driver_salary") \
        .delete() \
        .in_("date", edited_dates) \
        .execute()
    supabase.table("driver_salary").insert(records).execute()


def get_driver_salary() -> pd.DataFrame:
    res = supabase.table("driver_salary") \
        .select("*") \
        .order("date", desc=True) \
        .execute()

    if not res.data:
        return pd.DataFrame(columns=["Date", "Driver Name", "Salary", "Transaction"])

    df = pd.DataFrame(res.data)
    df = df.rename(columns={
        "date":        "Date",
        "driver_name": "Driver Name",
        "salary":      "Salary",
        "transaction": "Transaction",
    })
    return df[["Date", "Driver Name", "Salary", "Transaction"]]


# ══════════════════════════════════════════════
# VEHICLE EXPENSES
# ══════════════════════════════════════════════

def save_vehicle_expenses(bus_number: str, df: pd.DataFrame) -> None:
    records = [
        {
            "bus_number":  bus_number,
            "date":        str(row["Date"]),
            "category":    row["Category"].strip(),
            "amount":      float(row["Amount"] or 0),
            "description": row["Description"] or "",
        }
        for _, row in df.iterrows()
    ]

    edited_dates = df["Date"].astype(str).unique().tolist()
    supabase.table("vehicle_expenses") \
        .delete() \
        .eq("bus_number", bus_number) \
        .in_("date", edited_dates) \
        .execute()
    supabase.table("vehicle_expenses").insert(records).execute()


def get_vehicle_expenses(bus_number: str) -> pd.DataFrame:
    res = supabase.table("vehicle_expenses") \
        .select("*") \
        .eq("bus_number", bus_number) \
        .order("date", desc=True) \
        .execute()

    if not res.data:
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

    df = pd.DataFrame(res.data)
    df = df.rename(columns={
        "date":        "Date",
        "category":    "Category",
        "amount":      "Amount",
        "description": "Description",
    })
    return df[["Date", "Category", "Amount", "Description"]]


# ══════════════════════════════════════════════
# SALARY CHECK
# ══════════════════════════════════════════════

def get_salary_check(from_date: str = None, to_date: str = None) -> pd.DataFrame:
    res = supabase.table("salary_check").select("*").execute()

    if not res.data:
        return pd.DataFrame(columns=["Sr No", "Driver Name", "Conductor Name", "Duties", "Salary Given"])

    df = pd.DataFrame(res.data)
    df = df.rename(columns={
        "driver_id":      "Sr No",
        "driver_name":    "Driver Name",
        "conductor_name": "Conductor Name",
        "duties":         "Duties",
        "total_salary":   "Salary Given",
    })
    return df[["Sr No", "Driver Name", "Conductor Name", "Duties", "Salary Given"]]