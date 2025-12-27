# GitHub Setup Guide

## Step-by-Step: Push Your Code to GitHub

### 1. Create GitHub Account
If you don't have one: https://github.com/signup

### 2. Install Git (if not installed)
Download from: https://git-scm.com/download/win

Check if installed:
```powershell
git --version
```

### 3. Configure Git (First Time Only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Initialize Repository
```powershell
# Navigate to your project folder
cd "C:\Users\3CHUB\3D Objects\insurers part"

# Initialize git
git init

# Check status
git status
```

### 5. Create .gitignore (Already Done!)
Your `.gitignore` file already excludes:
- `.env` (API keys - NEVER commit this!)
- `__pycache__/`
- `node_modules/`
- `*.pyc`

### 6. Stage All Files
```powershell
# Add all files
git add .

# Check what will be committed
git status
```

### 7. Create First Commit
```powershell
git commit -m "Initial commit: Hyperlocal Intelligence Platform for Parametric Insurance"
```

### 8. Create GitHub Repository

**Option A: Via GitHub Website**
1. Go to https://github.com/new
2. Repository name: `hyperlocal-insurance-platform`
3. Description: `Hyperlocal intelligence platform for parametric insurance triggers`
4. Choose: Public or Private
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

**Option B: Via GitHub CLI** (if installed)
```powershell
gh repo create hyperlocal-insurance-platform --public --source=. --remote=origin
```

### 9. Link Local Repo to GitHub
```powershell
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/hyperlocal-insurance-platform.git

# Verify remote
git remote -v
```

### 10. Push to GitHub
```powershell
# Rename branch to main (if needed)
git branch -M main

# Push code
git push -u origin main
```

### 11. Verify on GitHub
Go to: `https://github.com/YOUR_USERNAME/hyperlocal-insurance-platform`

You should see all your files! ✅

---

## 🔐 Security Checklist Before Pushing

### ✅ Make Sure These Are NOT in Your Repo:
- [ ] `.env` file (contains API keys)
- [ ] `node_modules/` folder
- [ ] `__pycache__/` folders
- [ ] Any files with passwords or secrets

### ✅ Check Your .gitignore:
```powershell
# View what's ignored
type .gitignore
```

### ✅ Verify No Secrets in Commits:
```powershell
# Check what will be pushed
git log --oneline
git show HEAD
```

If you accidentally committed secrets:
```powershell
# Remove file from git but keep locally
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from tracking"

# Push
git push
```

---

## 🔄 Daily Git Workflow

### Making Changes:
```powershell
# 1. Make your code changes

# 2. Check what changed
git status

# 3. Add changes
git add .

# 4. Commit with descriptive message
git commit -m "Add new feature: risk scoring algorithm"

# 5. Push to GitHub
git push
```

### Useful Git Commands:
```powershell
# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard HEAD

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature
```

---

## 🚨 Common Git Issues & Fixes

### Issue: "Permission denied (publickey)"
**Fix**: Set up SSH key or use HTTPS with token
```powershell
# Use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/repo.git
```

### Issue: "Repository not found"
**Fix**: Check repository name and permissions
```powershell
git remote -v
git remote set-url origin https://github.com/CORRECT_USERNAME/repo.git
```

### Issue: "Failed to push some refs"
**Fix**: Pull first, then push
```powershell
git pull origin main --rebase
git push origin main
```

### Issue: Accidentally committed .env file
**Fix**: Remove from history
```powershell
git rm --cached .env
git commit -m "Remove .env from tracking"
git push

# Then change your API keys immediately!
```

---

## 📝 Good Commit Message Examples

✅ Good:
- `Add parametric trigger monitoring system`
- `Fix: CORS error in production deployment`
- `Update: Improve risk scoring algorithm`
- `Docs: Add deployment guide`

❌ Bad:
- `update`
- `fix stuff`
- `changes`
- `asdfasdf`

---

## 🌿 Branching Strategy (Optional)

For team projects:

```powershell
# Main branch (production)
main

# Development branch
git checkout -b develop

# Feature branches
git checkout -b feature/add-authentication
git checkout -b feature/email-notifications

# Bug fix branches
git checkout -b fix/cors-error
git checkout -b fix/api-timeout
```

---

## 🎯 Quick Reference

### First Time Setup:
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

### Daily Updates:
```powershell
git add .
git commit -m "Description of changes"
git push
```

### Pull Latest Changes:
```powershell
git pull origin main
```

---

## ✅ Verification Checklist

After pushing to GitHub, verify:
- [ ] All files are visible on GitHub
- [ ] `.env` is NOT in the repository
- [ ] README.md displays correctly
- [ ] Repository is set to correct visibility (public/private)
- [ ] All documentation files are present
- [ ] No sensitive data is exposed

---

## 🆘 Need Help?

- GitHub Docs: https://docs.github.com
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf
- GitHub Desktop (GUI): https://desktop.github.com

Ready to push? Follow the steps above! 🚀
