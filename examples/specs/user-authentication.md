# User Authentication

## Overview

Allow users to sign up, log in, and manage their account securely.

## User Stories

- As a new user, I want to create an account so that I can access the application
- As a returning user, I want to log in so that I can access my data
- As a logged-in user, I want to log out so that my session is secure
- As a user, I want to reset my password if I forget it

## Requirements

- [ ] Email/password registration with validation
- [ ] Email/password login with rate limiting
- [ ] Session management (JWT or session cookies)
- [ ] Logout functionality
- [ ] Password reset via email
- [ ] Input validation and sanitization

## Acceptance Criteria

- [ ] Users can register with valid email and password (min 8 chars)
- [ ] Users receive error messages for invalid input
- [ ] Login fails after 5 incorrect attempts (15 min lockout)
- [ ] Sessions expire after 24 hours of inactivity
- [ ] Password reset emails are sent within 30 seconds
- [ ] All auth endpoints have appropriate rate limiting

## Technical Notes

- Use bcrypt for password hashing (cost factor 12)
- Store sessions in Redis for scalability
- Implement CSRF protection for all state-changing operations

## Out of Scope

- Social login (OAuth) - separate spec
- Two-factor authentication - separate spec
- Account deletion - separate spec
