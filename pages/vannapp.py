import streamlit as st

from vanna.remote import VannaDefault

@st.cache_resource(ttl=3600)
def setup_vanna():
    vn = VannaDefault(model='super_sales', api_key='fcaea5a7cc08496eb79f31804da82b8e')
    vn.connect_to_sqlite('D:\Sales\sale\orders.db')  # Print the passed value
    return vn

@st.cache_data(show_spinner="Generating sample questions ...")
def generate_questions_cached():
    vn = setup_vanna()
    return vn.generate_questions()

@st.cache_data(show_spinner="Generating SQL query ...")
def generate_sql_cached(question: str):
    vn = setup_vanna()
    return vn.generate_sql(question=question, allow_llm_to_see_data=True)

@st.cache_data(show_spinner="Checking for valid SQL ...")
def is_sql_valid_cached(sql: str):
    vn = setup_vanna()
    return vn.is_sql_valid(sql=sql)

@st.cache_data(show_spinner="Running SQL query ...")
def run_sql_cached(sql: str):
    vn = setup_vanna()
    return vn.run_sql(sql=sql)

@st.cache_data(show_spinner="Checking if we should generate a chart ...")
def should_generate_chart_cached(question, sql, df):
    vn = setup_vanna()
    return vn.should_generate_chart(df=df)

@st.cache_data(show_spinner="Generating Plotly code ...")
def generate_plotly_code_cached(question, sql, df):
    vn = setup_vanna()
    code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    return code

@st.cache_data(show_spinner="Running Plotly code ...")
def generate_plot_cached(code, df):
    vn = setup_vanna()
    return vn.get_plotly_figure(plotly_code=code, df=df)

@st.cache_data(show_spinner="Generating follow-up questions ...")
def generate_followup_cached(question, sql, df):
    vn = setup_vanna()
    return vn.generate_followup_questions(question=question, sql=sql, df=df)

@st.cache_data(show_spinner="Generating summary ...")
def generate_summary_cached(question, df):
    vn = setup_vanna()
    return vn.generate_summary(question=question, df=df)

# Streamlit app layout and logic
st.title("Supermarket Sales Analysis")

# Use a specific question for the top 5 orders with highest price
question = "What are the top 5 orders with the highest price?"

sql_query = generate_sql_cached(question)
if is_sql_valid_cached(sql_query):
    result_df = run_sql_cached(sql_query)
    st.write(result_df)
    if should_generate_chart_cached(question, sql_query, result_df):
        plotly_code = generate_plotly_code_cached(question, sql_query, result_df)
        plotly_fig = generate_plot_cached(plotly_code, result_df)
        st.plotly_chart(plotly_fig)
    summary = generate_summary_cached(question, result_df)
    st.write(summary)
    followup_questions = generate_followup_cached(question, sql_query, result_df)
    st.write(followup_questions)
else:
    st.error("Generated SQL query is invalid. Please try rephrasing your question.")