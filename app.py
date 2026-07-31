import pandas as pd
import streamlit as st

# ---- Colors (ported from the original React dashboard) ----
NAVY = "#1F2A5C"
ACCENT = "#5B67D6"
GREEN = "#1E9E63"
GREENBG = "#E9F6EF"
RED = "#C23B34"
REDBG = "#FBEDEC"
AMBER = "#B8862A"
AMBERBG = "#FBF3E4"
INK = "#1A2340"
MUTED = "#6B7290"
BORDER = "#DDE0F5"
CALLOUT = "#EEF0FC"

st.set_page_config(page_title="GM weekly report", page_icon="\U0001F30A", layout="wide")

st.markdown(
    f"""
    <style>
    .stApp {{ background: #EFF1FA; }}
    .block-container {{ padding-top: 1rem; max-width: 1100px; }}
    .gac-header {{
        background: {NAVY}; padding: 22px 28px; border-radius: 12px;
        margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center;
    }}
    .gac-header h1 {{ color: #fff; font-size: 22px; margin: 0; }}
    .gac-header p {{ color: #C7CCF0; margin: 2px 0 0; font-size: 13px; }}
    .gac-tag {{
        display: inline-flex; align-items: center; font-size: 10.5px; font-weight: 700;
        padding: 3px 10px; border-radius: 20px; letter-spacing: 0.2px;
        text-transform: uppercase; white-space: nowrap;
    }}
    .gac-callout {{
        display: flex; gap: 10px; border-radius: 8px; padding: 10px 14px;
        font-size: 13px; line-height: 1.5; margin: 10px 0;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

TAG_STYLES = {
    "live": (GREENBG, "#0F6E45", "Live JackRabbit data"),
    "proxy": (AMBERBG, "#8A5F14", "Derived proxy · pending definition"),
    "mock": (REDBG, "#9C3A32", "Illustrative · source TBD"),
    "partial": (AMBERBG, "#8A5F14", "Partly live, partly illustrative"),
}

CALLOUT_STYLES = {
    "info": (CALLOUT, ACCENT, INK),
    "good": (GREENBG, GREEN, "#0F6E45"),
    "warn": (AMBERBG, AMBER, "#8A5F14"),
}


def tag_html(kind):
    bg, fg, label = TAG_STYLES[kind]
    return f'<span class="gac-tag" style="background:{bg};color:{fg};">{label}</span>'


def section_title(icon, title, subtitle, tag=None):
    left, right = st.columns([4, 1])
    with left:
        st.markdown(f"### {icon} {title}")
        st.caption(subtitle)
    with right:
        if tag:
            st.markdown(
                f'<div style="text-align:right;padding-top:10px">{tag_html(tag)}</div>',
                unsafe_allow_html=True,
            )


def kpi_row(items):
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            with st.container(border=True):
                st.markdown(
                    f'<div style="font-size:10.5px;font-weight:700;color:{MUTED};'
                    f'text-transform:uppercase;letter-spacing:0.4px">{item["label"]}</div>',
                    unsafe_allow_html=True,
                )
                delta = item.get("delta")
                st.metric(label="", value=item["value"], delta=delta, label_visibility="collapsed")
                if item.get("sub"):
                    st.caption(item["sub"])


def callout(text, tone="info"):
    bg, bar, fg = CALLOUT_STYLES[tone]
    st.markdown(
        f'<div class="gac-callout" style="background:{bg};border-left:3px solid {bar};color:{fg}">{text}</div>',
        unsafe_allow_html=True,
    )


def plain_table(df):
    st.dataframe(df, hide_index=True, use_container_width=True)


def data_table(df, filter_col=None, default_sort_col=None, default_sort_desc=False):
    filtered = df
    if filter_col:
        options = ["All"] + sorted(df[filter_col].unique().tolist())
        choice = st.selectbox(f"Filter by {filter_col}", options, key=f"filter_{filter_col}_{id(df)}")
        if choice != "All":
            filtered = df[df[filter_col] == choice]
        st.caption(f"{len(filtered)} of {len(df)} rows · click a column header to sort")
    if default_sort_col:
        filtered = filtered.sort_values(default_sort_col, ascending=not default_sort_desc)
    st.dataframe(filtered, hide_index=True, use_container_width=True)


# ============================================================
# REAL DATA (ported verbatim from gac_gm_dashboard_full.jsx,
# which was pulled from GAC_Monthly_Reporting_Pack_v04_March.xlsx/.pdf)
# ============================================================

weekly_active_raw = [
    ("2024-12-29", 315), ("2025-01-05", 423), ("2025-01-12", 636), ("2025-01-19", 644), ("2025-01-26", 644),
    ("2025-02-02", 644), ("2025-02-09", 648), ("2025-02-16", 649), ("2025-02-23", 650), ("2025-03-02", 640),
    ("2025-03-09", 640), ("2025-03-16", 643), ("2025-03-23", 648), ("2025-03-30", 648), ("2025-04-06", 643),
    ("2025-04-13", 644), ("2025-04-20", 646), ("2025-04-27", 648), ("2025-05-04", 623), ("2025-05-11", 502),
    ("2025-05-18", 387), ("2025-05-25", 190), ("2025-06-01", 19), ("2025-06-08", 493), ("2025-06-15", 509),
    ("2025-06-22", 514), ("2025-06-29", 513), ("2025-07-06", 510), ("2025-07-13", 519), ("2025-07-20", 521),
    ("2025-07-27", 524), ("2025-08-03", 464), ("2025-08-10", 465), ("2025-08-17", 255), ("2025-08-24", 257),
    ("2025-08-31", 298), ("2025-09-07", 488), ("2025-09-14", 627), ("2025-09-21", 634), ("2025-09-28", 636),
    ("2025-10-05", 629), ("2025-10-12", 634), ("2025-10-19", 641), ("2025-10-26", 644), ("2025-11-02", 639),
    ("2025-11-09", 639), ("2025-11-16", 599), ("2025-11-23", 599), ("2025-11-30", 579), ("2025-12-07", 579),
    ("2025-12-14", 575), ("2025-12-21", 278), ("2025-12-28", 277), ("2026-01-04", 283), ("2026-01-11", 588),
    ("2026-01-18", 603), ("2026-01-25", 612), ("2026-02-01", 609), ("2026-02-08", 614), ("2026-02-15", 620),
    ("2026-02-22", 621), ("2026-03-01", 622), ("2026-03-08", 626), ("2026-03-15", 629), ("2026-03-22", 628),
    ("2026-03-29", 632), ("2026-04-05", 621), ("2026-04-12", 623), ("2026-04-19", 623), ("2026-04-26", 627),
    ("2026-05-03", 601), ("2026-05-10", 464), ("2026-05-17", 409),
]
weekly_active = pd.DataFrame(weekly_active_raw, columns=["date", "active"])
weekly_active["date"] = pd.to_datetime(weekly_active["date"])

weekly_new_drops = pd.DataFrame(
    [
        ("Mar 29", 19, 3), ("Apr 5", 30, 15), ("Apr 12", 20, 1), ("Apr 19", 16, 6),
        ("Apr 26", 18, 6), ("May 3", 24, 38), ("May 10", 148, 131), ("May 17", 80, 62),
    ],
    columns=["week", "new", "drops"],
)
weekly_new_drops["net"] = weekly_new_drops["new"] - weekly_new_drops["drops"]

utilization_by_program = pd.DataFrame(
    [
        ("Recreation Gymnastics", 317, 424, 22, 75), ("Gymnastics", 67, 101, 0, 66),
        ("Ninja Zone", 46, 51, 1, 90), ("Level 6-10", 34, 42, 0, 81),
        ("Xcel G/P/D", 35, 40, 1, 88), ("Boys team", 23, 37, 0, 62),
        ("Camps Recreational", 22, 22, 8, 100), ("Xcel bronze", 35, 43, 0, 81),
        ("Level 3", 23, 24, 0, 96), ("Fast trak", 16, 24, 0, 67),
        ("Level 4", 6, 7, 0, 86), ("Level 5", 5, 6, 0, 83),
    ],
    columns=["Category", "Enrollment", "Capacity", "Waitlist", "Utilization"],
)

underfilled = pd.DataFrame(
    [
        ("Wed", "10:00 AM", "3 Year Old Gymnastics", "Recreation Gymnastics", 1, 6, 5),
        ("Thu", "4:45 PM", "3 Year Old Gymnastics", "Recreation Gymnastics", 3, 6, 3),
        ("Wed", "10:45 AM", "4 & 5 Yr Old Gymnastics", "Recreation Gymnastics", 0, 8, 8),
        ("Thu", "10:15 AM", "4 & 5 Yr Old Gymnastics", "Recreation Gymnastics", 0, 8, 8),
        ("Thu", "5:30 PM", "5 & 6 Yr Old Gymnastics", "Recreation Gymnastics", 3, 8, 5),
        ("Thu", "4:00 PM", "Acro & Tumbling Developmental Team", "Gymnastics", 5, 8, 3),
        ("Tue", "6:00 PM", "Boys Fast Trak (invite only)", "Recreation Gymnastics", 5, 8, 3),
        ("Mon", "6:30 PM", "Girls Beginning 6-9 Yr Olds", "Recreation Gymnastics", 2, 8, 6),
        ("Wed", "11:45 AM", "Girls Beginning 6-9 Yr Olds", "Recreation Gymnastics", 3, 8, 5),
        ("Thu", "6:30 PM", "Girls Beginning 6-9 Yr Olds", "Recreation Gymnastics", 4, 8, 4),
        ("Mon", "3:30 PM", "Girls Beginning 6-9 Yr Olds", "Recreation Gymnastics", 4, 8, 4),
        ("Wed", "5:15 PM", "Girls Intermediate Gymnastics", "Recreation Gymnastics", 5, 8, 3),
        ("Thu", "5:30 PM", "Girls Intermediate Gymnastics", "Recreation Gymnastics", 3, 8, 5),
        ("Thu", "5:00 PM", "Mini Fast Trak (invite only)", "Recreation Gymnastics", 3, 8, 5),
        ("Mon", "4:30 PM", "SKY NINJA 5-7 yrs old", "Ninja Zone", 5, 8, 3),
        ("Wed", "5:45 PM", "Trampoline & Tumbling Rec 7-12", "Gymnastics", 3, 8, 5),
        ("Tue", "3:30 PM", "Tumbling Ages 6-12", "Recreation Gymnastics", 4, 8, 4),
        ("Tue", "7:00 PM", "Tumbling - Advanced", "Recreation Gymnastics", 6, 10, 4),
        ("Mon", "5:15 PM", "XCEL Prep Girls 8+ (invite only)", "Recreation Gymnastics", 4, 8, 4),
    ],
    columns=["Day", "Time", "Class", "Program", "Filled", "Max", "Open"],
)

financials = pd.DataFrame(
    [
        ("Sep-25", 41446, 55654, 126259, 40974, 85286, 43373, 41913),
        ("Oct-25", 43532, 55400, 130336, 47341, 82995, 45348, 37646),
        ("Nov-25", 44767, 52875, 127769, 44966, 82803, 44572, 38231),
        ("Dec-25", 47153, 52509, 129060, 47806, 81254, 58581, 22673),
        ("Jan-26", 47156, 53132, 129684, 69586, 60098, 44903, 15194),
        ("Feb-26", 48699, 54873, 135327, 64559, 70769, 45647, 25121),
        ("Mar-26", 49453, 50589, 142839, 90333, 52507, 49946, 2560),
    ],
    columns=["month", "recTuition", "teamTuition", "revenue", "cos", "grossProfit", "ga", "ebitda"],
)

enrollment_progress = pd.DataFrame(
    [
        ("Rec Enrollment", "338", "331", "7", "2%", "351"),
        ("Team Enrollment", "265", "275", "-10", "-4%", "275"),
        ("Total Enrollment", "603", "606", "-3", "0%", "626"),
        ("Camp YTD", "303", "284", "19", "7%", "700"),
        ("Special Events YTD", "46", "0", "46", "—", "—"),
        ("Total Camp and Events", "349", "284", "65", "23%", "700"),
    ],
    columns=["", "Mar-26", "Mar-25", "+/-", "% Change", "Target"],
)

enrollment_by_program = pd.DataFrame(
    [
        ("Recreation Gymnastics", 317, 317, 329, "—", "(12)"),
        ("Boys Team", 23, 20, 20, "3", "3"),
        ("Ninja Zone", 46, 45, 35, "1", "11"),
        ("Level 6-10", 32, 34, 27, "(2)", "5"),
        ("XCEL G/P/D", 34, 33, 27, "1", "7"),
        ("Gymnastics", 68, 68, 74, "—", "(6)"),
        ("XCEL Bronze", 35, 36, 50, "(1)", "(15)"),
        ("Level 3", 21, 20, 15, "1", "6"),
        ("Fast Trak", 16, 17, 16, "(1)", "—"),
        ("Level 4", 6, 6, 7, "—", "(1)"),
        ("Level 5", 5, 5, 6, "—", "(1)"),
        ("Total", 603, 601, 606, "2", "(3)"),
    ],
    columns=["Program", "Mar-26", "Feb-26", "Mar-25", "MoM", "YoY"],
)

financial_progress = pd.DataFrame(
    [
        ("Revenue ($k)", "$125", "$106", "$19", "18%", "$114"),
        ("Revenue Growth", "18%", "—", "—", "—", "7%"),
        ("Year To Date", "$352", "$322", "$30", "9%", "$344"),
        ("YTD Growth", "9%", "—", "—", "—", "7%"),
        ("Rev (-) Payroll (Wages Only)", "$81", "$64", "$17", "27%", "$69"),
        ("Payroll % of Revenue", "35%", "40%", "—", "—", "—"),
        ("$ Growth", "$17", "—", "—", "—", "$5"),
        ("% Growth", "27%", "—", "—", "—", "8%"),
        ("YTD Rev (-) Payroll", "$78", "$58", "$20", "35%", "$63"),
        ("YTD $ Growth", "$20", "—", "—", "—", "$5"),
        ("YTD % Growth", "35%", "—", "—", "—", "8%"),
        ("Memo: Payroll (Wages Only)", "$44", "$43", "—", "—", "—"),
    ],
    columns=["", "Mar-26", "Mar-25", "+/-", "% Change", "Target"],
)

drops_by_program = pd.DataFrame(
    [
        ("Boys Team", "—", "—", "—"), ("Fast Trak", "—", "—", "—"),
        ("Gymnastics", "—", "—", "—"), ("Level 3", "—", "—", "—"),
        ("Level 4", "—", "—", "—"), ("Level 5", "—", "—", "—"),
        ("Level 6-10", "1", "—", "1"), ("Ninja Zone", "1", "1", "—"),
        ("Recreation Gymnastics", "11", "5", "6"), ("Clinics", "—", "—", "—"),
        ("Team Camp", "—", "—", "—"), ("XCEL Bronze", "1", "—", "1"),
        ("XCEL G/P/D", "—", "1", "(1)"), ("Total", "14", "7", "7"),
    ],
    columns=["Program", "Mar-26", "Feb-26", "MoM"],
)

drop_list_detail = pd.DataFrame(
    [
        (1, "Willow Stufflebean", "3/31", 137, "Other - See Notes", "", "Recreation Gymnastics"),
        (2, "Zoe Sellazzo", "3/31", 137, "Class Too Difficult", "struggling to listen with sister", "Recreation Gymnastics"),
        (3, "Stella Sellazzo", "3/31", 137, "Class Too Difficult", "struggling to focus with sister", "Recreation Gymnastics"),
        (4, "Reese Brittingham", "3/30", 327, "Other - See Notes", "Graduating senior", "Level 6-10"),
        (5, "Aria Stack", "3/30", 7, "Other - See Notes", "Will not update card on file", "Camps Recreational"),
        (6, "Saylor Stack", "3/30", 7, "Other - See Notes", "Will not update card on file", "Camps Recreational"),
        (7, "Calvin Childress", "3/30", 84, "Scheduling Conflict", "", "Ninja Zone"),
        (8, "Emerson Moody", "3/30", 229, "Other - See Notes", "Won a trip", "Xcel bronze"),
        (9, "Liliana-Marie Fabian", "3/11", 117, "Other - See Notes", "BAD DEBT - did not pay March", "Recreation Gymnastics"),
        (10, "Olivia Besco", "3/5", 57, "Other - See Notes", "", "Recreation Gymnastics"),
        (11, "Rachel Rosstedt", "3/2", 231, "Other - See Notes", "Registration expired, hasn't shown up so dropped", "Recreation Gymnastics"),
        (12, "Lauren Smolkowicz", "3/2", 231, "Other - See Notes", "Registration expired, hasn't come to class", "Recreation Gymnastics"),
        (13, "Cameron St Mar—", "3/2", 224, "Other - See Notes", "Registration expired, hasn't come to class", "Recreation Gymnastics"),
        (14, "Tara Sweeney", "3/2", 85, "Other - See Notes", "Registration expired, hasn't come to class", "Recreation Gymnastics"),
        (15, "Alivia Scott", "3/2", 101, "No Show", "", "Recreation Gymnastics"),
        (16, "Olivia Crosby", "3/1", 106, "Family Moved", "", "Recreation Gymnastics"),
    ],
    columns=["#", "Name", "Drop date", "Days in class", "Reason", "Notes", "Program"],
)

drop_reasons = pd.DataFrame(
    [
        ("Registration expired", 4), ("Billing / card issue", 3), ("Class too difficult", 2),
        ("Unspecified", 2), ("Graduating senior", 1), ("Won a trip", 1),
        ("Scheduling conflict", 1), ("No show", 1), ("Family moved", 1),
    ],
    columns=["reason", "count"],
)

funnel_detail = pd.DataFrame(
    [
        ("Leads", "47", "Illustrative"), ("Trials booked", "21", "Illustrative"),
        ("Trial → enroll conversion", "62%", "Illustrative"), ("Enrolled", "13", "Illustrative"),
        ("Waitlist", "32", "Real — utilization export"),
    ],
    columns=["Stage", "Value", "Source"],
)

fake_funnel = pd.DataFrame(
    [("Leads", 47), ("Trials booked", 21), ("Enrolled", 13)],
    columns=["stage", "value"],
)

fake_attendance = pd.DataFrame(
    [("Wk 1", 91), ("Wk 2", 89), ("Wk 3", 87), ("Wk 4", 84), ("Wk 5", 85), ("Wk 6", 82)],
    columns=["week", "rate"],
)
# Ordered categorical so the line chart plots Wk 1..Wk 6 in sequence, not alphabetically.
fake_attendance["week"] = pd.Categorical(fake_attendance["week"], categories=fake_attendance["week"], ordered=True)

# ---- Derived KPIs (same math as the JSX) ----
total_enrolled = int(utilization_by_program["Enrollment"].sum())
total_capacity = int(utilization_by_program["Capacity"].sum())
avg_util = round(total_enrolled / total_capacity * 100)
total_waitlist = int(utilization_by_program["Waitlist"].sum())
latest_active = int(weekly_active.iloc[-1]["active"])
prev_active = int(weekly_active.iloc[-2]["active"])
latest_week = weekly_new_drops.iloc[-1]
latest_fin = financials.iloc[-1]
recurring_tuition = int(latest_fin["recTuition"] + latest_fin["teamTuition"])

# ============================================================
# HEADER
# ============================================================
st.markdown(
    f"""
    <div class="gac-header">
        <div>
            <h1>\U0001F30A GM weekly report</h1>
            <p>Gymnastics Academy of Charleston &middot; Week of Mar 23&ndash;29, 2026</p>
        </div>
        <p style="color:#C7CCF0;font-size:12px;margin:0">Use Cmd/Ctrl+P to print this report</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_enrollment, tab_retention, tab_funnel, tab_utilization, tab_billing, tab_attendance = st.tabs(
    ["\U0001F465 Enrollment", "\U0001F4C8 Retention / churn", "\U0001F4CB Lead funnel",
     "\U0001F4C5 Capacity / utilization", "\U0001F4B0 Billing / cash", "⚠️ Attendance"]
)

# ============================================================
# ENROLLMENT TAB
# ============================================================
with tab_enrollment:
    section_title("\U0001F465", "Enrollment", "Source: weekly active-enrollment tracker + enrollment/drop export", "live")
    kpi_row([
        {"label": "ACTIVE STUDENTS", "value": latest_active, "delta": int(latest_active - prev_active), "sub": "Rec + Team, end of week"},
        {"label": "NEW ENROLLMENTS", "value": int(latest_week["new"]), "sub": "Unique students, latest week"},
        {"label": "DROPS", "value": int(latest_week["drops"]), "sub": "Unique students, latest week"},
        {"label": "NET CHANGE", "value": int(latest_week["net"]), "delta": int(latest_week["net"]), "sub": "New minus drops, latest week"},
    ])

    with st.container(border=True):
        st.markdown("**Active students, trailing weeks**")
        st.caption("Native line chart — the original's draggable zoom brush isn't available in Streamlit's built-in charts.")
        st.line_chart(weekly_active.set_index("date")["active"], color=ACCENT)

    with st.container(border=True):
        st.markdown("**New enrollments vs. drops, last 8 weeks**")
        st.caption("Hover any bar for the exact count. The May spike/dip is the summer camp session turnover.")
        st.bar_chart(weekly_new_drops.set_index("week")[["new", "drops"]], color=[GREEN, RED], stack=False, sort=False)

    callout(
        f"The tracker's week-over-week net (+4) and the raw adds-minus-drops net "
        f"({'+' if latest_week['net'] >= 0 else ''}{int(latest_week['net'])}) don't fully reconcile for the week of "
        f"Mar 23&ndash;29 &mdash; a real example of the data-cleanup layer the meeting prep doc flagged. The production "
        f"build needs one agreed definition of “new enrollment” so GMs see one number, not two.",
        "warn",
    )

    with st.expander("Table: Enrollment Progress — Mar-26 vs Mar-25, verbatim from the monthly pack"):
        plain_table(enrollment_progress)
    with st.expander("Table: Enrollment by Program — current vs. prior month vs. prior year, all 11 programs"):
        plain_table(enrollment_by_program)

# ============================================================
# RETENTION TAB
# ============================================================
with tab_retention:
    section_title("\U0001F4C8", "Retention / churn", "Computed from real drop counts, using a placeholder definition", "proxy")
    kpi_row([
        {"label": "MONTHLY CHURN (PROXY)", "value": "2.3%", "sub": "14 drops ÷ 603 active, Mar-26"},
        {"label": "WEEKLY CHURN (PROXY)", "value": "0.5%", "sub": "3 drops ÷ 628 active"},
        {"label": "MARCH DROPS", "value": "16", "sub": "Previously-active students"},
    ])

    with st.container(border=True):
        st.markdown("**Why students dropped in March (real, n=16)**")
        st.caption('Grouped from the drop-list notes field rather than the generic "Other" category JackRabbit assigns by default.')
        st.bar_chart(drop_reasons.set_index("reason")["count"], color=ACCENT, horizontal=True, sort=False)

    callout(
        "Registration expired is the single largest drop reason (4 of 16) &mdash; that's a renewal-process fix "
        "(reminders, auto-renew), not a program quality issue. Billing/card problems account for 3 more. Together, "
        'process-driven drops (7 of 16) outnumber dissatisfaction-driven ones (2, "class too difficult").',
        "good",
    )
    callout(
        "The 2.3% figure is a placeholder calculation (drops ÷ active), not Cole's real metric. His team still "
        "needs to decide the actual definition: 30/60/90-day churn, annual, or a rolling cohort view.",
        "warn",
    )

    with st.expander("Table: Drops by Program — Mar-26 vs Feb-26, verbatim from the monthly pack"):
        plain_table(drops_by_program)
    with st.expander("Table: March drop list detail — all 16 drops, with notes, verbatim from the pack", expanded=True):
        data_table(drop_list_detail, filter_col="Program")

# ============================================================
# FUNNEL TAB
# ============================================================
with tab_funnel:
    section_title("\U0001F4CB", "Lead-to-enroll funnel", "No leads/trials data exists in the JackRabbit export today", "mock")
    col1, col2 = st.columns([1.2, 1])
    with col1:
        with st.container(border=True):
            st.markdown("**Funnel (illustrative)**")
            st.bar_chart(fake_funnel.set_index("stage")["value"], color=ACCENT, horizontal=True, sort=False)
    with col2:
        kpi_row([
            {"label": "TRIAL → ENROLL CONVERSION", "value": "62%", "sub": "Illustrative"},
            {"label": "WAITLIST", "value": total_waitlist, "sub": "Real — total GAC waitlist across programs"},
        ])

    callout(
        f"Every number here except the waitlist count ({total_waitlist}, from the real utilization export) is "
        "illustrative. This page can't go live until we confirm whether leads and trials live inside JackRabbit at "
        "all, or in a separate CRM, per the open question in the meeting prep doc.",
        "warn",
    )

    with st.expander("Table: Funnel detail — mostly illustrative, see note on each row"):
        plain_table(funnel_detail)

# ============================================================
# UTILIZATION TAB
# ============================================================
with tab_utilization:
    section_title("\U0001F4C5", "Capacity / utilization", "Source: utilization and priority-classes export, as of Apr 27, 2026", "live")
    kpi_row([
        {"label": "OVERALL UTILIZATION", "value": f"{avg_util}%", "sub": f"{total_enrolled} enrolled / {total_capacity} capacity"},
        {"label": "TOTAL WAITLIST", "value": total_waitlist, "sub": "Mostly Recreation Gymnastics (22)"},
        {"label": "UNDERFILLED CLASSES", "value": len(underfilled), "sub": "3+ open spots each"},
    ])

    with st.container(border=True):
        st.markdown("**Fill rate by program**")
        st.caption(f"Dashed reference line in the original marks the {avg_util}% overall average — not available in Streamlit's native bar chart.")
        st.bar_chart(utilization_by_program.set_index("Category")["Utilization"], color=ACCENT, horizontal=True, sort=False)

    callout(
        "Recreation Gymnastics looks only 75% utilized in aggregate, but has 22 families on the waitlist. The "
        "openings sit in less-popular weekday morning slots (4 &amp; 5 Yr Old classes with 8 open spots each) while "
        "popular after-school and Saturday slots are full. A GM glancing at the 75% number alone would miss that "
        "they need more Saturday/afternoon sections, not more enrollment effort overall.",
        "good",
    )

    with st.expander("Table: Underfilled classes — all 19 classes with 3+ open spots", expanded=True):
        data_table(underfilled, filter_col="Program" if "Program" in underfilled.columns else None, default_sort_col="Open", default_sort_desc=True)
    with st.expander("Table: Utilization by program — all 12 programs, verbatim from the monthly pack"):
        total_row = pd.DataFrame([{
            "Category": "Total", "Enrollment": total_enrolled, "Capacity": total_capacity,
            "Waitlist": total_waitlist, "Utilization": avg_util,
        }])
        plain_table(pd.concat([utilization_by_program, total_row], ignore_index=True))

# ============================================================
# BILLING TAB
# ============================================================
with tab_billing:
    section_title("\U0001F4B0", "Billing / cash", "Tuition & revenue trend are real; failed payments are illustrative", "partial")
    kpi_row([
        {"label": "RECURRING TUITION BASE", "value": f"${recurring_tuition:,}", "sub": "Mar-26 actual, Rec + Team / mo"},
        {"label": "AR / PAST DUE", "value": "$569", "sub": "8 of 605 active families"},
        {"label": "FAILED PAYMENTS", "value": "3", "sub": "Illustrative — not in this export"},
    ])

    with st.container(border=True):
        st.markdown("**Revenue and EBITDA, last 7 months (real, post-close)**")
        st.caption("Note the EBITDA compression in Jan–Mar as meet expenses ramped.")
        st.bar_chart(financials.set_index("month")[["revenue", "ebitda"]], color=[ACCENT, GREEN], stack=False, sort=False)

    callout(
        "Recurring tuition base and the $569 past-due figure are computed straight from GAC's actual family-balance "
        "and financial data. Failed payments aren't captured anywhere in this export, so that number is a "
        "placeholder pending access to JackRabbit's billing module.",
        "warn",
    )

    with st.expander("Table: Financial Progress — Mar-26 vs Mar-25, verbatim from the monthly pack", expanded=True):
        plain_table(financial_progress)
    with st.expander("Table: Monthly financial detail — Rec/Team tuition, revenue, gross profit, EBITDA, 7 months"):
        display_fin = financials.rename(columns={
            "month": "Month", "recTuition": "Rec tuition", "teamTuition": "Team tuition",
            "revenue": "Total revenue", "grossProfit": "Gross profit", "ebitda": "EBITDA",
        })[["Month", "Rec tuition", "Team tuition", "Total revenue", "Gross profit", "EBITDA"]]
        for col in ["Rec tuition", "Team tuition", "Total revenue", "Gross profit", "EBITDA"]:
            display_fin[col] = display_fin[col].apply(lambda v: f"${v:,.0f}")
        data_table(display_fin)

# ============================================================
# ATTENDANCE TAB
# ============================================================
with tab_attendance:
    section_title("⚠️", "Attendance trends", "Per-session attendance isn't captured in the export today", "mock")

    with st.container(border=True):
        st.markdown("**Illustrative weekly attendance rate**")
        st.caption("Dashed in the original on purpose to signal it's not real data.")
        st.line_chart(fake_attendance.set_index("week")["rate"], color=RED)

    callout(
        "Entirely illustrative. This page can only go live once we confirm whether GAC (and other locations) log "
        "attendance per session in JackRabbit, per the open question in the meeting prep doc.",
        "warn",
    )

    with st.expander("Table: Weekly attendance rate — illustrative, not real data"):
        display_att = fake_attendance.copy()
        display_att["rate"] = display_att["rate"].apply(lambda v: f"{v}%")
        display_att.columns = ["Week", "Attendance rate"]
        plain_table(display_att)
