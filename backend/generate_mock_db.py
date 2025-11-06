"""
Mock Data Generator for BI Dashboard
Generates sample sales data for testing

"""
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()


def generate_mock_sales_data(num_records: int = 1000) -> list:
    """
    Generate mock sales data
    
    Args:
        num_records: Number of sales records to generate
        
    Returns:
        List of sales documents
    """
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home & Garden', 'Sports', 'Toys']
    regions = ['North', 'South', 'East', 'West', 'Central']
    products = {
        'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
        'Clothing': ['Shirt', 'Pants', 'Dress', 'Jacket', 'Shoes'],
        'Food': ['Organic Produce', 'Snacks', 'Beverages', 'Frozen Items', 'Bakery'],
        'Books': ['Fiction', 'Non-Fiction', 'Comics', 'Textbooks', 'Magazines'],
        'Home & Garden': ['Furniture', 'Decor', 'Kitchen', 'Garden Tools', 'Lighting'],
        'Sports': ['Equipment', 'Apparel', 'Accessories', 'Nutrition', 'Footwear'],
        'Toys': ['Action Figures', 'Puzzles', 'Board Games', 'Dolls', 'Building Sets']
    }
    
    sales_data = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_records):
        category = random.choice(categories)
        product = random.choice(products[category])
        region = random.choice(regions)
        
        # Generate date (last 12 months)
        days_ago = random.randint(0, 365)
        sale_date = start_date + timedelta(days=days_ago)
        
        # Generate amounts
        quantity = random.randint(1, 50)
        price = round(random.uniform(10, 1000), 2)
        amount = round(quantity * price, 2)
        
        # Calculate quarter
        quarter = f"Q{(sale_date.month - 1) // 3 + 1} {sale_date.year}"
        
        document = {
            'sale_id': f'SALE-{i+1:06d}',
            'date': sale_date,
            'category': category,
            'product': product,
            'region': region,
            'quantity': quantity,
            'price': price,
            'amount': amount,
            'quarter': quarter,
            'year': sale_date.year,
            'month': sale_date.month,
            'customer_id': f'CUST-{random.randint(1, 500):04d}',
            'status': random.choice(['completed', 'completed', 'completed', 'pending', 'cancelled'])
        }
        
        sales_data.append(document)
    
    return sales_data


def populate_database():
    """Populate MongoDB with mock data"""
    # Get configuration
    uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    db_name = os.getenv('MONGODB_DATABASE', 'bi_dashboard')
    collection_name = os.getenv('MONGODB_COLLECTION', 'sales')
    
    print(f"\n{'='*60}")
    print("🚀 Mock Data Generator")
    print(f"{'='*60}\n")
    
    try:
        # Connect to MongoDB
        print(f"📡 Connecting to MongoDB...")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Test connection
        print(f"✅ Connected successfully")
        
        db = client[db_name]
        collection = db[collection_name]
        
        # Check if data already exists
        existing_count = collection.count_documents({})
        if existing_count > 0:
            print(f"\n⚠️  Collection already contains {existing_count} documents")
            response = input("Do you want to drop and recreate? (yes/no): ")
            if response.lower() == 'yes':
                collection.drop()
                print(f"✅ Collection dropped")
            else:
                print(f"❌ Aborted")
                return
        
        # Generate data
        print(f"\n📊 Generating mock sales data...")
        sales_data = generate_mock_sales_data(1000)
        print(f"✅ Generated {len(sales_data)} sales records")
        
        # Insert data
        print(f"\n💾 Inserting data into MongoDB...")
        result = collection.insert_many(sales_data)
        print(f"✅ Inserted {len(result.inserted_ids)} documents")
        
        # Create indexes
        print(f"\n🔍 Creating indexes...")
        collection.create_index([("category", 1)])
        collection.create_index([("region", 1)])
        collection.create_index([("date", -1)])
        collection.create_index([("quarter", 1)])
        print(f"✅ Indexes created")
        
        # Show sample statistics
        print(f"\n{'='*60}")
        print("📈 Database Statistics")
        print(f"{'='*60}")
        print(f"Total Records: {collection.count_documents({})}")
        print(f"Database: {db_name}")
        print(f"Collection: {collection_name}")
        
        # Sample queries
        print(f"\n{'='*60}")
        print("🔍 Sample Queries to Try:")
        print(f"{'='*60}")
        print("1. 'show total sales by category'")
        print("2. 'average price per region'")
        print("3. 'total revenue by quarter'")
        print("4. 'top 5 products by sales amount'")
        print("5. 'sales trend over time'")
        print(f"{'='*60}\n")
        
        client.close()
        print("✅ Database setup complete!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure MongoDB is running and accessible.")


if __name__ == "__main__":
    populate_database()
