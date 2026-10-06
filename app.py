import streamlit as st
import sqlite3
import pandas as pd


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="VoiceExam | Admin Dashboard",
    page_icon="🎙️",
    layout="wide"
)


DATABASE_NAME = "voiceexam.db"


# ==================================================
# DATABASE
# ==================================================

def get_results():

    connection = sqlite3.connect(DATABASE_NAME)

    query = """
        SELECT
            id,
            student_name,
            exam_date,
            score,
            total_questions,
            percentage,
            status
        FROM exam_results
        ORDER BY id DESC
    """

    data = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return data


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #777777;
        margin-bottom: 25px;
    }

    .dashboard-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f7f9fc;
        border: 1px solid #e5e7eb;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🎙️ VoiceExam</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Voice-Based Examination System'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Dashboard")

    st.write(
        "Admin / Teacher Panel"
    )

    st.divider()

    if st.button(
        "🔄 Refresh Results",
        use_container_width=True
    ):

        st.rerun()


# ==================================================
# LOAD DATA
# ==================================================

data = get_results()


# ==================================================
# DASHBOARD STATISTICS
# ==================================================

if not data.empty:

    total_students = len(data)

    average_score = data["percentage"].mean()

    completed_exams = len(
        data[data["status"] == "Completed"]
    )

    highest_score = data["percentage"].max()


else:

    total_students = 0
    average_score = 0
    completed_exams = 0
    highest_score = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👨‍🎓 Total Students",
        total_students
    )


with col2:

    st.metric(
        "📊 Average Score",
        f"{average_score:.2f}%"
    )


with col3:

    st.metric(
        "✅ Completed Exams",
        completed_exams
    )


with col4:

    st.metric(
        "🏆 Highest Score",
        f"{highest_score:.2f}%"
    )


st.divider()


# ==================================================
# RESULTS
# ==================================================

st.subheader("📋 Examination Results")


if not data.empty:

    display_data = data.copy()

    display_data.columns = [
        "ID",
        "Student Name",
        "Exam Date",
        "Score",
        "Total Questions",
        "Percentage",
        "Status"
    ]


    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    search = st.text_input(
        "🔍 Search Student",
        placeholder="Enter student name..."
    )


    if search:

        display_data = display_data[
            display_data["Student Name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    # --------------------------------------------------
    # DISPLAY TABLE
    # --------------------------------------------------

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------
    # DOWNLOAD RESULTS
    # --------------------------------------------------

    csv = display_data.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Results",
        data=csv,
        file_name="voiceexam_results.csv",
        mime="text/csv"
    )


    # ==================================================
    # PERFORMANCE SECTION
    # ==================================================

    st.divider()

    st.subheader("📈 Student Performance")


    chart_data = data[
        [
            "student_name",
            "percentage"
        ]
    ].copy()


    chart_data = chart_data.set_index(
        "student_name"
    )


    st.bar_chart(
        chart_data
    )


else:

    st.info(
        "No examination results are available yet."
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "VoiceExam — AI-Powered Accessible Examination System"
)