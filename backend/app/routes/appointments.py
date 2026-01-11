from flask import Blueprint, jsonify, request
from app.models import Appointment
from app import db

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()
    patient_id = data.get("patient_id")
    provider_id = data.get("provider_id")
    appointment_time = data.get("appointment_time")
    reason = data.get("reason")

    if not all([patient_id, provider_id, appointment_time, reason]):
        return jsonify({"error": "Missing required fields"}), 400

    new_appointment = Appointment(patient_id=patient_id, provider_id=provider_id, appointment_time=appointment_time, reason=reason)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created successfully", "appointment": {"id": new_appointment.id, "patient_id": new_appointment.patient_id, "provider_id": new_appointment.provider_id}}), 201

@appointments_bp.route("/appointments", methods=["GET"])
def get_all_appointments():
    appointments = Appointment.query.all()
    output = []
    for appt in appointments:
        output.append({"id": appt.id, "patient_id": appt.patient_id, "provider_id": appt.provider_id, "appointment_time": str(appt.appointment_time), "reason": appt.reason})
    return jsonify({"appointments": output}), 200

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["GET"])
def get_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return jsonify({"id": appointment.id, "patient_id": appointment.patient_id, "provider_id": appointment.provider_id, "appointment_time": str(appointment.appointment_time), "reason": appointment.reason}), 200

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    data = request.get_json()
    appointment.patient_id = data.get("patient_id", appointment.patient_id)
    appointment.provider_id = data.get("provider_id", appointment.provider_id)
    appointment.appointment_time = data.get("appointment_time", appointment.appointment_time)
    appointment.reason = data.get("reason", appointment.reason)
    db.session.commit()
    return jsonify({"message": "Appointment updated successfully", "appointment": {"id": appointment.id, "patient_id": appointment.patient_id, "provider_id": appointment.provider_id}}), 200

@appointments_bp.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"}), 204

