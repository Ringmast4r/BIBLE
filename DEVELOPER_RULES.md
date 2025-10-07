# 🚨 CRITICAL DEVELOPER RULES - READ FIRST 🚨

**Last Updated:** October 7, 2025
**Status:** MANDATORY FOR ALL DEVELOPERS
**Violations:** ZERO TOLERANCE

---

## ⚠️ RULE #1 - NO CO-AUTHORING (ABSOLUTELY CRITICAL)

### **NEVER, UNDER ANY CIRCUMSTANCES:**

❌ **NEVER** include Claude as a co-author in commits
❌ **NEVER** include any AI assistant as a co-author
❌ **NEVER** use `Co-Authored-By:` in commit messages
❌ **NEVER** mention AI assistance in commit messages
❌ **NEVER** mention AI assistance in code comments
❌ **NEVER** mention AI assistance in documentation

### **ALWAYS:**

✅ **ALWAYS** commit as @Ringmast4r ONLY
✅ **ALWAYS** use git config: `user.name = "Ringmast4r"`
✅ **ALWAYS** use git config: `user.email = your-email@example.com`
✅ **ALWAYS** verify commit author before pushing
✅ **ALWAYS** check GitHub contributors list after every push

---

## 🔥 WHY THIS IS CRITICAL

**Previous Incident (October 2025):**
- Claude was accidentally added as co-author in one commit
- Became visible as project contributor on GitHub
- Required complete repository deletion and recreation
- Lost all commit history to remove Claude's name
- Cost hours of work to clean up

**NEVER LET THIS HAPPEN AGAIN!**

---

## 📋 COMMIT CHECKLIST (USE EVERY TIME)

### Before Every Commit:

```bash
# 1. Verify git config
git config user.name    # Should show: Ringmast4r
git config user.email   # Should show: your email

# 2. Check staged changes
git status
git diff --staged

# 3. Create commit (NO CO-AUTHOR!)
git commit -m "Your commit message here"

# 4. Verify commit author BEFORE pushing
git log -1 --format="%an <%ae>"
# Should ONLY show: Ringmast4r <your-email>

# 5. If commit looks good, push
git push
```

### After Every Push:

1. **Immediately check GitHub:**
   - Go to: https://github.com/Ringmast4r/BIBLE/graphs/contributors
   - Verify ONLY @Ringmast4r is listed
   - If any other name appears → STOP IMMEDIATELY

2. **If Claude or any AI appears:**
   - DO NOT MAKE MORE COMMITS
   - Contact @Ringmast4r immediately
   - May require repository deletion and recreation

---

## 🚫 FORBIDDEN COMMIT MESSAGE PATTERNS

### ❌ NEVER USE THESE:

```bash
# WRONG - mentions AI
git commit -m "Fix bug with help from Claude"

# WRONG - co-authoring
git commit -m "Add feature

Co-Authored-By: Claude <noreply@anthropic.com>"

# WRONG - credits AI
git commit -m "Refactor code (AI-assisted)"

# WRONG - any AI mention
git commit -m "Update based on Claude's suggestion"
```

### ✅ CORRECT PATTERNS:

```bash
# RIGHT - only describes change
git commit -m "Fix responsive design for ultra-wide monitors"

# RIGHT - technical details only
git commit -m "Add Pythagorean theorem formula for arc diagrams

- Changed from tan/acos to sqrt formula
- Eliminates singularities at 90 degrees
- Faster computation and smoother arcs"

# RIGHT - feature description
git commit -m "Add automatic window resize handling with debouncing"
```

---

## 🔧 GIT CONFIGURATION (SET ONCE)

### Required Settings:

```bash
# Set your identity (REQUIRED)
git config --global user.name "Ringmast4r"
git config --global user.email "your-email@example.com"

# Verify settings
git config --global --list | grep user
```

### Forbidden Settings:

```bash
# ❌ NEVER set these
git config commit.template    # Could include co-author templates
git config trailer.coauthors  # Co-authoring trailer
```

