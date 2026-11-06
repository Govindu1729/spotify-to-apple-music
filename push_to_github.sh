#!/bin/bash

# ============================================================================
# Spotify to Apple Music - GitHub Push Script
# This script will:
# 1. Install GitHub CLI if not present
# 2. Authenticate with GitHub
# 3. Create a new repository
# 4. Push the code
# ============================================================================

set -e  # Exit on error

echo "============================================================"
echo "🚀 GitHub Push Automation"
echo "============================================================"
echo ""

# Step 1: Check if GitHub CLI is installed
echo "🔍 Checking for GitHub CLI (gh)..."
if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI not found. Installing..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo '   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        exit 1
    fi
    
    # Install GitHub CLI
    echo "📦 Installing GitHub CLI via Homebrew..."
    brew install gh
    echo "✅ GitHub CLI installed successfully!"
else
    echo "✅ GitHub CLI is already installed."
fi

echo ""

# Step 2: Check authentication
echo "🔐 Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "⚠️  Not authenticated with GitHub. Let's log in..."
    echo ""
    echo "Please choose your preferred authentication method:"
    echo "  - Press 1 for GitHub.com"
    echo "  - Press 2 for GitHub Enterprise"
    echo ""
    gh auth login
else
    echo "✅ Already authenticated with GitHub."
fi

echo ""

# Step 3: Get repository details
echo "📝 Repository Configuration"
echo "============================"

# Get current directory name as default repo name
DEFAULT_REPO_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr '_' '-')
echo "Default repository name: $DEFAULT_REPO_NAME"

read -p "Enter repository name [$DEFAULT_REPO_NAME]: " REPO_NAME
REPO_NAME=${REPO_NAME:-$DEFAULT_REPO_NAME}

read -p "Enter repository description [Spotify to Apple Music migration tool]: " REPO_DESC
REPO_DESC=${REPO_DESC:-"Spotify to Apple Music migration tool"}

read -p "Make repository public? (y/n) [y]: " IS_PUBLIC
IS_PUBLIC=${IS_PUBLIC:-y}

if [[ $IS_PUBLIC == "y" || $IS_PUBLIC == "Y" ]]; then
    VISIBILITY="public"
else
    VISIBILITY="private"
fi

echo ""
echo "Creating repository: $REPO_NAME ($VISIBILITY)"
echo "Description: $REPO_DESC"
echo ""

# Step 4: Create repository
echo "🏗️  Creating GitHub repository..."
if gh repo view "$REPO_NAME" &> /dev/null; then
    echo "⚠️  Repository '$REPO_NAME' already exists!"
    read -p "Do you want to use the existing repository? (y/n): " USE_EXISTING
    if [[ $USE_EXISTING != "y" && $USE_EXISTING != "Y" ]]; then
        echo "❌ Please choose a different repository name."
        exit 1
    fi
    REPO_URL="https://github.com/$(gh api user -q .login)/$REPO_NAME.git"
else
    if [[ $IS_PUBLIC == "y" || $IS_PUBLIC == "Y" ]]; then
        gh repo create "$REPO_NAME" --public --description "$REPO_DESC" --source=. --remote=origin --push
    else
        gh repo create "$REPO_NAME" --private --description "$REPO_DESC" --source=. --remote=origin --push
    fi
    echo ""
    echo "✅ Repository created successfully!"
fi

echo ""

# Step 5: Ensure remote is configured
echo "🔗 Configuring git remote..."
if ! git remote get-url origin &> /dev/null; then
    # Get GitHub username
    GITHUB_USER=$(gh api user -q .login)
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "✅ Remote 'origin' added."
else
    echo "✅ Remote 'origin' already configured."
fi

echo ""

# Step 6: Initialize git if needed and commit
echo "📦 Preparing git repository..."

# Check if .git exists
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Configure git user if not set
if ! git config user.name &> /dev/null; then
    echo "⚠️  Git user name not configured."
    read -p "Enter your name: " GIT_NAME
    git config user.name "$GIT_NAME"
fi

if ! git config user.email &> /dev/null; then
    echo "⚠️  Git user email not configured."
    read -p "Enter your email: " GIT_EMAIL
    git config user.email "$GIT_EMAIL"
fi

# Add all files
echo "Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "✅ No changes to commit (files already committed)."
else
    echo "Committing files..."
    git commit -m "Initial commit: Spotify to Apple Music migration tool"
fi

echo ""

# Step 7: Push to GitHub
echo "🚀 Pushing to GitHub..."
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    CURRENT_BRANCH="main"
    git branch -M main
fi

# Try to push, handle case where remote already has commits
if git push -u origin "$CURRENT_BRANCH" 2>/dev/null; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
else
    echo "⚠️  Push failed. Remote might already have commits."
    echo "Trying to pull and merge..."
    git pull origin "$CURRENT_BRANCH" --allow-unrelated-histories --no-edit
    git push -u origin "$CURRENT_BRANCH"
    echo ""
    echo "✅ Successfully pushed to GitHub!"
fi

echo ""
echo "============================================================"
echo "🎉 All Done!"
echo "============================================================"
echo ""
echo "Repository URL: https://github.com/$(gh api user -q .login)/$REPO_NAME"
echo ""
echo "Next steps:"
echo "  - Share the repository URL with others"
echo "  - Add more features and push again with: git push"
echo ""
