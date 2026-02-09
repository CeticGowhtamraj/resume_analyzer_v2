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

def extract_linkedin_url(text):
    """Extract LinkedIn profile URL from resume"""
    patterns = [
        r'linkedin\.com/in/[\w-]+',
        r'www\.linkedin\.com/in/[\w-]+',
        r'https?://(?:www\.)?linkedin\.com/in/[\w-]+',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            url = match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            return url
    return None

def scrape_linkedin_profile(profile_url):
    """
    Scrape LinkedIn profile data
    Note: This is a simplified version. For production, use LinkedIn API or proper scraping tools
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Note: LinkedIn blocks scraping, this is a placeholder structure
        # In production, use LinkedIn API with proper authentication
        
        # Return sample structure - in real implementation, parse actual data
        return {
            'success': False,
            'message': 'LinkedIn scraping requires API access',
            'data': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': str(e),
            'data': None
        }

def analyze_linkedin_optimization_with_profile(resume_data, resume_text, linkedin_data=None):
    """
    Analyze LinkedIn profile by comparing resume with actual LinkedIn profile
    If linkedin_data is provided, compare resume vs LinkedIn
    Otherwise, provide resume-based recommendations
    """
    text_lower = resume_text.lower()
    linkedin_score = 0
    max_score = 100
    tips = []
    comparison = {}
    
    # Check if we have LinkedIn data to compare
    has_linkedin_data = linkedin_data and linkedin_data.get('success')
    
    if has_linkedin_data:
        # Compare resume with LinkedIn profile
        li_profile = linkedin_data.get('data', {})
        
        # 1. Headline Comparison (15 points)
        if li_profile.get('headline'):
            resume_skills = set([s.lower() for s in resume_data['skills'][:5]])
            linkedin_headline = li_profile.get('headline', '').lower()
            
            skills_in_headline = sum(1 for skill in resume_skills if skill in linkedin_headline)
            if skills_in_headline >= 2:
                linkedin_score += 15
                tips.append({
                    'icon': 'check',
                    'category': 'Professional Headline',
                    'status': 'Good',
                    'resume': ', '.join(resume_data['skills'][:3]),
                    'linkedin': li_profile.get('headline', 'Not set'),
                    'tip': 'Your headline includes relevant skills!'
                })
            else:
                linkedin_score += 5
                tips.append({
                    'icon': 'warn',
                    'category': 'Professional Headline',
                    'status': 'Needs Improvement',
                    'resume': ', '.join(resume_data['skills'][:3]),
                    'linkedin': li_profile.get('headline', 'Not set'),
                    'tip': f"Add these skills from your resume: {', '.join(resume_data['skills'][:3])}"
                })
        else:
            tips.append({
                'icon': 'cross',
                'category': 'Professional Headline',
                'status': 'Missing',
                'resume': ', '.join(resume_data['skills'][:3]),
                'linkedin': 'Not found',
                'tip': 'Add a professional headline with your key skills'
            })
        
        # 2. About Section (20 points)
        if li_profile.get('about') and len(li_profile.get('about', '')) > 100:
            linkedin_score += 20
            tips.append({
                'icon': 'check',
                'category': 'About Section',
                'status': 'Good',
                'resume': 'Present' if any(word in text_lower for word in ['summary', 'objective']) else 'Missing',
                'linkedin': f"{len(li_profile.get('about', ''))} characters",
                'tip': 'Your About section is well-developed'
            })
        elif li_profile.get('about'):
            linkedin_score += 10
            tips.append({
                'icon': 'warn',
                'category': 'About Section',
                'status': 'Too Short',
                'resume': 'Present' if any(word in text_lower for word in ['summary', 'objective']) else 'Missing',
                'linkedin': f"{len(li_profile.get('about', ''))} characters",
                'tip': 'Expand your About section to at least 200 characters. Add achievements and expertise'
            })
        else:
            tips.append({
                'icon': 'cross',
                'category': 'About Section',
                'status': 'Missing',
                'resume': 'Present' if any(word in text_lower for word in ['summary', 'objective']) else 'Missing',
                'linkedin': 'Empty',
                'tip': 'Write a compelling About section using your resume summary'
            })
        
        # 3. Skills Comparison (20 points)
        resume_skills_count = len(resume_data['skills'])
        linkedin_skills_count = len(li_profile.get('skills', []))
        
        if linkedin_skills_count >= 30:
            linkedin_score += 20
            missing_skills = [s for s in resume_data['skills'] if s.lower() not in [ls.lower() for ls in li_profile.get('skills', [])]]
            tips.append({
                'icon': 'check',
                'category': 'Skills & Endorsements',
                'status': 'Excellent',
                'resume': f"{resume_skills_count} skills",
                'linkedin': f"{linkedin_skills_count} skills",
                'tip': f"Great! Add these {len(missing_skills)} missing skills: {', '.join(missing_skills[:5])}" if missing_skills else "Perfect skills coverage!"
            })
        elif linkedin_skills_count >= 15:
            linkedin_score += 12
            tips.append({
                'icon': 'warn',
                'category': 'Skills & Endorsements',
                'status': 'Good',
                'resume': f"{resume_skills_count} skills",
                'linkedin': f"{linkedin_skills_count} skills",
                'tip': f"Add {50 - linkedin_skills_count} more skills. LinkedIn allows up to 50"
            })
        else:
            tips.append({
                'icon': 'cross',
                'category': 'Skills & Endorsements',
                'status': 'Insufficient',
                'resume': f"{resume_skills_count} skills",
                'linkedin': f"{linkedin_skills_count} skills",
                'tip': f"You need {50 - linkedin_skills_count} more skills. Add all skills from your resume"
            })
        
        # 4. Experience Comparison (25 points)
        linkedin_experience_count = len(li_profile.get('experience', []))
        resume_has_exp = any(word in text_lower for word in ['experience', 'work history'])
        
        if linkedin_experience_count >= 2:
            linkedin_score += 25
            tips.append({
                'icon': 'check',
                'category': 'Work Experience',
                'status': 'Complete',
                'resume': 'Present' if resume_has_exp else 'Not detected',
                'linkedin': f"{linkedin_experience_count} positions",
                'tip': 'Experience section looks good!'
            })
        elif linkedin_experience_count >= 1:
            linkedin_score += 15
            tips.append({
                'icon': 'warn',
                'category': 'Work Experience',
                'status': 'Incomplete',
                'resume': 'Present' if resume_has_exp else 'Not detected',
                'linkedin': f"{linkedin_experience_count} position",
                'tip': 'Add all your work experience from resume'
            })
        else:
            tips.append({
                'icon': 'cross',
                'category': 'Work Experience',
                'status': 'Missing',
                'resume': 'Present' if resume_has_exp else 'Not detected',
                'linkedin': '0 positions',
                'tip': 'Add your work experience from resume to LinkedIn'
            })
        
        # 5. Education (10 points)
        if li_profile.get('education'):
            linkedin_score += 10
            tips.append({
                'icon': 'check',
                'category': 'Education',
                'status': 'Present',
                'resume': 'Present' if any(word in text_lower for word in ['education', 'degree']) else 'Not detected',
                'linkedin': 'Added',
                'tip': 'Education section complete'
            })
        else:
            tips.append({
                'icon': 'cross',
                'category': 'Education',
                'status': 'Missing',
                'resume': 'Present' if any(word in text_lower for word in ['education', 'degree']) else 'Not detected',
                'linkedin': 'Missing',
                'tip': 'Add your educational background'
            })
        
        # 6. Profile Completeness (10 points)
        has_photo = li_profile.get('has_photo', False)
        has_custom_url = li_profile.get('has_custom_url', False)
        
        if has_photo and has_custom_url:
            linkedin_score += 10
            tips.append({
                'icon': 'check',
                'category': 'Profile Basics',
                'status': 'Complete',
                'resume': 'N/A',
                'linkedin': 'Photo & Custom URL',
                'tip': 'Profile basics are set up!'
            })
        else:
            missing = []
            if not has_photo:
                missing.append('professional photo')
            if not has_custom_url:
                missing.append('custom URL')
            tips.append({
                'icon': 'warn',
                'category': 'Profile Basics',
                'status': 'Incomplete',
                'resume': 'N/A',
                'linkedin': 'Missing items',
                'tip': f"Add: {', '.join(missing)}"
            })
    
    else:
        # No LinkedIn data - provide resume-based recommendations
        # (Keep original logic for when we don't have LinkedIn data)
        
        if resume_data['skills']:
            linkedin_score += 15
            tips.append({
                'icon': 'check',
                'category': 'Professional Headline',
                'status': 'Resume Ready',
                'resume': ', '.join(resume_data['skills'][:3]),
                'linkedin': 'Not checked',
                'tip': f"Use: '{', '.join(resume_data['skills'][:3])} Specialist'"
            })
        
        summary_keywords = ['summary', 'objective', 'profile']
        has_summary = any(word in text_lower for word in summary_keywords)
        
        if has_summary:
            linkedin_score += 20
            tips.append({
                'icon': 'check',
                'category': 'About Section',
                'status': 'Resume Ready',
                'resume': 'Present',
                'linkedin': 'Not checked',
                'tip': 'Transfer your resume summary to LinkedIn'
            })
        
        skill_count = len(resume_data['skills'])
        if skill_count >= 15:
            linkedin_score += 20
        elif skill_count >= 5:
            linkedin_score += 12
        
        tips.append({
            'icon': 'check' if skill_count >= 15 else 'warn',
            'category': 'Skills & Endorsements',
            'status': 'Resume Ready',
            'resume': f"{skill_count} skills",
            'linkedin': 'Not checked',
            'tip': f'Add all {skill_count} skills to LinkedIn'
        })
        
        has_experience = any(word in text_lower for word in ['experience', 'work history'])
        if has_experience:
            linkedin_score += 20
        
        tips.append({
            'icon': 'check' if has_experience else 'cross',
            'category': 'Work Experience',
            'status': 'Resume Ready',
            'resume': 'Present' if has_experience else 'Missing',
            'linkedin': 'Not checked',
            'tip': 'Copy work experience to LinkedIn with bullet points'
        })
        
        if any(word in text_lower for word in ['education', 'degree']):
            linkedin_score += 10
    
    # Bonus tips (always shown)
    bonus_tips = [
        {
            'icon': 'star',
            'category': 'Profile Photo',
            'tip': 'Use professional headshot: clear background, professional attire, smiling',
            'action': 'Upload or update your profile photo'
        },
        {
            'icon': 'star',
            'category': 'Custom URL',
            'tip': 'Create custom URL: linkedin.com/in/yourname',
            'action': 'Go to Settings → Edit public profile → Customize URL'
        },
        {
            'icon': 'star',
            'category': 'Recommendations',
            'tip': 'Get 3-5 recommendations from colleagues/managers',
            'action': 'Request recommendations from recent connections'
        },
        {
            'icon': 'star',
            'category': 'Activity & Posts',
            'tip': 'Post 2-3 times per week, engage with content daily',
            'action': 'Share an article or insight related to your field'
        },
        {
            'icon': 'star',
            'category': 'Featured Section',
            'tip': 'Showcase your best work in Featured section',
            'action': 'Add: GitHub repos, portfolio, articles, certifications'
        }
    ]
    
    return {
        'score': min(linkedin_score, max_score),
        'max_score': max_score,
        'tips': tips,
        'bonus_tips': bonus_tips,
        'has_comparison': has_linkedin_data,
        'comparison_data': comparison
    }

def analyze_linkedin_optimization(resume_data, resume_text):
    """Analyze and provide LinkedIn profile optimization tips"""
    text_lower = resume_text.lower()
    linkedin_score = 0
    max_score = 100
    tips = []
    
    # 1. Headline/Title Optimization (15 points)
    if resume_data['skills']:
        linkedin_score += 15
        tips.append({
            'icon': 'check',
            'category': 'Professional Headline',
            'tip': f"Use: '{resume_data['name']} | {', '.join(resume_data['skills'][:3])} Specialist'",
            'example': f"Example: 'John Doe | Python, React, AWS Specialist | Building Scalable Solutions'"
        })
    else:
        tips.append({
            'icon': 'cross',
            'category': 'Professional Headline',
            'tip': 'Add skills to your headline instead of just job title',
            'example': 'Instead of "Software Engineer" use "Software Engineer | Python, Cloud, AI | Tech Enthusiast"'
        })
    
    # 2. About/Summary Section (20 points)
    summary_keywords = ['summary', 'objective', 'profile', 'about']
    has_summary = any(word in text_lower for word in summary_keywords)
    
    if has_summary:
        linkedin_score += 20
        tips.append({
            'icon': 'check',
            'category': 'About Section',
            'tip': 'Transfer your resume summary to LinkedIn About section',
            'example': 'Include: your expertise, achievements, what drives you, and call-to-action'
        })
    else:
        tips.append({
            'icon': 'cross',
            'category': 'About Section',
            'tip': 'Write a compelling About section (3-5 paragraphs)',
            'example': 'Start with your expertise → Share achievements → Explain your passion → End with CTA'
        })
    
    # 3. Skills Section (20 points)
    skill_count = len(resume_data['skills'])
    if skill_count >= 15:
        linkedin_score += 20
        tips.append({
            'icon': 'check',
            'category': 'Skills & Endorsements',
            'tip': f'Add all {skill_count} skills from your resume (LinkedIn allows 50)',
            'example': 'Prioritize: Top 3 most important skills, then add 47 more relevant ones'
        })
    elif skill_count >= 5:
        linkedin_score += 12
        tips.append({
            'icon': 'warn',
            'category': 'Skills & Endorsements',
            'tip': f'You have {skill_count} skills. Aim for 50 skills on LinkedIn',
            'example': 'Add: technical skills, soft skills, tools, methodologies, certifications'
        })
    else:
        tips.append({
            'icon': 'cross',
            'category': 'Skills & Endorsements',
            'tip': 'Add at least 15-20 relevant skills',
            'example': 'Include both technical and soft skills for better visibility'
        })
    
    # 4. Experience Section (20 points)
    has_experience = any(word in text_lower for word in ['experience', 'work history', 'employment'])
    if has_experience:
        bullet_points = text_lower.count('•') + text_lower.count('-')
        if bullet_points >= 10:
            linkedin_score += 20
            tips.append({
                'icon': 'check',
                'category': 'Experience',
                'tip': 'Copy your detailed experience with bullet points to LinkedIn',
                'example': 'Use action verbs: Led, Developed, Increased, Achieved, Managed'
            })
        else:
            linkedin_score += 10
            tips.append({
                'icon': 'warn',
                'category': 'Experience',
                'tip': 'Add more detailed bullet points to each role (3-5 per role)',
                'example': '• Increased team productivity by 40% through agile implementation'
            })
    else:
        tips.append({
            'icon': 'cross',
            'category': 'Experience',
            'tip': 'Add work experience with achievements and metrics',
            'example': 'Focus on impact and results, not just responsibilities'
        })
    
    # 5. Education & Certifications (10 points)
    edu_keywords = ['education', 'degree', 'university', 'bachelor', 'master', 'certification']
    if any(word in text_lower for word in edu_keywords):
        linkedin_score += 10
        tips.append({
            'icon': 'check',
            'category': 'Education & Certifications',
            'tip': 'Add all degrees and certifications to LinkedIn',
            'example': 'Include: Institution, Degree, Year, Honors, Relevant coursework'
        })
    else:
        tips.append({
            'icon': 'cross',
            'category': 'Education & Certifications',
            'tip': 'Add educational background and certifications',
            'example': 'Include online courses, bootcamps, and professional certifications'
        })
    
    # 6. Projects & Portfolio (15 points)
    has_projects = any(word in text_lower for word in ['project', 'built', 'developed', 'portfolio'])
    if has_projects:
        linkedin_score += 15
        tips.append({
            'icon': 'check',
            'category': 'Featured Projects',
            'tip': 'Showcase projects in LinkedIn Featured section',
            'example': 'Add: GitHub repos, live demos, case studies, publications'
        })
    else:
        tips.append({
            'icon': 'cross',
            'category': 'Featured Projects',
            'tip': 'Create a projects section or add Featured content',
            'example': 'Upload: portfolio PDFs, project screenshots, GitHub links'
        })
    
    # Additional LinkedIn-specific tips
    bonus_tips = [
        {
            'icon': 'star',
            'category': 'Profile Photo',
            'tip': 'Use a professional headshot (not from resume)',
            'example': 'Clear background, professional attire, smiling, good lighting'
        },
        {
            'icon': 'star',
            'category': 'Custom URL',
            'tip': 'Create custom LinkedIn URL: linkedin.com/in/yourname',
            'example': 'Makes your profile easier to share and looks more professional'
        },
        {
            'icon': 'star',
            'category': 'Recommendations',
            'tip': 'Request 3-5 recommendations from colleagues/managers',
            'example': 'Reach out to people you\'ve worked with closely'
        },
        {
            'icon': 'star',
            'category': 'Keywords',
            'tip': 'Use keywords from job descriptions throughout your profile',
            'example': 'If targeting "Full Stack Developer" roles, use that exact phrase'
        },
        {
            'icon': 'star',
            'category': 'Engagement',
            'tip': 'Post regularly and engage with content (2-3 times/week)',
            'example': 'Share insights, comment on posts, publish articles'
        }
    ]
    
    return {
        'score': linkedin_score,
        'max_score': max_score,
        'tips': tips,
        'bonus_tips': bonus_tips
    }

def generate_linkedin_sections(resume_data, detected_field):
    """Generate ready-to-use LinkedIn content"""
    
    sections = {}
    
    # 1. Professional Headline
    top_skills = ', '.join(resume_data['skills'][:3]) if resume_data['skills'] else 'Professional'
    sections['headline'] = f"{detected_field or 'Professional'} | {top_skills} | Open to Opportunities"
    
    # 2. About Section Template
    sections['about'] = f"""🚀 About Me

I'm a passionate {detected_field or 'professional'} with expertise in {', '.join(resume_data['skills'][:5]) if resume_data['skills'] else 'various technologies'}.

💡 What I Do:
• [Add your main responsibilities/expertise]
• [Add your specialization]
• [Add what makes you unique]

🏆 Key Achievements:
• [Add achievement with metric - e.g., "Increased efficiency by 40%"]
• [Add another achievement]
• [Add third achievement]

🔧 Technical Skills:
{', '.join(resume_data['skills'][:15]) if resume_data['skills'] else '[Add your skills]'}

📫 Let's Connect:
I'm always interested in [your interests - e.g., "innovative projects", "collaboration opportunities"]
Feel free to reach out!
"""
    
    # 3. Experience Bullet Points Template
    sections['experience_template'] = """• Led [project/initiative] resulting in [quantifiable outcome]
• Developed [solution/feature] using [technologies] that [impact]
• Collaborated with [team size] team to [achievement]
• Implemented [process/system] which improved [metric] by [percentage]
• Managed [responsibility] ensuring [positive outcome]"""
    
    # 4. Skills to Add
    sections['skills_list'] = resume_data['skills'][:50] if resume_data['skills'] else []
    
    # 5. Featured Section Ideas
    sections['featured_ideas'] = [
        "GitHub repository links of your best projects",
        "Portfolio website or personal blog",
        "Published articles or technical blogs",
        "Certificates from online courses (Coursera, Udemy, etc.)",
        "Presentation slides from conferences/talks",
        "Case studies or project documentation"
    ]
    
    return sections

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
                    
                    # NEW: LinkedIn Optimization Section
                    st.header("💼 LinkedIn Profile Optimization")
                    
                    # Check if LinkedIn URL exists in resume
                    linkedin_url = extract_linkedin_url(resume_data['raw_text'])
                    linkedin_data = None
                    
                    if linkedin_url:
                        st.success(f"✅ LinkedIn profile found in resume: {linkedin_url}")
                        
                        with st.spinner("🔍 Analyzing your LinkedIn profile..."):
                            # Try to fetch LinkedIn data
                            linkedin_data = scrape_linkedin_profile(linkedin_url)
                            
                            if not linkedin_data.get('success'):
                                st.warning("⚠️ Unable to automatically fetch LinkedIn data (LinkedIn blocks automated access)")
                                st.info("💡 **Manual Option:** Please provide your LinkedIn profile details below for comparison")
                                
                                # Manual input option
                                with st.expander("📝 Enter LinkedIn Profile Details Manually", expanded=True):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        li_headline = st.text_input("Your LinkedIn Headline", 
                                                                   placeholder="e.g., Software Engineer at Tech Corp")
                                        li_about_length = st.number_input("About Section Length (characters)", 
                                                                         min_value=0, value=0)
                                        li_skills_count = st.number_input("Number of Skills on LinkedIn", 
                                                                         min_value=0, max_value=50, value=0)
                                    
                                    with col2:
                                        li_experience_count = st.number_input("Number of Work Experiences", 
                                                                             min_value=0, value=0)
                                        li_has_education = st.checkbox("Education section completed")
                                        li_has_photo = st.checkbox("Profile photo uploaded")
                                        li_has_custom_url = st.checkbox("Custom URL created")
                                    
                                    if st.button("Analyze My LinkedIn Profile"):
                                        # Create manual LinkedIn data structure
                                        linkedin_data = {
                                            'success': True,
                                            'data': {
                                                'headline': li_headline,
                                                'about': 'x' * li_about_length,
                                                'skills': ['skill'] * li_skills_count,
                                                'experience': [{}] * li_experience_count,
                                                'education': [{}] if li_has_education else [],
                                                'has_photo': li_has_photo,
                                                'has_custom_url': li_has_custom_url
                                            }
                                        }
                                        st.success("✅ Profile data captured! Scroll down to see analysis.")
                    else:
                        st.warning("⚠️ No LinkedIn profile URL found in your resume")
                        st.info("📌 Please provide your LinkedIn profile URL to get personalized optimization tips")
                        
                        # Ask for LinkedIn URL
                        user_linkedin_url = st.text_input(
                            "Enter your LinkedIn Profile URL",
                            placeholder="https://www.linkedin.com/in/your-profile",
                            help="Example: https://www.linkedin.com/in/johndoe"
                        )
                        
                        if user_linkedin_url:
                            if 'linkedin.com/in/' in user_linkedin_url.lower():
                                linkedin_url = user_linkedin_url
                                st.success(f"✅ LinkedIn URL captured: {linkedin_url}")
                                
                                # Provide manual input option
                                st.info("💡 Since automated fetching is limited, please provide your profile details:")
                                
                                with st.expander("📝 Enter Your LinkedIn Profile Details", expanded=True):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        li_headline = st.text_input("Current LinkedIn Headline", 
                                                                   placeholder="e.g., Data Scientist | Python, ML, AI")
                                        li_about_length = st.number_input("About Section Length (approx. characters)", 
                                                                         min_value=0, value=0,
                                                                         help="Open your About section and count characters")
                                        li_skills_count = st.number_input("Number of Skills Listed", 
                                                                         min_value=0, max_value=50, value=0)
                                    
                                    with col2:
                                        li_experience_count = st.number_input("Number of Job Positions", 
                                                                             min_value=0, value=0)
                                        li_has_education = st.checkbox("Education section is filled")
                                        li_has_photo = st.checkbox("I have a profile photo")
                                        li_has_custom_url = st.checkbox("I have a custom URL")
                                    
                                    if st.button("🔍 Analyze My LinkedIn vs Resume"):
                                        linkedin_data = {
                                            'success': True,
                                            'data': {
                                                'headline': li_headline,
                                                'about': 'x' * li_about_length,
                                                'skills': ['skill'] * li_skills_count,
                                                'experience': [{}] * li_experience_count,
                                                'education': [{}] if li_has_education else [],
                                                'has_photo': li_has_photo,
                                                'has_custom_url': li_has_custom_url
                                            }
                                        }
                                        st.success("✅ Analysis complete! See results below.")
                            else:
                                st.error("❌ Please enter a valid LinkedIn URL (should contain 'linkedin.com/in/')")
                    
                    # Perform LinkedIn analysis
                    linkedin_analysis = analyze_linkedin_optimization_with_profile(
                        resume_data, 
                        resume_data['raw_text'],
                        linkedin_data
                    )
                    
                    # Display LinkedIn Score
                    li_score = linkedin_analysis['score']
                    if li_score >= 80:
                        li_color = "#0077b5"
                        li_msg = "LinkedIn Optimized!" if linkedin_analysis['has_comparison'] else "Resume Ready for LinkedIn"
                    elif li_score >= 60:
                        li_color = "#fba171"
                        li_msg = "Good Progress" if linkedin_analysis['has_comparison'] else "Needs Some Work"
                    else:
                        li_color = "#d73b5c"
                        li_msg = "Needs Improvement"
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(f"""
                        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                            <h1 style='color: white; margin: 0; font-size: 48px;'>{li_score}/100</h1>
                            <p style='color: white; font-size: 18px; margin: 5px 0;'>{li_msg}</p>
                            <p style='color: #f0f0f0; font-size: 14px;'>{'Resume vs LinkedIn Comparison' if linkedin_analysis['has_comparison'] else 'Based on Resume Data'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.write("")  # Spacing
                    
                    # Show comparison or recommendations
                    if linkedin_analysis['has_comparison']:
                        st.success("🎯 **Comparison Mode:** Analyzing your resume against your LinkedIn profile")
                    else:
                        st.info("📋 **Recommendation Mode:** Showing how to transfer resume content to LinkedIn")
                    
                    # Display optimization tips with comparison
                    st.subheader("📊 Profile Analysis & Recommendations")
                    
                    for tip in linkedin_analysis['tips']:
                        icon_map = {
                            'check': '✅',
                            'warn': '⚠️',
                            'cross': '❌',
                            'star': '⭐'
                        }
                        icon = icon_map.get(tip['icon'], '•')
                        
                        with st.expander(f"{icon} {tip['category']} - {tip.get('status', 'Check')}", expanded=False):
                            if 'resume' in tip and 'linkedin' in tip:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("**📄 Resume:**")
                                    st.info(tip['resume'])
                                with col2:
                                    st.markdown("**💼 LinkedIn:**")
                                    if tip.get('status') == 'Good' or tip.get('status') == 'Complete':
                                        st.success(tip['linkedin'])
                                    elif tip.get('status') == 'Missing' or tip.get('status') == 'Insufficient':
                                        st.error(tip['linkedin'])
                                    else:
                                        st.warning(tip['linkedin'])
                            
                            st.markdown(f"**💡 Recommendation:**")
                            st.write(tip['tip'])
                    
                    # Bonus tips
                    st.subheader("⭐ Additional LinkedIn Tips")
                    bonus_cols = st.columns(2)
                    for idx, tip in enumerate(linkedin_analysis['bonus_tips']):
                        with bonus_cols[idx % 2]:
                            with st.container():
                                st.markdown(f"**{tip['category']}**")
                                st.write(f"💡 {tip['tip']}")
                                if 'action' in tip:
                                    st.caption(f"✓ Action: {tip['action']}")
                                st.divider()
                    
                    # Ready-to-use content (same as before)
                    linkedin_content = generate_linkedin_sections(resume_data, detected_field)
                    
                    # Ready-to-use LinkedIn content templates
                    st.header("📋 Ready-to-Use LinkedIn Content")
                    
                    if linkedin_analysis['has_comparison']:
                        st.success("✨ Based on your resume vs LinkedIn comparison, here are optimized templates:")
                    else:
                        st.info("📝 Copy these templates to quickly build your LinkedIn profile from your resume:")
                    
                    linkedin_content = generate_linkedin_sections(resume_data, detected_field)
                    
                    # Headline
                    with st.expander("💼 Professional Headline Template", expanded=True):
                        st.code(linkedin_content['headline'], language=None)
                        st.caption("📌 Copy this to: Edit Profile → Headline section")
                    
                    # About Section
                    with st.expander("📖 About Section Template", expanded=True):
                        st.text_area("About Section", linkedin_content['about'], height=300, key='about_template')
                        st.caption("📌 Copy this to: Edit Profile → About section (customize with your details)")
                    
                    # Experience bullets
                    with st.expander("💼 Experience Bullet Points"):
                        st.code(linkedin_content['experience_template'], language=None)
                        st.caption("📌 Use this format for each job in: Experience → Edit position → Description")
                    
                    # Skills List
                    if linkedin_content['skills_list']:
                        with st.expander("🎯 Skills to Add (Copy All)"):
                            st.write("**Skills detected from your resume:**")
                            skills_text = ', '.join(linkedin_content['skills_list'])
                            st.text_area("Copy these skills", skills_text, height=150)
                            st.caption(f"{len(linkedin_content['skills_list'])} skills found. LinkedIn allows up to 50 skills.")
                    
                    # Featured Section Ideas
                    with st.expander("⭐ Featured Section Ideas"):
                        st.write("**Add these to your LinkedIn Featured section:**")
                        for idea in linkedin_content['featured_ideas']:
                            st.write(f"• {idea}")
                    
                    # LinkedIn Action Plan
                    st.subheader("🎯 Your LinkedIn Action Plan")
                    st.markdown("""
                    **Complete these steps to optimize your profile:**
                    
                    1. ✅ Update your professional headline using the template above
                    2. ✅ Rewrite your About section with the provided template
                    3. ✅ Add all detected skills to your Skills section
                    4. ✅ Update each job with detailed bullet points
                    5. ✅ Upload a professional profile photo
                    6. ✅ Create a custom LinkedIn URL
                    7. ✅ Request 3-5 recommendations
                    8. ✅ Add Featured content (projects, certificates)
                    9. ✅ Post your first update announcing your profile refresh
                    10. ✅ Connect with 50+ people in your industry
                    
                    **🎓 Pro Tip:** Complete profiles get 40x more opportunities!
                    """)
                    
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