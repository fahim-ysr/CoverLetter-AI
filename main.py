import streamlit as st
from pipeline import Pipeline
from portfolio import Portfolio
from text_cleaner import text_cleaner
from langchain_community.document_loaders import WebBaseLoader

def create_app(llm, portfolio, text_cleaner):
    st.set_page_config(layout= "wide", page_title= "CoverLetter AI")
    st.title("CoverLetterAI")
    input_url = st.text_input("Enter URL: ")
    submit = st.button("Submit")

    if submit:
        try:
            # Using the WebBaseLoader to scrape content of a webpage. Using a demo job description link for testing purposes
            loader = WebBaseLoader("https://jobs.foundever.com/job/Canada-IT-Site-System-Supt-Admin-Onsite-in-London%2C-ON-Cana/1286688600/?")

            # Stores the loaded data of the webpage after cleaning it
            # data = text_cleaner(loader.load().pop().page_content)
            data = loader.load().pop().page_content
            
            # Loads data and inserts data into a Vector Database
            portfolio.load_portfolio()

            # Extracts the job details and stores it in the variable
            jobs = llm.extract_jobs(data)

            # Validation check in case if jobs were not found
            if not jobs:
                st.error("No jobs extracted from the URL")
                st.stop()

            for job in jobs:
                skills = job.get("skills", [])
                portfolio_urls = portfolio.query_links(skills)
                email = llm.write_email(job, portfolio_urls)
                st.code(email, language= "markdown")

        except Exception as e:
            st.error(f"An error has occured!: {e}")


if __name__ == "__main__":
    chain = Pipeline()
    portfolio = Portfolio(path= "./demo_portfolio.csv")
    create_app(chain, portfolio, text_cleaner)