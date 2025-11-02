# 🍬 Sweet Shop Management System

A full-stack Sweet Shop Management System built with **FastAPI (Python)**, **PostgreSQL**, and **React (TypeScript)**, following **Test-Driven Development (TDD)** principles and modern software engineering best practices.

> **Live Demo**: [Frontend](https://sweet-shop-management-system-snowy.vercel.app) | [Backend API](https://sweetshopmanagement.up.railway.app)

## 🎯 Project Overview

This project is a comprehensive management system for a sweet shop that allows:

### Core Functionality
- ✅ **User Registration & Authentication** - Secure JWT-based authentication with role-based access control (User/Admin)
- ✅ **Sweet Inventory Management** - Add, view, edit, delete, and search sweets with real-time updates
- ✅ **Purchase System** - Users can purchase sweets with quantity validation and stock management
- ✅ **Admin Features** - Complete CRUD operations for managing inventory and restocking items
- ✅ **Purchase History** - Track all purchases with detailed records for users and admins
- ✅ **Forgot Password** - Secure password reset flow with email verification tokens

### Key Features
- 🔐 **Token-based Authentication** - JWT tokens with role-based authorization
- 🔍 **Advanced Search & Filtering** - Search by name, filter by category and price range
- 🛡️ **Security** - Password hashing (bcrypt), input validation, SQL injection prevention
- 📱 **Responsive Design** - Professional UI with modern gradients and smooth animations
- 🇮🇳 **Localization** - Currency displayed in Indian Rupees (₹)
- 📊 **Purchase Analytics** - Admin dashboard with purchase history and revenue tracking

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest with test coverage

### Frontend
- **Framework**: React with TypeScript
- **Routing**: React Router
- **HTTP Client**: Axios
- **State Management**: React Context API

## 📋 Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- npm or yarn

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Sweet Shop Management System"
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
createdb sweet_shop_db

# Create .env file
cp .env.example .env
# Edit .env with your database credentials:
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/sweet_shop_db
# SECRET_KEY=your-secret-key-here

# Initialize database tables
python -m app.main
# Press Ctrl+C to stop, tables are created

# Run the server
uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will run on `http://localhost:3000`

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
pytest --cov=app --cov-report=html
```

View coverage report in `backend/htmlcov/index.html`

### Frontend Tests

```bash
cd frontend
npm test
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```

- `POST /api/auth/login` - Login (form-data: username, password)
  - Returns: `{ "access_token": "...", "token_type": "bearer", "user": {...} }`

- `GET /api/auth/me` - Get current user info (Protected)

### Sweets (Protected - requires Bearer token)
- `GET /api/sweets` - Get all sweets
- `GET /api/sweets/search?name=chocolate&category=Chocolate&min_price=5&max_price=20` - Search sweets
- `POST /api/sweets` - Create new sweet (Admin only)
  ```json
  {
    "name": "Chocolate Bar",
    "category": "Chocolate",
    "price": 5.99,
    "quantity": 50
  }
  ```
- `PUT /api/sweets/{id}` - Update sweet (Admin only)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin only)

### Inventory (Protected)
- `POST /api/sweets/{id}/purchase` - Purchase sweet
  ```json
  { "quantity": 2 }
  ```
- `POST /api/sweets/{id}/restock` - Restock sweet (Admin only)
  ```json
  { "quantity": 20 }
  ```

## 🎨 Features

### User Features
- ✅ User registration and login
- ✅ View all available sweets
- ✅ Search sweets by name, category, and price range
- ✅ Purchase sweets (decreases quantity)
- ✅ Disabled purchase button when out of stock

### Admin Features
- ✅ Add new sweets
- ✅ Edit existing sweets
- ✅ Delete sweets
- ✅ Restock sweets (increase quantity)

## 🧪 Test-Driven Development

This project follows TDD principles:
1. **Red**: Write failing tests first
2. **Green**: Implement minimum code to pass tests
3. **Refactor**: Improve code while keeping tests passing

### Test Coverage

Backend test coverage includes:
- ✅ User registration (success and duplicate cases)
- ✅ User login (success and failure cases)
- ✅ Sweet CRUD operations (with admin/user permissions)
- ✅ Search functionality (name, category, price range)
- ✅ Purchase and restock operations
- ✅ Authorization and authentication middleware

## 🧪 Test-Driven Development (TDD)

This project follows strict **TDD principles** with a clear **Red-Green-Refactor** pattern:

### TDD Workflow
1. **Red** 🔴: Write failing tests first that define the desired behavior
2. **Green** 🟢: Implement minimum code to make tests pass
3. **Refactor** 🔵: Improve code while keeping all tests passing

### Test Coverage
**Backend Tests** (pytest):
- ✅ User registration (success, duplicates, validation errors)
- ✅ User login (success, incorrect credentials, JWT generation)
- ✅ Authentication middleware (protected routes, role-based access)
- ✅ Sweet CRUD operations (create, read, update, delete)
- ✅ Admin-only operations (authorization checks)
- ✅ Search functionality (name, category, price range filters)
- ✅ Purchase operations (quantity validation, stock management)
- ✅ Restock operations (admin authorization)

**Test Structure:**
```
backend/tests/
├── conftest.py          # Test fixtures and database setup
├── test_auth.py         # Authentication tests
└── test_sweets.py       # Sweet CRUD and business logic tests
```

**Running Tests:**
```bash
cd backend
pytest --cov=app --cov-report=html
```

View detailed coverage report in `backend/htmlcov/index.html`

### TDD Examples

**Example 1: User Registration**
```
1. Red: Write test for registration with duplicate username
2. Green: Implement validation to check username uniqueness
3. Refactor: Extract validation logic into reusable function
```

**Example 2: Purchase Sweet**
```
1. Red: Write test for purchase exceeding available stock
2. Green: Implement stock validation logic
3. Refactor: Add purchase history tracking
```

## 📸 Screenshots

### Authentication Flow
![Login Page](screenshots/login.png)
*Clean and professional login interface*

![Registration](screenshots/register.png)
*Role-based user registration with validation*

### Main Dashboard
![Dashboard](screenshots/dashboard.png)
*Beautiful dashboard with search and filters*

### Admin Features
![Admin Panel](screenshots/admin.png)
*Admin view with full CRUD operations*

![Purchase History](screenshots/purchase-history.png)
*Detailed purchase history and analytics*

## 🤖 My AI Usage

### AI Tools & Usage

**Primary AI Assistant**: **Cursor AI** (Cursor IDE's built-in AI)
- Used throughout the development process for code generation, debugging, and optimization

### How I Used AI in This Project

#### 1. **Project Initialization & Structure**
- **AI Help**: Used Cursor AI to generate initial FastAPI project structure, directory layout, and configuration files
- **My Contribution**: Designed the overall architecture, selected tech stack (FastAPI + React), and organized folder structure
- **Learning**: AI helped me understand FastAPI patterns and best practices for project organization

#### 2. **Test-Driven Development**
- **AI Help**: Used AI to generate initial test templates and fixtures for pytest
- **My Contribution**: 
  - Designed the TDD workflow and test strategy
  - Wrote specific test cases for business logic and edge cases
  - Implemented test coverage for authentication, CRUD operations, and authorization
- **Result**: Achieved high test coverage while maintaining focus on meaningful tests

#### 3. **Backend API Development**
- **AI Help**: 
  - Generated boilerplate for API routes and database models
  - Assisted with SQLAlchemy ORM patterns and JWT authentication setup
- **My Contribution**:
  - Designed database schema and relationships
  - Implemented custom business logic (admin ownership tracking, purchase history)
  - Created authorization middleware and role-based access control
  - Optimized database queries and error handling
- **Learning**: AI helped me understand SQLAlchemy relationships and FastAPI dependency injection

#### 4. **Frontend Development**
- **AI Help**: Generated React component structures and TypeScript interfaces
- **My Contribution**:
  - Designed the UI/UX flow and component architecture
  - Implemented context-based state management
  - Created responsive design with modern CSS animations
  - Built purchase confirmation modal and purchase history features
- **Challenge**: Had to manually integrate AI-generated components with my authentication flow

#### 5. **Deployment & DevOps**
- **AI Help**: Assisted with Railway and Vercel deployment configurations
- **My Contribution**:
  - Set up environment variables and CORS configuration
  - Implemented automatic database migrations
  - Fixed deployment issues with Python versions and dependencies
  - Configured Nixpacks for Railway deployment
- **Troubleshooting**: Used AI to debug CORS errors, database connection issues, and build failures

#### 6. **Code Quality & Debugging**
- **AI Help**: Used for error identification and debugging suggestions
- **My Contribution**:
  - Analyzed and fixed complex bugs (foreign key cascade issues)
  - Improved code organization and documentation
  - Refactored redundant code
  - Optimized performance bottlenecks

### Impact on Workflow & Reflection

**Positive Impacts:**
- ⚡ **Productivity**: Reduced development time by ~50%, especially for boilerplate and configuration
- 🎯 **Quality**: AI helped catch bugs early and suggest best practices
- 📚 **Learning**: AI explanations helped me understand FastAPI, React, and deployment patterns
- 🎨 **Consistency**: AI ensured consistent code style across backend and frontend

**Challenges Faced:**
- 🧠 **Verification**: Always needed to verify AI-generated code for correctness and edge cases
- 🔧 **Customization**: Required significant manual work to adapt AI suggestions to specific requirements
- 🐛 **Debugging**: Some AI-generated code had subtle bugs that required careful testing
- 📖 **Understanding**: Had to deeply understand the codebase to effectively leverage AI suggestions

**My Work vs AI Work (50/50 Split):**
- **My Original Work** (50%):
  - Project architecture and tech stack selection
  - Database schema design and relationships
  - Core business logic implementation
  - Authentication and authorization flow
  - UI/UX design and responsive layouts
  - Security features (JWT, password hashing, validation)
  - Deployment strategy and configuration
  - Problem-solving and debugging approach
  
- **AI-Assisted Work** (50%):
  - Initial project boilerplate and setup
  - Test templates and comprehensive test cases
  - Code debugging and error resolution
  - React component structures
  - API route implementation patterns
  - Documentation and configuration files
  - TDD workflow automation

**Key Learnings:**
1. **AI is a Force Multiplier**: Best used for repetitive tasks and learning, not replacement for critical thinking
2. **TDD + AI = Powerful**: Writing tests first ensured AI-generated code met actual requirements
3. **Verification is Essential**: Always review and understand AI suggestions before using them
4. **Iterative Improvement**: Used AI suggestions as starting points, then refined based on testing

The most effective AI usage was in:
1. **Test Generation**: Could generate comprehensive test cases quickly but modified them for specific edge cases
2. **TypeScript Interfaces**: AI helped create type-safe interfaces, I implemented the actual components
3. **Deployment Debugging**: AI provided valuable troubleshooting suggestions for deployment issues

**Bottom Line**: This project represents a true **collaboration** between human creativity and AI assistance. While AI handled boilerplate, templates, and learning support, my strategic thinking, design decisions, and problem-solving shaped the final product. The 50/50 split allowed me to focus on complex logic while AI accelerated development. The TDD approach ensured quality regardless of the code's origin.

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1 (async Python web framework)
- **Database**: PostgreSQL with SQLAlchemy 2.0.23 ORM
- **Authentication**: JWT (JSON Web Tokens) via python-jose
- **Security**: bcrypt password hashing via passlib
- **Validation**: Pydantic 2.5.0 for data validation
- **Testing**: pytest with coverage reporting

### Frontend
- **Framework**: React 18.2.0 with TypeScript 5.3.3
- **Routing**: React Router 6.20.1 for SPA navigation
- **HTTP Client**: Axios 1.6.2 for API communication
- **State Management**: React Context API
- **Styling**: CSS3 with modern gradients and animations

### DevOps & Deployment
- **Backend**: Railway.app (PostgreSQL + FastAPI deployment)
- **Frontend**: Vercel (React static hosting)
- **Version Control**: Git with GitHub
- **CI/CD**: Automatic deployments on push

## 📝 Git Workflow & Version Control

This project follows **TDD-driven Git workflow** with frequent, meaningful commits:

### Commit Message Convention
```bash
# Test-driven commits
test: Add authentication test cases
feat: Implement user registration endpoint
fix: Resolve database connection issue
refactor: Improve error handling in auth controller
docs: Update API documentation
```

### Branch Strategy
- **main**: Production-ready code (deployed to Railway/Vercel)
- **feature branches**: For new features following Red-Green-Refactor
- **TDD pattern**: Tests committed before implementation

### Commit History Highlights
The commit history demonstrates:
- ✅ Clear TDD workflow (test → implement → refactor)
- ✅ Meaningful commit messages describing changes
- ✅ Regular commits showing incremental progress
- ✅ Proper resolution of conflicts and bugs

## 🚢 Live Deployment

**Production URLs:**
- 🌐 **Frontend**: https://sweet-shop-management-system-snowy.vercel.app
- 🔌 **Backend API**: https://sweetshopmanagement.up.railway.app
- 📚 **API Docs**: https://sweetshopmanagement.up.railway.app/docs

**Deployment Details:**
- ✅ Backend deployed on Railway with PostgreSQL database
- ✅ Frontend deployed on Vercel with automatic HTTPS
- ✅ Environment variables configured for production
- ✅ CORS properly configured for cross-origin requests
- ✅ Automatic database migrations on backend startup

### How I Deployed This Project

I deployed this application using a modern cloud stack:

**Backend & Database: Railway.app**
1. Created Railway account and new project
2. Added PostgreSQL database service
3. Deployed backend from GitHub repository
4. Configured Root Directory as `backend`
5. Set environment variables:
   - `DATABASE_URL` - Private Railway database URL
   - `SECRET_KEY` - Strong JWT secret
   - `ALLOWED_ORIGINS` - CORS configuration for frontend
   - `PYTHON_VERSION` - Fixed to 3.12.7 for compatibility

**Frontend: Vercel**
1. Connected GitHub repository to Vercel
2. Configured Root Directory as `frontend`
3. Set environment variable: `REACT_APP_API_URL` pointing to Railway backend
4. Enabled automatic deployments on push to main branch

**Key Challenges Solved:**
- Fixed Python version compatibility issues with pydantic-core
- Resolved CORS errors by configuring ALLOWED_ORIGINS
- Implemented automatic database migrations on startup
- Configured Nixpacks for Railway deployment
- Handled foreign key cascade issues in sweet deletion

## 🎓 Learning Outcomes

This project helped me master:
- ✅ **Full-Stack Development**: Building end-to-end applications
- ✅ **TDD Methodology**: Test-first development approach
- ✅ **Modern Frameworks**: FastAPI and React best practices
- ✅ **Database Design**: Schema design and optimization
- ✅ **Security**: Authentication, authorization, and input validation
- ✅ **Deployment**: Production deployment on cloud platforms
- ✅ **AI-Assisted Development**: Leveraging AI tools effectively

## 📄 License

This project is part of a **TDD Kata assignment** demonstrating software engineering best practices.

## 👤 Author

**Built with**: TDD principles, modern tech stack, and AI assistance

---

> **💡 Note**: This project demonstrates production-ready code with comprehensive testing, security, and deployment practices. The codebase is well-documented, maintainable, and scalable.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+
- PostgreSQL 12+
- Git

### One-Command Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:3000` to see the application!

**⚠️ Remember**: Configure PostgreSQL database and `.env` file before running!


