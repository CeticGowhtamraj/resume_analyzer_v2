"""
Smart Resume Analyzer - Clean Professional Version
Clean UI with proper layout and simple ATS score display
UPDATED: Stricter ATS scoring + Better internship vs job experience detection
"""

import streamlit as st
import nltk
import re
import pandas as pd
import base64
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

# Import course data from courese_1
from courese_1 import (
    # Data Science roles
    data_scientist_courses, data_analyst_courses, data_engineer_courses,
    # Software Development roles
    software_engineer_courses, sde1_courses, sde2_courses,
    web_developer_courses, frontend_courses, backend_courses,
    # Mobile Development
    android_courses, ios_courses, cross_platform_courses,
    # Other roles
    uiux_courses, design_tools_courses, bi_analyst_courses,
    cloud_devops_courses,
    # Resources
    resume_resources, interview_resources, soft_skills_courses,
    practice_platforms, certifications,
    # Legacy compatibility
    resume_videos, interview_videos
)

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# ==================== HELPER FUNCTIONS ====================

def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    import re
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def is_youtube_url(url):
    """Check if URL is a YouTube link"""
    return 'youtube.com' in url or 'youtu.be' in url

# ==================== DATABASE ====================

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
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        yield None
    finally:
        if connection:
            connection.close()


# ==================== CUSTOM CSS ====================

