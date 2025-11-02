# Sweet Shop Management System - Complete Testing Guide

## 🎯 Prerequisites

1. **Backend Server Running:**
   ```powershell
   cd "D:\Sweet Shop Management System\backend"
   .\venv\Scripts\activate
   uvicorn app.main:app --reload
   ```
   - Should see: `INFO: Uvicorn running on http://127.0.0.1:8000`
   - Should see: `✅ Database tables created/verified successfully`

2. **Frontend Server Running:**
   ```powershell
   cd "D:\Sweet Shop Management System\frontend"
   npm start
   ```
   - Should open automatically at `http://localhost:3000`

3. **PostgreSQL Running:**
   - Database: `sweet_shop_db`
   - User: `postgres`
   - Password: (your password)

---

## 📋 Testing Checklist

### ✅ Test 1: User Registration

**Steps:**
1. Open `http://localhost:3000`
2. Click "Register" or "Register here"
3. Fill the form:
   - **Username:** `testuser`
   - **Email:** `testuser@example.com`
   - **Password:** `password123` (min 8 characters)
4. Click "Register"

**Expected Results:**
- ✅ Success message or redirect to dashboard
- ✅ Welcome message shows: "Welcome, testuser! (user)"
- ✅ Dashboard loads (may show "No sweets found")

---

### ✅ Test 2: User Login

**Steps:**
1. If already logged in, click "Logout"
2. Click "Login here" or go to login page
3. Enter credentials:
   - **Username:** `testuser`
   - **Password:** `password123`
4. Click "Login"

**Expected Results:**
- ✅ Redirects to dashboard
- ✅ Welcome message: "Welcome, testuser! (user)"
- ✅ Can see sweets list (empty initially)

---

### ✅ Test 3: Make User Admin (Required for Admin Features)

**Steps:**
1. In backend terminal, run:
   ```python
   python -c "from app.database import SessionLocal; from app.models import User; db = SessionLocal(); user = db.query(User).filter(User.username == 'testuser').first(); user.role = 'admin'; db.commit(); print('✅ User is now admin'); db.close()"
   ```
2. **Important:** Logout and login again in the frontend to refresh the token

**Expected Results:**
- ✅ After re-login, see "+ Add New Sweet" button
- ✅ Welcome message shows: "Welcome, testuser! (admin)"

---

### ✅ Test 4: Add Sweets (Admin Only)

**Steps:**
1. Click "+ Add New Sweet" button
2. Fill the form with these test sweets:

   **Sweet 1:**
   - Name: `Gulab Jamun`
   - Category: `Indian Sweets`
   - Price: `150`
   - Quantity: `20`
   - Click "Save"

   **Sweet 2:**
   - Name: `Rasgulla`
   - Category: `Indian Sweets`
   - Price: `120`
   - Quantity: `15`

   **Sweet 3:**
   - Name: `Ladoo`
   - Category: `Indian Sweets`
   - Price: `100`
   - Quantity: `25`

   **Sweet 4:**
   - Name: `Chocolate Bar`
   - Category: `Confectionery`
   - Price: `50`
   - Quantity: `30`

**Expected Results:**
- ✅ Sweet appears in dashboard grid
- ✅ Can see name, category, price, and stock quantity
- ✅ No errors in console or backend

---

### ✅ Test 5: View All Sweets

**Steps:**
1. Dashboard should automatically load all sweets
2. Check each sweet card displays:
   - Sweet name
   - Category
   - Price (formatted correctly)
   - Stock quantity

**Expected Results:**
- ✅ All added sweets visible
- ✅ Cards display correctly
- ✅ Information is accurate

---

### ✅ Test 6: Search Functionality

**Test 6a: Search by Name**
1. Type "Gulab" in search box
2. **Expected:** Only "Gulab Jamun" appears
3. Clear search

**Test 6b: Filter by Category**
1. Select "Indian Sweets" from dropdown
2. **Expected:** Shows Gulab Jamun, Rasgulla, Ladoo (not Chocolate Bar)
3. Select "All Categories" to clear

**Test 6c: Filter by Price Range**
1. Set Min Price: `100`
2. Set Max Price: `130`
3. **Expected:** Shows Rasgulla (120) and Ladoo (100)
4. Clear price filters

**Test 6d: Combined Filters**
1. Category: "Indian Sweets"
2. Min Price: `110`
3. Max Price: `160`
4. **Expected:** Shows Gulab Jamun (150) only

---

### ✅ Test 7: Purchase Sweets (All Users)

**Steps:**
1. Find a sweet with quantity > 0 (e.g., Rasgulla with 15)
2. Click "Purchase" button
3. Check the quantity decreased

**Expected Results:**
- ✅ Quantity decreases by 1
- ✅ Dashboard refreshes showing updated quantity
- ✅ Purchase button works multiple times

