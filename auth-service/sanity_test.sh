#!/bin/bash
# File: sanity_test.sh
# Enhanced sanity test for Auth Service API endpoints

# Load .env variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found! Exiting..."
    exit 1
fi

# Construct base URL
FULL_BASE_URL="${BASE_URL}:${PORT}/api/v1"

# Check for jq
if ! command -v jq &> /dev/null; then
    echo "jq is required but not installed. Install it and rerun."
    exit 1
fi

# Utility function to make curl requests
function test_endpoint() {
    local METHOD=$1
    local URL=$2
    local DATA=$3
    local HEADERS=$4
    echo "----------------------------------------"
    echo "Testing $METHOD $URL"
    if [ -z "$DATA" ]; then
        curl -s -w "\nHTTP Status: %{http_code}\n" -X $METHOD "$URL" $HEADERS
    else
        curl -s -w "\nHTTP Status: %{http_code}\n" -X $METHOD "$URL" \
             -H "Content-Type: application/json" $HEADERS \
             -d "$DATA"
    fi
    echo ""
}

# ------------------------------
# 1. Health Endpoints
# ------------------------------
test_endpoint GET "$FULL_BASE_URL/health/server"
test_endpoint GET "$FULL_BASE_URL/health/database"
test_endpoint GET "$FULL_BASE_URL/health/redis"
test_endpoint GET "$FULL_BASE_URL/health/"

# ------------------------------
# 2. Auth Endpoints
# ------------------------------
EMAIL="testuser@example.com"
PASSWORD="TestPass123"

REGISTER_DATA="{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}"
LOGIN_DATA="{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}"

echo "Registering test user..."
test_endpoint POST "$FULL_BASE_URL/auth/register" "$REGISTER_DATA"

echo "Logging in test user..."
LOGIN_RESPONSE=$(curl -s -X POST "$FULL_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "$LOGIN_DATA")

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.access_token // empty')
REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.refresh_token // empty')

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Login failed, cannot extract access token!"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi

echo "Access token extracted successfully."

# ------------------------------
# 3. Users Endpoints
# ------------------------------
USER_HEADERS="-H \"Authorization: Bearer $ACCESS_TOKEN\""
test_endpoint GET "$FULL_BASE_URL/users/user-data" "" "$USER_HEADERS"
test_endpoint GET "$FULL_BASE_URL/users/profile" "" "$USER_HEADERS"

# ------------------------------
# 4. Token Refresh & Logout
# ------------------------------
REFRESH_DATA="{\"refresh_token\":\"$REFRESH_TOKEN\"}"
LOGOUT_DATA="{\"refresh_token\":\"$REFRESH_TOKEN\"}"

test_endpoint POST "$FULL_BASE_URL/auth/refresh" "$REFRESH_DATA"
test_endpoint POST "$FULL_BASE_URL/auth/logout" "$LOGOUT_DATA"

# ------------------------------
# 5. Admin Endpoints (requires admin JWT)
# ------------------------------
# Optional: provide admin credentials in .env for testing
if [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
    ADMIN_LOGIN_DATA="{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}"
    ADMIN_RESPONSE=$(curl -s -X POST "$FULL_BASE_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d "$ADMIN_LOGIN_DATA")
    ADMIN_TOKEN=$(echo "$ADMIN_RESPONSE" | jq -r '.data.access_token // empty')
    if [ -n "$ADMIN_TOKEN" ]; then
        ADMIN_HEADERS="-H \"Authorization: Bearer $ADMIN_TOKEN\""
        test_endpoint GET "$FULL_BASE_URL/admin/dashboard" "" "$ADMIN_HEADERS"
        test_endpoint GET "$FULL_BASE_URL/admin/user-data" "" "$ADMIN_HEADERS"
    else
        echo "Admin login failed, skipping admin endpoint tests."
    fi
else
    echo "ADMIN_EMAIL and ADMIN_PASSWORD not set in .env, skipping admin tests."
fi

echo "Sanity test completed!"