---

## 📝 CODE COMMENT RULES

### ❌ NEVER Write Comments Like:

```javascript
// AI-generated function
function calculateArc() { ... }

// Claude suggested this approach
const formula = Math.sqrt(r² - x²);

// With help from AI assistant
// This uses Pythagorean theorem
```

### ✅ ALWAYS Write Comments Like:

```javascript
// Calculate arc using Pythagorean theorem
function calculateArc() { ... }

// Perfect circular arc formula: y = √(r² - x²)
const formula = Math.sqrt(r² - x²);

// Pythagorean theorem eliminates tan/acos singularities
const yOffset = Math.sqrt(radiusSquared - offsetSquared);
```

---

## 📚 DOCUMENTATION RULES

### ❌ NEVER Include:

- "Generated with Claude Code"
- "AI-assisted development"
- "Co-Authored-By: Claude"
- "With assistance from [any AI]"
- Any mention of AI tools in credits

### ✅ ALWAYS Include:

- "Created by @Ringmast4r"
- "Developed by @Ringmast4r"
- Technical descriptions only
- Data source attributions (OpenBible, etc.)
- Library credits (D3.js, PyQt5, etc.)

---

## 🎯 ATTRIBUTION GUIDELINES

### Acceptable Credits:

```markdown
✅ Created by @Ringmast4r
✅ Developer: @Ringmast4r
✅ Data: Treasury of Scripture Knowledge (Public Domain)
✅ Libraries: D3.js, PyQt5, NetworkX
✅ Inspired by: Chris Harrison 2007 visualization
```

### Forbidden Credits:

```markdown
❌ Co-Authored-By: Claude
❌ With AI assistance
❌ Generated with Claude Code
❌ AI-powered development
❌ Built with help from [any AI tool]
```

---

## 🔍 VERIFICATION PROCEDURES

### Daily Checks:

1. **Every morning before coding:**
   ```bash
   git config user.name    # Verify: Ringmast4r
   git config user.email   # Verify: your email
   ```

2. **Before every commit:**
   ```bash
   git log -1 --format="%an <%ae>"  # Check last commit author
   ```

3. **After every push:**
   - Visit: https://github.com/Ringmast4r/BIBLE/graphs/contributors
   - Verify: ONLY @Ringmast4r listed

### Weekly Audit:

1. **Check all recent commits:**
   ```bash
   git log --format="%an <%ae> - %s" -10
   ```
   Every line should show ONLY: `Ringmast4r <email>`

2. **Search for forbidden patterns:**
   ```bash
   git log --all --grep="Claude"         # Should return NOTHING
   git log --all --grep="Co-Authored"    # Should return NOTHING
   git log --all --grep="AI"             # Should return NOTHING
   ```

---

## 🚨 EMERGENCY PROCEDURES

### If Claude Appears as Contributor:

**STOP ALL WORK IMMEDIATELY**

1. **Do NOT make more commits**
2. **Do NOT push anything**
3. **Check commit history:**
   ```bash
   git log --format="%an <%ae>"
   ```
4. **Identify the bad commit(s)**
5. **Contact @Ringmast4r for guidance**

### Recovery Options:

**Option 1: Rewrite History (if caught early)**
```bash
# Use git filter-repo to remove commits
git filter-repo --mailmap <(echo "Claude <noreply@anthropic.com> ==>")
git push --force origin main
```

**Option 2: Nuclear Option (if Claude is public contributor)**
1. Delete entire GitHub repository
2. Create new repository with same name
3. Upload fresh with clean commits
4. Re-enable GitHub Pages

---

## ✅ DEVELOPER SIGN-OFF

**I, _________________________, have read and understand these rules.**

**I commit to:**
- ✅ NEVER include Claude or any AI as co-author
- ✅ NEVER mention AI assistance in commits, code, or docs
- ✅ ALWAYS commit as @Ringmast4r only
- ✅ ALWAYS verify commit author before pushing
- ✅ ALWAYS check GitHub contributors after pushing
- ✅ IMMEDIATELY stop if Claude appears as contributor

