from google.cloud import firestore

gcp_project = "air-paradise"
firebase_collection = "radio_paradise"
db = firestore.Client(project=gcp_project)
