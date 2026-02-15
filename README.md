# 🚀 Portfolio Backend API

A modern, serverless FastAPI backend for a personal portfolio website, built with AWS Lambda, DynamoDB, and Cloudflare R2 storage.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python)](https://www.python.org/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900?style=flat&logo=aws-lambda)](https://aws.amazon.com/lambda/)
[![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-4053D6?style=flat&logo=amazon-dynamodb)](https://aws.amazon.com/dynamodb/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Environment Variables](#-environment-variables)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

This is a production-ready serverless backend API that powers a personal portfolio website. It provides comprehensive content management capabilities including blog posts, projects, skills, comments, and profile information. The API is designed with a clean architecture separating concerns into repositories, services, and API layers.

**Live API**: Deployed on AWS Lambda with API Gateway  
**Frontend**: Supports both public-facing portfolio and admin dashboard

---

## ✨ Features

### 🔐 Authentication & Authorization
- **Passkey-based authentication** for admin access
- **JWT token generation** and validation
- Secure middleware for protected routes
- Admin email/password authentication

### 📝 Blog Management
- Create, read, update, and delete blog posts
- Draft and published status support
- Rich content with markdown support
- Automatic timestamp tracking
- Public and admin endpoints

### 💼 Project Showcase
- Full CRUD operations for projects
- Project metadata (title, description, tech stack)
- Image upload support via Cloudflare R2
- Draft/published status
- GitHub and live demo links

### 🛠️ Skills Management
- Organize skills by categories
- Proficiency levels
- Icon/image support
- Easy CRUD operations

### 💬 Comment System
- Nested comment support for blog posts
- Moderation capabilities
- Timestamp tracking
- User information capture

### 👤 Profile Management
- Dynamic bio and about sections
- Hero and about page images
- Social media links
- Contact information
- SEO metadata

### 📤 File Upload
- Cloudflare R2 integration for image storage
- Secure file upload with validation
- Public CDN URLs
- Support for multiple image formats

### 🔧 Admin Features
- Centralized admin dashboard endpoints
- Fetch all content including drafts
- Bulk operations support
- Content moderation

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                    # API route handlers
│   │   ├── admin/             # Protected admin endpoints
│   │   │   ├── auth.py        # Authentication & JWT
│   │   │   ├── blog.py        # Blog management
│   │   │   ├── comment.py     # Comment moderation
│   │   │   ├── profile.py     # Profile management
│   │   │   ├── projects.py    # Project management
│   │   │   ├── skills.py      # Skills management
│   │   │   └── upload.py      # File upload handler
│   │   └── public/            # Public-facing endpoints
│   │       ├── blog.py        # Public blog posts
│   │       ├── comment.py     # Public comments
│   │       ├── profile.py     # Public profile data
│   │       ├── projects.py    # Public projects
│   │       └── skills.py      # Public skills
│   ├── core/                  # Core configuration
│   ├── db/                    # Database utilities
│   ├── middleware/            # Custom middleware
│   ├── repositories/          # Data access layer
│   ├── schemas/               # Pydantic models
│   ├── services/              # Business logic layer
│   └── main.py               # FastAPI application entry
├── scripts/                   # Utility scripts
├── tests/                     # Test suite
├── template.yaml             # AWS SAM template
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

### Architecture Layers

**API Layer** (`app/api/`)
- Route handlers and request/response management
- Input validation using Pydantic schemas
- Separated into admin (protected) and public endpoints

**Service Layer** (`app/services/`)
- Business logic implementation
- Orchestrates repository operations
- Handles complex workflows

**Repository Layer** (`app/repositories/`)
- Direct database interactions
- DynamoDB query abstractions
- Data persistence logic

**Schemas** (`app/schemas/`)
- Pydantic models for request/response validation
- Type safety and automatic documentation
- Data transformation

---

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for local development

### Cloud Infrastructure
- **AWS Lambda** - Serverless compute
- **AWS API Gateway** - HTTP API management
- **AWS DynamoDB** - NoSQL database
- **AWS SAM** - Serverless Application Model for deployment
- **Cloudflare R2** - Object storage for images

### Authentication & Security
- **python-jose** - JWT token handling
- **passlib** - Password hashing
- **argon2-cffi** - Secure password hashing algorithm

### Additional Libraries
- **boto3** - AWS SDK for Python
- **mangum** - AWS Lambda adapter for ASGI applications
- **python-multipart** - File upload support
- **python-dotenv** - Environment variable management

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- AWS Account with configured credentials
- AWS SAM CLI (for deployment)
- Cloudflare R2 account (for file storage)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   BLOG_TABLE=BlogsTable
   COMMENTS_TABLE=BlogCommentsTable
   SKILL_TABLE=SkillsTable
   PROJECTS_TABLE=ProjectsTable
   PROFILE_TABLE=ProfileTable
   USERS_TABLE=UsersTable
   
   PASSKEY=your_admin_passkey
   JWT_SECRET=your_jwt_secret_key
   
   R2_ACCOUNT_ID=your_r2_account_id
   R2_ACCESS_KEY_ID=your_r2_access_key
   R2_SECRET_ACCESS_KEY=your_r2_secret_key
   R2_BUCKET_NAME=your_bucket_name
   R2_PUBLIC_BASE_URL=https://your-cdn-url.com
   
   ADMIN_EMAIL=your_admin_email
   ADMIN_PASSWORD=your_admin_password
   ```

5. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

---

## 📚 API Documentation

### Public Endpoints

#### Blog
- `GET /public/blog` - Get all published blog posts
- `GET /public/blog/{blog_id}` - Get a specific blog post

#### Projects
- `GET /public/projects` - Get all published projects
- `GET /public/projects/{project_id}` - Get a specific project

#### Skills
- `GET /public/skills` - Get all skills

#### Profile
- `GET /public/bio` - Get profile/bio information

#### Comments
- `GET /public/comments/{blog_id}` - Get comments for a blog post
- `POST /public/comments` - Submit a new comment

### Admin Endpoints (Protected)

#### Authentication
- `POST /admin/login` - Admin login (returns JWT)
- `POST /admin/verify-passkey` - Verify admin passkey

#### Blog Management
- `GET /admin/blog` - Get all blogs (including drafts)
- `POST /admin/blog` - Create a new blog post
- `PUT /admin/blog/{blog_id}` - Update a blog post
- `DELETE /admin/blog/{blog_id}` - Delete a blog post

#### Project Management
- `GET /admin/projects` - Get all projects (including drafts)
- `POST /admin/projects` - Create a new project
- `PUT /admin/projects/{project_id}` - Update a project
- `DELETE /admin/projects/{project_id}` - Delete a project

#### Skills Management
- `GET /admin/skills` - Get all skills
- `POST /admin/skills` - Create a new skill
- `PUT /admin/skills/{skill_id}` - Update a skill
- `DELETE /admin/skills/{skill_id}` - Delete a skill

#### Profile Management
- `PUT /admin/bio` - Update profile/bio information
- `PUT /admin/admin-settings` - Update admin settings

#### Comment Moderation
- `DELETE /admin/comments/{comment_id}` - Delete a comment

#### File Upload
- `POST /admin/upload` - Upload an image to R2 storage

---

## 🚢 Deployment

This project uses AWS SAM for serverless deployment.

### Deploy to AWS

1. **Build the application**
   ```bash
   sam build
   ```

2. **Deploy to AWS**
   ```bash
   sam deploy --guided
   ```

3. **Follow the prompts** to configure:
   - Stack name
   - AWS Region
   - Parameter values (table names, etc.)
   - Confirm changes before deploy

### Update Existing Deployment

```bash
sam build && sam deploy
```

### Environment Configuration

The `template.yaml` file contains all AWS infrastructure as code, including:
- Lambda function configuration
- API Gateway setup
- DynamoDB table references
- IAM permissions
- Environment variables

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BLOG_TABLE` | DynamoDB table name for blogs | Yes |
| `COMMENTS_TABLE` | DynamoDB table name for comments | Yes |
| `SKILL_TABLE` | DynamoDB table name for skills | Yes |
| `PROJECTS_TABLE` | DynamoDB table name for projects | Yes |
| `PROFILE_TABLE` | DynamoDB table name for profile | Yes |
| `USERS_TABLE` | DynamoDB table name for users | Yes |
| `PASSKEY` | Admin passkey for authentication | Yes |
| `JWT_SECRET` | Secret key for JWT token generation | Yes |
| `R2_ACCOUNT_ID` | Cloudflare R2 account ID | Yes |
| `R2_ACCESS_KEY_ID` | Cloudflare R2 access key | Yes |
| `R2_SECRET_ACCESS_KEY` | Cloudflare R2 secret key | Yes |
| `R2_BUCKET_NAME` | R2 bucket name for file storage | Yes |
| `R2_PUBLIC_BASE_URL` | Public CDN URL for uploaded files | Yes |
| `ADMIN_EMAIL` | Admin email for authentication | Yes |
| `ADMIN_PASSWORD` | Admin password for authentication | Yes |

---

## 🎨 CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (Development - Frontend)
- `http://localhost:5174` (Development - Admin)
- `https://kanbs.me` (Production - Frontend)
- `https://www.kanbs.me` (Production - Frontend)
- `https://admin.kanbs.me` (Production - Admin)
- `https://www.admin.kanbs.me` (Production - Admin)

---

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Test DynamoDB connection:

```bash
curl http://localhost:8000/test-dynamodb
```

---

## 📝 License

This project is open source and available for personal and educational use.

---

## 🙏 Acknowledgments

### Special Thanks

**Created by**: [Kartik Nagare](https://kanbs.me)  
**GitHub**: [@kartik3165](https://github.com/kartik3165)  
**Email**: kartiknagare3165@gmail.com

### Technologies & Inspirations

- **FastAPI Team** - For creating an amazing Python web framework
- **AWS** - For providing robust serverless infrastructure
- **Cloudflare** - For R2 object storage solution
- **Python Community** - For excellent libraries and tools

---

## 🤝 Contributing

While this is a personal portfolio project, suggestions and feedback are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your thoughts and ideas

---

## 📞 Contact

For questions, collaborations, or just to say hi:

- **Website**: [https://kanbs.me](https://kanbs.me)
- **Email**: kartiknagare3165@gmail.com
- **GitHub**: [@kartik3165](https://github.com/kartik3165)

---

<div align="center">

**Built with ❤️ by Kartik Nagare**

⭐ Star this repo if you find it helpful!

</div>
