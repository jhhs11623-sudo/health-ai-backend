"""
Database and Authentication Testing Script
Tests all database and auth endpoints
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def print_json(data):
    print(json.dumps(data, indent=2))

# Test data
TEST_USER = {
    "username": "testuser123",
    "email": "testuser123@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "age": 30,
    "gender": "M"
}

def test_1_register():
    """Test user registration"""
    print_test("User Registration")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json=TEST_USER
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 201:
            print_success("User registered successfully")
            return response.json().get('token')
        else:
            print_error(f"Registration failed: {response.json().get('error')}")
            return None
            
    except Exception as e:
        print_error(f"Registration test failed: {str(e)}")
        return None

def test_2_login(token=None):
    """Test user login"""
    print_test("User Login")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            token = response.json().get('token')
            print_success(f"Login successful, token: {token[:20]}...")
            return token
        else:
            print_error(f"Login failed: {response.json().get('error')}")
            return token
            
    except Exception as e:
        print_error(f"Login test failed: {str(e)}")
        return token

def test_3_get_profile(token):
    """Test getting user profile"""
    print_test("Get User Profile")
    
    if not token:
        print_error("No token available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{API_URL}/auth/profile",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            print_success("Profile retrieved successfully")
            return True
        else:
            print_error(f"Failed to get profile: {response.json().get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Get profile test failed: {str(e)}")
        return False

def test_4_update_profile(token):
    """Test updating user profile"""
    print_test("Update User Profile")
    
    if not token:
        print_error("No token available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {
            "first_name": "Updated",
            "age": 31
        }
        
        response = requests.put(
            f"{API_URL}/auth/profile",
            headers=headers,
            json=update_data
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            print_success("Profile updated successfully")
            return True
        else:
            print_error(f"Failed to update profile: {response.json().get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Update profile test failed: {str(e)}")
        return False

def test_5_add_medical_record(token):
    """Test adding medical history record"""
    print_test("Add Medical History Record")
    
    if not token:
        print_error("No token available")
        return None
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        medical_data = {
            "record_type": "general",
            "blood_type": "O+",
            "allergies": "Penicillin, Sulfa drugs",
            "medications": "Aspirin, Multivitamin",
            "blood_pressure": "120/80",
            "heart_rate": 72,
            "temperature": 98.6,
            "weight": 70.5,
            "height": 175.0,
            "consultation_notes": "Annual checkup - patient is healthy",
            "doctor_name": "Dr. John Smith",
            "symptoms": ["none"],
            "medical_conditions": ["None"]
        }
        
        response = requests.post(
            f"{API_URL}/auth/medical-history",
            headers=headers,
            json=medical_data
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 201:
            record_id = response.json().get('record', {}).get('id')
            print_success(f"Medical record added successfully (ID: {record_id})")
            return record_id
        else:
            print_error(f"Failed to add record: {response.json().get('error')}")
            return None
            
    except Exception as e:
        print_error(f"Add medical record test failed: {str(e)}")
        return None

def test_6_get_medical_history(token):
    """Test getting medical history"""
    print_test("Get Medical History")
    
    if not token:
        print_error("No token available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{API_URL}/auth/medical-history",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            total = response.json().get('total', 0)
            print_success(f"Medical history retrieved successfully ({total} records)")
            return True
        else:
            print_error(f"Failed to get history: {response.json().get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Get medical history test failed: {str(e)}")
        return False

def test_7_get_specific_record(token, record_id):
    """Test getting specific medical record"""
    print_test("Get Specific Medical Record")
    
    if not token or not record_id:
        print_error("No token or record ID available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{API_URL}/auth/medical-history/{record_id}",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            print_success("Specific record retrieved successfully")
            return True
        else:
            print_error(f"Failed to get record: {response.json().get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Get specific record test failed: {str(e)}")
        return False

def test_8_update_medical_record(token, record_id):
    """Test updating medical record"""
    print_test("Update Medical Record")
    
    if not token or not record_id:
        print_error("No token or record ID available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {
            "consultation_notes": "Updated consultation notes - patient doing well",
            "blood_pressure": "118/78"
        }
        
        response = requests.put(
            f"{API_URL}/auth/medical-history/{record_id}",
            headers=headers,
            json=update_data
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            print_success("Medical record updated successfully")
            return True
        else:
            print_error(f"Failed to update record: {response.json().get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Update medical record test failed: {str(e)}")
        return False

def test_9_change_password(token):
    """Test changing password"""
    print_test("Change Password")
    
    if not token:
        print_error("No token available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        password_data = {
            "old_password": TEST_USER["password"],
            "new_password": "NewPassword123!"
        }
        
        response = requests.post(
            f"{API_URL}/auth/change-password",
            headers=headers,
            json=password_data
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 200:
            print_success("Password changed successfully")
            # Reset password for next tests
            TEST_USER["password"] = "NewPassword123!"
            return True
        else:
            print_error(f"Failed to change password: {response.json().get('error')}")
            return False
            
    except Exception as e:
        print_error(f"Change password test failed: {str(e)}")
        return False

def test_10_invalid_token():
    """Test invalid token handling"""
    print_test("Invalid Token Handling")
    
    try:
        headers = {"Authorization": "Bearer invalid.token.here"}
        
        response = requests.get(
            f"{API_URL}/auth/profile",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print_json(response.json())
        
        if response.status_code == 401:
            print_success("Invalid token properly rejected")
            return True
        else:
            print_error("Invalid token not properly handled")
            return False
            
    except Exception as e:
        print_error(f"Invalid token test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("HEALTH AI DATABASE & AUTHENTICATION TEST SUITE")
    print(f"{'='*60}{Colors.END}")
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=2)
    except:
        print_error("Cannot connect to server. Make sure Flask server is running on port 5000")
        print_info("Run: python app.py")
        return
    
    # Run tests
    results = {}
    
    # Test 1: Register
    token = test_1_register()
    results['Registration'] = token is not None
    
    # Test 2: Login (if registration failed, we still get a token)
    if not token:
        token = test_2_login()
    else:
        test_2_login(token)
    
    results['Login'] = token is not None
    
    if token:
        # Test 3: Get Profile
        results['Get Profile'] = test_3_get_profile(token)
        
        # Test 4: Update Profile
        results['Update Profile'] = test_4_update_profile(token)
        
        # Test 5: Add Medical Record
        record_id = test_5_add_medical_record(token)
        results['Add Medical Record'] = record_id is not None
        
        # Test 6: Get Medical History
        results['Get Medical History'] = test_6_get_medical_history(token)
        
        # Test 7: Get Specific Record
        if record_id:
            results['Get Specific Record'] = test_7_get_specific_record(token, record_id)
            
            # Test 8: Update Medical Record
            results['Update Medical Record'] = test_8_update_medical_record(token, record_id)
        
        # Test 9: Change Password
        results['Change Password'] = test_9_change_password(token)
    
    # Test 10: Invalid Token
    results['Invalid Token Handling'] = test_10_invalid_token()
    
    # Print summary
    print_test("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if result else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

if __name__ == '__main__':
    main()
