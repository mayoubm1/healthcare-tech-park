from flask import Blueprint, jsonify, request
from app.models import M23MResearch
from app import db

m23m_research_bp = Blueprint("m23m_research", __name__)

@m23m_research_bp.route("/m23m_research", methods=["POST"])
def create_m23m_research_entry():
    data = request.get_json()
    research_name = data.get("research_name")
    description = data.get("description")
    research_data = data.get("research_data")
    collaboration_status = data.get("collaboration_status")

    if not research_name:
        return jsonify({"error": "Research name is required"}), 400

    new_entry = M23MResearch(research_name=research_name, description=description, research_data=research_data, collaboration_status=collaboration_status)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "M23M Research entry created successfully", "entry": {"id": new_entry.id, "research_name": new_entry.research_name}}), 201

@m23m_research_bp.route("/m23m_research", methods=["GET"])
def get_all_m23m_research_entries():
    entries = M23MResearch.query.all()
    output = []
    for entry in entries:
        output.append({"id": entry.id, "research_name": entry.research_name, "description": entry.description, "research_data": entry.research_data, "collaboration_status": entry.collaboration_status})
    return jsonify({"entries": output}), 200

@m23m_research_bp.route("/m23m_research/<int:entry_id>", methods=["GET"])
def get_m23m_research_entry(entry_id):
    entry = M23MResearch.query.get_or_404(entry_id)
    return jsonify({"id": entry.id, "research_name": entry.research_name, "description": entry.description, "research_data": entry.research_data, "collaboration_status": entry.collaboration_status}), 200

@m23m_research_bp.route("/m23m_research/<int:entry_id>", methods=["PUT"])
def update_m23m_research_entry(entry_id):
    entry = M23MResearch.query.get_or_404(entry_id)
    data = request.get_json()
    entry.research_name = data.get("research_name", entry.research_name)
    entry.description = data.get("description", entry.description)
    entry.research_data = data.get("research_data", entry.research_data)
    entry.collaboration_status = data.get("collaboration_status", entry.collaboration_status)
    db.session.commit()
    return jsonify({"message": "M23M Research entry updated successfully", "entry": {"id": entry.id, "research_name": entry.research_name}}), 200

@m23m_research_bp.route("/m23m_research/<int:entry_id>", methods=["DELETE"])
def delete_m23m_research_entry(entry_id):
    entry = M23MResearch.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "M23M Research entry deleted successfully"}), 204

