from flask import Blueprint, jsonify, request
from app.models import Teleconsultation
from app import db

telemed_bp = Blueprint("telemed", __name__)

@telemed_bp.route("/telemed", methods=["POST"])
def create_teleconsultation():
    data = request.get_json()
    patient_id = data.get("patient_id")
    provider_id = data.get("provider_id")
    consultation_time = data.get("consultation_time")
    status = data.get("status")

    if not all([patient_id, provider_id, consultation_time, status]):
        return jsonify({"error": "Missing required fields"}), 400

    new_consultation = Teleconsultation(patient_id=patient_id, provider_id=provider_id, consultation_time=consultation_time, status=status)
    db.session.add(new_consultation)
    db.session.commit()
    return jsonify({"message": "Teleconsultation created successfully", "consultation": {"id": new_consultation.id, "patient_id": new_consultation.patient_id, "provider_id": new_consultation.provider_id}}), 201

@telemed_bp.route("/telemed", methods=["GET"])
def get_all_teleconsultations():
    consultations = Teleconsultation.query.all()
    output = []
    for consultation in consultations:
        output.append({"id": consultation.id, "patient_id": consultation.patient_id, "provider_id": consultation.provider_id, "consultation_time": str(consultation.consultation_time), "status": consultation.status})
    return jsonify({"consultations": output}), 200

@telemed_bp.route("/telemed/<int:consultation_id>", methods=["GET"])
def get_teleconsultation(consultation_id):
    consultation = Teleconsultation.query.get_or_404(consultation_id)
    return jsonify({"id": consultation.id, "patient_id": consultation.patient_id, "provider_id": consultation.provider_id, "consultation_time": str(consultation.consultation_time), "status": consultation.status}), 200

@telemed_bp.route("/telemed/<int:consultation_id>", methods=["PUT"])
def update_teleconsultation(consultation_id):
    consultation = Teleconsultation.query.get_or_404(consultation_id)
    data = request.get_json()
    consultation.patient_id = data.get("patient_id", consultation.patient_id)
    consultation.provider_id = data.get("provider_id", consultation.provider_id)
    consultation.consultation_time = data.get("consultation_time", consultation.consultation_time)
    consultation.status = data.get("status", consultation.status)
    db.session.commit()
    return jsonify({"message": "Teleconsultation updated successfully", "consultation": {"id": consultation.id, "patient_id": consultation.patient_id, "provider_id": consultation.provider_id}}), 200

@telemed_bp.route("/telemed/<int:consultation_id>", methods=["DELETE"])
def delete_teleconsultation(consultation_id):
    consultation = Teleconsultation.query.get_or_404(consultation_id)
    db.session.delete(consultation)
    db.session.commit()
    return jsonify({"message": "Teleconsultation deleted successfully"}), 204

