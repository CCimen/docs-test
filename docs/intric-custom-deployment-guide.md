# Complete Intric Deployment Guide - Your Own Instance

## 🎯 What You're Building
You'll deploy your own Intric AI platform with:
- **Your own domain** (not aiverkstad.se)
- **Your own AI API keys** (OpenAI, Claude, or Gemini)
- **Your own secure passwords**
- **Automatic SSL certificates** via Traefik

## 📋 Before You Start

### What You Need:
- [ ] Access to YOUR Portainer instance
- [ ] Your own domain name (e.g., `platform.yourdomain.com`)
- [ ] DNS A record pointing your domain to your server IP
- [ ] At least one AI API key:
  - OpenAI: starts with `sk-...`
  - Anthropic Claude: starts with `sk-ant-...`
  - Google Gemini: your API key
- [ ] The deployment files (docker-compose.yml and env files)
- [ ] 15-20 minutes of time

### ⚠️ IMPORTANT: Replace ALL References
Throughout this guide, you'll see `plattform.aiverkstad.se` - you must replace EVERY instance with YOUR domain name!

---

## 🔐 Step 1: Generate Your Security Keys

**On your computer**, open a terminal and run these commands one by one:

```bash
# Generate JWT_SECRET (copy this value - you'll use it twice!)
openssl rand -hex 32

# Generate URL_SIGNING_KEY (copy this value)
openssl rand -hex 32

# Generate database password (copy this value)
openssl rand -base64 24
```

### 📝 Save These Values!
Create a temporary text file and save:
```
JWT_SECRET: [your-first-generated-value]
URL_SIGNING_KEY: [your-second-generated-value]
DB_PASSWORD: [your-third-generated-value]
```

---

## ✏️ Step 2: Edit Your Configuration Files

You have 4 files to edit. Let's go through each one:

### 2.1 Edit `docker-compose.yml`

**CRITICAL: Replace ALL instances of `plattform.aiverkstad.se` with YOUR domain!**

Find and replace (usually 8-10 places):
- Search for: `plattform.aiverkstad.se`
- Replace with: `your-domain.com` (your actual domain)

Example changes:
```yaml
# BEFORE:
- "traefik.http.routers.intric-frontend.rule=Host(`plattform.aiverkstad.se`)"

# AFTER:
- "traefik.http.routers.intric-frontend.rule=Host(`your-domain.com`)"
```

### 2.2 Edit `env_backend`

1. **Add your AI API key** (at least one):
   ```bash
   # Choose at least ONE of these:
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   ANTHROPIC_API_KEY=sk-ant-your-actual-claude-key-here
   ```

2. **Replace the security placeholders**:
   ```bash
   # BEFORE:
   JWT_SECRET=CHANGE_THIS_GENERATE_WITH_OPENSSL_RAND_HEX_32
   URL_SIGNING_KEY=CHANGE_THIS_GENERATE_WITH_OPENSSL_RAND_HEX_32
   POSTGRES_PASSWORD=CHANGE_THIS_SECURE_PASSWORD_123!

   # AFTER (use YOUR generated values):
   JWT_SECRET=your-first-generated-value-from-step-1
   URL_SIGNING_KEY=your-second-generated-value-from-step-1
   POSTGRES_PASSWORD=your-third-generated-value-from-step-1
   ```

### 2.3 Edit `env_frontend`

1. **Replace the domain references**:
   ```bash
   # BEFORE:
   ORIGIN=https://plattform.aiverkstad.se
   INTRIC_BACKEND_URL=https://plattform.aiverkstad.se

   # AFTER (use YOUR domain):
   ORIGIN=https://your-domain.com
   INTRIC_BACKEND_URL=https://your-domain.com
   ```

2. **Replace JWT_SECRET** (MUST match env_backend!):
   ```bash
   # Use the SAME JWT_SECRET as in env_backend
   JWT_SECRET=your-first-generated-value-from-step-1
   ```

### 2.4 Edit `env_db`

**Replace the database password** (MUST match env_backend!):
```bash
# Use the SAME password as in env_backend
POSTGRES_PASSWORD=your-third-generated-value-from-step-1
```

### ✅ Double-Check Checklist:
- [ ] JWT_SECRET is IDENTICAL in env_backend and env_frontend
- [ ] POSTGRES_PASSWORD is IDENTICAL in env_backend and env_db
- [ ] Your domain replaces ALL instances of plattform.aiverkstad.se
- [ ] You've added at least one AI API key

---

## 🚀 Step 3: Deploy in Portainer

### 3.1 Login to Your Portainer
1. Open your Portainer URL in a web browser
2. Login with your credentials
3. Select your environment (e.g., `sb-aipoc01` or your environment name)

### 3.2 Navigate to Stacks
1. Click **Stacks** in the left sidebar
2. Click the blue **+ Add stack** button

### 3.3 Configure Your Stack
1. **Stack name**: Enter a name (e.g., `intric-platform` or `my-ai-platform`)
2. **Build method**: Select **Upload**

### 3.4 Upload Your Files
1. **Upload docker-compose.yml**:
   - Click **Select file** next to "Compose file"
   - Choose your edited `docker-compose.yml`
   - Click **Open**

2. **Add Environment Variables**:
   - Scroll down to "Environment variables"
   - Click **Load variables from .env file**
   - Upload files in this order:
     1. First: `env_backend`
     2. Second: `env_frontend`
     3. Third: `env_db`

### ⚠️ Yellow Warning About Duplicates?
If you see a yellow warning about duplicate variables:
- This is normal! Some variables appear in multiple files
- Click **Remove** on the duplicate entries
- Keep only one instance of each variable

