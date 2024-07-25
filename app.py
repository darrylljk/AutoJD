import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

api_key = st.secrets["OPENAI_API_KEY"] # for streamlit cloud

# [uncomment below if running local, store api key in .env file]
# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)
model = "gpt-3.5-turbo"

def generate_job_description(job_title, company, experience, education, degree, skills):
    """
    Generate a JD based on the following inputs:
    - job title
    - company
    - experience
    - education
    - degree
    - skills
    """

    prompt = f"""
    
    Create a detailed job description for the following position:

    Job Title: {job_title}

    Company: {company}
    
    Work Experience: {experience}
    
    Education: {education}

    Relevant Degree: {degree}

    Required Skills: {skills}

    The job description should include sections such as:
    1. About Company
    2. Job Summary
    3. Responsibilities
    4. Requirements

    Expand on the provided inputs to create a comprehensive and realistic job description. Use the input as a guide, but do not limit the description strictly to the input. Incorporate related and relevant skills and qualifications as necessary to make the job description thorough.
    Job Summary should have at least 3 paragraphs. 
    There should be at least 10 bullet points for Responsibilities and Requirements section each.
    You may expand on the provided inputs.

    Job Description:
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system", "content":"You are a skilled job description writer."},
            {"role":"user", "content":prompt}
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0
    )

    return response.choices[0].message.content.strip()

def main():
    st.set_page_config(page_title="AutoJD", page_icon="✍️")
    st.title('AutoJD')
    st.write('''
    Welcome to AutoJD ✍️

    We are delighted to introduce AutoJD, your go-to solution for creating comprehensive job descriptions effortlessly. Whether you're hiring for a new position or updating an existing role, AutoJD simplifies the process, ensuring you capture all the essential details in a well-structured format.

    **How It Works:**

    1. **Job Title:** Start by entering the job title.
    2. **Company:** Specify the company or department that is hiring.
    2. **Work Experience:** Specify the required work experience to ensure you attract qualified candidates.
    3. **Education:** Indicate the education level needed for the role.
    4. **Major:** Highlight specific majors that are pertinent to the role.
    5. **Required Skills:** List the key skills necessary for success in the role.

    With this information, AutoJD will generate a professional and detailed job description tailored to your needs. It's quick, easy, and designed to help you find the perfect fit for your team.

    Let's get started and create a job description that stands out! 🚀
    ''')

    with st.form(key='job_description_form'):
        job_title = st.text_input("Job Title", "Data Analyst")
        company = st.text_input('Company', 'Amazon')
        experience = st.selectbox('Work Experience', ['0-2 years', '3-5 years', '5-10 years', 'More than 10 years'])
        education = st.selectbox('Education', ['Diploma', 'Bachelor', 'Master', 'PhD'])
        degree = st.multiselect('Major', ['Any', 'Engineering', 'Business', 'Finance', 'Computing', 'Data Science', 'Accountancy', 'Arts and Social Science'])
        skills = st.text_area('Skills', 'Proficiency in Python, SQL, Big Data, Cloud Computing, and Data Visualization tools.', help='List the skills required for the position')
        submit_button = st.form_submit_button(label='Generate Job Description')
   
    if submit_button:
        with st.spinner('Generating job description...'):
            progress_bar = st.progress(0)

            for percent_complete in range(100):
                time.sleep(0.05)
                progress_bar.progress(percent_complete+1)
            
            job_description = generate_job_description(job_title, company, experience, education, degree, skills)

        st.subheader("Generated Job Description:")
        st.write(job_description)
        st.download_button(label="Download Job Description as TXT", data=job_description, file_name="job_description.txt", mime="text/plain")

if __name__ == "__main__":
    main()
