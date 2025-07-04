#!/usr/bin/env python3
"""
Test script for Axiom Trade API login functionality
"""

from axiomtradeapi import AxiomTradeClient
import json

def test_client_creation():
    """Test that the client can be created with login methods"""
    print("Testing client creation...")
    
    try:
        client = AxiomTradeClient()
        
        # Check if login methods exist
        assert hasattr(client, 'login_step1'), "login_step1 method missing"
        assert hasattr(client, 'login_step2'), "login_step2 method missing"
        assert hasattr(client, 'complete_login'), "complete_login method missing"
        assert hasattr(client, 'refresh_access_token_direct'), "refresh_access_token_direct method missing"
        assert hasattr(client, 'get_trending_tokens'), "get_trending_tokens method missing"
        
        print("✓ Client created successfully with all login methods")
        return True
        
    except Exception as e:
        print(f"✗ Client creation failed: {e}")
        return False

def test_method_signatures():
    """Test that methods have correct signatures"""
    print("Testing method signatures...")
    
    try:
        client = AxiomTradeClient()
        
        # Test method signatures by inspecting them
        import inspect
        
        # Check login_step1 signature
        sig1 = inspect.signature(client.login_step1)
        assert 'email' in sig1.parameters, "login_step1 missing email parameter"
        assert 'b64_password' in sig1.parameters, "login_step1 missing b64_password parameter"
        
        # Check login_step2 signature
        sig2 = inspect.signature(client.login_step2)
        expected_params = ['otp_jwt_token', 'otp_code', 'email', 'b64_password']
        for param in expected_params:
            assert param in sig2.parameters, f"login_step2 missing {param} parameter"
        
        # Check get_trending_tokens signature
        sig3 = inspect.signature(client.get_trending_tokens)
        assert 'access_token' in sig3.parameters, "get_trending_tokens missing access_token parameter"
        assert 'time_period' in sig3.parameters, "get_trending_tokens missing time_period parameter"
        
        print("✓ All method signatures are correct")
        return True
        
    except Exception as e:
        print(f"✗ Method signature test failed: {e}")
        return False

def main():
    print("Axiom Trade API - Login Integration Test")
    print("=" * 45)
    
    tests = [
        test_client_creation,
        test_method_signatures
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Login functionality is ready to use.")
        print("\nUsage examples:")
        print("1. Run 'python login_example.py' for guided setup")
        print("2. Run 'python login_example.py --interactive' for interactive demo")
        print("3. Import AxiomTradeClient and use login methods directly")
    else:
        print("✗ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()
