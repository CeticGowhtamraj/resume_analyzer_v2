import streamlit as st
import nltk
import re
import pandas as pd
import base64
import random
import time
import datetime
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from contextlib import contextmanager
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy
import plotly.express as px

nltk.download('stopwords', quiet=True)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'port': 3308,
    'database': 'resume_analyzer',
    'charset': 'utf8mb4'
}

@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
    except pymysql.err.OperationalError as e:
        st.error(f"Database connection error: {str(e)}")
        yield None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        yield None
    finally:
        if connection:
            connection.close()

def fetch_yt_video(link):
    try:
        video = pafy.new(link)
        return video.title
    except:
        return "Video Tutorial"

def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

def pdf_reader(file_path):
    try:
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def show_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except:
        pass

def course_recommender(course_list):
    st.subheader("Courses & Certificates Recommendations")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

def extract_email(text):
    patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        r'\b[A-Za-z0-9]+[\._]?[A-Za-z0-9]+[@]\w+[.]\w{2,3}\b'
    ]
    for pattern in patterns:
        emails = re.findall(pattern, text, re.IGNORECASE)
        if emails:
            return emails[0].lower()
    return None

def extract_phone(text):
    patterns = [
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        r'\b\d{10}\b',
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\+\d{1,3}\s?\d{9,}',
    ]
    for pattern in patterns:
        phones = re.findall(pattern, text)
        if phones:
            phone = re.sub(r'[^\d+]', '', phones[0])
            if len(phone) >= 10:
                return phone
    return None

def extract_name(text, email):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for line in lines[:5]:
        if any(word in line.lower() for word in ['resume', 'cv', 'curriculum', 'vitae']):
            continue
        if email and email in line.lower():
            continue
        if re.search(r'\d{3,}', line):
            continue
        words = line.split()
        if 2 <= len(words) <= 4:
            if re.match(r'^[A-Za-z\s\.]+$', line):
                return line.title()
    
    return lines[0] if lines else 'Unknown'

def extract_skills_advanced(text):
    text_lower = text.lower()
    
    skill_database = {
        'Programming Languages': [
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 
            'rust', 'swift', 'kotlin', 'typescript', 'r', 'matlab', 'scala'
        ],
        'Web Development': [
            'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express',
            'django', 'flask', 'fastapi', 'spring', 'laravel',
            'jquery', 'bootstrap', 'tailwind', 'sass', 'webpack', 'redux'
        ],
        'Mobile Development': [
            'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic'
        ],
        'Data Science & AI': [
            'machine learning', 'deep learning', 'artificial intelligence',
            'data science', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
            'pandas', 'numpy', 'matplotlib', 'nlp', 'computer vision', 'opencv'
        ],
        'Databases': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 
            'firebase', 'elasticsearch'
        ],
        'Cloud & DevOps': [
            'aws', 'azure', 'google cloud', 'docker', 'kubernetes',
            'jenkins', 'terraform', 'git', 'github', 'linux'
        ],
        'UI/UX Design': [
            'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
            'ui design', 'ux design', 'wireframing', 'prototyping'
        ]
    }
    
    found_skills = {}
    all_skills = []
    
    for category, skills in skill_database.items():
        category_skills = []
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                category_skills.append(skill.title())
                all_skills.append(skill.title())
        if category_skills:
            found_skills[category] = category_skills
    
    return found_skills, list(set(all_skills))

def determine_job_field(skills_by_category):
    field_weights = {
        'Data Science': {
            'Data Science & AI': 3,
            'Programming Languages': 1
        },
        'Web Development': {
            'Web Development': 3,
            'Programming Languages': 1
        },
        'Mobile Development': {
            'Mobile Development': 3
        },
        'UI/UX Design': {
            'UI/UX Design': 3
        },
        'DevOps': {
            'Cloud & DevOps': 3
        },
        'Full Stack Development': {
            'Web Development': 2,
            'Databases': 2
        }
    }
    
    field_scores = {}
    for field, weights in field_weights.items():
        score = 0
        for category, weight in weights.items():
            if category in skills_by_category:
                score += len(skills_by_category[category]) * weight
        field_scores[field] = score
    
    if not field_scores or max(field_scores.values()) == 0:
        return None
    
    return max(field_scores, key=field_scores.get)

