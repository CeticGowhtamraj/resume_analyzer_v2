"""
Comprehensive Course Recommendations - 2024/2025
Organized by role, skill level, and current market demands
"""

# ==================== DATA SCIENCE ROLES ====================

# Data Scientist Courses (Machine Learning, AI, Statistics)
data_scientist_courses = {
    'Beginner': [
        ['Machine Learning Crash Course by Google [Free]', 'https://developers.google.com/machine-learning/crash-course'],
        ['Python for Data Science - freeCodeCamp [Free]', 'https://youtu.be/LHBE6Q9XlzI'],
        ['Statistics for Data Science [Free]', 'https://youtu.be/xxpc-HPKN28'],
        ['Data Science Foundations by IBM [Free]', 'https://www.coursera.org/professional-certificates/ibm-data-science'],
        ['Introduction to Machine Learning - Udacity [Free]', 'https://www.udacity.com/course/intro-to-machine-learning--ud120'],
    ],
    'Intermediate': [
        ['Machine Learning A-Z by Udemy', 'https://www.udemy.com/course/machinelearning/'],
        ['Machine Learning Specialization by Andrew NG', 'https://www.coursera.org/specializations/machine-learning-introduction'],
        ['Deep Learning Specialization by DeepLearning.AI', 'https://www.coursera.org/specializations/deep-learning'],
        ['Applied Data Science with Python', 'https://www.coursera.org/specializations/data-science-python'],
        ['TensorFlow Developer Certificate', 'https://www.tensorflow.org/certificate'],
    ],
    'Advanced': [
        ['Advanced Machine Learning Specialization', 'https://www.coursera.org/specializations/aml'],
        ['MLOps Specialization by DeepLearning.AI', 'https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops'],
        ['Natural Language Processing Specialization', 'https://www.coursera.org/specializations/natural-language-processing'],
        ['Computer Vision by Stanford [Free]', 'https://youtu.be/dJYGatp4SvA'],
        ['Reinforcement Learning Specialization', 'https://www.coursera.org/specializations/reinforcement-learning'],
    ]
}

# Data Analyst Courses (SQL, Excel, BI Tools)
data_analyst_courses = {
    'Beginner': [
        ['SQL for Data Analysis - freeCodeCamp [Free]', 'https://youtu.be/HXV3zeQKqGY'],
        ['Excel Skills for Data Analytics', 'https://www.coursera.org/specializations/excel'],
        ['Google Data Analytics Certificate [Free Trial]', 'https://www.coursera.org/professional-certificates/google-data-analytics'],
        ['Tableau for Beginners [Free]', 'https://youtu.be/6xv1KvCMF1Q'],
        ['Power BI for Beginners [Free]', 'https://youtu.be/NNSHu0rkew8'],
    ],
    'Intermediate': [
        ['SQL - MySQL for Data Analytics and BI', 'https://www.udemy.com/course/sql-mysql-for-data-analytics-and-business-intelligence/'],
        ['Data Analysis with Python', 'https://www.freecodecamp.org/learn/data-analysis-with-python/'],
        ['Tableau Desktop Specialist Certification', 'https://www.tableau.com/learn/certification/desktop-specialist'],
        ['Microsoft Power BI Data Analyst', 'https://learn.microsoft.com/en-us/certifications/power-bi-data-analyst-associate/'],
        ['Statistics for Business Analytics', 'https://www.coursera.org/specializations/statistics-for-data-science'],
    ],
    'Advanced': [
        ['Advanced SQL for Data Scientists', 'https://www.linkedin.com/learning/advanced-sql-for-data-scientists'],
        ['Python for Data Visualization', 'https://www.udacity.com/course/data-visualization-in-python--ud1206'],
        ['Business Intelligence Analyst Specialization', 'https://www.coursera.org/specializations/bi-analyst'],
        ['Advanced Tableau - Dashboard Design', 'https://www.udemy.com/course/tableau-advanced/'],
        ['Data Analytics with R Programming', 'https://www.coursera.org/learn/data-analysis-r'],
    ]
}