def load_css():
    st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Score card */
    .score-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 3px solid #667eea;
    }
    
    .score-number {
        font-size: 5rem;
        font-weight: 800;
        color: #667eea;
        line-height: 1;
        margin: 0;
    }
    
    .score-label {
        font-size: 1.3rem;
        color: #666;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .score-verdict {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 1rem;
    }
    
    .verdict-excellent { color: #10b981; }
    .verdict-good { color: #3b82f6; }
    .verdict-fair { color: #f59e0b; }
    .verdict-poor { color: #ef4444; }
    
    /* Info cards */
    .info-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .info-card h3 {
        margin: 0 0 1rem 0;
        color: #333;
        font-size: 1.2rem;
    }
    
    .info-row {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .info-row:last-child {
        border-bottom: none;
    }
    
    .info-label {
        font-weight: 600;
        color: #555;
        min-width: 120px;
    }
    
    .info-value {
        color: #333;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    .badge-role {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .badge-fresher {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #333;
    }
    
    .badge-entry-level {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
    }
    
    .badge-intermediate {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
    }
    
    .badge-senior {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .badge-expert {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #333;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Skills */
    .skill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .skill-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Feedback boxes */
    .feedback-box {
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 0.7rem 0;
        font-size: 1rem;
        border-left: 4px solid;
    }
    
    .feedback-success {
        background: #d1fae5;
        border-color: #10b981;
        color: #065f46;
    }
    
    .feedback-warning {
        background: #fef3c7;
        border-color: #f59e0b;
        color: #92400e;
    }
    
    .feedback-error {
        background: #fee2e2;
        border-color: #ef4444;
        color: #991b1b;
    }
    
    /* PDF container */
    .pdf-container {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Course grid */
    .course-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    /* Video card styling */
    .video-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        border: 2px solid #f0f0f0;
    }
    
    .video-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .video-thumbnail {
        width: 100%;
        height: 180px;
        object-fit: cover;
        display: block;
    }
    
    .video-content {
        padding: 1.2rem;
    }
    
    .video-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 0.8rem;
        line-height: 1.4;
        min-height: 2.8rem;
    }
    
    .video-link {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s;
    }
    
    .video-link:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== ROLE DETECTION ====================

ROLE_SKILLS = {
    'Data Scientist': {
        'required': ['python', 'machine learning', 'statistics'],
        'optional': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'deep learning', 'nlp'],
        'keywords': ['data science', 'predictive modeling', 'neural network', 'ai', 'artificial intelligence']
    },
    'Data Analyst': {
        'required': ['sql', 'excel', 'data analysis'],
        'optional': ['python', 'r', 'tableau', 'power bi', 'statistics', 'pandas'],
        'keywords': ['data visualization', 'reporting', 'dashboard', 'business intelligence', 'analytics']
    },
    'Data Engineer': {
        'required': ['sql', 'python', 'etl', 'data pipeline'],
        'optional': ['spark', 'hadoop', 'airflow', 'kafka', 'aws', 'azure', 'gcp', 'snowflake'],
        'keywords': ['data warehouse', 'big data', 'streaming', 'batch processing', 'data lake']
    },
    'Software Engineer': {
        'required': ['programming', 'algorithms', 'data structures'],
        'optional': ['java', 'python', 'c++', 'javascript', 'system design', 'databases', 'git'],
        'keywords': ['software development', 'coding', 'oop', 'api', 'microservices', 'agile']
    },
    'Web Developer': {
        'required': ['html', 'css', 'javascript'],
        'optional': ['react', 'angular', 'vue', 'node.js', 'express', 'mongodb', 'rest api'],
        'keywords': ['web development', 'frontend', 'backend', 'full stack', 'responsive']
    },
    'Mobile Developer': {
        'required': ['mobile development'],
        'optional': ['android', 'ios', 'kotlin', 'swift', 'react native', 'flutter'],
        'keywords': ['app development', 'mobile app', 'android studio', 'xcode']
    },
    'UI/UX Designer': {
        'required': ['ui', 'ux', 'design'],
        'optional': ['figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator', 'prototyping'],
        'keywords': ['user interface', 'user experience', 'wireframe', 'mockup', 'design thinking']
    },
    'DevOps Engineer': {
        'required': ['devops', 'ci/cd'],
        'optional': ['docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'aws', 'azure'],
        'keywords': ['automation', 'infrastructure', 'deployment', 'monitoring', 'cloud']
    }
}

def detect_role(resume_text, skills):
    """Enhanced role detection with confidence score"""
    resume_lower = resume_text.lower()
    skills_lower = [s.lower() for s in skills]
    
    role_scores = {}
    
    for role, criteria in ROLE_SKILLS.items():
        score = 0
        matches = []
        
        # Check required skills (high weight)
        required_matches = sum(1 for skill in criteria['required'] 
                             if skill in skills_lower or skill in resume_lower)
        score += required_matches * 15
        
        # Check optional skills (medium weight)
        optional_matches = sum(1 for skill in criteria['optional'] 
                              if skill in skills_lower or skill in resume_lower)
        score += optional_matches * 8
        
        # Check keywords (low weight)
        keyword_matches = sum(1 for keyword in criteria['keywords'] 
                             if keyword in resume_lower)
        score += keyword_matches * 3
        
        role_scores[role] = score
    
    if max(role_scores.values()) == 0:
        return None, 0
    
    best_role = max(role_scores.items(), key=lambda x: x[1])
    max_possible = len(ROLE_SKILLS[best_role[0]]['required']) * 15 + \
                   len(ROLE_SKILLS[best_role[0]]['optional']) * 8 + \
                   len(ROLE_SKILLS[best_role[0]]['keywords']) * 3
    
    confidence = min(100, int((best_role[1] / max_possible) * 100)) if max_possible > 0 else 0
    
    return best_role[0] if confidence > 20 else None, confidence


# ==================== COURSE RECOMMENDATION SYSTEM ====================

def get_recommended_courses(job_role, experience_level):
    """
    Get personalized course recommendations based on role and experience
    Returns a dictionary with different course categories
    """
    recommendations = {
        'primary_courses': [],
        'skill_building': [],
        'certifications': [],
        'practice_platforms': [],
        'soft_skills': []
    }
    
    # Map experience level to course level
    level_mapping = {
        'Fresher': 'Beginner',
        'Entry Level': 'Beginner',
        'Intermediate': 'Intermediate',
        'Senior': 'Advanced',
        'Expert': 'Advanced'
    }
    
    course_level = level_mapping.get(experience_level, 'Intermediate')
    
    # Role-specific course mapping
    role_course_map = {
        'Data Scientist': data_scientist_courses,
        'Data Analyst': data_analyst_courses,
        'Data Engineer': data_engineer_courses,
        'Software Engineer': software_engineer_courses,
        'Web Developer': web_developer_courses,
        'Mobile Developer': android_courses,  # Can be enhanced to choose android/ios
        'UI/UX Designer': uiux_courses,
        'DevOps Engineer': cloud_devops_courses  # Using cloud_devops_courses instead
    }
    
    # Get primary courses for the role
    if job_role in role_course_map:
        course_dict = role_course_map[job_role]
        
        # Special handling for DevOps (uses AWS/Azure/GCP structure)
        if job_role == 'DevOps Engineer':
            # cloud_devops_courses has AWS, Azure, Google Cloud keys
            recommendations['primary_courses'] = cloud_devops_courses.get('AWS', [])[:3]
            recommendations['skill_building'] = cloud_devops_courses.get('Azure', [])[:2]
            if 'Google Cloud' in cloud_devops_courses:
                recommendations['skill_building'].extend(cloud_devops_courses['Google Cloud'][:2])
        else:
            # Normal structure with Beginner/Intermediate/Advanced
            if course_level in course_dict:
                recommendations['primary_courses'] = course_dict[course_level]
            
            # Add courses from adjacent levels for comprehensive learning
            if course_level == 'Intermediate':
                if 'Beginner' in course_dict:
                    recommendations['skill_building'].extend(course_dict['Beginner'][:2])
                if 'Advanced' in course_dict:
                    recommendations['skill_building'].extend(course_dict['Advanced'][:2])
    
    # Add special courses for SDE roles
    if job_role == 'Software Engineer':
        if experience_level in ['Fresher', 'Entry Level']:
            if 'Essential' in sde1_courses:
                recommendations['skill_building'].extend(sde1_courses['Essential'][:3])
        elif experience_level in ['Intermediate', 'Senior']:
            if 'Essential' in sde2_courses:
                recommendations['skill_building'].extend(sde2_courses['Essential'][:3])
    
    # Add relevant certifications
    cert_map = {
        'Data Scientist': 'Data',
        'Data Analyst': 'Data',
        'Data Engineer': 'Data',
        'DevOps Engineer': 'Cloud',
        'Software Engineer': 'Cloud'
    }
    
    if job_role in cert_map and cert_map[job_role] in certifications:
        recommendations['certifications'] = certifications[cert_map[job_role]][:3]
    
    # Add practice platforms
    if job_role in ['Software Engineer', 'Data Scientist', 'Web Developer']:
        recommendations['practice_platforms'] = practice_platforms['Coding Practice'][:3]
    
    # Add soft skills courses
    recommendations['soft_skills'] = soft_skills_courses['Communication'][:2]
    
    return recommendations


def display_course_recommendations(job_role, experience_level):
    """Display personalized course recommendations in the UI with thumbnails"""
    
    # Move recommendations to full width (outside the two-column layout)
    st.markdown("---")
    st.markdown("<div class='section-header' style='text-align: center;'>📚 Your Personalized Learning Path</div>", 
                unsafe_allow_html=True)
    
    courses = get_recommended_courses(job_role, experience_level)
    
    # Primary Courses with thumbnails
    if courses['primary_courses']:
        st.markdown(f"""
            <div style='text-align: center; margin: 2rem 0 1.5rem 0;'>
                <h2 style='color: #667eea; margin: 0;'>🎯 {job_role} - {experience_level} Level</h2>
                <p style='color: #666; font-size: 1.1rem; margin-top: 0.5rem;'>
                    Curated courses tailored to your role and experience
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create grid layout for video cards
        st.markdown("<div class='course-grid'>", unsafe_allow_html=True)
        
        for course_name, course_url in courses['primary_courses']:
            # Check if it's a YouTube video
            video_id = extract_youtube_id(course_url) if is_youtube_url(course_url) else None
            
            if video_id:
                # YouTube video with thumbnail
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                st.markdown(f"""
                    <div class='video-card'>
                        <img src='{thumbnail_url}' class='video-thumbnail' alt='{course_name}' 
                             onerror="this.src='https://img.youtube.com/vi/{video_id}/hqdefault.jpg'">
                        <div class='video-content'>
                            <div class='video-title'>{course_name}</div>
                            <a href='{course_url}' target='_blank' class='video-link'>
                                ▶ Watch Now
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Regular course (non-YouTube)
                st.markdown(f"""
                    <div class='video-card'>
                        <div class='video-content' style='padding: 1.5rem;'>
                            <div class='video-title'>{course_name}</div>
                            <a href='{course_url}' target='_blank' class='video-link'>
                                🔗 Access Course
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional Resources in expandable sections
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Skill Building Courses
        if courses['skill_building']:
            with st.expander("💡 Skill Building Courses", expanded=False):
                for course_name, course_url in courses['skill_building']:
                    st.markdown(f"🎓 [{course_name}]({course_url})")
    
    with col2:
        # Certifications
        if courses['certifications']:
            with st.expander("🏆 Professional Certifications", expanded=False):
                for cert_name, cert_url in courses['certifications']:
                    st.markdown(f"📜 [{cert_name}]({cert_url})")
    
    with col3:
        # Practice Platforms
        if courses['practice_platforms']:
            with st.expander("⚡ Practice Platforms", expanded=False):
                for platform_name, platform_url in courses['practice_platforms']:
                    st.markdown(f"💻 [{platform_name}]({platform_url})")
    
    # Soft Skills (full width)
    if courses['soft_skills']:
        with st.expander("🗣️ Soft Skills Development", expanded=False):
            cols = st.columns(2)
            for idx, (skill_name, skill_url) in enumerate(courses['soft_skills']):
                with cols[idx % 2]:
                    st.markdown(f"✨ [{skill_name}]({skill_url})")



def display_resume_interview_resources():
    """Display resume and interview resources with thumbnails"""
    
    st.markdown("---")
    st.markdown("<div class='section-header' style='text-align: center;'>📄 Resume & Interview Mastery</div>", 
                unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; margin: 1rem 0 2rem 0;'>
            <p style='color: #666; font-size: 1.05rem;'>
                Stand out from the competition with these expert resources
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for Resume and Interview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <h3 style='color: #667eea; text-align: center; margin-bottom: 1.5rem;'>
                📝 Resume Building
            </h3>
        """, unsafe_allow_html=True)
        
        for resource_name, resource_url in resume_resources['Resume Writing'][:4]:
            video_id = extract_youtube_id(resource_url) if is_youtube_url(resource_url) else None
            
            if video_id:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                st.markdown(f"""
                    <div class='video-card'>
                        <img src='{thumbnail_url}' class='video-thumbnail' alt='{resource_name}'
                             onerror="this.src='https://img.youtube.com/vi/{video_id}/hqdefault.jpg'">
                        <div class='video-content'>
                            <div class='video-title'>{resource_name}</div>
                            <a href='{resource_url}' target='_blank' class='video-link'>
                                ▶ Watch Now
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='video-card'>
                        <div class='video-content' style='padding: 1.5rem;'>
                            <div class='video-title'>{resource_name}</div>
                            <a href='{resource_url}' target='_blank' class='video-link'>
                                🔗 Access Resource
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <h3 style='color: #667eea; text-align: center; margin-bottom: 1.5rem;'>
                🎤 Interview Preparation
            </h3>
        """, unsafe_allow_html=True)
        
        for resource_name, resource_url in interview_resources['Interview Tips'][:4]:
            video_id = extract_youtube_id(resource_url) if is_youtube_url(resource_url) else None
            
            if video_id:
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                st.markdown(f"""
                    <div class='video-card'>
                        <img src='{thumbnail_url}' class='video-thumbnail' alt='{resource_name}'
                             onerror="this.src='https://img.youtube.com/vi/{video_id}/hqdefault.jpg'">
                        <div class='video-content'>
                            <div class='video-title'>{resource_name}</div>
                            <a href='{resource_url}' target='_blank' class='video-link'>
                                ▶ Watch Now
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='video-card'>
                        <div class='video-content' style='padding: 1.5rem;'>
                            <div class='video-title'>{resource_name}</div>
                            <a href='{resource_url}' target='_blank' class='video-link'>
                                🔗 Access Resource
                            </a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)


# ==================== PDF PARSING ====================

def pdf_reader(file):
    """Extract text from PDF"""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    return text


# ==================== SKILL EXTRACTION ====================

SKILL_CATEGORIES = {
    'Programming Languages': [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
        'go', 'rust', 'typescript', 'scala', 'r', 'matlab', 'perl', 'dart'
    ],
    'Web Technologies': [
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
        'flask', 'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'sass',
        'webpack', 'next.js', 'nuxt.js'
    ],
    'Databases': [
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server',
        'cassandra', 'dynamodb', 'elasticsearch', 'sqlite', 'mariadb'
    ],
    'Data Science & ML': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
        'scikit-learn', 'pandas', 'numpy', 'nlp', 'computer vision', 'opencv',
        'data science', 'statistics', 'data analysis', 'neural networks'
    ],
    'Cloud & DevOps': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
        'ansible', 'ci/cd', 'devops', 'linux', 'git', 'github', 'gitlab'
    ],
    'Mobile Development': [
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'android studio',
        'xcode', 'mobile development'
    ],
    'Tools & Frameworks': [
        'power bi', 'tableau', 'excel', 'git', 'jira', 'confluence', 'postman',
        'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator'
    ],
    'Big Data': [
        'spark', 'hadoop', 'kafka', 'airflow', 'etl', 'data pipeline', 'hive',
        'pig', 'flink', 'storm', 'snowflake', 'databricks'
    ]
}

def extract_skills(text):
    """Extract skills from resume text"""
    text_lower = text.lower()
    found_skills = []
    skills_by_category = {}
    
    for category, skills in SKILL_CATEGORIES.items():
        category_skills = []
        for skill in skills:
            # Match whole words or common variations
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
                    category_skills.append(skill.title())
        
        if category_skills:
            skills_by_category[category] = category_skills
    
    return found_skills, skills_by_category


# ==================== SIMPLIFIED & ACCURATE EXPERIENCE CALCULATION ====================

def extract_experience_years(text):
    """
    COMPLETELY REWRITTEN: Simple, accurate experience extraction
    Focus: Get the actual work experience years correctly
    """
    text_lower = text.lower()
    current_year = 2026
    
    # ===== STEP 1: Check for EXPLICIT experience statement (TRUST THIS!) =====
    explicit_patterns = [
        r'(?:total\s+)?(?:work\s+)?(?:professional\s+)?experience\s*[:\-]?\s*(\d+)[\.\+]?\d*\s*(?:years?|yrs?)',
        r'(\d+)[\.\+]?\d*\s*(?:years?|yrs?)\s+(?:of\s+)?(?:work\s+)?(?:professional\s+)?experience',
        r'experience\s*[:\-]?\s*(\d+)[\.\+]?\d*\s*(?:years?|yrs?)',
    ]
    
    for pattern in explicit_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            # Get the highest mentioned year count
            years = [float(m) for m in matches if m.replace('.', '').isdigit()]
            if years:
                return int(round(max(years)))
    
    # ===== STEP 2: Check if definitely a fresher =====
    fresher_indicators = [
        'fresher', 'fresh graduate', 'recent graduate', 
        'seeking first job', 'looking for first position',
        'no prior experience', 'no work experience',
        'currently pursuing', 'final year', 'seeking internship'
    ]
    
    if any(indicator in text_lower for indicator in fresher_indicators):
        return 0
    
    # ===== STEP 3: Find experience section and extract date ranges =====
    # Try to find experience section
    experience_section = None
    exp_section_patterns = [
        r'(?:work\s+experience|professional\s+experience|employment\s+history|experience)[:\s]+(.*?)(?=\n\s*(?:education|academic|skills|technical\s+skills|projects|certifications|achievements)|$)',
        r'(?:experience)[:\s]+(.*?)(?=\n\s*(?:education|academic|skills|projects)|$)',
    ]
    
    for pattern in exp_section_patterns:
        match = re.search(pattern, text_lower, re.DOTALL | re.IGNORECASE)
        if match:
            experience_section = match.group(1)
            break
    
    # If no clear section, use full text but be more careful
    if not experience_section or len(experience_section) < 30:
        experience_section = text_lower
    
    # ===== STEP 4: Extract work date ranges (NOT education dates) =====
    # Look for date patterns like "2020 - 2023", "Jan 2020 - Present", etc.
    date_patterns = [
        # Pattern: Year - Year or Year - Present
        r'(\d{4})\s*[-–—]\s*(\d{4}|present|current)',
        # Pattern: Month Year - Month Year or Present
        r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*(\d{4})\s*[-–—]\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?(\d{4}|present|current)',
    ]
    
    date_ranges = []
    for pattern in date_patterns:
        matches = re.findall(pattern, experience_section, re.IGNORECASE)
        for match in matches:
            start_year_str = match[0] if match[0].isdigit() else match[1] if len(match) > 1 and match[1].isdigit() else None
            end_year_str = match[1] if len(match) > 1 else match[0]
            
            if not start_year_str:
                continue
                
            start_year = int(start_year_str)
            
            # Handle end year
            if 'present' in end_year_str.lower() or 'current' in end_year_str.lower():
                end_year = current_year
            elif end_year_str.isdigit():
                end_year = int(end_year_str)
            else:
                continue
            
            # Sanity checks
            if start_year < 1990 or start_year > current_year:
                continue
            if end_year < start_year or end_year > current_year + 1:
                continue
                
            duration = end_year - start_year
            
            # Only accept reasonable durations (0-25 years per job)
            if 0 <= duration <= 25:
                date_ranges.append({
                    'start': start_year,
                    'end': end_year,
                    'duration': duration
                })
    
    # ===== STEP 5: Check if dates are from education (IMPORTANT!) =====
    # Remove date ranges that are clearly from education section
    if date_ranges:
        filtered_ranges = []
        
        for date_range in date_ranges:
            start_year = date_range['start']
            end_year = date_range['end']
            
            # Check if this date range is near education keywords
            education_check_pattern = rf'(?:education|university|college|school|bachelor|master|b\.tech|m\.tech|degree|diploma|pursuing).*?{start_year}.*?{end_year}'
            education_check_pattern2 = rf'{start_year}.*?{end_year}.*?(?:education|university|college|bachelor|master|degree|graduation)'
            
            is_education = re.search(education_check_pattern, text_lower, re.DOTALL) or \
                          re.search(education_check_pattern2, text_lower, re.DOTALL)
            
            # If this is in education section, skip it
            if not is_education:
                filtered_ranges.append(date_range)
        
        date_ranges = filtered_ranges
    
    # ===== STEP 6: Calculate total experience =====
    if date_ranges:
        # Sort by start year
        date_ranges.sort(key=lambda x: x['start'])
        
        # Check for overlapping jobs (concurrent employment)
        total_experience = 0
        last_end_year = 0
        
        for date_range in date_ranges:
            if date_range['start'] >= last_end_year:
                # No overlap - add full duration
                total_experience += date_range['duration']
                last_end_year = date_range['end']
            else:
                # Overlap - only add non-overlapping portion
                overlap_start = max(date_range['start'], last_end_year)
                if date_range['end'] > overlap_start:
                    total_experience += (date_range['end'] - overlap_start)
                    last_end_year = date_range['end']
        
        return min(total_experience, 30)  # Cap at 30 years max
    
    # ===== STEP 7: Fallback - Look for any job titles with rough estimation =====
    job_titles = [
        'engineer', 'developer', 'analyst', 'manager', 'designer',
        'consultant', 'specialist', 'lead', 'architect', 'scientist'
    ]
    
    # Check if they mention working/worked
    has_work_experience = any(word in text_lower for word in [
        'worked at', 'working at', 'employed at', 'position at',
        'role at', 'job at'
    ])
    
    # Check for job titles (but NOT intern versions)
    has_job_title = False
    for title in job_titles:
        # Make sure it's not "Software Engineer Intern"
        pattern = rf'\b{title}\b(?!\s+intern)'
        if re.search(pattern, text_lower):
            has_job_title = True
            break
    
    # If they have work indicators and job titles, estimate conservatively
    if has_work_experience and has_job_title:
        # Look at all years mentioned
        all_years = re.findall(r'\b(19|20)\d{2}\b', text)
        if all_years:
            years_list = [int(y) for y in all_years]
            earliest = min(years_list)
            
            # If earliest year is recent (within 5 years), probably entry level
            if current_year - earliest <= 5:
                return 1  # Give them at least 1 year
            else:
                # Estimate conservatively (subtract education years)
                estimated = (current_year - earliest) - 4
                return max(1, min(estimated, 10))  # Between 1-10 years
    
    # ===== STEP 8: Check for internship only =====
    has_intern = 'intern' in text_lower or 'internship' in text_lower
    if has_intern and not has_job_title:
        return 0  # Only internship experience
    
    # ===== Default: Cannot determine experience =====
    return 0


def determine_experience_level(years):
    """Determine experience level based on years"""
    if years == 0:
        return 'Fresher'
    elif years <= 2:
        return 'Entry Level'
    elif years <= 5:
        return 'Intermediate'
    elif years <= 10:
        return 'Senior'
    else:
        return 'Expert'


# ==================== RESUME PARSING ====================

def parse_resume(file):
    """Main resume parsing function"""
    try:
        text = pdf_reader(file)
        
        if not text or len(text.strip()) < 100:
            return None, "Resume appears empty or too short"
        
        # Extract basic info
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        
        # Extract skills
        skills, skills_by_category = extract_skills(text)
        
        # Calculate experience
        years = extract_experience_years(text)
        experience_level = determine_experience_level(years)
        
        # Detect role
        job_role, role_confidence = detect_role(text, skills)
        
        # Count pages
        with open(file, 'rb') as f:
            pages = len(list(PDFPage.get_pages(f)))
        
        resume_data = {
            'name': name or 'Not Found',
            'email': email or 'Not Found',
            'mobile_number': phone or 'Not Found',
            'skills': skills,
            'skills_by_category': skills_by_category,
            'no_of_pages': pages,
            'experience_years': years,
            'experience_level': experience_level,
            'job_role': job_role,
            'role_confidence': role_confidence,
            'raw_text': text
        }
        
        return resume_data, "Success"
        
    except Exception as e:
        return None, f"Error parsing resume: {str(e)}"


def extract_name(text):
    """Extract name from resume (simple heuristic)"""
    lines = text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 3 and len(line) < 50:
            # Simple check: name usually contains 2-4 words, mostly alphabetic
            words = line.split()
            if 2 <= len(words) <= 4 and all(w.replace('.', '').isalpha() for w in words):
                return line
    return None

def extract_email(text):
    """Extract email from resume"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_phone(text):
    """Extract phone number from resume - Enhanced for international formats"""
    patterns = [
        # Indian format: +91 12345 67890 or +91-12345-67890 or +91 1234567890
        r'\+91[\s-]?\d{5}[\s-]?\d{5}',
        r'\+91[\s-]?\d{10}',
        # International with country code: +1-234-567-8901 or +44 20 1234 5678
        r'\+\d{1,3}[\s-]?\(?\d{2,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,4}',
        # US format: (123) 456-7890 or 123-456-7890
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        # Simple 10 digit
        r'\b\d{10}\b',
        # International: +12345678901 (up to 15 digits)
        r'\+\d{10,15}'
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            phone = match.group(0)
            # Clean up the phone number
            phone = re.sub(r'\s+', ' ', phone)  # Normalize spaces
            return phone.strip()
    return None


# ==================== BALANCED ATS SCORING ====================

def calculate_ats_score(resume_data, resume_text, job_role, role_confidence):
    """
    BALANCED: Calculate comprehensive ATS score with moderate, fair requirements
    Rewards good resumes while identifying clear areas for improvement
    """
    score = 0
    feedback = []
    text_lower = resume_text.lower()
    
    # ========== Contact Information (18 points total) ==========
    if resume_data['email'] and resume_data['email'] != 'Not Found':
        score += 7
        feedback.append(('success', 'Email address found'))
    else:
        feedback.append(('error', 'Email address missing - Critical for ATS'))
    
    if resume_data['mobile_number'] and resume_data['mobile_number'] != 'Not Found':
        score += 6
        feedback.append(('success', 'Phone number found'))
    else:
        feedback.append(('error', 'Phone number missing - Important contact info'))
    
    # Check for professional links (LinkedIn, GitHub, Portfolio)
    professional_links = ['linkedin', 'github', 'portfolio', 'gitlab', 'behance', 'medium']
    links_found = [link for link in professional_links if link in text_lower]
    
    if len(links_found) >= 2:
        score += 5
        feedback.append(('success', f'Multiple professional links found: {", ".join(links_found[:2])}'))
    elif len(links_found) == 1:
        score += 3
        feedback.append(('success', f'Professional link found: {links_found[0]}'))
    else:
        score += 1
        feedback.append(('warning', 'Consider adding LinkedIn or GitHub profile'))
    
    # ========== Professional Summary (8 points) ==========
    summary_keywords = ['summary', 'objective', 'profile', 'about me', 'professional summary']
    has_summary = any(word in text_lower for word in summary_keywords)
    
    if has_summary:
        # Check if summary is substantial
        summary_pattern = r'(?:summary|objective|profile|about me)[\s:]*([^\n]{40,})'
        summary_match = re.search(summary_pattern, text_lower, re.IGNORECASE)
        
        if summary_match:
            score += 8
            feedback.append(('success', 'Professional summary present'))
        else:
            score += 4
            feedback.append(('warning', 'Summary exists but could be more detailed'))
    else:
        score += 2
        feedback.append(('warning', 'Consider adding a professional summary'))
    
    # ========== Skills Section (22 points) - BALANCED ==========
    skill_count = len(resume_data['skills'])
    
    if skill_count >= 18:
        score += 22
        feedback.append(('success', f'Excellent skills: {skill_count} technical skills detected'))
    elif skill_count >= 12:
        score += 18
        feedback.append(('success', f'Good skills: {skill_count} skills found'))
    elif skill_count >= 8:
        score += 14
        feedback.append(('success', f'Decent skills: {skill_count} skills - add 4-6 more for better score'))
    elif skill_count >= 5:
        score += 9
        feedback.append(('warning', f'Moderate skills: {skill_count} skills - add 5-10 more relevant technical skills'))
    else:
        score += 4
        feedback.append(('error', f'Limited skills: Only {skill_count} skills - aim for at least 10+ technical skills'))
    
    # ========== Work Experience (25 points) - BALANCED ==========
    has_experience_section = any(word in text_lower for word in [
        'work experience', 'professional experience', 'employment history', 
        'work history', 'experience', 'employment'
    ])
    
    year_matches = len(re.findall(r'\b(19|20)\d{2}\b', resume_text))
    exp_years = resume_data['experience_years']
    
    if has_experience_section:
        if year_matches >= 4:  # Multiple experiences with dates
            score += 25
            feedback.append(('success', 'Detailed work experience with multiple dates'))
        elif year_matches >= 2:  # At least one experience with dates
            score += 20
            feedback.append(('success', 'Work experience with dates present'))
        else:
            score += 12
            feedback.append(('warning', 'Work experience found - add specific dates for better score'))
    else:
        if exp_years > 0:
            score += 10
            feedback.append(('warning', 'Experience mentioned - add a proper "Work Experience" section'))
        elif 'intern' in text_lower:
            score += 8
            feedback.append(('success', 'Internship experience found - good for entry-level'))
        else:
            score += 3
            feedback.append(('warning', 'Add work experience or internships - include projects if fresher'))
    
    # ========== Education (10 points) ==========
    education_keywords = [
        'education', 'degree', 'university', 'college', 'bachelor', 'master', 
        'b.tech', 'm.tech', 'b.e', 'm.e', 'b.sc', 'm.sc', 'bca', 'mca'
    ]
    has_education = any(word in text_lower for word in education_keywords)
    
    if has_education:
        # Check for graduation year
        education_pattern = r'(?:bachelor|master|b\.tech|m\.tech|b\.e|m\.e|degree).*?(\d{4})'
        education_match = re.search(education_pattern, text_lower)
        
        if education_match:
            score += 10
            feedback.append(('success', 'Education details with graduation year present'))
        else:
            score += 7
            feedback.append(('success', 'Education section present - add graduation year for completeness'))
    else:
        score += 3
        feedback.append(('warning', 'Education section missing - add your degree and institution'))
    
    # ========== Projects/Achievements (12 points) ==========
    project_keywords = ['project', 'projects', 'built', 'developed', 'created', 'implemented', 'designed']
    project_count = sum(1 for keyword in project_keywords if keyword in text_lower)
    
    if project_count >= 3:
        score += 12
        feedback.append(('success', 'Multiple projects/achievements mentioned'))
    elif project_count >= 2:
        score += 9
        feedback.append(('success', 'Projects mentioned - good!'))
    elif project_count >= 1:
        score += 5
        feedback.append(('warning', 'Limited project descriptions - add 2-3 more projects'))
    else:
        score += 2
        feedback.append(('warning', 'Add relevant projects - essential for freshers and entry-level'))
    
    # ========== Quality Feedback (Non-scoring - informational) ==========
    
    # Check for action verbs
    action_verbs = [
        'led', 'managed', 'developed', 'created', 'implemented', 'designed', 
        'built', 'increased', 'improved', 'achieved', 'delivered', 'launched',
        'optimized', 'automated'
    ]
    verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    
    if verb_count >= 6:
        feedback.append(('success', f'Good use of action verbs ({verb_count} found)'))
    elif verb_count >= 3:
        feedback.append(('success', f'Some action verbs found ({verb_count}) - add more for impact'))
    else:
        feedback.append(('warning', f'Use more action verbs (Led, Managed, Developed, etc.) - only {verb_count} found'))
    
    # Check for quantifiable achievements
    metrics_patterns = [
        r'\d+%',  # Percentages
        r'\$\d+',  # Money
        r'\d+x',  # Multiples
        r'\d+\s*(?:users|customers|clients)',  # User counts
        r'\d+\s*(?:projects|applications)',  # Project counts
    ]
    
    metrics_count = sum(1 for pattern in metrics_patterns if re.search(pattern, text_lower))
    
    if metrics_count >= 2:
        feedback.append(('success', f'Quantifiable achievements found ({metrics_count} metrics)'))
    elif metrics_count >= 1:
        feedback.append(('success', 'Some metrics found - add more to show impact'))
    else:
        feedback.append(('warning', 'Add numbers/metrics to show impact (e.g., "improved by 30%", "managed 5 projects")'))
    
    # Resume length check
    pages = resume_data['no_of_pages']
    if pages == 1:
        feedback.append(('success', 'Perfect resume length: 1 page'))
    elif pages == 2:
        feedback.append(('success', 'Good resume length: 2 pages'))
    elif pages == 3:
        feedback.append(('warning', f'{pages} pages - consider condensing to 2 pages'))
    else:
        feedback.append(('warning', f'{pages} pages - too long, aim for 1-2 pages'))
    
    # Role clarity feedback
    if job_role:
        if role_confidence >= 70:
            feedback.append(('success', f'Clear role alignment: {job_role} ({role_confidence}% confidence)'))
        elif role_confidence >= 50:
            feedback.append(('success', f'Role identified: {job_role} ({role_confidence}% confidence)'))
        elif role_confidence >= 30:
            feedback.append(('warning', f'Weak role signal: {job_role} ({role_confidence}% confidence) - strengthen role-specific skills'))
        else:
            feedback.append(('warning', f'Unclear role focus ({role_confidence}% confidence) - highlight your target role more clearly'))
    else:
        feedback.append(('warning', 'Cannot determine target role - consider highlighting your desired position'))
    
    # Cap score at 100
    return min(score, 100), feedback



# ==================== DATABASE ====================

def insert_data(name, email, score, timestamp, pages, role, level, skills, experience):
    """Insert resume data into database"""
    try:
        with get_db_connection() as connection:
            if connection:
                cursor = connection.cursor()
                query = """INSERT INTO user_data 
                          (Name, Email_ID, resume_score, Timestamp, Page_no, 
                           Predicted_Field, User_level, Actual_skills, Experience)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (name, email, score, timestamp, pages, 
                                      role, level, skills, experience))
                connection.commit()
                cursor.close()
    except Exception as e:
        st.warning(f"Could not save to database: {str(e)}")


def get_all_users():
    """Retrieve all users from database"""
    try:
        with get_db_connection() as connection:
            if connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM user_data')
                data = cursor.fetchall()
                columns = ['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 
                          'Page Count', 'Predicted Field', 'User Level', 
                          'Skills', 'Experience']
                df = pd.DataFrame(data, columns=columns)
                cursor.close()
                return df
    except Exception as e:
        st.error(f"Database error: {str(e)}")
    return None


def verify_admin(username, password):
    """Verify admin credentials"""
    # Simple hardcoded check - in production, use proper authentication
    return username == "admin" and password == "admin123"


# ==================== MAIN APP ====================

def run():
    """Main application"""
    st.set_page_config(page_title='Resume Analyzer', layout="wide")
    load_css()
    
    # Header
    st.markdown("""
        <div class='main-header'>
            <h1>📄 AI Resume Analyzer</h1>
            <p>Professional ATS Scoring & Career Analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### Choose Mode")
        choice = st.radio("", ["Resume Analysis", "Admin Dashboard"])
        
        st.markdown("---")
        st.markdown("### Supported Roles")
        for role in ROLE_SKILLS.keys():
            st.markdown(f"• {role}")
    
    # ==================== USER MODE ====================
    
    if choice == "Resume Analysis":
        
        # Upload section
        st.markdown("### Upload Resume")
        pdf_file = st.file_uploader("Choose your resume (PDF only)", type=["pdf"])
        
        if pdf_file:
            import os
            os.makedirs('./Uploaded_Resumes', exist_ok=True)
            save_path = './Uploaded_Resumes/' + pdf_file.name
            
            with open(save_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            # Two column layout
            col1, col2 = st.columns([1, 1])
            
            # LEFT: PDF Preview
            with col1:
                st.markdown("### Resume Preview")
                try:
                    with open(save_path, "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    st.markdown(f"""
                        <div class='pdf-container'>
                            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                                    width="100%" height="800px" type="application/pdf">
                            </iframe>
                        </div>
                    """, unsafe_allow_html=True)
                except:
                    st.error("Could not display PDF")
            
            # RIGHT: Analysis Results
            with col2:
                with st.spinner('Analyzing resume...'):
                    resume_data, message = parse_resume(save_path)
                
                if resume_data is None:
                    st.error(f"❌ {message}")
                else:
                    # Calculate score
                    ats_score, feedback = calculate_ats_score(
                        resume_data, resume_data['raw_text'],
                        resume_data['job_role'], resume_data['role_confidence']
                    )
                    
                    # Score Card - BALANCED THRESHOLDS
                    if ats_score >= 80:
                        verdict = "Excellent"
                        verdict_class = "verdict-excellent"
                    elif ats_score >= 65:
                        verdict = "Good"
                        verdict_class = "verdict-good"
                    elif ats_score >= 45:
                        verdict = "Fair"
                        verdict_class = "verdict-fair"
                    else:
                        verdict = "Needs Work"
                        verdict_class = "verdict-poor"
                    
                    st.markdown(f"""
                        <div class='score-card'>
                            <div class='score-number'>{ats_score}</div>
                            <div class='score-label'>ATS Score out of 100</div>
                            <div class='score-verdict {verdict_class}'>{verdict}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Basic Info Card
                    st.markdown(f"""
                        <div class='info-card'>
                            <h3>📋 Basic Information</h3>
                            <div class='info-row'>
                                <span class='info-label'>Name:</span>
                                <span class='info-value'>{resume_data['name']}</span>
                            </div>
                            <div class='info-row'>
                                <span class='info-label'>Email:</span>
                                <span class='info-value'>{resume_data['email']}</span>
                            </div>
                            <div class='info-row'>
                                <span class='info-label'>Phone:</span>
                                <span class='info-value'>{resume_data['mobile_number']}</span>
                            </div>
                            <div class='info-row'>
                                <span class='info-label'>Pages:</span>
                                <span class='info-value'>{resume_data['no_of_pages']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Experience & Role Card
                    exp_badge_class = f"badge-{resume_data['experience_level'].lower().replace(' ', '-')}"
                    
                    role_display = f"""
                        <div class='info-row'>
                            <span class='info-label'>Job Role:</span>
                            <span class='badge badge-role'>{resume_data['job_role']} ({resume_data['role_confidence']}%)</span>
                        </div>
                    """ if resume_data['job_role'] else """
                        <div class='info-row'>
                            <span class='info-label'>Job Role:</span>
                            <span class='info-value'>Not Determined</span>
                        </div>
                    """
                    
                    st.markdown(f"""
                        <div class='info-card'>
                            <h3>💼 Experience & Role</h3>
                            <div class='info-row'>
                                <span class='info-label'>Level:</span>
                                <span class='badge {exp_badge_class}'>{resume_data['experience_level']}</span>
                            </div>
                            <div class='info-row'>
                                <span class='info-label'>Experience:</span>
                                <span class='info-value'>{resume_data['experience_years']} Years</span>
                            </div>
                            {role_display}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Skills
                    if resume_data['skills_by_category']:
                        st.markdown("<div class='section-header'>🎯 Skills</div>", 
                                  unsafe_allow_html=True)
                        
                        for category, skills in resume_data['skills_by_category'].items():
                            with st.expander(f"{category} ({len(skills)} skills)"):
                                skills_html = "".join([f"<span class='skill-tag'>{s}</span>" 
                                                      for s in skills])
                                st.markdown(f"<div class='skill-container'>{skills_html}</div>", 
                                          unsafe_allow_html=True)
                    
                    # Feedback
                    st.markdown("<div class='section-header'>📝 Detailed Feedback</div>", 
                              unsafe_allow_html=True)
                    
                    for ftype, msg in feedback:
                        if ftype == 'success':
                            st.markdown(f"<div class='feedback-box feedback-success'>✅ {msg}</div>", 
                                      unsafe_allow_html=True)
                        elif ftype == 'warning':
                            st.markdown(f"<div class='feedback-box feedback-warning'>⚠️ {msg}</div>", 
                                      unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='feedback-box feedback-error'>❌ {msg}</div>", 
                                      unsafe_allow_html=True)
            
            # COURSE RECOMMENDATIONS - FULL WIDTH BELOW THE TWO COLUMNS
            if pdf_file and resume_data is not None and resume_data['job_role']:
                # PERSONALIZED COURSE RECOMMENDATIONS
                display_course_recommendations(
                    resume_data['job_role'], 
                    resume_data['experience_level']
                )
                
                # Resume and Interview Resources
                display_resume_interview_resources()
                
                # Save to DB
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
                insert_data(resume_data['name'], resume_data['email'], str(ats_score),
                          timestamp, str(resume_data['no_of_pages']),
                          resume_data['job_role'], resume_data['experience_level'],
                          str(resume_data['skills'][:30]), resume_data['experience_years'])
    
    # ==================== ADMIN MODE ====================
    
    else:
        st.markdown("### 🔐 Admin Login")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            
            if st.button('Login', use_container_width=True):
                if verify_admin(username, password):
                    st.success(f"Welcome, {username}!")
                    
                    df = get_all_users()
                    if df is not None and not df.empty:
                        st.markdown("### 📊 Dashboard")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        with m1:
                            st.metric("Total Resumes", len(df))
                        with m2:
                            avg = pd.to_numeric(df['Resume Score'], errors='coerce').mean()
                            st.metric("Avg Score", f"{avg:.1f}")
                        with m3:
                            top = df['Predicted Field'].mode()[0] if not df.empty else "N/A"
                            st.metric("Top Role", top)
                        with m4:
                            today = datetime.datetime.now().strftime('%Y-%m-%d')
                            today_count = len(df[df['Timestamp'].str.contains(today)])
                            st.metric("Today", today_count)
                        
                        st.markdown("### 📋 Records")
                        st.dataframe(df, use_container_width=True, height=400)
                        
                        csv = df.to_csv(index=False)
                        st.download_button("Download CSV", csv, "data.csv", "text/csv")
                    else:
                        st.warning("No data available")
                else:
                    st.error("Invalid credentials")


if __name__ == '__main__':
    run()