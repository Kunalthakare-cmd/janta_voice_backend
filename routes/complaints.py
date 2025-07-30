from flask import Blueprint, request, jsonify
from ..db import complaints_collection
from ..utils.telegram_utils import send_telegram_message


import uuid

complaints_bp = Blueprint("complaints", __name__)

@complaints_bp.route("/api/complaints", methods=["POST"])
def submit_complaint():
    data = request.json

    # Generate unique complaint ID
    complaint_id = f"CMP-{uuid.uuid4().hex[:6].upper()}"
    data["complaint_id"] = complaint_id

    # Save to MongoDB
    complaints_collection.insert_one(data)

    # Send WhatsApp
    try:
         send_telegram_message(data, complaint_id)
    except Exception as e:
        return jsonify({"error": "WhatsApp failed", "details": str(e)}), 500

    return jsonify({
        "success": True,
        "complaint_id": complaint_id,
        "track_url": f"https://jantavoice.vercel.app/track/{complaint_id}"
    })

@complaints_bp.route("/api/complaints/<complaint_id>", methods=["GET"])
def get_complaint_by_id(complaint_id):
    complaint = complaints_collection.find_one({"complaint_id": complaint_id})
    
    if complaint:
        # Convert ObjectId to string
        complaint["_id"] = str(complaint["_id"])
        return jsonify({"success": True, "complaint": complaint})
    else:
        return jsonify({"success": False, "error": "Complaint not found"}), 404