### 3.5 Deploy!
1. Scroll to the bottom
2. Click the blue **Deploy the stack** button
3. Wait... deployment takes 2-3 minutes

---

## 📊 Step 4: Monitor Your Deployment

### 4.1 Check Container Status
1. Go to **Containers** in the left sidebar
2. Look for your 6 new containers:

| Container | Expected Status | What it does |
|-----------|----------------|--------------|
| `[stack]_frontend` | ✅ Running | Web interface |
| `[stack]_backend` | ✅ Running | API server |
| `[stack]_worker` | ✅ Running | Background tasks |
| `[stack]_db` | ✅ Running | Database |
| `[stack]_redis` | ✅ Running | Cache |
| `[stack]_db_init` | ⚪ Exited (0) | Initial setup |

### 4.2 If db_init Container Fails
If the db_init container shows red/failed status:
1. Click on the container name
2. Click **Restart** button
3. Wait 30 seconds
4. Check if it exits with code 0 (success)

### 4.3 Check Container Logs
For each running container:
1. Click the container name
2. Click **Logs** tab
3. Look for success messages:
   - Frontend: "Listening on 0.0.0.0:3000"
   - Backend: "Uvicorn running on http://0.0.0.0:8000"
   - Database: "database system is ready to accept connections"

---

## 🌐 Step 5: Access Your Platform

### 5.1 First Access
1. Wait 2-3 minutes after deployment
2. Open a new browser tab
3. Go to: `https://your-domain.com` (YOUR actual domain!)
4. You should see the Intric login page

### 🔒 SSL Certificate Note
- Traefik automatically gets SSL certificates
- First visit might take 10-30 seconds while certificate is obtained
- If you see a certificate warning, wait 2 minutes and refresh

### 5.2 Login with Default Admin
- **Email**: `user@example.com`
- **Password**: `Password1!`

### 🚨 SECURITY ALERT: Change This Password NOW!

### 5.3 Change Admin Password Immediately
1. Click your profile icon (top right)
2. Go to **Settings** or **Profile**
3. Click **Change Password**
4. Create a strong password
5. Save changes

---

## 🎯 Step 6: Configure Your AI Platform

### 6.1 Create Your First Space
1. Look for **Create Space** button
2. Name it (e.g., "Production", "Main", or your company name)
3. Click **Create**

### 6.2 Configure AI Models
1. Click the gear icon for **Space Settings**
2. Go to **Models** section
3. **Add Completion Model**:
   - Provider: Select based on your API key (OpenAI/Anthropic/Google)
   - Model: Choose one:
     - OpenAI: `gpt-4o` or `gpt-4o-mini`
     - Anthropic: `claude-3-5-sonnet-20241022`
     - Google: `gemini-1.5-pro`
4. **Add Embedding Model**:
   - Usually: `text-embedding-3-small` (OpenAI)
5. Click **Save**

### 6.3 Test Your Setup
1. Click **Create Assistant**
2. Name: "Test Assistant"
3. Instructions: "You are a helpful AI assistant"
4. Click **Create**
5. Test with: "Hello, can you hear me?"

---

## 🔧 Troubleshooting Common Issues

### Cannot Access Your Domain
**Problem**: Browser can't reach your site

**Solutions**:
1. Check DNS propagation (can take up to 24 hours)
2. Verify your domain's A record points to server IP
3. Check if Traefik container is running in Portainer
4. Look at Traefik logs for certificate errors

### Login Fails / Invalid Credentials
**Problem**: Can't login with admin@example.com

**Check**:
1. JWT_SECRET is EXACTLY the same in both env files
2. Backend container is running
3. db_init completed successfully (exit code 0)

**Fix**:
1. Check backend logs for JWT errors
2. Redeploy stack with matching secrets

### 500 Server Error
**Problem**: Server error when accessing site

**Check**:
1. Database container is running
2. POSTGRES_PASSWORD matches in both files
3. All containers are healthy

### File Upload Fails
**Problem**: Can't upload documents

**Fix in Portainer**:
1. Go to your backend container
2. Click **Console**
3. Select `/bin/sh`
4. Run:
   ```bash
   chown -R 999:999 /app/data
   chmod -R 775 /app/data
   ```

---

## ✅ Final Verification Checklist

- [ ] All 6 containers running (except db_init which should show "Exited 0")
- [ ] Can access https://your-domain.com (with YOUR domain)
- [ ] SSL certificate works (padlock in browser)
- [ ] Can login with admin@example.com / admin
- [ ] Changed default admin password
- [ ] Created first Space
- [ ] Added AI models to Space
- [ ] Created and tested first Assistant
- [ ] Assistant responds to questions

---

## 🎉 Congratulations!

Your Intric AI platform is now running at your domain!

### What's Next?
1. Create user accounts for your team
2. Build custom assistants for different use cases
3. Upload documents for knowledge base
4. Explore web crawling features
5. Customize the platform for your needs

### Need Help?
- Check container logs first
- Verify all passwords match between files
- Ensure your domain is properly configured
- Remember: db_init can be restarted if it fails

---

## 📝 Quick Reference

### Your Custom Values:
- **Domain**: `your-domain.com` (replace everywhere!)
- **Stack Name**: Your chosen name in Portainer
- **Container Prefix**: `[your-stack-name]_`

### Default Logins:
- **Intric Admin**: user@example.com / Password1! (CHANGE THIS!)
- **Database**: postgres / [your-generated-password]

### Important URLs:
- **Your Platform**: https://your-domain.com
- **API Docs**: https://your-domain.com/docs
- **OpenAPI Spec**: https://your-domain.com/openapi.json

Good luck with your deployment! 🚀
