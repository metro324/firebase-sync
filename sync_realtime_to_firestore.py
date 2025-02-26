import firebase_admin
from firebase_admin import credentials, db, firestore
import os

# Initialize Firebase Admin SDK using service account credentials
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))  # Ensure your service account key is provided in an environment variable
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com'  # Replace with your Realtime Database URL
})

# Initialize Firestore
firestore_db = firestore.client()

# Define the paths to your Realtime Database and Firestore collections
realtime_db_path = '/sensorData'  # Replace with your Realtime Database path
firestore_collection = 'sensor_data'  # Firestore collection where data will be stored

# Function to sync data from Realtime Database to Firestore
def sync_data():
    # Fetch the data from Realtime Database
    realtime_data = db.reference(realtime_db_path).get()

    if realtime_data:
        print("Data fetched from Realtime Database:")
        for device_id, sensor_data in realtime_data.items():
            print(f"Device: {device_id}")
            print(f"Light Level: {sensor_data['light']}")
            print(f"Sound Level: {sensor_data['sound']}")

            # Prepare data to be added to Firestore
            document_ref = firestore_db.collection(firestore_collection).document(device_id)
            document_ref.set({
                'light': sensor_data['light'],
                'sound': sensor_data['sound'],
                'timestamp': firestore.SERVER_TIMESTAMP  # Firestore will automatically set the timestamp
            })
            print(f"Data synced to Firestore for {device_id}")

# Call the sync function
if __name__ == "__main__":
    sync_data()
