# view_users.py
import json

def show_collected_users():
    try:
        with open('user_data.json', 'r') as f:
            data = json.load(f)
        
        users = data.get("registered_users", {})
        
        if not users:
            print(" No users collected yet")
            return
        
        print(f" COLLECTED USERS ({len(users)} total):")
        print("=" * 50)
        
        for chat_id, info in users.items():
            print(f" {info['name']}")
            print(f" Username: @{info['username']}")
            print(f" Chat ID: {chat_id}")
            print(f"Added: {info['timestamp']}")
            print("-" * 30)
        
    except FileNotFoundError:
        print(" user_data.json not found")
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    show_collected_users()