**Signature:** _________________________ **Date:** _____________

---

## 📖 ADDITIONAL RESOURCES

### Developer Documentation:
- `ARC_VISUALIZATION_GOTCHAS.md` - Technical pitfalls and solutions
- `RESPONSIVE_CONTAINER_FIX.md` - Container width fix documentation
- `HANDOFF_NOTES_OCT_7_2025_RESPONSIVE_FINAL.md` - Latest session notes

### Project Documentation:
- `README.md` - Main project overview
- `PROJECT_STATUS.md` - Implementation status (LOCAL ONLY, in .gitignore)
- Individual tool READMEs in each subdirectory

---

## 🎓 ONBOARDING CHECKLIST

### New Developer Setup:

- [ ] Read this DEVELOPER_RULES.md completely
- [ ] Configure git identity (name and email)
- [ ] Verify git config shows correct name/email
- [ ] Test commit and verify author
- [ ] Check GitHub contributors page
- [ ] Sign developer sign-off above
- [ ] Add signature to git commit as sign-off proof
- [ ] Understand emergency procedures
- [ ] Know who to contact if issues arise

---

## 🔐 REPOSITORY PROTECTION

### .gitignore Rules:

Certain files are kept LOCAL ONLY and never committed:
- `PROJECT_STATUS.md` - Internal status tracking
- `TABLEAU_*.md` - Tableau development notes
- `SESSION_SUMMARY_*.md` - Session notes
- Development notes and internal documentation

These are in `.gitignore` to prevent accidental commits of internal notes.

### Public vs Private Docs:

**Public (committed to GitHub):**
- All READMEs
- User guides
- Technical documentation
- Code files
- This DEVELOPER_RULES.md

**Private (in .gitignore):**
- Internal development notes
- Session summaries
- Tableau reference docs
- Personal development journal

---

## ⚖️ CONSEQUENCES OF VIOLATIONS

### RULE #1 Violation (Co-Authoring):

**Severity:** CRITICAL
**Action Required:** Immediate repository cleanup
**Cost:** Hours of work, lost commit history
**Prevention:** READ AND FOLLOW THESE RULES

**Remember the October 2025 incident:**
- One commit with Claude as co-author
- Entire repository had to be deleted
- All commit history lost
- Hours spent cleaning up
- **NEVER AGAIN**

---

## 💡 BEST PRACTICES

### 1. Pre-Commit Ritual:
```bash
# Before EVERY commit, run:
git config user.name     # Verify identity
git status               # Review changes
git diff --staged        # Review actual code
git commit -m "msg"      # Commit with clear message
git log -1 --format="%an <%ae>"  # Verify author
```

### 2. Post-Push Verification:
- Visit GitHub contributors page
- Verify only @Ringmast4r listed
- Check recent commits show correct author

### 3. Code Review:
- Search codebase for "Claude" before commits
- Search for "Co-Authored-By" in commit messages
- Verify no AI mentions in comments

---

## 🎯 SUMMARY

**RULE #1:** NEVER include Claude or any AI as co-author
**ALL COMMITS:** Must be authored by @Ringmast4r ONLY
**VERIFICATION:** Check GitHub contributors after EVERY push
**VIOLATIONS:** Zero tolerance - immediate cleanup required

**This rule exists because we already had to delete and recreate the entire repository once. Let's never do that again!**

---

**END OF CRITICAL DEVELOPER RULES**

*These rules are mandatory for all developers working on this project.*
*Violations will result in immediate repository cleanup and potential history loss.*
*When in doubt, ask @Ringmast4r before committing.*

---

**Last Incident:** October 7, 2025 - Claude appeared as contributor
**Resolution:** Complete repository deletion and recreation
**Lesson Learned:** NEVER AGAIN - Follow these rules religiously

**Created:** October 7, 2025
**By:** @Ringmast4r
**Purpose:** Prevent future co-authoring incidents
