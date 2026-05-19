# Contributing to FINDER

Thank you for your interest in contributing to FINDER! This document provides guidelines and instructions for contributing to this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Get Started](#how-to-get-started)
- [Creating Issues](#creating-issues)
- [Taking/Assigning Issues](#takingassigning-issues)
- [Making Commits](#making-commits)
- [Creating Pull Requests](#creating-pull-requests)
- [Development Workflow](#development-workflow)

## Code of Conduct

By participating in this project, you agree to be respectful and constructive in all interactions. We value diverse perspectives and collaborative problem-solving.

## How to Get Started

### Prerequisites
- Python 3.10+ (recommended: Python 3.12)
- pip (Python package manager)
- PostgreSQL 14+
- Git
- Docker & Docker Compose (for PostgreSQL)
- Virtual environment tool (venv built-in to Python)

### Setup Local Development

1. **Fork the repository** (if you're not a direct collaborator)
   ```bash
   git clone https://github.com/YOUR_USERNAME/FINDER-WEB.git
   cd FINDER-WEB
   ```

2. **Add upstream remote** (to keep your fork in sync)
   ```bash
   git remote add upstream https://github.com/Rafhrss/FINDER-WEB.git
   ```

3. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements/development.txt
   ```

6. **Start PostgreSQL container**
   ```bash
   docker compose up -d postgres
   ```

7. **Run migrations**
   ```bash
   python manage.py migrate
   ```

8. **Create seed data (optional)**
   ```bash
   python manage.py seed_dummy_data --reset
   ```

9. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

10. **Run the development server**
    ```bash
    python manage.py runserver
    ```

Server akan berjalan di `http://localhost:8000`

### Code Style & Linting

This project uses standard Django/Python conventions. Before committing:

```bash
# Check for issues (optional: install flake8, pylint)
python manage.py check

# Format code (optional: install black)
black .
```

## Creating Issues

### Issue Title Format
Use the following format for consistency:
```
[FIN-XX] <Brief Description>
```

**Examples:**
- ✅ `[FIN-01] Feature: Add image upload to reports`
- ✅ `[FIN-02] Bug: Fix chat expiration logic`
- ✅ `[FIN-03] Docs: Add API endpoint documentation`
- ❌ `Add image upload`
- ❌ `Bug fix`

**Notes:**
- `FIN` stands for "FINDER"
- Use sequential numbering (FIN-1, FIN-2, FIN-3, etc.)
- Keep descriptions concise but descriptive

### Issue Body Structure

Use the following sections in issue descriptions:

1. **Description** - What is this issue about?
2. **Requirements** - What needs to be done? (use subsections if complex)
3. **Acceptance Criteria** - How to verify it's complete? (use checkboxes)
4. **Files to Modify** - Which files need changes? (if applicable)
5. **Related Issues** - Link to related issues/PRs if applicable

### Labels

When creating issues, use appropriate labels:
- **enhancement**: New features or improvements
- **bug**: Bug fixes
- **feature**: New feature development
- **backend**: Backend/Django changes
- **frontend**: Frontend/Web template changes
- **api**: API endpoint changes
- **refactor**: Code refactoring
- **documentation**: Documentation updates
- **database**: Database/model changes
- **question**: Questions or clarifications needed

### Issue Template Example

```markdown
## Description
Brief description of what this issue is about. Include context about the problem or feature request.

## Requirements
- Requirement 1
- Requirement 2
- Requirement 3

## Files to Modify
- `apps/reports/models.py`
- `api/v1/reports/views.py`
- `api/v1/reports/serializers.py`

## Acceptance Criteria
- [ ] Criterion 1 is met
- [ ] Criterion 2 is met
- [ ] Criterion 3 is met
- [ ] Tests pass: `python manage.py test`
- [ ] No linting errors: `python manage.py check`

## Related
Issue #1, Issue #5
```

## Taking/Assigning Issues

### How to Assign an Issue to Yourself

1. **Find an issue** you want to work on
2. **Leave a comment** on the issue: "I'll take this" or "Let me work on this"
3. **Wait for confirmation** from maintainers (or they may auto-assign)
4. **Create a branch** with the issue number (see [Branch Naming](#branch-naming))

### Guidelines

- **One person per issue**: Don't work on an issue someone else is already assigned to
- **Ask for clarification**: If an issue is unclear, ask in the comments
- **Communicate delays**: If you get stuck, update the issue with your progress
- **Respect issue assignments**: Always check if someone is already working on it
- **Estimated time**: Include when you expect to complete the task

## Making Commits

### Commit Message Format

Use the conventional commit format:
```
type(scope): message
```

### Commit Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, imports, etc.)
- **refactor**: Code refactoring without changing functionality
- **perf**: Performance improvements
- **test**: Test-related changes
- **chore**: Build process, dependencies, tooling

### Scope

The scope should specify which part of the codebase is affected:
- `users`: User models, authentication
- `reports`: Report CRUD functionality
- `chats`: Chat/messaging features
- `api`: API endpoints
- `web`: Django templates, web views
- `models`: Database models
- `services`: Business logic services
- `selectors`: Database query selectors
- `settings`: Configuration files
- `admin`: Django admin customization
- `migrations`: Database migrations
- `docs`: Documentation

### Message

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter
- No period at the end
- Keep it concise but descriptive
- Reference issue number if applicable

### Examples

```bash
# Good commit messages
git commit -m "feat(reports): add image upload to report creation"
git commit -m "fix(chats): correct chat expiration logic for >7 days"
git commit -m "docs(api): add complete endpoint documentation"
git commit -m "refactor(services): simplify user authentication service"
git commit -m "perf(reports): optimize report list query with select_related"
git commit -m "test(chats): add unit tests for chat expiration"
git commit -m "chore(requirements): update Django to 5.0"

# Bad commit messages
git commit -m "Fixed stuff"
git commit -m "Changes"
git commit -m "WIP"
git commit -m "update"
```

## Creating Pull Requests

### Branch Naming

Use the following format for branch names:
```
FIN-xx
```

**Examples:**
```
FIN-01
FIN-02
FIN-15
```

This makes it easy to track issues and maintain organization.

### Before You Open a PR

- [ ] Application runs locally without errors: `python manage.py runserver`
- [ ] Migrations applied: `python manage.py migrate`
- [ ] Django checks pass: `python manage.py check`
- [ ] Changes are related to a single issue
- [ ] Branch is up-to-date with `main`
- [ ] Commits follow the [commit message format](#making-commits)
- [ ] No hardcoded credentials or secrets in code

### Step-by-Step PR Creation

1. **Sync with main branch**
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Create a work branch**
   ```bash
   git checkout -b FIN-xx
   ```

3. **Make your changes and commit**
   ```bash
   git add .
   git commit -m "type(scope): description"
   ```

4. **Verify everything works locally**
   ```bash
   python manage.py check
   python manage.py migrate
   python manage.py runserver
   ```

5. **Push to your fork**
   ```bash
   git push -u origin FIN-xx
   ```

6. **Create a Pull Request** on GitHub with:
   - **Title**: Use the same format as issues: `[FIN-xx] Brief description`
   - **Description**: Include:
     - Summary of changes
     - Related issue reference (e.g., `Closes #FIN-01`)
     - Files changed
     - Testing notes
     - Any breaking changes or migration steps required

### PR Template Example

```markdown
## Description
Brief summary of changes made and why they were necessary.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Enhancement
- [ ] Documentation
- [ ] Refactoring
- [ ] Database migration

## Related Issue
Closes #FIN-01

## Changes Made
- Change 1
- Change 2
- Change 3

## Files Changed
- `apps/reports/models.py`
- `api/v1/reports/views.py`
- `api/v1/reports/serializers.py`

## How Has This Been Tested?
- [ ] Tested locally with `python manage.py runserver`
- [ ] Migrations applied successfully
- [ ] Django checks pass: `python manage.py check`
- [ ] Tested with seed data: `python manage.py seed_dummy_data --reset`
- [ ] API endpoints tested (with cURL or Postman)

## Testing Instructions
```bash
# Run migrations
python manage.py migrate

# Create test data
python manage.py seed_dummy_data --reset

# Test endpoint
curl -X GET http://localhost:8000/api/v1/reports/ \
  -H "Authorization: Token <token>"
```

## Screenshots (if applicable)
<!-- Add screenshots or screen recordings for web/API changes -->

## Checklist
- [ ] My code follows Django/Python conventions
- [ ] I have performed a self-review
- [ ] I have commented complex areas of code
- [ ] Django checks pass: `python manage.py check`
- [ ] Application runs without errors
- [ ] No secrets or credentials in code
- [ ] Database migrations are included (if needed)
```

### PR Review Process

1. **Author submits PR** with all required information
2. **Maintainers review** the code for:
   - Code quality and style
   - Logic correctness
   - Adherence to architecture (services/selectors pattern)
   - Security issues
   - Performance considerations
3. **Address feedback** if changes are requested
4. **Maintainers merge** when approved

## Development Workflow

### Project Architecture Overview

```
FINDER-WEB/
├── apps/              # Business logic & models
│   ├── users/         # User authentication & profile
│   ├── reports/       # Report CRUD logic
│   ├── chats/         # Chat & messaging logic
│   └── core/          # Shared utilities
├── api/v1/            # REST API endpoints
│   ├── users/         # Auth endpoints
│   ├── reports/       # Report endpoints
│   └── chats/         # Chat endpoints
├── web/               # Django template views
│   ├── views/         # View handlers
│   └── templates/     # HTML templates
├── config/            # Settings & configuration
│   └── settings/      # base, development, production
└── requirements/      # Dependencies
```

**Key Architecture Principles:**
- **Services**: All business logic goes in `apps/{app}/services.py`
- **Selectors**: Database queries go in `apps/{app}/selectors.py`
- **Views**: API/Web views are thin wrappers around services
- **Serializers**: DRF serializers for API data validation
- **Models**: Domain models with validation

### Complete Workflow Example

```bash
# 1. Sync your local main with upstream
git checkout main
git pull upstream main

# 2. Create a new branch for the issue
git checkout -b FIN-05

# 3. Make your changes
# ... edit files in apps/, api/, web/ ...

# 4. Verify everything works
python manage.py migrate
python manage.py check
python manage.py runserver

# 5. Test your changes
# - Test web interface: http://localhost:8000
# - Test API endpoints with curl or Postman
# - Verify with seed data: python manage.py seed_dummy_data --reset

# 6. Stage and commit changes
git add .
git commit -m "feat(reports): add image upload to report creation"

# 7. Push to your fork
git push -u origin FIN-05

# 8. Open a PR on GitHub
# Go to https://github.com/Rafhrss/FINDER-WEB and click "New Pull Request"
```

### Keeping Your Fork Updated

```bash
# Fetch updates from upstream
git fetch upstream

# Rebase your branch on top of upstream/main
git rebase upstream/main

# Push the updated branch
git push -f origin your-branch-name
```

### Testing Your Changes

```bash
# Run Django checks
python manage.py check

# Create/reset seed data
python manage.py seed_dummy_data --reset

# Test API with curl
curl -X GET http://localhost:8000/api/v1/reports/ \
  -H "Authorization: Token YOUR_TOKEN"

# Access web interface
# Open http://localhost:8000 in browser

# Check Django admin
# Open http://localhost:8000/admin
```

## Troubleshooting

### Issue: "Port 5432 already in use"
```bash
# Kill the PostgreSQL container that's using the port
docker ps  # Find the container ID
docker stop <container-id>

# Or change the port in docker-compose.yml and .env
# Then restart
docker compose up -d postgres
```

### Issue: "ModuleNotFoundError: No module named..."
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements/development.txt
```

### Issue: "Database connection error"
```bash
# Check if PostgreSQL container is running
docker ps

# Check .env file has correct DB credentials
cat .env

# Run migrations
python manage.py migrate
```

### Issue: "Branch is behind main"
```bash
git fetch upstream
git rebase upstream/main
git push -f origin your-branch-name
```

### Issue: "Merge conflicts"
1. Update your branch: `git fetch upstream && git rebase upstream/main`
2. Resolve conflicts in your editor
3. Stage resolved files: `git add .`
4. Continue rebase: `git rebase --continue`
5. Push: `git push -f origin your-branch-name`

### Issue: "Invalid email domain validation"
```bash
# When testing with non-@umkt.ac.id email
# Use test email: test@umkt.ac.id
# Email validation is enforced in:
# - apps/users/models.py
# - apps/users/services.py
```

## Project Guidelines

### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Django Best Practices
- Keep models thin (use services for logic)
- Use querysets efficiently (select_related, prefetch_related)
- Write database queries in selectors
- Use DRF serializers for API validation
- Add docstrings to complex functions

### Security
- Never commit `.env` files with real credentials
- Use `@umkt.ac.id` email validation for tests
- Don't hardcode secrets
- Validate user input in serializers
- Check ownership in services before modifications

### Documentation
- Update README.md if adding new setup steps
- Document new API endpoints
- Add docstrings to complex business logic
- Update CONTRIBUTING.md if workflow changes

## Questions?

If you have questions or need clarification:
- Check existing issues and PRs
- Leave a comment on the issue
- Ask maintainers for help
- Read the README.md and API documentation

## Thank You!

Thank you for contributing to FINDER! Your efforts help make this project better for everyone. We appreciate your time and dedication to improving the platform for our campus community.

---

**Happy contributing! 🚀**
