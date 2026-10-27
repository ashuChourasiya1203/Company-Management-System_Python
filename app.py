import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from db_connection import run_query

st.set_page_config(
    page_title="Company Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS (Light + Dark mode adaptive) ────────────────────────────────
st.markdown("""
<style>
/* ── Import Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid rgba(250,189,0,0.15);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label { color: #cbd5e1 !important; font-size: 0.88rem; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] { gap: 4px; }
[data-testid="stSidebar"] hr { border-color: rgba(250,189,0,0.2) !important; }
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(250,189,0,0.12);
    border: 1px solid rgba(250,189,0,0.3);
    color: #fabd00 !important;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.5rem 1rem;
    transition: all 0.2s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(250,189,0,0.25);
    border-color: #fabd00;
}
[data-testid="stSidebar"] .streamlit-expanderHeader {
    background: rgba(250,189,0,0.08) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    color: #fabd00 !important;
    padding: 0.5rem 0.75rem !important;
    margin-bottom: 2px;
}
[data-testid="stSidebar"] .streamlit-expanderContent {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 0 0 8px 8px !important;
    padding: 4px 8px 8px 8px !important;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, rgba(250,189,0,0.12) 0%, rgba(30,41,59,0.6) 100%);
    border: 1px solid rgba(250,189,0,0.25);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(250,189,0,0.15);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #fabd00, #f97316);
    border-radius: 14px 14px 0 0;
}
.kpi-icon {
    font-size: 2rem;
    margin-bottom: 0.4rem;
    display: block;
}
.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.2rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #fabd00;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #64748b;
    margin-top: 0.3rem;
}
.kpi-badge {
    display: inline-block;
    background: rgba(34,197,94,0.15);
    color: #22c55e;
    border-radius: 20px;
    padding: 0.1rem 0.5rem;
    font-size: 0.7rem;
    font-weight: 600;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 1.2rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(250,189,0,0.3);
}
.section-header h3 {
    font-size: 1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
    letter-spacing: 0.02em;
}
.section-icon {
    background: rgba(250,189,0,0.15);
    border-radius: 8px;
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}

/* ── Page Header ── */
.page-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, rgba(250,189,0,0.08) 100%);
    border: 1px solid rgba(250,189,0,0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.page-header h1 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 0.2rem 0;
}
.page-header p {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}
.page-header .gold { color: #fabd00; }

/* ── Chart Cards ── */
.chart-card {
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba(250,189,0,0.12);
    border-radius: 14px;
    padding: 1rem 1.2rem;
}

/* ── Recent Activity Table ── */
.activity-row {
    display: flex;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    gap: 0.8rem;
    font-size: 0.83rem;
}
.activity-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    white-space: nowrap;
}
.badge-green  { background: rgba(34,197,94,0.15);  color: #22c55e; }
.badge-yellow { background: rgba(250,189,0,0.15);  color: #fabd00; }
.badge-red    { background: rgba(239,68,68,0.15);  color: #ef4444; }
.badge-blue   { background: rgba(59,130,246,0.15); color: #3b82f6; }

/* ── Dividers ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(250,189,0,0.4), transparent);
    margin: 1rem 0;
}

/* ── Tabs styling ── */
[data-baseweb="tab-list"] { gap: 4px; }
[data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(250,189,0,0.05);
    border: 1px solid rgba(250,189,0,0.15);
    border-radius: 12px;
    padding: 0.8rem 1rem;
}
[data-testid="stMetricLabel"] { font-size: 0.75rem !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #fabd00 !important; font-weight: 700 !important; }

/* ── Sidebar brand ── */
.sidebar-brand {
    text-align: center;
    padding: 1rem 0.5rem 0.5rem;
}
.sidebar-brand .brand-icon { font-size: 2.5rem; }
.sidebar-brand .brand-title {
    font-size: 1rem;
    font-weight: 700;
    color: #fabd00 !important;
    letter-spacing: 0.05em;
}
.sidebar-brand .brand-sub {
    font-size: 0.7rem;
    color: #64748b !important;
    letter-spacing: 0.1em;
}
.sidebar-section-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569 !important;
    padding: 0.6rem 0.5rem 0.2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div class="sidebar-brand">
  <div class="brand-icon">🏢</div>
  <div class="brand-title">CMS Pro</div>
  <div class="brand-sub">Build · Grow · Succeed</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

if st.sidebar.button("🏠  Dashboard", key="home_btn"):
    st.session_state.active_section = "home"

st.sidebar.markdown('<div class="sidebar-section-label">Master Data</div>', unsafe_allow_html=True)
with st.sidebar.expander("👥  HR Management", expanded=True):
    hr_page = st.radio("HR", ["Employees", "Departments", "Designations", "Managers"],
                       label_visibility="collapsed", key="hr_radio")

st.sidebar.markdown('<div class="sidebar-section-label">Operations</div>', unsafe_allow_html=True)
with st.sidebar.expander("📋  Operations", expanded=False):
    ops_page = st.radio("Ops", ["Attendance", "Leave Requests", "Payroll"],
                        label_visibility="collapsed", key="ops_radio")

st.sidebar.markdown('<div class="sidebar-section-label">Projects</div>', unsafe_allow_html=True)
with st.sidebar.expander("🚀  Projects & Reviews", expanded=False):
    proj_page = st.radio("Projects", ["Projects", "Performance Reviews"],
                         label_visibility="collapsed", key="proj_radio")

st.sidebar.markdown("---")
now = datetime.now()
st.sidebar.markdown(f"""
<div style="text-align:center; font-size:0.72rem; color:#475569; padding: 0.3rem 0;">
  📅 {now.strftime('%b %d, %Y')} &nbsp;·&nbsp; {now.strftime('%A')}
</div>
""", unsafe_allow_html=True)

# ── Page routing ─────────────────────────────────────────────────────────────
if "active_section" not in st.session_state:
    st.session_state.active_section = "home"

prev_hr   = st.session_state.get("prev_hr",   hr_page)
prev_ops  = st.session_state.get("prev_ops",  ops_page)
prev_proj = st.session_state.get("prev_proj", proj_page)

if hr_page != prev_hr:
    st.session_state.active_section = "hr"
elif ops_page != prev_ops:
    st.session_state.active_section = "ops"
elif proj_page != prev_proj:
    st.session_state.active_section = "proj"

st.session_state.prev_hr   = hr_page
st.session_state.prev_ops  = ops_page
st.session_state.prev_proj = proj_page

section = st.session_state.active_section
page = (hr_page if section == "hr" else
        ops_page if section == "ops" else
        proj_page if section == "proj" else "home")


# ── Helpers ──────────────────────────────────────────────────────────────────
def qdf(sql, params=None):
    rows = run_query(sql, params)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def page_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
      <h1>{icon} &nbsp;<span class="gold">{title}</span></h1>
      <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def section_header(icon, title):
    st.markdown(f"""
    <div class="section-header">
      <div class="section-icon">{icon}</div>
      <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(icon, label, value, sub="", badge=""):
    badge_html = f'<div class="kpi-badge">↑ {badge}</div>' if badge else ""
    st.markdown(f"""
    <div class="kpi-card">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub} {badge_html}</div>
    </div>
    """, unsafe_allow_html=True)

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", size=11),
    margin=dict(t=20, b=30, l=10, r=10),
)
GOLD_PALETTE = ["#fabd00", "#f97316", "#3b82f6", "#22c55e", "#a855f7", "#ec4899", "#14b8a6"]


# ════════════════════════════════════════════════════════════════════════════
# HOME DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
def show_home():
    # ── Header
    st.markdown(f"""
    <div class="page-header" style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h1>🏢 &nbsp;<span class="gold">Company Management System</span></h1>
        <p>Manage People &nbsp;·&nbsp; Track Performance &nbsp;·&nbsp; Build Success</p>
      </div>
      <div style="text-align:right; color:#64748b; font-size:0.82rem;">
        <div style="font-size:1.3rem; font-weight:700; color:#fabd00;">{datetime.now().strftime('%b %d, %Y')}</div>
        <div>{datetime.now().strftime('%A')}</div>
        <div style="margin-top:4px; color:#475569;">System Administrator</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs
    emp_r   = run_query("SELECT COUNT(*) AS c FROM employees WHERE employment_status='Active'")
    dept_r  = run_query("SELECT COUNT(*) AS c FROM departments WHERE is_active=1")
    proj_r  = run_query("SELECT COUNT(*) AS c FROM projects")
    pay_r   = run_query("SELECT SUM(net_salary) AS total FROM payroll")
    att_r   = run_query(f"SELECT COUNT(*) AS c FROM attendance WHERE attendance_date='{datetime.now().date()}' AND status='Present'")
    leave_r = run_query("SELECT COUNT(*) AS c FROM leave_requests WHERE status='Pending'")

    emp_val  = emp_r[0]["c"]  if emp_r  else 0
    dept_val = dept_r[0]["c"] if dept_r else 0
    proj_val = proj_r[0]["c"] if proj_r else 0
    pay_val  = pay_r[0]["total"] if pay_r and pay_r[0]["total"] else 0
    att_val  = att_r[0]["c"]  if att_r  else 0
    leave_val= leave_r[0]["c"] if leave_r else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("👥", "Total Employees",    str(emp_val),  "Active headcount",       "Active")
    with c2: kpi_card("🏬", "Departments",         str(dept_val), "Active departments",     "")
    with c3: kpi_card("🚀", "Active Projects",     str(proj_val), "Ongoing & planning",    "")
    with c4: kpi_card("💰", "Total Payroll (INR)", f"₹{pay_val:,.0f}", "All-time net salary", "")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5: kpi_card("📅", "Attendance Today",   f"{att_val} / {emp_val}", f"{round(att_val/emp_val*100) if emp_val else 0}% present", "")
    with c6: kpi_card("🏖", "Pending Leaves",      str(leave_val), "Awaiting approval", "")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ── Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        section_header("👥", "Department-wise Employee Count")
        data = qdf("""
            SELECT d.department_name AS Department, COUNT(e.employee_id) AS Employees
            FROM departments d
            LEFT JOIN employees e ON e.department_id=d.department_id AND e.employment_status='Active'
            GROUP BY d.department_name ORDER BY Employees DESC
        """)
        if not data.empty:
            fig = px.bar(data, x="Department", y="Employees",
                         color="Employees", color_continuous_scale=[[0,"#1e3a5f"],[1,"#fabd00"]],
                         text="Employees")
            fig.update_traces(textposition="outside", textfont_size=10)
            fig.update_layout(**CHART_THEME, coloraxis_showscale=False,
                              xaxis=dict(tickangle=-30, gridcolor="rgba(255,255,255,0.05)"),
                              yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("🏖", "Leave Request Status Distribution")
        data = qdf("SELECT status AS Status, COUNT(*) AS Count FROM leave_requests GROUP BY status")
        if not data.empty:
            fig = px.pie(data, names="Status", values="Count", hole=0.5,
                         color_discrete_sequence=GOLD_PALETTE)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(**CHART_THEME,
                              annotations=[dict(text=f"{data['Count'].sum()}<br>Total", x=0.5, y=0.5,
                                                font_size=13, showarrow=False, font_color="#fabd00")])
            st.plotly_chart(fig, use_container_width=True)

    # ── Charts row 2
    col3, col4 = st.columns(2)

    with col3:
        section_header("💰", "Monthly Payroll Trend")
        data = qdf("""
            SELECT CONCAT(pay_year,'-',LPAD(pay_month,2,'0')) AS Month,
                   SUM(net_salary) AS Net_Salary
            FROM payroll
            GROUP BY pay_year, pay_month
            ORDER BY pay_year, pay_month
            LIMIT 12
        """)
        if not data.empty:
            fig = px.line(data, x="Month", y="Net_Salary",
                          markers=True, line_shape="spline")
            fig.update_traces(line_color="#fabd00", marker_color="#f97316",
                              marker_size=7, fill="tozeroy",
                              fillcolor="rgba(250,189,0,0.08)")
            fig.update_layout(**CHART_THEME,
                              xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                              yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No payroll data available yet.")

    with col4:
        section_header("🚀", "Project Status Overview")
        data = qdf("SELECT status AS Status, COUNT(*) AS Count FROM projects GROUP BY status")
        if not data.empty:
            color_map = {"Planning":"#3b82f6","In Progress":"#fabd00",
                         "Completed":"#22c55e","On Hold":"#a855f7","Cancelled":"#ef4444"}
            colors = [color_map.get(s, "#64748b") for s in data["Status"]]
            fig = px.bar(data, x="Status", y="Count", text="Count",
                         color="Status", color_discrete_map=color_map)
            fig.update_traces(textposition="outside", textfont_size=11)
            fig.update_layout(**CHART_THEME, showlegend=False,
                              xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                              yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
            st.plotly_chart(fig, use_container_width=True)

    # ── Recent Employees
    section_header("🕐", "Recently Joined Employees")
    data = qdf("""
        SELECT e.employee_id AS ID,
               CONCAT(e.first_name,' ',e.last_name) AS Name,
               d.department_name AS Department,
               des.designation_title AS Designation,
               e.joining_date AS Joined,
               e.employment_type AS Type,
               e.employment_status AS Status
        FROM employees e
        JOIN departments d ON d.department_id=e.department_id
        JOIN designations des ON des.designation_id=e.designation_id
        ORDER BY e.joining_date DESC LIMIT 8
    """)
    if not data.empty:
        st.dataframe(data, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════════
# EMPLOYEES
# ════════════════════════════════════════════════════════════════════════════
def show_employees():
    page_header("👥", "Employees", "Manage your workforce — view, search, add and update employee records")
    tab1, tab2 = st.tabs(["📋  View & Search", "➕  Add Employee"])

    with tab1:
        c1, c2 = st.columns([3, 1])
        search = c1.text_input("🔍  Search by name or email", placeholder="e.g. Rahul or rahul@company.com")
        status_f = c2.selectbox("Filter Status", ["All", "Active", "Inactive", "Terminated", "On Leave"])

        base = """
            SELECT e.employee_id AS ID, CONCAT(e.first_name,' ',e.last_name) AS Name,
                   e.email AS Email, e.phone AS Phone,
                   d.department_name AS Department, des.designation_title AS Designation,
                   e.joining_date AS Joined, e.salary AS Salary,
                   e.employment_type AS Type, e.employment_status AS Status
            FROM employees e
            JOIN departments d ON d.department_id=e.department_id
            JOIN designations des ON des.designation_id=e.designation_id
        """
        filters, params = [], []
        if search:
            filters.append("(e.first_name LIKE %s OR e.last_name LIKE %s OR e.email LIKE %s)")
            params += [f"%{search}%", f"%{search}%", f"%{search}%"]
        if status_f != "All":
            filters.append("e.employment_status=%s")
            params.append(status_f)
        where = ("WHERE " + " AND ".join(filters)) if filters else ""
        data = qdf(base + where + " ORDER BY e.joining_date DESC", params or None)
        st.caption(f"Showing **{len(data)}** employees")
        st.dataframe(data, use_container_width=True, hide_index=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        section_header("✏️", "Update Employee Salary / Status")
        st.caption("Enter the Employee ID from the table above to update their details.")
        with st.form("update_emp"):
            c1, c2, c3 = st.columns(3)
            emp_id     = c1.number_input("Employee ID", min_value=1, step=1)
            salary     = c2.number_input("New Annual Salary (INR)", min_value=0.0, step=1000.0)
            emp_status = c3.selectbox("Employment Status", ["Active", "Inactive", "Terminated", "On Leave"])
            if st.form_submit_button("💾  Save Changes"):
                ok = run_query(
                    "UPDATE employees SET salary=%s, employment_status=%s WHERE employee_id=%s",
                    (salary, emp_status, emp_id), fetch=False)
                st.success("✅ Employee updated successfully!") if ok else st.error("Update failed.")

    with tab2:
        section_header("➕", "Add New Employee")
        st.caption("Fill in all required fields to register a new employee in the system.")
        depts  = run_query("SELECT department_id, department_name FROM departments WHERE is_active=1")
        desigs = run_query("SELECT designation_id, designation_title FROM designations")
        dept_map  = {d["department_name"]: d["department_id"] for d in depts}  if depts  else {}
        desig_map = {d["designation_title"]: d["designation_id"] for d in desigs} if desigs else {}

        with st.form("add_emp"):
            st.markdown("**Personal Information**")
            c1, c2, c3 = st.columns(3)
            first_name = c1.text_input("First Name *")
            last_name  = c2.text_input("Last Name *")
            gender     = c3.selectbox("Gender", ["Male", "Female", "Other"])
            c4, c5, c6 = st.columns(3)
            email = c4.text_input("Email *")
            phone = c5.text_input("Phone *")
            dob   = c6.date_input("Date of Birth")

            st.markdown("**Work Details**")
            c7, c8, c9 = st.columns(3)
            dept_sel     = c7.selectbox("Department *", list(dept_map.keys()))
            desig_sel    = c8.selectbox("Designation *", list(desig_map.keys()))
            emp_type     = c9.selectbox("Employment Type", ["Full-Time", "Part-Time", "Contract", "Intern"])
            c10, c11, c12 = st.columns(3)
            joining_date = c10.date_input("Joining Date")
            salary       = c11.number_input("Annual Salary (INR) *", min_value=0.0, step=1000.0)

            st.markdown("**Address**")
            c13, c14 = st.columns(2)
            address = c13.text_input("Address")
            city    = c14.text_input("City")
            c15, c16 = st.columns(2)
            state  = c15.text_input("State")
            postal = c16.text_input("Postal Code")

            if st.form_submit_button("➕  Add Employee"):
                ok = run_query("""
                    INSERT INTO employees
                    (first_name,last_name,email,phone,department_id,designation_id,
                     joining_date,salary,employment_type,gender,date_of_birth,
                     address,city,state,postal_code)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (first_name, last_name, email, phone,
                      dept_map.get(dept_sel), desig_map.get(desig_sel),
                      joining_date, salary, emp_type, gender, dob,
                      address, city, state, postal), fetch=False)
                st.success("✅ Employee added successfully!") if ok else st.error("Insert failed.")


# ════════════════════════════════════════════════════════════════════════════
# DEPARTMENTS
# ════════════════════════════════════════════════════════════════════════════
def show_departments():
    page_header("🏬", "Departments", "View and manage all company departments, budgets and heads")
    tab1, tab2 = st.tabs(["📋  View Departments", "➕  Add / Update"])

    with tab1:
        data = qdf("""
            SELECT d.department_id AS ID, d.department_code AS Code,
                   d.department_name AS Name, d.location AS Location,
                   d.annual_budget AS Budget, d.phone_extension AS Ext,
                   CONCAT(e.first_name,' ',e.last_name) AS Head,
                   d.is_active AS Active
            FROM departments d
            LEFT JOIN employees e ON e.employee_id=d.head_employee_id
        """)
        st.caption(f"**{len(data)}** departments found")
        st.dataframe(data, use_container_width=True, hide_index=True)

        # Mini budget chart
        if not data.empty:
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            section_header("💰", "Budget Distribution")
            fig = px.bar(data.sort_values("Budget", ascending=False),
                         x="Name", y="Budget", color="Budget",
                         color_continuous_scale=[[0,"#1e3a5f"],[1,"#fabd00"]],
                         text="Budget")
            fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig.update_layout(**CHART_THEME, coloraxis_showscale=False,
                              xaxis=dict(tickangle=-30, gridcolor="rgba(255,255,255,0.05)"),
                              yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        section_header("➕", "Add Department")
        st.caption("Create a new department by filling in the details below.")
        with st.form("add_dept"):
            c1, c2, c3 = st.columns(3)
            code   = c1.text_input("Department Code *", placeholder="e.g. ENG")
            name   = c2.text_input("Department Name *")
            loc    = c3.text_input("Location *")
            c4, c5 = st.columns(2)
            budget = c4.number_input("Annual Budget (INR)", min_value=0.0, step=10000.0)
            ext    = c5.text_input("Phone Extension")
            if st.form_submit_button("➕  Add Department"):
                ok = run_query("""
                    INSERT INTO departments (department_code,department_name,location,annual_budget,phone_extension)
                    VALUES (%s,%s,%s,%s,%s)
                """, (code, name, loc, budget, ext or None), fetch=False)
                st.success("✅ Department added!") if ok else st.error("Insert failed.")

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        section_header("✏️", "Update Department Budget")
        with st.form("upd_dept"):
            c1, c2 = st.columns(2)
            dept_id = c1.number_input("Department ID", min_value=1, step=1)
            budget  = c2.number_input("New Annual Budget (INR)", min_value=0.0, step=10000.0)
            if st.form_submit_button("💾  Update Budget"):
                ok = run_query("UPDATE departments SET annual_budget=%s WHERE department_id=%s",
                               (budget, dept_id), fetch=False)
                st.success("✅ Budget updated!") if ok else st.error("Failed.")


# ════════════════════════════════════════════════════════════════════════════
# DESIGNATIONS
# ════════════════════════════════════════════════════════════════════════════
def show_designations():
    page_header("🎖", "Designations", "Manage job titles, grade levels and salary bands")
    data = qdf("""
        SELECT des.designation_id AS ID, des.designation_title AS Title,
               d.department_name AS Department, des.job_level AS Level,
               des.min_salary AS Min_Salary, des.max_salary AS Max_Salary,
               des.is_managerial AS Managerial
        FROM designations des
        JOIN departments d ON d.department_id=des.department_id
        ORDER BY des.job_level DESC
    """)
    st.caption(f"**{len(data)}** designations")
    st.dataframe(data, use_container_width=True, hide_index=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    section_header("➕", "Add New Designation")
    st.caption("Define a new role with salary band and job level.")
    with st.form("add_desig"):
        c1, c2, c3 = st.columns(3)
        title    = c1.text_input("Designation Title *")
        depts    = run_query("SELECT department_id, department_name FROM departments WHERE is_active=1")
        dept_map = {d["department_name"]: d["department_id"] for d in depts} if depts else {}
        dept_sel = c2.selectbox("Department *", list(dept_map.keys()))
        job_lvl  = c3.number_input("Job Level", min_value=1, step=1)
        c4, c5, c6 = st.columns(3)
        min_sal  = c4.number_input("Min Salary (INR)", min_value=0.0, step=1000.0)
        max_sal  = c5.number_input("Max Salary (INR)", min_value=0.0, step=1000.0)
        is_mgr   = c6.checkbox("Is Managerial Role")
        if st.form_submit_button("➕  Add Designation"):
            ok = run_query("""
                INSERT INTO designations (designation_title,department_id,job_level,min_salary,max_salary,is_managerial)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (title, dept_map.get(dept_sel), job_lvl, min_sal, max_sal, is_mgr), fetch=False)
            st.success("✅ Added!") if ok else st.error("Failed.")


# ════════════════════════════════════════════════════════════════════════════
# MANAGERS
# ════════════════════════════════════════════════════════════════════════════
def show_managers():
    page_header("👔", "Managers", "View all department managers and their tenure details")
    data = qdf("""
        SELECT m.manager_id AS ID,
               CONCAT(e.first_name,' ',e.last_name) AS Manager,
               d.department_name AS Department,
               m.manager_level AS Level,
               m.appointed_date AS Appointed,
               m.is_active AS Active
        FROM managers m
        JOIN employees e ON e.employee_id=m.employee_id
        JOIN departments d ON d.department_id=m.department_id
        ORDER BY m.appointed_date DESC
    """)
    st.caption(f"**{len(data)}** managers")
    st.dataframe(data, use_container_width=True, hide_index=True)

    if not data.empty:
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        section_header("📊", "Managers by Department")
        dept_count = data.groupby("Department").size().reset_index(name="Count")
        fig = px.pie(dept_count, names="Department", values="Count", hole=0.45,
                     color_discrete_sequence=GOLD_PALETTE)
        fig.update_layout(**CHART_THEME)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# ATTENDANCE
# ════════════════════════════════════════════════════════════════════════════
def show_attendance():
    page_header("📅", "Attendance", "Track daily attendance — check-in/out times and present/absent status")
    tab1, tab2 = st.tabs(["📋  View Records", "➕  Log Attendance"])

    with tab1:
        c1, c2 = st.columns([2, 2])
        emp_id   = c1.number_input("Filter by Employee ID (0 = all)", min_value=0, step=1)
        status_f = c2.selectbox("Filter by Status", ["All", "Present", "Absent", "Late", "Half-day", "WFH"])

        if emp_id and status_f != "All":
            data = qdf("SELECT * FROM attendance WHERE employee_id=%s AND status=%s ORDER BY attendance_date DESC LIMIT 50",
                       (emp_id, status_f))
        elif emp_id:
            data = qdf("SELECT * FROM attendance WHERE employee_id=%s ORDER BY attendance_date DESC LIMIT 50", (emp_id,))
        elif status_f != "All":
            data = qdf("SELECT * FROM attendance WHERE status=%s ORDER BY attendance_date DESC LIMIT 100", (status_f,))
        else:
            data = qdf("SELECT * FROM attendance ORDER BY attendance_date DESC LIMIT 100")

        st.caption(f"Showing **{len(data)}** records")
        st.dataframe(data, use_container_width=True, hide_index=True)

    with tab2:
        section_header("➕", "Log Attendance Entry")
        st.caption("Mark attendance for an employee. Duplicate entries update existing records.")
        with st.form("log_att"):
            c1, c2, c3 = st.columns(3)
            emp_id   = c1.number_input("Employee ID *", min_value=1, step=1)
            att_date = c2.date_input("Date")
            status   = c3.selectbox("Status", ["Present", "Absent", "Late", "Half-day", "WFH"])
            c4, c5 = st.columns(2)
            check_in  = c4.time_input("Check In Time")
            check_out = c5.time_input("Check Out Time")
            if st.form_submit_button("💾  Save Attendance"):
                ok = run_query("""
                    INSERT INTO attendance (employee_id,attendance_date,status,check_in,check_out)
                    VALUES (%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE status=%s, check_in=%s, check_out=%s
                """, (emp_id, att_date, status, check_in, check_out,
                      status, check_in, check_out), fetch=False)
                st.success("✅ Attendance logged!") if ok else st.error("Failed.")


# ════════════════════════════════════════════════════════════════════════════
# LEAVE REQUESTS
# ════════════════════════════════════════════════════════════════════════════
def show_leave():
    page_header("🏖", "Leave Requests", "Manage employee leave applications — approve, reject or submit new requests")
    tab1, tab2 = st.tabs(["📋  View & Manage", "➕  New Request"])

    with tab1:
        c1, c2 = st.columns(2)
        status_filter = c1.selectbox("Filter by Status", ["All", "Pending", "Approved", "Rejected"])
        leave_type_f  = c2.selectbox("Filter by Type", ["All", "Annual", "Sick", "Casual", "Maternity", "Paternity", "Unpaid"])

        base = """
            SELECT lr.leave_id AS ID,
                   CONCAT(e.first_name,' ',e.last_name) AS Employee,
                   lr.leave_type AS Type, lr.start_date AS From,
                   lr.end_date AS To, lr.total_days AS Days,
                   lr.reason AS Reason, lr.status AS Status,
                   lr.applied_at AS Applied
            FROM leave_requests lr
            JOIN employees e ON e.employee_id=lr.employee_id
        """
        filters, params = [], []
        if status_filter != "All":
            filters.append("lr.status=%s"); params.append(status_filter)
        if leave_type_f != "All":
            filters.append("lr.leave_type=%s"); params.append(leave_type_f)
        where = ("WHERE " + " AND ".join(filters)) if filters else ""
        data = qdf(base + where + " ORDER BY lr.applied_at DESC LIMIT 100", params or None)
        st.caption(f"**{len(data)}** leave requests")
        st.dataframe(data, use_container_width=True, hide_index=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        section_header("✏️", "Approve / Reject a Leave Request")
        st.caption("Enter the Leave ID from the table above.")
        with st.form("upd_leave"):
            c1, c2, c3 = st.columns(3)
            leave_id   = c1.number_input("Leave ID", min_value=1, step=1)
            new_status = c2.selectbox("New Status", ["Approved", "Rejected", "Pending"])
            remarks    = c3.text_input("Reviewer Comments")
            if st.form_submit_button("💾  Update Status"):
                ok = run_query(
                    "UPDATE leave_requests SET status=%s, reviewer_comments=%s WHERE leave_id=%s",
                    (new_status, remarks, leave_id), fetch=False)
                st.success("✅ Updated!") if ok else st.error("Failed.")

    with tab2:
        section_header("➕", "Submit New Leave Request")
        st.caption("Fill in the details to submit a leave request on behalf of an employee.")
        with st.form("new_leave"):
            c1, c2, c3 = st.columns(3)
            emp_id     = c1.number_input("Employee ID *", min_value=1, step=1)
            leave_type = c2.selectbox("Leave Type", ["Annual", "Sick", "Casual", "Maternity", "Paternity", "Unpaid"])
            c4, c5 = st.columns(2)
            start_date = c4.date_input("Start Date")
            end_date   = c5.date_input("End Date")
            reason     = st.text_area("Reason for Leave *", placeholder="Briefly describe the reason...")
            if st.form_submit_button("📤  Submit Request"):
                ok = run_query("""
                    INSERT INTO leave_requests (employee_id,leave_type,start_date,end_date,reason)
                    VALUES (%s,%s,%s,%s,%s)
                """, (emp_id, leave_type, start_date, end_date, reason), fetch=False)
                st.success("✅ Leave request submitted!") if ok else st.error("Failed.")


# ════════════════════════════════════════════════════════════════════════════
# PAYROLL
# ════════════════════════════════════════════════════════════════════════════
def show_payroll():
    page_header("💰", "Payroll", "View monthly salary records, process payments and add new payroll entries")
    tab1, tab2 = st.tabs(["📋  View Payroll", "➕  Add Entry"])

    with tab1:
        c1, c2 = st.columns(2)
        month = c1.selectbox("Month", list(range(1, 13)),
                             format_func=lambda m: datetime(2000,m,1).strftime("%B"), index=9)
        year  = c2.number_input("Year", min_value=2020, max_value=2030, value=2025)
        data  = qdf("""
            SELECT p.payroll_id AS ID,
                   CONCAT(e.first_name,' ',e.last_name) AS Employee,
                   p.pay_month AS Month, p.pay_year AS Year,
                   p.basic_salary AS Basic, p.hra AS HRA,
                   p.special_allowance AS Allowance, p.bonus AS Bonus,
                   p.gross_salary AS Gross, p.total_deductions AS Deductions,
                   p.net_salary AS Net, p.payment_status AS Status
            FROM payroll p JOIN employees e ON e.employee_id=p.employee_id
            WHERE p.pay_month=%s AND p.pay_year=%s
            ORDER BY p.net_salary DESC
        """, (month, year))

        if not data.empty:
            m1, m2, m3 = st.columns(3)
            m1.metric("Employees Paid",  len(data))
            m2.metric("Total Gross Pay", f"₹{data['Gross'].sum():,.0f}")
            m3.metric("Total Net Pay",   f"₹{data['Net'].sum():,.0f}")
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.caption(f"**{len(data)}** payroll records")
        st.dataframe(data, use_container_width=True, hide_index=True)

    with tab2:
        section_header("➕", "Add Payroll Entry")
        st.caption("Enter monthly salary components for an employee.")
        with st.form("add_payroll"):
            c1, c2, c3, c4 = st.columns(4)
            emp_id    = c1.number_input("Employee ID *", min_value=1, step=1)
            month_    = c2.number_input("Month", min_value=1, max_value=12)
            year_     = c3.number_input("Year", min_value=2020, max_value=2030, value=2025)
            days_in   = c4.number_input("Days in Month", min_value=28, max_value=31, value=30)
            c5, c6 = st.columns(2)
            paid_days = c5.number_input("Paid Days", min_value=0.0, max_value=31.0, value=30.0)
            status_   = c6.selectbox("Payment Status", ["Pending", "Processed", "Failed"])

            st.markdown("**Earnings**")
            e1, e2, e3, e4 = st.columns(4)
            basic   = e1.number_input("Basic Salary", min_value=0.0, step=1000.0)
            hra     = e2.number_input("HRA", min_value=0.0, step=500.0)
            special = e3.number_input("Special Allowance", min_value=0.0, step=500.0)
            bonus   = e4.number_input("Bonus", min_value=0.0, step=500.0)

            st.markdown("**Deductions**")
            d1, d2, d3 = st.columns(3)
            pf = d1.number_input("PF Deduction", min_value=0.0, step=100.0)
            pt = d2.number_input("Professional Tax", min_value=0.0, step=100.0)
            it = d3.number_input("Income Tax", min_value=0.0, step=100.0)

            est_net = basic + hra + special + bonus - pf - pt - it
            st.info(f"💡 Estimated Net Salary: **₹{est_net:,.2f}**")

            if st.form_submit_button("💾  Add Payroll Entry"):
                ok = run_query("""
                    INSERT INTO payroll
                    (employee_id,pay_year,pay_month,days_in_month,paid_days,
                     basic_salary,hra,special_allowance,bonus,
                     pf_deduction,professional_tax,income_tax,payment_status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (emp_id, year_, month_, days_in, paid_days,
                      basic, hra, special, bonus, pf, pt, it, status_), fetch=False)
                st.success("✅ Payroll entry added!") if ok else st.error("Failed.")


# ════════════════════════════════════════════════════════════════════════════
# PROJECTS
# ════════════════════════════════════════════════════════════════════════════
def show_projects():
    page_header("🚀", "Projects", "Track all company projects — view status, assign team members and manage budgets")
    tab1, tab2, tab3 = st.tabs(["📋  View Projects", "👤  Assign Employee", "➕  Add Project"])

    with tab1:
        status_f = st.selectbox("Filter by Status", ["All", "Planning", "In Progress", "On Hold", "Completed", "Cancelled"])
        if status_f == "All":
            data = qdf("""
                SELECT p.project_id AS ID, p.project_name AS Name, p.project_code AS Code,
                       d.department_name AS Department, p.start_date AS Start,
                       p.end_date AS End, p.status AS Status,
                       p.priority AS Priority, p.budget AS Budget
                FROM projects p LEFT JOIN departments d ON d.department_id=p.department_id
                ORDER BY p.start_date DESC
            """)
        else:
            data = qdf("""
                SELECT p.project_id AS ID, p.project_name AS Name, p.project_code AS Code,
                       d.department_name AS Department, p.start_date AS Start,
                       p.end_date AS End, p.status AS Status,
                       p.priority AS Priority, p.budget AS Budget
                FROM projects p LEFT JOIN departments d ON d.department_id=p.department_id
                WHERE p.status=%s ORDER BY p.start_date DESC
            """, (status_f,))
        st.caption(f"**{len(data)}** projects")
        st.dataframe(data, use_container_width=True, hide_index=True)

    with tab2:
        section_header("👤", "Assign Employee to Project")
        st.caption("Link an employee to a project with their role and start date.")
        with st.form("assign_proj"):
            c1, c2, c3, c4 = st.columns(4)
            proj_id = c1.number_input("Project ID *", min_value=1, step=1)
            emp_id  = c2.number_input("Employee ID *", min_value=1, step=1)
            role    = c3.text_input("Role on Project *", placeholder="e.g. Developer")
            start   = c4.date_input("Assigned Date")
            if st.form_submit_button("👤  Assign"):
                ok = run_query("""
                    INSERT INTO employee_projects (project_id,employee_id,project_role,assigned_date)
                    VALUES (%s,%s,%s,%s)
                """, (proj_id, emp_id, role, start), fetch=False)
                st.success("✅ Assigned!") if ok else st.error("Failed.")

    with tab3:
        section_header("➕", "Add New Project")
        st.caption("Create a new project and assign it to a department.")
        with st.form("add_proj"):
            c1, c2, c3 = st.columns(3)
            name   = c1.text_input("Project Name *")
            code   = c2.text_input("Project Code *")
            depts  = run_query("SELECT department_id, department_name FROM departments WHERE is_active=1")
            dept_map = {d["department_name"]: d["department_id"] for d in depts} if depts else {}
            dept_sel = c3.selectbox("Department *", list(dept_map.keys()))
            c4, c5, c6 = st.columns(3)
            start   = c4.date_input("Start Date")
            end     = c5.date_input("End Date")
            budget  = c6.number_input("Budget (INR)", min_value=0.0, step=10000.0)
            c7, c8 = st.columns(2)
            status_ = c7.selectbox("Status", ["Planning", "In Progress", "On Hold", "Completed", "Cancelled"])
            priority= c8.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            desc    = st.text_area("Project Description", placeholder="Brief overview of the project goals...")
            if st.form_submit_button("🚀  Add Project"):
                ok = run_query("""
                    INSERT INTO projects
                    (project_name,project_code,department_id,start_date,end_date,budget,status,priority,description)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (name, code, dept_map.get(dept_sel), start, end, budget, status_, priority, desc), fetch=False)
                st.success("✅ Project added!") if ok else st.error("Failed.")


# ════════════════════════════════════════════════════════════════════════════
# PERFORMANCE REVIEWS
# ════════════════════════════════════════════════════════════════════════════
def show_reviews():
    page_header("⭐", "Performance Reviews", "Track employee performance across key skill areas and cycles")
    tab1, tab2 = st.tabs(["📋  View Reviews", "➕  Add Review"])

    with tab1:
        c1, c2 = st.columns(2)
        year_f  = c1.number_input("Filter by Year", min_value=2020, max_value=2030, value=2025)
        cycle_f = c2.selectbox("Filter by Cycle", ["All", "H1", "H2", "Q1", "Q2", "Q3", "Q4"])

        if cycle_f == "All":
            data = qdf("""
                SELECT pr.review_id AS ID,
                       CONCAT(e.first_name,' ',e.last_name) AS Employee,
                       pr.review_year AS Year, pr.review_cycle AS Cycle,
                       pr.review_date AS Date, pr.technical_skills AS Tech,
                       pr.communication AS Comm, pr.teamwork AS Team,
                       pr.productivity AS Prod, pr.leadership AS Lead,
                       pr.overall_rating AS Rating,
                       pr.promotion_recommended AS Promotion,
                       pr.review_status AS Status
                FROM performance_reviews pr
                JOIN employees e ON e.employee_id=pr.employee_id
                WHERE pr.review_year=%s ORDER BY pr.review_date DESC
            """, (year_f,))
        else:
            data = qdf("""
                SELECT pr.review_id AS ID,
                       CONCAT(e.first_name,' ',e.last_name) AS Employee,
                       pr.review_year AS Year, pr.review_cycle AS Cycle,
                       pr.review_date AS Date, pr.technical_skills AS Tech,
                       pr.communication AS Comm, pr.teamwork AS Team,
                       pr.productivity AS Prod, pr.leadership AS Lead,
                       pr.overall_rating AS Rating,
                       pr.promotion_recommended AS Promotion,
                       pr.review_status AS Status
                FROM performance_reviews pr
                JOIN employees e ON e.employee_id=pr.employee_id
                WHERE pr.review_year=%s AND pr.review_cycle=%s
                ORDER BY pr.review_date DESC
            """, (year_f, cycle_f))
        st.caption(f"**{len(data)}** reviews")
        st.dataframe(data, use_container_width=True, hide_index=True)

        if not data.empty and "Rating" in data.columns:
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            section_header("📊", "Average Skill Scores")
            skills = ["Tech", "Comm", "Team", "Prod", "Lead"]
            avgs   = [round(data[s].mean(), 1) for s in skills]
            fig = go.Figure(go.Bar(x=skills, y=avgs, marker_color=GOLD_PALETTE[:5],
                                   text=avgs, textposition="outside"))
            fig.update_layout(**CHART_THEME, yaxis_range=[0, 11],
                              xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                              yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        section_header("➕", "Submit Performance Review")
        st.caption("Rate an employee across five key dimensions for a given review cycle.")
        with st.form("add_review"):
            c1, c2, c3, c4 = st.columns(4)
            emp_id   = c1.number_input("Employee ID *", min_value=1, step=1)
            rev_year = c2.number_input("Review Year", min_value=2020, max_value=2030, value=2025)
            cycle    = c3.selectbox("Cycle", ["H1", "H2", "Q1", "Q2", "Q3", "Q4"])
            rev_date = c4.date_input("Review Date")

            st.markdown("**Skill Ratings (1 = Poor → 10 = Excellent)**")
            s1, s2, s3, s4, s5 = st.columns(5)
            tech = s1.slider("Technical", 1, 10, 7)
            comm = s2.slider("Communication", 1, 10, 7)
            team = s3.slider("Teamwork", 1, 10, 7)
            prod = s4.slider("Productivity", 1, 10, 7)
            lead = s5.slider("Leadership", 1, 10, 7)

            c7, c8 = st.columns(2)
            promo    = c7.checkbox("Recommend for Promotion")
            comments = c8.text_area("Comments", placeholder="Summarize the review...")

            avg = round((tech + comm + team + prod + lead) / 5, 1)
            st.info(f"⭐ Calculated Overall Rating: **{avg} / 10**")

            if st.form_submit_button("⭐  Submit Review"):
                ok = run_query("""
                    INSERT INTO performance_reviews
                    (employee_id,review_year,review_cycle,review_date,
                     technical_skills,communication,teamwork,productivity,leadership,
                     promotion_recommended,comments)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (emp_id, rev_year, cycle, rev_date,
                      tech, comm, team, prod, lead, promo, comments), fetch=False)
                st.success("✅ Review submitted!") if ok else st.error("Failed.")


# ── Router ────────────────────────────────────────────────────────────────────
PAGE_MAP = {
    "home":                show_home,
    "Employees":           show_employees,
    "Departments":         show_departments,
    "Designations":        show_designations,
    "Managers":            show_managers,
    "Attendance":          show_attendance,
    "Leave Requests":      show_leave,
    "Payroll":             show_payroll,
    "Projects":            show_projects,
    "Performance Reviews": show_reviews,
}

PAGE_MAP.get(page, show_home)()
