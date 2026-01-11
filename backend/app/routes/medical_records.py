from flask import Blueprint, jsonify, request
from app.models import MedicalRecord
from app import db

medical_records_bp = Blueprint("medical_records", __name__)

@medical_records_bp.route("/medical-records", methods=["POST"])
def create_medical_record():
    data = request.get_json()
    patient_id = data.get("patient_id")
    record_details = data.get("record_details")

    if not all([patient_id, record_details]):
        return jsonify({"error": "Missing required fields"}), 400

    new_record = MedicalRecord(patient_id=patient_id, record_details=record_details)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Medical record created successfully", "record": {"id": new_record.id, "patient_id": new_record.patient_id}}), 201

@medical_records_bp.route("/medical-records", methods=["GET"])
def get_all_medical_records():
    records = MedicalRecord.query.all()
    output = []
    for record in records:
        output.append({"id": record.id, "patient_id": record.patient_id, "record_details": record.record_details})
    return jsonify({"records": output}), 200

@medical_records_bp.route("/medical-records/<int:record_id>", methods=["GET"])
def get_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    return jsonify({"id": record.id, "patient_id": record.patient_id, "record_details": record.record_details}), 200

@medical_records_bp.route("/medical-records/<int:record_id>", methods=["PUT"])
def update_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    data = request.get_json()
    record.patient_id = data.get("patient_id", record.patient_id)
    record.record_details = data.get("record_details", record.record_details)
    db.session.commit()
    return jsonify({"message": "Medical record updated successfully", "record": {"id": record.id, "patient_id": record.patient_id}}), 200

@medical_records_bp.route("/medical-records/<int:record_id>", methods=["DELETE"])
def delete_medical_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Medical record deleted successfully"}), 204