**Test 7b: Purchase Until Out of Stock**
1. Keep clicking "Purchase" on same sweet
2. When quantity reaches 0
3. **Expected:** Purchase button becomes disabled
4. Card shows "Out of Stock"

**Test 7c: Try Purchasing Out-of-Stock Item**
1. Find sweet with quantity = 0
2. **Expected:** Purchase button is disabled/grayed out

---

### ✅ Test 8: Edit Sweets (Admin Only)

**Steps:**
1. Click "Edit" button on any sweet
2. Modify fields:
   - Name: `Gulab Jamun (Premium)`
   - Price: `180`
   - Quantity: `25`
3. Click "Save"

**Expected Results:**
- ✅ Sweet card updates with new information
- ✅ Changes persist after page refresh
- ✅ No errors

---

### ✅ Test 9: Restock Sweets (Admin Only)

**Steps:**
1. Find a sweet with low/zero quantity
2. Enter quantity in restock input (e.g., `10`)
3. Click "Restock" button

**Expected Results:**
- ✅ Quantity increases by entered amount
- ✅ Dashboard refreshes
- ✅ Restock input clears

---

### ✅ Test 10: Delete Sweets (Admin Only)

**Steps:**
1. Click "Delete" button on a sweet
2. Confirm deletion in popup
3. **Expected:** Sweet disappears from dashboard

---

### ✅ Test 11: Regular User Permissions

**Steps:**
1. Logout from admin account
2. Create a new regular user:
   - Username: `regularuser`
   - Email: `regular@example.com`
   - Password: `password123`
3. Login as regular user
4. Check dashboard

**Expected Results:**
- ✅ Can view all sweets
- ✅ Can search and filter
- ✅ Can purchase sweets
- ❌ **Cannot** see "+ Add New Sweet" button
- ❌ **Cannot** see "Edit" buttons
- ❌ **Cannot** see "Delete" buttons
- ❌ **Cannot** see "Restock" inputs

---

### ✅ Test 12: Error Handling

**Test 12a: Duplicate Registration**
1. Try registering with existing username
2. **Expected:** Error: "Username or email already exists"

**Test 12b: Wrong Password**
1. Try login with wrong password
2. **Expected:** Error: "Incorrect username or password"

**Test 12c: Invalid Form Data**
1. Try adding sweet with empty fields
2. **Expected:** Form validation errors

**Test 12d: Unauthorized Access**
1. As regular user, try to access admin endpoints directly
2. **Expected:** 403 Forbidden error

---

### ✅ Test 13: Session Management

**Test 13a: Logout**
1. Click "Logout" button
2. **Expected:** Redirects to login page

**Test 13b: Protected Route**
1. While logged out, try accessing `/dashboard` directly
2. **Expected:** Redirects to login page

**Test 13c: Token Persistence**
1. Login
2. Close browser tab (don't close browser)
3. Reopen `http://localhost:3000`
4. **Expected:** Still logged in (token in localStorage)

---

### ✅ Test 14: API Documentation (Optional)

**Steps:**
1. Open `http://localhost:8000/docs` in browser
2. Explore Swagger UI
3. Test endpoints using "Try it out" feature

**Expected Results:**
- ✅ All endpoints listed
- ✅ Can see request/response schemas
- ✅ Can test endpoints interactively

---

## 🎯 Quick Test Summary

### Must-Have Features Working:
- [ ] User registration
- [ ] User login/logout
- [ ] View all sweets
- [ ] Search by name
- [ ] Filter by category
- [ ] Filter by price
- [ ] Purchase sweet (reduces quantity)
- [ ] Out of stock handling (button disabled)
- [ ] Admin can add sweets
- [ ] Admin can edit sweets
- [ ] Admin can delete sweets
- [ ] Admin can restock sweets
- [ ] Regular users cannot access admin features
- [ ] Protected routes work correctly

---

## 🐛 Troubleshooting

### Issue: "Failed to load sweets"
- ✅ Check backend is running
- ✅ Check database connection
- ✅ Check browser console for errors
- ✅ Check backend terminal for errors

### Issue: "403 Forbidden" when adding sweets
- ✅ Make sure user role is "admin" in database
- ✅ Logout and login again to refresh token
- ✅ Check backend terminal for role info

### Issue: "404 Not Found" on purchase
- ✅ Check route ordering in backend
- ✅ Ensure URL doesn't have trailing slash issues
- ✅ Check backend terminal for route matching

### Issue: Authorization header missing
- ✅ Check frontend is sending token
- ✅ Verify token is stored in localStorage
- ✅ Check CORS settings in backend

---

## 📊 Test Report Template

After completing tests, note:
- ✅ Passed tests
- ❌ Failed tests (with error messages)
- 🔍 Issues found
- 💡 Suggestions for improvement

---

**Happy Testing! 🎉**


