# Auth Service – Full Task List

## ✅ 1. Project Setup
- [x] Scaffold FastAPI project  
- [x] Configure PostgreSQL  
- [x] Setup .env for configs  
- [x] Create database session (AsyncSession)  
- [x] Configure Alembic for migrations  

## ✅ 2. Core Auth & Users
- [x] User model (User)  
- [x] Fields: id, email, hashed_password, role, is_active, is_superuser, created_at, updated_at  
- [x] CRUD operations  
- [x] get_user_by_email, create_user, etc.  
- [x] Pydantic schemas  
- [x] UserCreate, UserLogin, etc.  

## ✅ 3. JWT Authentication
- [x] Implement access + refresh tokens  
- [x] create_access_token, create_refresh_token, decode_token  
- [x] Login endpoint issues both tokens  
- [x] Refresh endpoint issues new access token  

## ✅ 4. RBAC / Roles
- [x] Enum for UserRole (USER, ADMIN)  
- [x] Include role in JWT payload  
- [x] require_roles dependency for endpoint protection  
- [x] Admin-only and user-or-admin endpoints  

## ✅ 5. Tests & Quality
- [x] Unit & integration tests  
- [x] JWT flows, refresh tokens, role enforcement  
- [x] pytest for async endpoints  
- [x] mypy type checking  
- [x] pylint linting  
- [x] Code documentation  

## ⏳ 6. Remaining Enhancements
- [x] Refresh token revocation / blacklist (Redis or DB-backed)  
- [x] Rate limiting / brute-force prevention (Redis recommended for fast counter storage)  
- [x] Detailed OpenAPI documentation  
- [ ] CI/CD linting & test automation  
    - [x] Dockerize the test from inside infra/ directory 
- [x] Dockerize the service from inside infra/ directory  
- [ ] Build container image  
- [x] Configure environment variables (DB, JWT, Redis)  
- [ ] Kubernetes deployment manifests  
- [ ] Deployment, Service, ConfigMap, Secret  
- [ ] Include Redis as sidecar or external service  

## ⏳ 7. Social Login / OAuth 2.0
- [ ] Integrate providers: Google, Facebook, GitHub, Apple  
- [ ] Handle OAuth flow:  
  - [ ] Frontend redirects to provider login  
  - [ ] Provider returns authorization code / token  
  - [ ] Exchange code for user info  
- [ ] Auto-create new user if first-time login  
- [ ] Issue standard JWT access + refresh tokens  
- [ ] Include role in JWT payload  
- [ ] Optional: Link multiple social accounts to the same user  
