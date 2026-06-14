# 📤 Upload Project to GitHub - Complete Guide

## STEP 1: CREATE GITHUB ACCOUNT

1. Go to: **github.com**
2. Click "Sign up"
3. Enter email: your_email@gmail.com
4. Create password: strong_password_123
5. Username: your_username (or grocery-store-mgmt)
6. Verify email
7. Done! ✅

---

## STEP 2: CREATE NEW REPOSITORY

1. Click **"+"** icon (top right)
2. Select **"New repository"**
3. Fill in details:

   **Repository name:** `grocery-store-management`
   
   **Description:** Grocery Store Management System - Flask, MySQL, Python
   
   **Visibility:** Select **"Private"** (only you can see)
   
   **Initialize with:** Check "Add a README file"
   
4. Click **"Create repository"**

5. You'll see: `https://github.com/your_username/grocery-store-management`

---

## STEP 3: INSTALL GIT ON YOUR COMPUTER

### **For Windows:**

1. Go to: **git-scm.com**
2. Download "Git for Windows"
3. Run installer
4. Click "Next" for all defaults
5. Finish installation
6. Open Command Prompt (cmd)
7. Type: `git --version`
8. Should show: `git version 2.x.x`

### **For Mac:**

```bash
brew install git
git --version
```

### **For Linux:**

```bash
sudo apt install git
git --version
```

---

## STEP 4: CONFIGURE GIT (First Time Only)

Open Command Prompt and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@gmail.com"
```

Example:
```bash
git config --global user.name "Kanishka Weerasinghe"
git config --global user.email "kanishka@example.com"
```

---

## STEP 5: NAVIGATE TO YOUR PROJECT

Open Command Prompt and go to your project folder:

```bash
cd c:\Users\Administrator\OneDrive\Desktop\Grocery Store
```

---

## STEP 6: CREATE .gitignore FILE

This tells Git which files NOT to upload (like passwords).

Create file: `.gitignore`

```
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.sql
*.sqlite
*.sqlite3

# Logs
*.log
npm-debug.log*
yarn-debug.log*

# Node modules (if any)
node_modules/

# Backups
*.backup
*.bak
```

---

## STEP 7: INITIALIZE GIT REPOSITORY

In Command Prompt, type:

```bash
git init
```

---

## STEP 8: ADD ALL FILES

```bash
git add .
```

This stages all your files for commit.

---

## STEP 9: FIRST COMMIT

```bash
git commit -m "Initial commit: Grocery Store Management System"
```

---

## STEP 10: ADD GITHUB REMOTE

Get the URL from GitHub (from Step 2), then run:

```bash
git branch -M main
git remote add origin https://github.com/your_username/grocery-store-management.git
```

Replace `your_username` with your actual GitHub username!

---

## STEP 11: PUSH TO GITHUB

```bash
git push -u origin main
```

It will ask for:
- **Username:** your_github_username
- **Password:** your_github_password

**OR** use Personal Access Token (more secure):

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token
3. Copy token
4. Paste as password when prompted

---

## ✅ DONE!

Go to GitHub and refresh: `https://github.com/your_username/grocery-store-management`

Your project files should now be visible! 🎉

---

## 📝 HOW TO UPDATE GITHUB LATER

Whenever you make changes locally:

```bash
# 1. See what changed
git status

# 2. Add changes
git add .

# 3. Commit with message
git commit -m "Fixed inventory bug"

# 4. Push to GitHub
git push
```

---

## COMMON COMMANDS

### Check status
```bash
git status
```

### View commit history
```bash
git log
```

### Undo last commit
```bash
git reset --soft HEAD~1
```

### Check what's staged
```bash
git diff --cached
```

### Clone repo on another computer
```bash
git clone https://github.com/your_username/grocery-store-management.git
cd grocery-store-management
```

---

## 🔐 SENSITIVE DATA

**NEVER upload:**
- Database passwords
- API keys
- Secret keys
- Personal information

Put these in `.env` file (which is in `.gitignore`)

---

## 📊 GITHUB TIPS

### Create branch for features
```bash
git checkout -b feature/new-feature
git add .
git commit -m "Added new feature"
git push origin feature/new-feature
```

Then create Pull Request on GitHub to merge.

### See all branches
```bash
git branch -a
```

### Delete branch
```bash
git branch -d feature/new-feature
```

---

## DEPLOYMENT FROM GITHUB

When deploying to VPS:

```bash
cd /var/www
git clone https://github.com/your_username/grocery-store-management.git
cd grocery-store-management
git pull  # to update code later
```

---

## TROUBLESHOOTING

### Error: "fatal: not a git repository"
**Fix:** Make sure you're in correct folder with `cd` command

### Error: "Permission denied (publickey)"
**Fix:** Use Personal Access Token instead of password

### Error: "Your branch is ahead of 'origin/main'"
**Fix:** Run `git push`

### Want to start over?
```bash
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your_username/repo.git
git push -u origin main
```

---

## 📋 QUICK CHECKLIST

- [ ] Created GitHub account
- [ ] Created repository
- [ ] Installed Git
- [ ] Configured Git (name + email)
- [ ] Created .gitignore file
- [ ] Ran `git init`
- [ ] Ran `git add .`
- [ ] Ran `git commit -m "message"`
- [ ] Added remote: `git remote add origin ...`
- [ ] Pushed to GitHub: `git push -u origin main`
- [ ] Verified files on GitHub.com

---

## WHAT YOUR GITHUB SHOULD LOOK LIKE

```
grocery-store-management/
├── Backend/
│   ├── server.py
│   ├── inventory_dao.py
│   ├── analytics_dao.py
│   ├── order_dao.py
│   ├── products_dao.py
│   ├── admin_dao.py
│   ├── uom_dao.py
│   └── sql_connection.py
├── UI/
│   ├── index.html
│   ├── login.html
│   ├── manage-product.html
│   ├── order.html
│   ├── edit-order.html
│   ├── inventory.html
│   ├── analytics.html
│   ├── js/
│   │   ├── custom/
│   │   │   ├── common.js
│   │   │   ├── dashboard.js
│   │   │   ├── inventory.js
│   │   │   ├── analytics.js
│   │   │   └── ...
│   ├── css/
│   └── images/
├── .gitignore
├── .env (NOT uploaded - in .gitignore)
├── requirements.txt
└── README.md
```

---

## CREATE README.md

Create `README.md` in project root:

```markdown
# Grocery Store Management System

Professional e-commerce management system built with Flask, MySQL, and Bootstrap.

## Features

- ✅ Admin Authentication
- ✅ Product Management
- ✅ Order Management
- ✅ Inventory Tracking
- ✅ Analytics & Reports

## Installation

```bash
pip install -r requirements.txt
python server.py
```

## Database

Create MySQL database and import schema:

```bash
mysql -u root -p
CREATE DATABASE gs;
```

## Deployment

See DEPLOYMENT_GUIDE.md for production setup.

## License

MIT License
```

---

## 🚀 YOU'RE DONE!

Your project is now on GitHub and ready for:
✅ Version control
✅ Team collaboration
✅ Easy deployment
✅ Backup
✅ Portfolio showcase

---

## NEXT: DEPLOY FROM GITHUB TO VPS

When you're ready to deploy:

```bash
# On VPS
cd /var/www
git clone https://github.com/your_username/grocery-store-management.git
cd grocery-store-management

# Follow VPS setup guide from here
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

**Happy coding! 🎉**
