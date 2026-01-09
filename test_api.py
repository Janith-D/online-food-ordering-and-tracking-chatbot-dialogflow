"""
Test script to verify the setup and basic functionality
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test if the API is running"""
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_new_order():
    """Test creating a new order"""
    print("\n2. Testing new order...")
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "new.order"
            },
            "parameters": {
                "food-item": ["Pepperoni Pizza", "Coca Cola"],
                "number": [2, 1]
            },
            "queryText": "I want 2 pizzas and 1 coke"
        },
        "session": "test-session-001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_add_to_order():
    """Test adding items to order"""
    print("\n3. Testing add to order...")
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "order.add - context: ongoing-order"
            },
            "parameters": {
                "food-item": ["French Fries"],
                "number": [1]
            },
            "queryText": "Add french fries"
        },
        "session": "test-session-001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_complete_order():
    """Test completing an order"""
    print("\n4. Testing order completion...")
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "order.complete - context: ongoing-order"
            },
            "parameters": {},
            "queryText": "Complete my order"
        },
        "session": "test-session-001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Extract order ID from response
        response_text = response.json().get("fulfillmentText", "")
        if "Order ID:" in response_text:
            order_id = response_text.split("Order ID:")[1].split(".")[0].strip()
            print(f"Created Order ID: {order_id}")
            return response.status_code == 200, order_id
        
        return response.status_code == 200, None
    except Exception as e:
        print(f"Error: {str(e)}")
        return False, None


def test_track_order(order_id):
    """Test order tracking"""
    print(f"\n5. Testing order tracking for Order ID: {order_id}...")
    payload = {
        "queryResult": {
            "intent": {
                "displayName": "track.order"
            },
            "parameters": {
                "number": order_id
            },
            "queryText": f"Track order {order_id}"
        },
        "session": "test-session-002"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/webhook", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Food Ordering Chatbot - API Tests")
    print("=" * 60)
    print("\nMake sure the server is running on http://localhost:8000")
    print("Start the server with: python main.py")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: New order
    results.append(("New Order", test_new_order()))
    
    # Test 3: Add to order
    results.append(("Add to Order", test_add_to_order()))
    
    # Test 4: Complete order
    success, order_id = test_complete_order()
    results.append(("Complete Order", success))
    
    # Test 5: Track order (if we have an order ID)
    if order_id:
        results.append(("Track Order", test_track_order(order_id)))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
