#!/bin/bash
# File: sanity_test.sh
# Sanity test for Auth Service API endpoints using test environment

set -e

# Load .env variables
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found! Exiting..."
    exit 1
fi

# Use test variables if present
if [ ! -z "$TEST_BASE_URL" ]; then
    FULL_BASE_URL="$TEST_BASE_URL:$PORT/api/v1"
else
    FULL_BASE_URL="${BASE_URL}:${PORT}/api/v1"
fi

# Utility function for curl requests
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
REGISTER_DATA='{"email":"testuser@example.com","password":"TestPass123"}'
LOGIN_DATA='{"email":"testuser@example.com","password":"TestPass123"}'

# Register
test_endpoint POST "$FULL_BASE_URL/auth/register" "$REGISTER_DATA"

# Login and capture JWT tokens
LOGIN_RESPONSE=$(curl -s -X POST "$FULL_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "$LOGIN_DATA")

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.access_token')
REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.refresh_token')

if [ "$ACCESS_TOKEN" == "null" ] || [ -z "$ACCESS_TOKEN" ]; then
    echo "Login failed! Cannot continue sanity tests."
    exit 1
fi

USER_HEADERS="-H \"Authorization: Bearer $ACCESS_TOKEN\""

# ------------------------------
# 3. Users Endpoints
# ------------------------------
test_endpoint GET "$FULL_BASE_URL/users/user-data" "" "$USER_HEADERS"
test_endpoint GET "$FULL_BASE_URL/users/profile" "" "$USER_HEADERS"

# ------------------------------
# 4. Admin Endpoints
# ------------------------------
# For CI, you can use a predefined admin account
ADMIN_LOGIN_DATA='{"email":"admin@example.com","password":"AdminPass123"}'

ADMIN_RESPONSE=$(curl -s -X POST "$FULL_BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d "$ADMIN_LOGIN_DATA")

ADMIN_TOKEN=$(echo "$ADMIN_RESPONSE" | jq -r '.data.access_token')
ADMIN_HEADERS="-H \"Authorization: Bearer $ADMIN_TOKEN\""

test_endpoint GET "$FULL_BASE_URL/admin/dashboard" "" "$ADMIN_HEADERS"
test_endpoint GET "$FULL_BASE_URL/admin/user-data" "" "$ADMIN_HEADERS"

echo "Sanity test completed!"
