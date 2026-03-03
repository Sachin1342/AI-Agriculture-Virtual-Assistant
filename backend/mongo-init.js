db.createCollection("chatbot_logs");
db.createCollection("disease_predictions");
db.createCollection("groundwater_data");
db.createCollection("user_profiles");

db.chatbot_logs.createIndex({ "timestamp": 1 });
db.disease_predictions.createIndex({ "crop_id": 1, "timestamp": 1 });
db.groundwater_data.createIndex({ "location": 1, "timestamp": 1 });
db.user_profiles.createIndex({ "email": 1 });

print("MongoDB collections and indexes created successfully");