def get_smart_recommendations(detected_field, current_skills):
    recommendations = {
        'Data Science': {
            'skills': ['Deep Learning', 'Neural Networks', 'Statistical Modeling',
                      'Data Visualization', 'Big Data', 'Feature Engineering'],
            'courses': ds_course
        },
        'Web Development': {
            'skills': ['TypeScript', 'GraphQL', 'Microservices', 
                      'Docker', 'API Design', 'Testing'],
            'courses': web_course
        },
        'Mobile Development': {
            'skills': ['Cross-platform Development', 'App Store Optimization',
                      'Mobile Security', 'Push Notifications'],
            'courses': android_course
        },
        'UI/UX Design': {
            'skills': ['User Research', 'Information Architecture',
                      'Accessibility', 'Design Systems'],
            'courses': uiux_course
        },
        'DevOps': {
            'skills': ['Infrastructure as Code', 'Monitoring',
                      'Security Automation', 'Cloud Architecture'],
            'courses': web_course
        },
        'Full Stack Development': {
            'skills': ['System Design', 'Database Optimization',
                      'Scalability', 'Testing'],
            'courses': web_course
        }
    }
    
    if detected_field in recommendations:
        rec = recommendations[detected_field]
        current_lower = [s.lower() for s in current_skills]
        new_skills = [s for s in rec['skills'] if s.lower() not in current_lower]
        return new_skills[:10], rec['courses']
    
    return [], web_course

def improved_resume_parser(file_path):
    try:
        text = pdf_reader(file_path)
        
        if not text or len(text) < 50:
            st.error("Could not extract text from PDF")
            return None
        
        email = extract_email(text)
        phone = extract_phone(text)
        name = extract_name(text, email)
        
        with open(file_path, 'rb') as f:
            pages = len(list(PDFPage.get_pages(f)))
        
        skills_by_category, all_skills = extract_skills_advanced(text)
        
        return {
            'name': name,
            'email': email or 'Not found',
            'mobile_number': phone or 'Not found',
            'no_of_pages': pages,
            'skills': all_skills,
            'skills_by_category': skills_by_category,
            'raw_text': text
        }
        
    except Exception as e:
        st.error(f"Error parsing resume: {str(e)}")
        return None

