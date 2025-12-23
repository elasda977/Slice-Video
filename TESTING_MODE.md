# Testing Mode - Authentication Toggle

This document explains how to enable/disable authentication for testing purposes.

## 🔧 How to Enable/Disable Authentication

### Option 1: Environment Variable (Recommended)

Edit `backend/.env` and set:

```bash
# Disable authentication for testing
ENABLE_AUTH=false

# Enable authentication for production
ENABLE_AUTH=true
```

### Option 2: Configuration File

Edit `backend/config.py` and change:

```python
# Testing - Set to False to disable authentication (ONLY FOR DEVELOPMENT!)
ENABLE_AUTH: bool = False  # Change to True to enable
```

## 🔄 Current Behavior

### When `ENABLE_AUTH=false` (Testing Mode) ✅

- **No login required** - All endpoints work without authentication
- **All videos visible** - Can see and manage all videos
- **No user ownership** - Videos created without user_id
- **Full access** - Can delete, convert, and manage any video

**Perfect for:**
- Local testing
- Development
- Demo environments
- Quick prototyping

### When `ENABLE_AUTH=true` (Production Mode) 🔒

- **Login required** - Must authenticate to use endpoints
- **User-specific** - Can only see your own videos
- **Ownership checks** - Can only modify videos you created
- **Secure** - JWT token validation on all requests

**Use for:**
- Production deployments
- Multi-user environments
- Staging servers
- Any public-facing instance

## 🚀 Quick Start Testing

### 1. Disable Authentication

```bash
cd backend
echo "ENABLE_AUTH=false" >> .env
```

### 2. Start Backend

```bash
source venv/bin/activate
python main.py
```

### 3. Start Frontend

```bash
cd ../frontend
npm run dev
```

### 4. Test Without Login

- Navigate to http://localhost:3000
- You can now use all features without logging in!
- No need to visit /login or /register

## 🔐 Re-enabling Authentication

When you're ready to enable authentication:

```bash
cd backend
# Edit .env file
sed -i 's/ENABLE_AUTH=false/ENABLE_AUTH=true/' .env

# Or manually set in .env:
# ENABLE_AUTH=true
```

Then restart the backend server.

## ⚠️ Important Security Notes

1. **NEVER deploy with `ENABLE_AUTH=false` in production!**
2. This is a development/testing feature only
3. In testing mode:
   - Anyone can delete all videos
   - Anyone can upload files
   - No rate limiting applies
   - All data is unprotected

## 🧪 Testing Checklist

With authentication disabled, you should test:

- ✅ Video upload
- ✅ Video conversion with progress tracking
- ✅ Video playback
- ✅ Video deletion
- ✅ Dashboard statistics
- ✅ Cleanup (delete all)

## 🔄 Switching Modes

The application automatically detects the `ENABLE_AUTH` setting:

```
ENABLE_AUTH=false → Testing Mode
                    ↓
     All endpoints accept requests without token
                    ↓
          Videos have user_id=None
                    ↓
         No ownership validation

ENABLE_AUTH=true  → Production Mode
                    ↓
      All endpoints require Bearer token
                    ↓
     Videos must have valid user_id
                    ↓
       Full ownership validation
```

## 📊 Endpoint Behavior Matrix

| Endpoint | Testing Mode | Production Mode |
|----------|--------------|-----------------|
| `GET /api/videos` | Shows all videos | Shows only user's videos |
| `GET /api/videos/{id}` | Any video | Only owned videos |
| `DELETE /api/videos/{id}` | Can delete any | Only owned videos |
| `POST /api/videos/upload` | No auth needed | Requires auth |
| `POST /api/convert` | No auth needed | Requires auth |
| `DELETE /api/cleanup` | Deletes ALL | Deletes only user's |
| `GET /api/status` | All statistics | User statistics |

## 🐛 Troubleshooting

### Frontend still asking for login?

The frontend axios interceptor still tries to send tokens. This is OK - the backend will accept requests even without valid tokens when `ENABLE_AUTH=false`.

### Videos not showing?

Check that videos have been created. In testing mode, videos might have `user_id=None`.

### Backend returning 401?

Make sure `ENABLE_AUTH=false` is set in your `.env` file and restart the backend.

## 💡 Tips

1. **Use .env for toggling** - Don't commit changes to config.py
2. **Restart backend** after changing ENABLE_AUTH
3. **Clear browser cache** if you see auth issues
4. **Check console logs** - backend prints auth mode on startup

## 🎬 Demo Mode Script

Quick script to start in testing mode:

```bash
#!/bin/bash
# demo-mode.sh

cd backend
echo "ENABLE_AUTH=false" > .env
source venv/bin/activate
python main.py &

cd ../frontend
npm run dev
```

---

**Need help?** Check the main README.md or open an issue.
