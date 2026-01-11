from flask import Blueprint, jsonify, request
from app.services.wearable_data_service import WearableDataService
from app.utils.auth_middleware import token_required

wearable_data_bp = Blueprint("wearable_data", __name__)

@wearable_data_bp.route("/patients/<string:patient_id>/wearable_data", methods=["POST"])
@token_required
def add_wearable_data(patient_id):
    data = request.get_json()
    data["patient_id"] = patient_id
    wearable_data = WearableDataService.create_wearable_data(data)
    if wearable_data:
        return jsonify(wearable_data.to_dict()), 201
    return jsonify({"message": "Unable to add wearable data"}), 400

@wearable_data_bp.route("/patients/<string:patient_id>/wearable_data", methods=["GET"])
@token_required
def get_wearable_data_for_patient(patient_id):
    wearable_data_list = WearableDataService.get_wearable_data_by_patient_id(patient_id)
    return jsonify([wd.to_dict() for wd in wearable_data_list]), 200

@wearable_data_bp.route("/wearable_data/<string:wearable_data_id>", methods=["GET"])
@token_required
def get_wearable_data(wearable_data_id):
    wearable_data = WearableDataService.get_wearable_data_by_id(wearable_data_id)
    if wearable_data:
        return jsonify(wearable_data.to_dict()), 200
    return jsonify({"message": "Wearable data not found"}), 404

@wearable_data_bp.route("/wearable_data/<string:wearable_data_id>", methods=["PUT"])
@token_required
def update_wearable_data(wearable_data_id):
    data = request.get_json()
    wearable_data = WearableDataService.update_wearable_data(wearable_data_id, data)
    if wearable_data:
        return jsonify(wearable_data.to_dict()), 200
    return jsonify({"message": "Wearable data not found or unable to update"}), 404

@wearable_data_bp.route("/wearable_data/<string:wearable_data_id>", methods=["DELETE"])
@token_required
def delete_wearable_data(wearable_data_id):
    if WearableDataService.delete_wearable_data(wearable_data_id):
        return jsonify({"message": "Wearable data deleted successfully"}), 200
    return jsonify({"message": "Wearable data not found"}), 404