def calculate_ats_score(resume_data, resume_text):
    score = 0
    feedback = []
    text_lower = resume_text.lower()
    
    # Contact Information (20 points)
    if resume_data['email'] and resume_data['email'] != 'Not found':
        score += 8
        feedback.append(('check', 'Email address found'))
    else:
        feedback.append(('cross', 'Email address missing'))
    
    if resume_data['mobile_number'] and resume_data['mobile_number'] != 'Not found':
        score += 7
        feedback.append(('check', 'Phone number found'))
    else:
        feedback.append(('cross', 'Phone number missing'))
    
    if any(word in text_lower for word in ['linkedin', 'github', 'portfolio']):
        score += 5
        feedback.append(('check', 'Professional links found'))
    else:
        feedback.append(('warn', 'Add LinkedIn/GitHub links'))
    
    # Professional Summary (10 points)
    if any(word in text_lower for word in ['summary', 'objective', 'profile']):
        score += 10
        feedback.append(('check', 'Professional summary present'))
    else:
        feedback.append(('cross', 'Add professional summary'))
    
    # Skills (25 points)
    skill_count = len(resume_data['skills'])
    if skill_count >= 15:
        score += 25
        feedback.append(('check', f'{skill_count} skills detected'))
    elif skill_count >= 10:
        score += 20
        feedback.append(('check', f'{skill_count} skills found'))
    elif skill_count >= 5:
        score += 12
        feedback.append(('warn', f'Only {skill_count} skills'))
    else:
        score += 5
        feedback.append(('cross', f'Only {skill_count} skills'))
    
    # Work Experience (25 points)
    if any(word in text_lower for word in ['experience', 'work history']):
        year_matches = len(re.findall(r'\b(19|20)\d{2}\b', resume_text))
        if year_matches >= 4:
            score += 25
            feedback.append(('check', 'Detailed work experience'))
        elif year_matches >= 2:
            score += 18
            feedback.append(('check', 'Work experience found'))
        else:
            score += 10
            feedback.append(('warn', 'Add dates to experience'))
    else:
        feedback.append(('cross', 'Work experience missing'))
    
    # Education (10 points)
    if any(word in text_lower for word in ['education', 'degree', 'university']):
        score += 10
        feedback.append(('check', 'Education details present'))
    else:
        feedback.append(('cross', 'Add education details'))
    
    # Projects (10 points)
    if any(word in text_lower for word in ['project', 'built', 'developed']):
        score += 10
        feedback.append(('check', 'Projects mentioned'))
    else:
        feedback.append(('cross', 'Add relevant projects'))
    
    return min(score, 100), feedback

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, 
                cand_level, skills, recommended_skills, courses):
    with get_db_connection() as connection:
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            insert_sql = """
                INSERT INTO users 
                (name, email, resume_score, timestamp, page_no, predicted_field, 
                 user_level, actual_skills, recommended_skills, recommended_courses, pdf_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            rec_values = (name, email, str(res_score), timestamp, str(no_of_pages), 
                         reco_field, cand_level, skills, recommended_skills, courses, 'resume.pdf')
            cursor.execute(insert_sql, rec_values)
            connection.commit()
            return True
        except:
            return False

def verify_admin(username, password):
    with get_db_connection() as connection:
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM admin WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            return cursor.fetchone() is not None
        except:
            return False

def get_all_users():
    with get_db_connection() as connection:
        if connection is None:
            return None
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users ORDER BY timestamp DESC")
            data = cursor.fetchall()
            if not data:
                return None
            df = pd.DataFrame(data, columns=[
                'ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                'Predicted Field', 'User Level', 'Actual Skills', 
                'Recommended Skills', 'Recommended Course', 'PDF Name'
            ])
            return df
        except:
            return None

st.set_page_config(page_title="Smart Resume Analyzer", page_icon='📄')

def run():
    st.title("Smart Resume Analyzer")
    st.sidebar.markdown("# Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    
    try:
        img = Image.open('./Logo/SRA_Logo.jpg')
        img = img.resize((250, 250))
        st.image(img)
    except:
        pass

    if choice == 'Normal User':
        st.info("Upload your resume in PDF format for analysis")
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        
        if pdf_file is not None:
            try:
                save_image_path = './Uploaded_Resumes/' + pdf_file.name
                with open(save_image_path, "wb") as f:
                    f.write(pdf_file.getbuffer())
                
                show_pdf(save_image_path)
                
                with st.spinner('Analyzing your resume...'):
                    resume_data = improved_resume_parser(save_image_path)
                
                if resume_data:
                    st.success("Resume parsed successfully!")
                    
                    st.header("Your Profile")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Name", resume_data['name'])
                        st.metric("Email", resume_data['email'])
                    with col2:
                        st.metric("Phone", resume_data['mobile_number'])
                        st.metric("Resume Pages", resume_data['no_of_pages'])
                    
                    pages = resume_data['no_of_pages']
                    if pages == 1:
                        cand_level = "Fresher"
                    elif pages == 2:
                        cand_level = "Intermediate"
                    else:
                        cand_level = "Experienced"
                    
                    st.subheader(f"Experience Level: {cand_level}")
                    
                    st.header("Skills Analysis")
                    
                    if resume_data['skills_by_category']:
                        for category, skills in resume_data['skills_by_category'].items():
                            with st.expander(f"{category} ({len(skills)} skills)"):
                                st.write(", ".join(skills))
                    else:
                        st.warning("No technical skills detected")
                    
                    st_tags(label='All Detected Skills', 
                           text='Your skills', 
                           value=resume_data['skills'][:30], 
                           key='detected')
                    
                    detected_field = determine_job_field(resume_data['skills_by_category'])
                    
                    if detected_field:
                        st.success(f"Predicted Career Field: {detected_field}")
                        reco_field = detected_field
                        
                        recommended_skills, course_list = get_smart_recommendations(detected_field, resume_data['skills'])
                        
                        if recommended_skills:
                            st.subheader("Recommended Skills")
                            st_tags(label='Skills to add', 
                                   text='Boost your profile',
                                   value=recommended_skills, 
                                   key='recommended')
                        
                        rec_course = course_recommender(course_list)
                    else:
                        st.warning("Could not determine field")
                        reco_field = "General"
                        recommended_skills = []
                        rec_course = []
                    
                    st.header("ATS Score Analysis")
                    ats_score, feedback = calculate_ats_score(resume_data, resume_data['raw_text'])
                    
                    if ats_score >= 80:
                        score_color = "#1ed760"
                        score_msg = "Excellent!"
                    elif ats_score >= 60:
                        score_color = "#fba171"
                        score_msg = "Good"
                    else:
                        score_color = "#d73b5c"
                        score_msg = "Needs improvement"
                    
                    st.markdown(f"<h1 style='text-align: center; color: {score_color};'>{ats_score}/100</h1>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'>{score_msg}</p>", unsafe_allow_html=True)
                    
                    st.subheader("Detailed Feedback")
                    for icon_type, msg in feedback:
                        if icon_type == 'check':
                            st.success(f"✓ {msg}")
                        elif icon_type == 'cross':
                            st.error(f"✗ {msg}")
                        else:
                            st.warning(f"⚠ {msg}")
                    
                    ts = time.time()
                    cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    timestamp = str(cur_date + '_' + cur_time)
                    
                    insert_data(
                        resume_data['name'],
                        resume_data['email'],
                        str(ats_score),
                        timestamp,
                        str(resume_data['no_of_pages']),
                        reco_field,
                        cand_level,
                        str(resume_data['skills'][:50]),
                        str(recommended_skills[:20]),
                        str(rec_course[:10])
                    )
                    
                    st.header("Learning Resources")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Resume Tips")
                        try:
                            vid = random.choice(resume_videos)
                            st.video(vid)
                        except:
                            pass
                    
                    with col2:
                        st.subheader("Interview Prep")
                        try:
                            vid = random.choice(interview_videos)
                            st.video(vid)
                        except:
                            pass
                    
                    st.balloons()
                
                else:
                    st.error("Could not parse resume")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.success('Admin Portal')
        
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        
        if st.button('Login'):
            if verify_admin(ad_user, ad_password):
                st.success(f"Welcome {ad_user}!")
                
                df = get_all_users()
                
                if df is not None:
                    st.header("User Analytics")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Resumes", len(df))
                    with col2:
                        avg_score = df['Resume Score'].astype(float).mean()
                        st.metric("Avg Score", f"{avg_score:.1f}")
                    with col3:
                        top_field = df['Predicted Field'].mode()[0] if not df.empty else "N/A"
                        st.metric("Top Field", top_field)
                    
                    st.subheader("Resume Records")
                    st.dataframe(df, use_container_width=True)
                    st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download CSV'), unsafe_allow_html=True)
                    
                    if not df.empty:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("Career Fields")
                            field_counts = df['Predicted Field'].value_counts()
                            fig = px.pie(values=field_counts.values, names=field_counts.index)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            st.subheader("Experience Levels")
                            level_counts = df['User Level'].value_counts()
                            fig = px.pie(values=level_counts.values, names=level_counts.index)
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Invalid credentials")

if __name__ == '__main__':
    run()