# Data Engineer Courses (ETL, Big Data, Cloud)
data_engineer_courses = {
    'Beginner': [
        ['Data Engineering Basics [Free]', 'https://youtu.be/qWru-b6m030'],
        ['SQL for Data Engineering [Free]', 'https://youtu.be/7mz73uXD9DA'],
        ['Introduction to Apache Spark [Free]', 'https://youtu.be/zC9cnh8rJd0'],
        ['AWS Certified Cloud Practitioner [Free Resources]', 'https://aws.amazon.com/certification/certified-cloud-practitioner/'],
        ['Python for Data Engineering [Free]', 'https://youtu.be/WGJJIrtnfpk'],
    ],
    'Intermediate': [
        ['Data Engineering on Google Cloud Platform', 'https://www.coursera.org/professional-certificates/gcp-data-engineering'],
        ['Apache Spark and Python for Big Data', 'https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/'],
        ['Data Pipelines with Apache Airflow', 'https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/'],
        ['AWS Certified Data Engineer', 'https://aws.amazon.com/certification/certified-data-engineer-associate/'],
        ['Kafka for Data Engineers', 'https://www.udemy.com/course/apache-kafka/'],
    ],
    'Advanced': [
        ['Advanced Data Engineering on AWS', 'https://www.coursera.org/learn/data-engineering-aws'],
        ['Databricks Lakehouse Platform', 'https://www.databricks.com/learn/training'],
        ['Snowflake Data Warehouse Complete Guide', 'https://www.udemy.com/course/snowflake-masterclass/'],
        ['Real-time Data Processing with Apache Flink', 'https://www.udemy.com/course/apache-flink/'],
        ['Data Engineering with dbt', 'https://courses.getdbt.com/collections'],
    ]
}

# ==================== SOFTWARE DEVELOPMENT ROLES ====================

# Software Engineer / SDE Courses
software_engineer_courses = {
    'Beginner': [
        ['CS50 - Introduction to Computer Science [Free]', 'https://cs50.harvard.edu/x/'],
        ['Python Programming for Beginners [Free]', 'https://youtu.be/rfscVS0vtbw'],
        ['Java Programming Masterclass', 'https://www.udemy.com/course/java-the-complete-java-developer-course/'],
        ['Data Structures and Algorithms [Free]', 'https://youtu.be/8hly31xKli0'],
        ['Git and GitHub for Beginners [Free]', 'https://youtu.be/RGOj5yH7evk'],
    ],
    'Intermediate': [
        ['Complete Data Structures & Algorithms', 'https://www.udemy.com/course/datastructurescncpp/'],
        ['System Design for Interviews', 'https://www.educative.io/courses/grokking-the-system-design-interview'],
        ['Design Patterns in Java/Python', 'https://refactoring.guru/design-patterns'],
        ['Microservices Architecture', 'https://www.udemy.com/course/microservices-architecture/'],
        ['Docker and Kubernetes Complete Guide', 'https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/'],
    ],
    'Advanced': [
        ['Advanced System Design', 'https://www.educative.io/courses/grokking-adv-system-design-intvw'],
        ['Distributed Systems MIT Course [Free]', 'https://pdos.csail.mit.edu/6.824/'],
        ['Cloud Architecture Patterns', 'https://www.udemy.com/course/aws-solutions-architect-associate-practice-tests/'],
        ['High Performance Computing', 'https://www.coursera.org/learn/cloud-computing'],
        ['Software Architecture Patterns', 'https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/'],
    ]
}

