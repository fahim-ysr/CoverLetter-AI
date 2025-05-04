# Importing dependencies
from langchain_core.exceptions import OutputParserException
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser




# Extracting the key
import os                                                                          
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(Path(".env.local"))
KEY = os.getenv("GROQ_API_KEY")


# Creating a pipeline
class Pipeline:


    # This (Constructor) function defines the LLM that is going to be used for data extraction
    def __init__(self):
        self.llm = ChatGroq(
            model= 'llama-3.3-70b-versatile',
            temperature= 0,
            groq_api_key= KEY,
            max_tokens= None,
            timeout= None,
            max_retries= 2,
            # Other Parameters...
        )


    # This function extract job by its description
    def extract_jobs(self, text_cleaner):
        try:
            # Using prompt on the model

            extract_from_prompt = PromptTemplate.from_template(
                """
                I will give you scraped text from job postings. Your job is to extract the details and requirements in a JSON format containing the following keywords: 'role', 'experience', 'skills', 'description'
                Only return the JSON. No preamble please.
                Here is the scraped text: {page_data}
                """
            )

            chain_extract = extract_from_prompt | self.llm
            answer = chain_extract.invoke(input= {'page_data': text_cleaner})

            try:
                parser = JsonOutputParser()
                json_answer = parser.parse(answer.content)
            except OutputParserException:
                raise OutputParserException("Content exceeding limit. Unable to parse!")
            
            return json_answer if isinstance(json_answer, list) else [json_answer]
        
        # In case of empty LLM responses
        except Exception as e:
            print(f"Extraction failed: {e}")
            return []


    # This function generates email according to the job description
    def write_email(self, job_desc, urls):

        # Setting up prompt for writing the email

        email_prompt = PromptTemplate.from_template(
            """
            I will give you a role and a task that you have to perform in that specific role.
            Your role: Your name is Fahim. You are an incredible business development officer who who knows how to get clients. You work for ABC Consulting Firm, your firm works with all kinds of IT clients and provide solutions in the domain of Data Science and AI.
            CoverLetter AI focuses on efficient tailored solutions for all clients keeping costs down. 
            Your Job: Your Job is to write cold emails to clients regarding the Job openings that they have advertised. Try to pitch your clients with an email hook that opens a conversation about a possibility of working with them. Add the most relevant portfolio URLs from
            the following (shared below) to showcase that we have the right expertise to get the job done.
            I will provide you with email and phone number. Email: abc@def.com, Phone: +12345678. Only include them at the end after the initials.
            I will now provide you with the Job description and the portfolio URLs:
            JOB DESCRIPTION: {job_description}
            ------
            PORTFOLIO URLS: {portfolio_urls}
            """
        )

        # Extracting the answer
        chain_email = email_prompt | self.llm
        answer = chain_email.invoke({'job_description': str(job_desc), 'portfolio_urls': urls})

        return answer.content