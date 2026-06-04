## Description
This PR adds the MIT License to the repository and implements a Terms of Service page, including an explicit agreement link on the login pages. It resolves the legal and compliance needs specified in FIN-19.

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Enhancement
- [x] Documentation
- [ ] Refactoring
- [ ] Database migration

## Related Issue
Closes #39

## Changes Made
- Added `LICENSE` file containing the MIT License
- Created a standard DaisyUI/Tailwind Terms of Service page extending `base.html`
- Created `terms_of_service_view` and mapped to `/terms/` URL
- Updated both `account/login.html` and `socialaccount/login.html` to include the agreement text linking to the Terms of Service
- Fixed a dependency conflict issue in `requirements/base.txt` regarding `rich` and `pyiceberg` versions

## Files Changed
- `LICENSE`
- `requirements/base.txt`
- `web/urls.py`
- `web/views/home.py`
- `web/views/__init__.py`
- `web/templates/terms_of_service.html`
- `web/templates/account/login.html`
- `web/templates/socialaccount/login.html`

## How Has This Been Tested?
- [x] Tested locally with `python manage.py runserver`
- [x] Django checks pass: `python manage.py check`
- [ ] Migrations applied successfully
- [ ] Tested with seed data: `python manage.py seed_dummy_data --reset`
- [ ] API endpoints tested (with cURL or Postman)

## Testing Instructions
```bash
# Run Django checks
python manage.py check

# Run server
python manage.py runserver
```
Visit `http://localhost:8000/terms/` or check the login pages.

## Checklist
- [x] My code follows Django/Python conventions
- [x] I have performed a self-review
- [x] I have commented complex areas of code
- [x] Django checks pass: `python manage.py check`
- [x] Application runs without errors
- [x] No secrets or credentials in code
- [ ] Database migrations are included (if needed)
