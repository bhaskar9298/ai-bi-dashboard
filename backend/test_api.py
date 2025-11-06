"""
Test Script for AI BI Dashboard
Tests all components: MongoDB, Agents, API endpoints
"""
import requests
import json
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

API_URL = "http://localhost:8000"

def print_success(message):
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def print_header(message):
    print(f"\n{Fore.YELLOW}{'='*60}")
    print(f"{message}")
    print(f"{'='*60}{Style.RESET_ALL}\n")


def test_health_check():
    """Test API health endpoint"""
    print_header("Test 1: Health Check")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("API is healthy")
            print_info(f"MongoDB: {data.get('mongodb')}")
            print_info(f"Document count: {data.get('document_count')}")
            print_info(f"LLM Provider: {data.get('llm_provider')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Cannot connect to API: {e}")
        print_info("Make sure the backend is running on port 8000")
        return False


def test_schema_endpoint():
    """Test schema retrieval"""
    print_header("Test 2: Schema Endpoint")
    try:
        response = requests.get(f"{API_URL}/schema", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                schema = data.get('schema', {})
                fields = schema.get('fields', [])
                print_success(f"Schema retrieved: {len(fields)} fields")
                print_info("Sample fields:")
                for field in fields[:5]:
                    print(f"  - {field['name']}: {', '.join(field['types'])}")
                return True
            else:
                print_error("Schema retrieval failed")
                return False
        else:
            print_error(f"Schema endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Schema request failed: {e}")
        return False


def test_query(query_text):
    """Test a natural language query"""
    print_header(f"Testing Query: '{query_text}'")
    try:
        payload = {"prompt": query_text}
        response = requests.post(
            f"{API_URL}/generate_chart",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print_success("Query processed successfully")
                
                # Show pipeline
                pipeline = data.get('pipeline', [])
                print_info(f"Pipeline stages: {len(pipeline)}")
                print(f"Pipeline: {json.dumps(pipeline, indent=2)}")
                
                # Show results
                results = data.get('data', [])
                print_info(f"Results: {len(results)} records")
                if results:
                    print(f"Sample result: {json.dumps(results[0], indent=2)}")
                
                # Show chart info
                metadata = data.get('metadata', {})
                print_info(f"Chart type: {metadata.get('chart_type')}")
                
                return True
            else:
                print_error(f"Query failed: {data.get('error')}")
                return False
        else:
            print_error(f"API returned status {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print_error("Query timed out (30s)")
        return False
    except requests.exceptions.RequestException as e:
        print_error(f"Query request failed: {e}")
        return False


def run_all_tests():
    """Run all test cases"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print("🧪 AI BI Dashboard - Automated Test Suite")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Schema
    results.append(("Schema Endpoint", test_schema_endpoint()))
    
    # Test 3-7: Various queries
    test_queries = [
        "show total sales by category",
        "average price per region",
        "total revenue by quarter",
        "top 5 products by sales amount",
        "sales distribution by region"
    ]
    
    for query in test_queries:
        results.append((f"Query: {query}", test_query(query)))
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} tests passed\n")
    
    for test_name, result in results:
        status = f"{Fore.GREEN}✅ PASS" if result else f"{Fore.RED}❌ FAIL"
        print(f"{status}: {test_name}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    if passed == total:
        print_success("All tests passed! 🎉")
    else:
        print_error(f"{total - passed} test(s) failed")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print_info("\nTests interrupted by user")
        exit(1)
