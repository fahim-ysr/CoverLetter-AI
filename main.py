import streamlit as st
from pipeline import Pipeline
from portfolio import Portfolio
from text_cleaner import text_cleaner
from langchain_community.document_loaders import WebBaseLoader




def create_app(llm, portfolio, text_cleaner):
    st.set_page_config(
        layout= "wide", 
        page_title= "CoverLetter AI",
        page_icon= "🌐",
        initial_sidebar_state = "expanded"
        )

    # st.markdown(
    #     """
    #     <style>
        
    #     .stApp {
    #         background: linear-gradient(45deg, #000000, #434343);
    #         background-size: 200% 200%;
    #         animation: gradientBG 5s ease infinite;
    #         }
            
    #     @keyframes gradientBG {
    #         0% {background-position: 0% 50%;}
    #         50% {background-position: 100% 50%;}
    #         100% {background-position: 0% 50%;}
    #         }

    #     </style>
    #     """,
    #     unsafe_allow_html=True
    #     )
    
    st.image("./logo.png", width=150)
    
    st.markdown("<h1 style='margin-bottom:0;'>CoverLetter AI</h1>", unsafe_allow_html=True)
    st.caption("🚀 Generate tailored cover letters from any job posting URL.")
    
    st.markdown("---")

    # Sidebar for info

    st.header("❔ How to Use")
    st.write(
        "1. Paste a job posting URL.\n"
        "2. Click **Submit**.\n"
        "3. Review and copy your generated cover letter."
    )

    # Main input section

    with st.container():
        st.subheader("Paste the Job Description URL")
        input_url = st.text_input(
            "Job Posting URL",
            placeholder="https://example.com/job-posting"
        )
        submit = st.button("Submit", type= "primary")

    if submit:
        with st.spinner("Scraping and generating your cover letter..."):
            try:
                # Using the WebBaseLoader to scrape content of a webpage. Using a demo job description link for testing purposes
                loader = WebBaseLoader([input_url])

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
                    st.success("🎉 Your cover letter is ready!")
                    st.markdown("#### Generated Cover Letter")
                    st.code(email, language= "markdown", wrap_lines=True)

            except Exception as e:
                st.error(f"An error has occured!: {e}")


if __name__ == "__main__":
    chain = Pipeline()
    portfolio = Portfolio(path= "./demo_portfolio.csv")
    create_app(chain, portfolio, text_cleaner)