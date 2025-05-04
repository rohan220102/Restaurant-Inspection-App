import sqlite3
import pandas as pd
import streamlit as st
import hashlib

# --- 1. Database connection ----------------------------------------
# New decorator in recent Streamlit
@st.cache_resource
def get_connection():
    return sqlite3.connect("restaurant_inspections.db", check_same_thread=False)

conn = get_connection()



# --- 2. User table init & auth helpers ----------------------------
def init_user_table():
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username: str, password: str) -> bool:
    cur = conn.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    return bool(row and row[0] == hash_password(password))

init_user_table()

# --- 3. Authentication pages ---------------------------------------
def signup_page():
    st.header("🔐 Sign Up")
    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")
    if st.button("Create account"):
        if not new_user or not new_pass:
            st.error("Fill both fields.")
        elif conn.execute("SELECT 1 FROM users WHERE username = ?", (new_user,)).fetchone():
            st.error("That username is already taken.")
        else:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (new_user, hash_password(new_pass))
            )
            conn.commit()
            st.success("Account created! Please switch to Log In.")

def login_page():
    st.header("🔑 Log In")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Log In"):
        if verify_password(user, pwd):
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"Welcome, {user}!")
        else:
            st.error("Invalid username or password.")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# --- 4. Show auth or main app --------------------------------------
if not st.session_state.logged_in:
    st.sidebar.title("Account")
    choice = st.sidebar.radio("", ["Log In", "Sign Up"])
    if choice == "Sign Up":
        signup_page()
    else:
        login_page()
    st.stop()  # stop here until logged in

# --- 5. After login: show logout button ----------------------------
st.sidebar.write(f"👤 Logged in as **{st.session_state.user}**")
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.sidebar.success("You’ve been logged out. Please refresh the page or click any control to continue.")


# --- 6. Main CRUD + Visualization ---------------------------------
st.sidebar.title("Controls")
tables = ["establishment", "employee", "inspection", "violation", "inspection_point"]
table = st.sidebar.selectbox("Select table", tables)
action = st.sidebar.selectbox("Action", ["Read", "Create", "Update", "Delete", "Visualize"])

# Load table into DataFrame
df = pd.read_sql(f"SELECT * FROM {table}", conn)

if action == "Read":
    st.header(f"All records in `{table}`")
    st.dataframe(df)

elif action == "Create":
    st.header(f"Create a new record in `{table}`")
    inputs = {}
    for col, dtype in zip(df.columns, df.dtypes):
        # skip primary key (assumed first column with 'id' or 'no')
        if col == df.columns[0]:
            continue
        if dtype == "int64":
            inputs[col] = st.number_input(col, value=0, step=1)
        elif dtype == "float64":
            inputs[col] = st.number_input(col, value=0.0)
        else:
            inputs[col] = st.text_input(col, "")

    if st.button("Insert"):
        cols = ", ".join(inputs.keys())
        placeholders = ", ".join("?" for _ in inputs)
        conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})", tuple(inputs.values()))
        conn.commit()
        st.success("Record inserted!")

elif action == "Update":
    st.header(f"Update an existing record in `{table}`")
    pk = df.columns[0]
    record_id = st.selectbox(f"Select {pk} to update", df[pk].tolist())
    record = df[df[pk] == record_id].iloc[0]

    updates = {}
    for col, dtype in zip(df.columns, df.dtypes):
        if col == pk:
            continue
        if dtype == "int64":
            updates[col] = st.number_input(col, value=int(record[col]), step=1)
        elif dtype == "float64":
            updates[col] = st.number_input(col, value=float(record[col]))
        else:
            updates[col] = st.text_input(col, value=str(record[col]))

    if st.button("Save changes"):
        set_clause = ", ".join(f"{c}=?" for c in updates)
        conn.execute(f"UPDATE {table} SET {set_clause} WHERE {pk} = ?", (*updates.values(), record_id))
        conn.commit()
        st.success("Record updated!")

elif action == "Delete":
    st.header(f"Delete a record from `{table}`")
    pk = df.columns[0]
    record_id = st.selectbox(f"Select {pk} to delete", df[pk].tolist())
    if st.button("Delete"):
        conn.execute(f"DELETE FROM {table} WHERE {pk} = ?", (record_id,))
        conn.commit()
        st.success("Record deleted!")

elif action == "Visualize":
    st.header(f"Visualize `{table}`")
    numerics = df.select_dtypes(["int64", "float64"]).columns.tolist()
    categories = df.select_dtypes(["object", "string"]).columns.tolist()

    chart = st.selectbox("Chart type", ["Bar chart", "Line chart", "Map"])
    if chart in ["Bar chart", "Line chart"]:
        x = st.selectbox("X (categorical)", categories)
        y = st.selectbox("Y (numeric)", numerics)
        agg = st.selectbox("Aggregation", ["mean", "sum", "count"])
        grouped = getattr(df.groupby(x)[y], agg)().reset_index().set_index(x)
        if chart == "Bar chart":
            st.bar_chart(grouped)
        else:
            st.line_chart(grouped)

    else:  # Map
        if {"latitude", "longitude"}.issubset(df.columns):
            st.map(df[["latitude", "longitude"]].dropna())
        else:
            st.error("No latitude/longitude in this table.")
