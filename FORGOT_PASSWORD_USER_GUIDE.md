# 🔐 Forgot Password - User Guide

## ✅ Step 1: Reset Link Request

जब आप **"Send Reset Link"** button click करते हैं और green success message आता है:

**Message**: "Password reset instructions have been sent to your email."

---

## 📋 Step 2: Reset Token लें (Development Mode में)

### Scenario A: अगर Reset Token दिख रहा है ✅

Success message में अगर आपको **Reset Token** दिख रहा है (जैसे):

```
Password reset instructions have been sent to your email.

Reset Token: abc123xyz789...
```

तो:

1. **Token को copy करें** (पूरा token)
2. Page **automatically 2 seconds बाद** reset password form पर switch हो जाएगा
3. अगर automatic switch नहीं हुआ, तो manually URL use करें:
   ```
   /forgot-password?token=YOUR_TOKEN_HERE
   ```
   (अपने token को replace करें)

---

### Scenario B: अगर Token नहीं दिख रहा (Production Mode)

अगर सिर्फ message दिख रहा है और token नहीं दिख रहा:

**Option 1: Email Check करें** (Production में)
- Email inbox check करें
- Reset link पर click करें
- Link में token automatically होगा

**Option 2: Manual Token (अगर email नहीं मिला)**
- Backend developer से token लें
- या Railway logs में token check करें
- या database में directly check करें

---

## 🔄 Step 3: Reset Password Form

Reset password form खुलने पर:

1. **New Password** enter करें:
   - Minimum 8 characters
   - Strong password use करें
   
2. **Confirm New Password** enter करें:
   - Same password दोबारा type करें
   
3. **"Reset Password"** button click करें

---

## ✅ Step 4: Success!

अगर reset successful होगा:

- ✅ Green success message: "Password reset successful! Redirecting to login..."
- ✅ 2 seconds बाद **automatically login page** पर redirect हो जाएगा

---

## 🔐 Step 5: Login with New Password

1. Login page पर अपना **username** enter करें
2. **नया password** enter करें (जो आपने reset किया था)
3. **Login** button click करें
4. ✅ Successfully login हो जाएंगे!

---

## ⚠️ Troubleshooting

### Problem 1: "Reset token is missing"

**Solution**: 
- Token URL में properly नहीं है
- दोबारा forgot password request करें
- URL में token check करें: `/forgot-password?token=YOUR_TOKEN`

### Problem 2: "Invalid or expired reset token"

**Solution**:
- Token expired हो गया है (1 hour valid)
- नया token request करें
- Forgot password दोबारा करें

### Problem 3: "Passwords do not match"

**Solution**:
- New Password और Confirm Password same होनी चाहिए
- दोबारा carefully type करें

### Problem 4: "Password must be at least 8 characters"

**Solution**:
- Password minimum 8 characters होनी चाहिए
- Longer, stronger password use करें

---

## 📝 Quick Summary

1. ✅ **Email enter करें** → Send Reset Link click करें
2. 🔑 **Reset Token लें** (message में या email से)
3. 🌐 **URL पर जाएं**: `/forgot-password?token=YOUR_TOKEN`
4. 🔐 **New Password enter करें** (min 8 characters)
5. ✅ **Reset Password click** करें
6. 🎉 **Login page** → नए password से login करें

---

## 💡 Tips

- **Token 1 hour तक valid** रहता है
- Token को **copy-paste** करके use करें (typing न करें)
- Password को **securely store** करें
- **Strong password** use करें (letters, numbers, symbols)

---

**🎯 Ready to reset? Follow the steps above!**

