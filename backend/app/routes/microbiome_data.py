from flask import Blueprint, jsonify, request
from app.services.microbiome_data_service import MicrobiomeDataService
from app.utils.auth_middleware import token_required

microbiome_data_bp = Blueprint("microbiome_data", __name__)

@microbiome_data_bp.route("/patients/<string:patient_id>/microbiome_data", methods=["POST"])
@token_required
def add_microbiome_data(patient_id):
    data = request.get_json()
    data["patient_id"] = patient_id
    microbiome_data = MicrobiomeDataService.create_microbiome_data(data)
    if microbiome_data:
        return jsonify(microbiome_data.to_dict()), 201
    return jsonify({"message": "Unable to add microbiome data"}), 400

@microbiome_data_bp.route("/patients/<string:patient_id>/microbiome_data", methods=["GET"])
@token_required
def get_microbiome_data_for_patient(patient_id):
    microbiome_data_list = MicrobiomeDataService.get_microbiome_data_by_patient_id(patient_id)
    return jsonify([md.to_dict() for md in microbiome_data_list]), 200

@microbiome_data_bp.route("/microbiome_data/<string:microbiome_data_id>", methods=["GET"])
@token_required
def get_microbiome_data(microbiome_data_id):
    microbiome_data = MicrobiomeDataService.get_microbiome_data_by_id(microbiome_data_id)
    if microbiome_data:
        return jsonify(microbiome_data.to_dict()), 200
    return jsonify({"message": "Microbiome data not found"}), 404

@microbiome_data_bp.route("/microbiome_data/<string:microbiome_data_id>", methods=["PUT"])
@token_required
def update_microbiome_data(microbiome_data_id):
    data = request.get_json()
    microbiome_data = MicrobiomeDataService.update_microbiome_data(microbiome_data_id, data)
    if microbiome_data:
        return jsonify(microbiome_data.to_dict()), 200
    return jsonify({"message": "Microbiome data not found or unable to update"}), 404

@microbiome_data_bp.route("/microbiome_data/<string:microbiome_data_id>", methods=["DELETE"])
@token_required
def delete_microbiome_data(microbiome_data_id):
    if MicrobiomeDataService.delete_microbiome_data(microbiome_data_id):
        return jsonify({"message": "Microbiome data deleted successfully"}), 200
    return jsonify({"message": "Microbiome data not found"}), 404

