# Sweet Shop Management System

A full-stack Sweet Shop Management System built with **FastAPI (Python)**, **PostgreSQL**, and **React (TypeScript)**, following Test-Driven Development (TDD) principles.

## 🎯 Project Overview

This project is a comprehensive management system for a sweet shop that allows:
- User registration and authentication with JWT
- Viewing and searching sweets inventory
- Purchasing sweets (decreases quantity)
- Admin-only features: Add, update, delete, and restock sweets

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

## 📸 Screenshots

![Login Page](screenshots/login.png)
*User login interface*

![Dashboard](screenshots/dashboard.png)
*Main dashboard showing all sweets*

![Admin Panel](screenshots/admin.png)
*Admin view with edit/delete/restock options*

## 🤖 My AI Usage

### AI Tools Used
- **Cursor AI** (primary development assistant)
- **GitHub Copilot** (code suggestions)

### How I Used AI

1. **Initial Project Structure**
   - Used Cursor AI to generate the initial FastAPI project structure, including directory layout, configuration files, and basic setup.

2. **Test Generation**
   - Used AI to generate comprehensive test cases for authentication, CRUD operations, and edge cases. The AI helped create test fixtures and mock data structures.

3. **Boilerplate Code**
   - AI assisted in generating:
     - Database models and schemas
     - API route handlers
     - React component structures
     - Authentication middleware

4. **Code Debugging**
   - Used AI to identify and fix:
     - Import errors
     - Type mismatches
     - Database connection issues
     - CORS configuration problems

5. **Documentation**
   - AI helped structure the README and generate API documentation examples.

### Impact on Workflow

**Positive Impacts:**
- **Speed**: Significantly faster project setup and boilerplate generation
- **Quality**: AI suggestions helped catch potential bugs early
- **Learning**: AI explanations helped understand FastAPI patterns and React best practices
- **Consistency**: AI ensured consistent code style across the project

**Challenges:**
- Sometimes needed to verify AI-generated code for correctness
- Had to manually adjust generated code to match specific requirements
- Required understanding the codebase to effectively use AI suggestions

**Reflection:**
AI tools were invaluable for this project, especially for generating test cases and maintaining consistency. However, I always reviewed and understood the generated code rather than blindly accepting it. The TDD approach was crucial - writing tests first ensured the AI-generated code met the actual requirements.

The most effective use of AI was in:
1. Generating comprehensive test cases (would have taken much longer manually)
2. Creating type-safe TypeScript interfaces for React
3. Setting up authentication flow with proper error handling

## 🛠️ Technologies Used

### Backend
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL (psycopg2-binary)
- python-jose (JWT)
- passlib (password hashing)
- pytest (testing)

### Frontend
- React 18.2.0
- TypeScript 5.3.3
- React Router 6.20.1
- Axios 1.6.2
- React Testing Library

## 📝 Git Workflow

This project follows a TDD workflow with frequent commits:
- Each feature branch follows Red-Green-Refactor cycle
- Commit messages describe what was added/changed
- Tests are committed before implementation

Example commits:
```
test: Add authentication test cases
feat: Implement user registration endpoint
refactor: Improve error handling in auth controller
```

## 🚢 Deployment (Optional)

### Backend (Heroku/Railway/Fly.io)
1. Set environment variables in deployment platform
2. Set `DATABASE_URL` to production PostgreSQL
3. Deploy using git push or platform CLI

### Frontend (Vercel/Netlify)
1. Build: `npm run build`
2. Deploy the `build` folder
3. Set API URL in environment variables

## 📄 License

This project is part of a TDD Kata assignment.

## 👤 Author

Built following TDD principles with AI assistance.

---

**Note**: Remember to set up your PostgreSQL database and configure the `.env` file before running the application!