# SDE-1 Specific (Entry Level Focus)
sde1_courses = {
    'Essential': [
        ['Cracking Coding Interview Prep [Free]', 'https://youtu.be/KdZ4HF1SrFs'],
        ['LeetCode Patterns - 14 Patterns [Free]', 'https://youtu.be/xo7XrRVxH8Y'],
        ['Object-Oriented Programming [Free]', 'https://youtu.be/m_MQYyJpIjg'],
        ['Clean Code Principles [Free]', 'https://youtu.be/7EmboKQH8lM'],
        ['REST API Design Best Practices [Free]', 'https://youtu.be/0oXYLzuucwE'],
    ],
    'Practice': [
        ['100 Days of Code - Python', 'https://www.udemy.com/course/100-days-of-code/'],
        ['JavaScript Algorithms and Data Structures', 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/'],
        ['Interview Prep Course', 'https://www.educative.io/courses/grokking-coding-interview'],
        ['System Design Primer [Free]', 'https://github.com/donnemartin/system-design-primer'],
        ['Daily Coding Problem', 'https://www.dailycodingproblem.com/'],
    ]
}

# SDE-2 Specific (Mid-Senior Focus)
sde2_courses = {
    'Essential': [
        ['System Design Interview Guide', 'https://www.educative.io/courses/grokking-the-system-design-interview'],
        ['Scalable Web Architecture', 'https://www.udemy.com/course/developer-to-architect/'],
        ['Leadership Principles for Engineers', 'https://www.linkedin.com/learning/engineering-leadership'],
        ['Code Review Best Practices', 'https://google.github.io/eng-practices/review/'],
        ['Technical Writing for Engineers', 'https://developers.google.com/tech-writing'],
    ],
    'Advanced': [
        ['Building Scalable Microservices', 'https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud/'],
        ['Database Performance Optimization', 'https://www.udemy.com/course/database-performance-optimization/'],
        ['Cloud Native Architecture', 'https://www.coursera.org/specializations/cloud-native-app-development'],
        ['DevOps and SRE Practices', 'https://www.coursera.org/professional-certificates/sre-devops-engineer-google-cloud'],
        ['Engineering Management Fundamentals', 'https://www.linkedin.com/learning/paths/become-an-engineering-manager'],
    ]
}

# ==================== WEB DEVELOPMENT ====================

# Full Stack Web Developer
web_developer_courses = {
    'Beginner': [
        ['HTML & CSS Full Course [Free]', 'https://youtu.be/G3e-cpL7ofc'],
        ['JavaScript Full Course [Free]', 'https://youtu.be/PkZNo7MFNFg'],
        ['Web Development Bootcamp', 'https://www.udemy.com/course/the-complete-web-development-bootcamp/'],
        ['Responsive Web Design [Free]', 'https://www.freecodecamp.org/learn/2022/responsive-web-design/'],
        ['Git and GitHub Crash Course [Free]', 'https://youtu.be/RGOj5yH7evk'],
    ],
    'Intermediate': [
        ['React - The Complete Guide', 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/'],
        ['Node.js - Complete Developer Course', 'https://www.udemy.com/course/the-complete-nodejs-developer-course-2/'],
        ['Full Stack Open - Modern Web Development [Free]', 'https://fullstackopen.com/en/'],
        ['Next.js 14 Complete Course [Free]', 'https://youtu.be/wm5gMKuwSYk'],
        ['TypeScript Complete Course', 'https://www.udemy.com/course/understanding-typescript/'],
    ],
    'Advanced': [
        ['Advanced React Patterns', 'https://www.udemy.com/course/react-design-patterns/'],
        ['GraphQL Complete Guide', 'https://www.udemy.com/course/graphql-bootcamp/'],
        ['AWS for Full Stack Developers', 'https://www.udemy.com/course/aws-serverless-a-complete-introduction/'],
        ['Web Performance Optimization', 'https://web.dev/learn/'],
        ['Progressive Web Apps (PWA)', 'https://www.udemy.com/course/progressive-web-app-pwa-the-complete-guide/'],
    ]
}

# Frontend Frameworks
frontend_courses = {
    'React': [
        ['React Full Course 2024 [Free]', 'https://youtu.be/CgkZ7MvWUAA'],
        ['React with TypeScript', 'https://www.udemy.com/course/react-and-typescript-build-a-portfolio-project/'],
        ['Redux Toolkit Complete Guide', 'https://redux-toolkit.js.org/tutorials/overview'],
        ['React Testing Library [Free]', 'https://testing-library.com/docs/react-testing-library/intro/'],
    ],
    'Angular': [
        ['Angular Complete Course [Free]', 'https://youtu.be/3qBXWUpoPHo'],
        ['Angular - The Complete Guide', 'https://www.udemy.com/course/the-complete-guide-to-angular-2/'],
        ['Angular Testing Masterclass', 'https://www.udemy.com/course/angular-testing-course/'],
    ],
    'Vue': [
        ['Vue.js 3 Complete Course [Free]', 'https://youtu.be/YrxBCBibVo0'],
        ['Vue - The Complete Guide', 'https://www.udemy.com/course/vuejs-2-the-complete-guide/'],
        ['Nuxt.js for Vue Developers', 'https://masteringnuxt.com/'],
    ]
}

# Backend Frameworks
backend_courses = {
    'Node.js': [
        ['Node.js Full Course [Free]', 'https://youtu.be/Oe421EPjeBE'],
        ['Express.js Complete Guide', 'https://www.udemy.com/course/nodejs-express-mongodb-bootcamp/'],
        ['NestJS Complete Developer Guide', 'https://www.udemy.com/course/nestjs-zero-to-hero/'],
    ],
    'Python': [
        ['Django Full Course [Free]', 'https://youtu.be/F5mRW0jo-U4'],
        ['FastAPI Complete Course', 'https://www.udemy.com/course/completefastapi/'],
        ['Flask Web Development', 'https://www.udemy.com/course/rest-api-flask-and-python/'],
    ],
    'Java': [
        ['Spring Boot Complete Guide', 'https://www.udemy.com/course/spring-hibernate-tutorial/'],
        ['Microservices with Spring Boot', 'https://www.udemy.com/course/microservices-with-spring-boot-and-spring-cloud/'],
    ]
}

# ==================== MOBILE DEVELOPMENT ====================

# Android Developer
android_courses = {
    'Beginner': [
        ['Android Development for Beginners [Free]', 'https://youtu.be/fis26HvvDII'],
        ['Kotlin Programming Full Course [Free]', 'https://youtu.be/EExSSotojVI'],
        ['Android Basics with Compose [Free]', 'https://developer.android.com/courses/android-basics-compose/course'],
        ['Android Studio Tutorial [Free]', 'https://youtu.be/fwY4YmRQMnE'],
    ],
    'Intermediate': [
        ['The Complete Android 14 Developer Course', 'https://www.udemy.com/course/complete-android-n-developer-course/'],
        ['Jetpack Compose Complete Guide', 'https://www.udemy.com/course/kotling-android-jetpack-compose-/'],
        ['Android Architecture Components', 'https://www.udemy.com/course/android-architecture/'],
        ['Firebase for Android Development', 'https://www.udemy.com/course/firebase-course-android/'],
    ],
    'Advanced': [
        ['Advanced Android Development', 'https://www.udacity.com/course/advanced-android-app-development--ud855'],
        ['Android Testing Complete Guide', 'https://www.udemy.com/course/android-testing/'],
        ['Kotlin Coroutines and Flow', 'https://www.udemy.com/course/kotlin-coroutines/'],
        ['Associate Android Developer Certification', 'https://developers.google.com/certification/associate-android-developer'],
    ]
}

# iOS Developer
ios_courses = {
    'Beginner': [
        ['iOS Development for Beginners [Free]', 'https://youtu.be/09TeUXjzpKs'],
        ['Swift Programming Tutorial [Free]', 'https://youtu.be/comQ1-x2a1Q'],
        ['SwiftUI Basics [Free]', 'https://developer.apple.com/tutorials/swiftui'],
        ['Xcode for Beginners [Free]', 'https://youtu.be/uRHdlR_eQ3k'],
    ],
    'Intermediate': [
        ['iOS 17 & Swift 5.9 Complete Bootcamp', 'https://www.udemy.com/course/ios-13-app-development-bootcamp/'],
        ['SwiftUI Masterclass', 'https://www.udemy.com/course/swiftui-masterclass-course-ios-development-with-swift/'],
        ['Combine Framework Complete Guide', 'https://www.udemy.com/course/combine-framework/'],
        ['Core Data in SwiftUI', 'https://www.udemy.com/course/swiftui-coredata/'],
    ],
    'Advanced': [
        ['Advanced iOS Development', 'https://www.udacity.com/course/ios-developer-nanodegree--nd003'],
        ['iOS Design Patterns', 'https://www.udemy.com/course/ios-design-patterns/'],
        ['App Architecture and Clean Code', 'https://www.udemy.com/course/solid-principles-in-swift/'],
        ['App Store Optimization', 'https://www.udemy.com/course/app-marketing/'],
    ]
}

# Cross-Platform Mobile
cross_platform_courses = {
    'Flutter': [
        ['Flutter Complete Course [Free]', 'https://youtu.be/VPvVD8t02U8'],
        ['Flutter & Dart - Complete Guide', 'https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/'],
        ['Flutter State Management', 'https://www.udemy.com/course/flutter-bloc/'],
        ['Flutter Firebase Course', 'https://www.udemy.com/course/flutter-firebase-course/'],
    ],
    'React Native': [
        ['React Native Complete Course [Free]', 'https://youtu.be/0-S5a0eXPoc'],
        ['React Native - The Practical Guide', 'https://www.udemy.com/course/react-native-the-practical-guide/'],
        ['React Native Navigation', 'https://www.udemy.com/course/react-native-navigation/'],
    ]
}

# ==================== UI/UX DESIGN ====================

uiux_courses = {
    'Beginner': [
        ['UI/UX Design Tutorial [Free]', 'https://youtu.be/c9Wg6Cb_YlU'],
        ['Google UX Design Certificate', 'https://www.coursera.org/professional-certificates/google-ux-design'],
        ['Figma UI Design Tutorial [Free]', 'https://youtu.be/FTFaQWZBqQ8'],
        ['Design Principles [Free]', 'https://youtu.be/a5KYlHNKQB8'],
        ['Color Theory for Designers [Free]', 'https://youtu.be/_2LLXnUdUIc'],
    ],
    'Intermediate': [
        ['UI/UX Design Specialization', 'https://www.coursera.org/specializations/ui-ux-design'],
        ['User Experience Design Fundamentals', 'https://www.udemy.com/course/user-experience-design-fundamentals/'],
        ['Advanced Figma for Designers', 'https://www.udemy.com/course/advanced-figma/'],
        ['Design System Creation', 'https://www.udemy.com/course/design-system/'],
        ['Wireframing and Prototyping', 'https://www.udemy.com/course/wireframing/'],
    ],
    'Advanced': [
        ['UX Strategy Fundamentals', 'https://www.linkedin.com/learning/ux-strategy'],
        ['User Research Methods', 'https://www.coursera.org/learn/user-research'],
        ['Interaction Design Specialization', 'https://www.coursera.org/specializations/interaction-design'],
        ['Accessibility for Designers', 'https://www.udemy.com/course/web-accessibility/'],
        ['Design Leadership', 'https://www.linkedin.com/learning/design-leadership'],
    ]
}

# Design Tools Specific
design_tools_courses = {
    'Figma': [
        ['Figma Complete Course [Free]', 'https://youtu.be/FTFaQWZBqQ8'],
        ['Figma UI/UX Design Essentials', 'https://www.udemy.com/course/figma-ux-ui-design/'],
        ['Figma Prototyping and Animation', 'https://www.udemy.com/course/figma-prototyping/'],
    ],
    'Adobe XD': [
        ['Adobe XD Complete Tutorial [Free]', 'https://youtu.be/68w2VwalD5w'],
        ['Adobe XD UI/UX Design', 'https://www.udemy.com/course/adobe-xd-course/'],
    ],
    'Sketch': [
        ['Sketch for Beginners', 'https://www.udemy.com/course/sketch-design/'],
        ['Advanced Sketch Techniques', 'https://www.udemy.com/course/sketch-advanced/'],
    ]
}

# ==================== BUSINESS INTELLIGENCE ====================

bi_analyst_courses = {
    'Beginner': [
        ['Business Intelligence Basics [Free]', 'https://youtu.be/yZvFH7B6gKI'],
        ['SQL for BI [Free]', 'https://youtu.be/HXV3zeQKqGY'],
        ['Excel for Business Intelligence', 'https://www.coursera.org/specializations/excel'],
        ['Introduction to Tableau [Free]', 'https://youtu.be/6xv1KvCMF1Q'],
    ],
    'Intermediate': [
        ['Tableau Desktop Specialist', 'https://www.udemy.com/course/tableau-desktop-specialist/'],
        ['Microsoft Power BI Complete Course', 'https://www.udemy.com/course/powerbi-complete-introduction/'],
        ['Business Analytics with Excel', 'https://www.udemy.com/course/business-analytics-and-data-visualization/'],
        ['DAX for Power BI', 'https://www.udemy.com/course/dax-powerbi/'],
    ],
    'Advanced': [
        ['Advanced Tableau for BI', 'https://www.udemy.com/course/tableau-advanced/'],
        ['Power BI Data Modeling', 'https://www.udemy.com/course/power-bi-data-modeling/'],
        ['Business Intelligence Analyst Specialization', 'https://www.coursera.org/specializations/bi-analyst'],
        ['Qlik Sense for BI', 'https://www.udemy.com/course/qlik-sense/'],
    ]
}

# ==================== CLOUD & DEVOPS ====================

cloud_devops_courses = {
    'AWS': [
        ['AWS Certified Cloud Practitioner [Free]', 'https://youtu.be/SOTamWNgDKc'],
        ['AWS Solutions Architect Associate', 'https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/'],
        ['AWS DevOps Engineer Professional', 'https://www.udemy.com/course/aws-certified-devops-engineer-professional/'],
    ],
    'Azure': [
        ['Azure Fundamentals [Free]', 'https://youtu.be/NKEFWyqJ5XA'],
        ['Azure Administrator Certification', 'https://www.udemy.com/course/microsoft-azure-administrator-az-104/'],
        ['Azure DevOps Complete Guide', 'https://www.udemy.com/course/azure-devops-course/'],
    ],
    'Google Cloud': [
        ['GCP Complete Course [Free]', 'https://youtu.be/IUU6OR8yHCc'],
        ['Google Cloud Engineer Certification', 'https://www.coursera.org/professional-certificates/cloud-engineering-gcp'],
        ['GCP for DevOps', 'https://www.udemy.com/course/google-cloud-platform-gcp/'],
    ],
    'DevOps Tools': [
        ['Docker Complete Course [Free]', 'https://youtu.be/fqMOX6JJhGo'],
        ['Kubernetes Complete Guide', 'https://www.udemy.com/course/learn-kubernetes/'],
        ['Jenkins CI/CD Pipeline', 'https://www.udemy.com/course/jenkins-from-zero-to-hero/'],
        ['Terraform Infrastructure as Code', 'https://www.udemy.com/course/terraform-beginner-to-advanced/'],
    ]
}

# ==================== SOFT SKILLS & INTERVIEW PREP ====================

# Resume Building Resources
resume_resources = {
    'Resume Writing': [
        ['How to Write a Resume in 2024 [Free]', 'https://youtu.be/Tt08KmFfIYQ'],
        ['Resume Tips from Google Recruiter [Free]', 'https://youtu.be/BYUy1yvjHxE'],
        ['ATS-Friendly Resume Guide [Free]', 'https://youtu.be/qJXT_5lw5rQ'],
        ['Resume Projects That Impress [Free]', 'https://youtu.be/oC483DTjRXU'],
        ['Tech Resume Masterclass [Free]', 'https://youtu.be/y8YH0Qbu5h4'],
    ],
    'LinkedIn Optimization': [
        ['LinkedIn Profile Optimization [Free]', 'https://youtu.be/KWGhGU9T_3g'],
        ['LinkedIn for Job Search [Free]', 'https://youtu.be/bx6HTxpm8qE'],
        ['LinkedIn Networking Tips [Free]', 'https://youtu.be/QoxvdJ3KmVo'],
    ]
}

# Interview Preparation
interview_resources = {
    'General Interview': [
        ['Interview Tips from Ex-Google Recruiter [Free]', 'https://youtu.be/BjSoJIWnx5o'],
        ['Tell Me About Yourself [Free]', 'https://youtu.be/kayOhGRcNt4'],
        ['STAR Method Interview [Free]', 'https://youtu.be/VKu6O7Bk_Uk'],
        ['Salary Negotiation Tips [Free]', 'https://youtu.be/u9BoG1n1948'],
    ],
    'Technical Interview': [
        ['System Design Interview [Free]', 'https://youtu.be/bUHFg8CZFws'],
        ['Coding Interview Patterns [Free]', 'https://youtu.be/xo7XrRVxH8Y'],
        ['Behavioral Interview Questions [Free]', 'https://youtu.be/bx6HTxpm8qE'],
        ['Mock Interview Practice [Free]', 'https://www.pramp.com/'],
    ],
    'Role Specific': [
        ['Data Science Interview Prep [Free]', 'https://youtu.be/fqMkAF1R8VM'],
        ['Software Engineer Interview [Free]', 'https://youtu.be/DVx8L7F-YKU'],
        ['Frontend Developer Interview [Free]', 'https://youtu.be/h3bClP9rOvw'],
        ['Product Manager Interview [Free]', 'https://youtu.be/fmvXpwZgTRE'],
    ]
}

# Soft Skills Development
soft_skills_courses = {
    'Communication': [
        ['Effective Communication Skills', 'https://www.coursera.org/learn/wharton-communication-skills'],
        ['Technical Writing for Engineers', 'https://developers.google.com/tech-writing'],
        ['Presentation Skills Masterclass', 'https://www.udemy.com/course/presentation-skills-training/'],
    ],
    'Leadership': [
        ['Leadership Principles [Free]', 'https://youtu.be/hpRytrAk5e0'],
        ['Team Management Essentials', 'https://www.linkedin.com/learning/managing-a-team'],
        ['Project Management Fundamentals', 'https://www.coursera.org/learn/project-management-fundamentals'],
    ],
    'Problem Solving': [
        ['Critical Thinking Skills', 'https://www.coursera.org/learn/critical-thinking-skills'],
        ['Creative Problem Solving', 'https://www.linkedin.com/learning/creative-problem-solving'],
        ['Decision Making Frameworks', 'https://www.udemy.com/course/decision-making/'],
    ]
}

# ==================== PRACTICE PLATFORMS ====================

practice_platforms = {
    'Coding Practice': [
        ['LeetCode', 'https://leetcode.com/'],
        ['HackerRank', 'https://www.hackerrank.com/'],
        ['CodeSignal', 'https://codesignal.com/'],
        ['Codewars', 'https://www.codewars.com/'],
        ['InterviewBit', 'https://www.interviewbit.com/'],
    ],
    'System Design': [
        ['System Design Primer [Free]', 'https://github.com/donnemartin/system-design-primer'],
        ['Educative - System Design', 'https://www.educative.io/courses/grokking-the-system-design-interview'],
        ['ByteByteGo', 'https://bytebytego.com/'],
    ],
    'Project Ideas': [
        ['Build Your Own X [Free]', 'https://github.com/codecrafters-io/build-your-own-x'],
        ['Project Ideas by Role [Free]', 'https://github.com/practical-tutorials/project-based-learning'],
        ['App Ideas Collection [Free]', 'https://github.com/florinpop17/app-ideas'],
    ]
}

# ==================== CERTIFICATION PATHS ====================

certifications = {
    'Cloud': [
        ['AWS Solutions Architect', 'https://aws.amazon.com/certification/certified-solutions-architect-associate/'],
        ['Azure Administrator', 'https://learn.microsoft.com/en-us/certifications/azure-administrator/'],
        ['Google Cloud Engineer', 'https://cloud.google.com/certification/cloud-engineer'],
    ],
    'Security': [
        ['CompTIA Security+', 'https://www.comptia.org/certifications/security'],
        ['Certified Ethical Hacker (CEH)', 'https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/'],
        ['CISSP', 'https://www.isc2.org/Certifications/CISSP'],
    ],
    'Data': [
        ['TensorFlow Developer Certificate', 'https://www.tensorflow.org/certificate'],
        ['Microsoft Certified: Data Analyst', 'https://learn.microsoft.com/en-us/certifications/data-analyst-associate/'],
        ['Tableau Desktop Specialist', 'https://www.tableau.com/learn/certification/desktop-specialist'],
    ]
}

# ==================== LEGACY COMPATIBILITY ====================
# Keep these for backward compatibility with existing code

ds_course = data_scientist_courses['Intermediate']
web_course = web_developer_courses['Intermediate']
android_course = android_courses['Intermediate']
ios_course = ios_courses['Intermediate']
uiux_course = uiux_courses['Intermediate']

# Updated video lists with 2024 content
resume_videos = [
    'https://youtu.be/Tt08KmFfIYQ',  # Resume 2024
    'https://youtu.be/BYUy1yvjHxE',  # Google Recruiter Tips
    'https://youtu.be/qJXT_5lw5rQ',  # ATS Resume
    'https://youtu.be/oC483DTjRXU',  # Projects
    'https://youtu.be/y8YH0Qbu5h4',  # Tech Resume
    'https://youtu.be/KWGhGU9T_3g',  # LinkedIn
]

interview_videos = [
    'https://youtu.be/BjSoJIWnx5o',  # Interview Tips
    'https://youtu.be/kayOhGRcNt4',  # Tell Me About Yourself
    'https://youtu.be/VKu6O7Bk_Uk',  # STAR Method
    'https://youtu.be/bUHFg8CZFws',  # System Design
    'https://youtu.be/xo7XrRVxH8Y',  # Coding Patterns
    'https://youtu.be/u9BoG1n1948',  # Salary Negotiation
]