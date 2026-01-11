from flask import Blueprint, jsonify, request
from app.services.genomic_data_service import GenomicDataService
from app.utils.auth_middleware import token_required

genomic_data_bp = Blueprint("genomic_data", __name__)

@genomic_data_bp.route("/patients/<string:patient_id>/genomic_data", methods=["POST"])
@token_required
def add_genomic_data(patient_id):
    data = request.get_json()
    data["patient_id"] = patient_id
    genomic_data = GenomicDataService.create_genomic_data(data)
    if genomic_data:
        return jsonify(genomic_data.to_dict()), 201
    return jsonify({"message": "Unable to add genomic data"}), 400

@genomic_data_bp.route("/patients/<string:patient_id>/genomic_data", methods=["GET"])
@token_required
def get_genomic_data_for_patient(patient_id):
    genomic_data_list = GenomicDataService.get_genomic_data_by_patient_id(patient_id)
    return jsonify([gd.to_dict() for gd in genomic_data_list]), 200

@genomic_data_bp.route("/genomic_data/<string:genomic_data_id>", methods=["GET"])
@token_required
def get_genomic_data(genomic_data_id):
    genomic_data = GenomicDataService.get_genomic_data_by_id(genomic_data_id)
    if genomic_data:
        return jsonify(genomic_data.to_dict()), 200
    return jsonify({"message": "Genomic data not found"}), 404

@genomic_data_bp.route("/genomic_data/<string:genomic_data_id>", methods=["PUT"])
@token_required
def update_genomic_data(genomic_data_id):
    data = request.get_json()
    genomic_data = GenomicDataService.update_genomic_data(genomic_data_id, data)
    if genomic_data:
        return jsonify(genomic_data.to_dict()), 200
    return jsonify({"message": "Genomic data not found or unable to update"}), 404

@genomic_data_bp.route("/genomic_data/<string:genomic_data_id>", methods=["DELETE"])
@token_required
def delete_genomic_data(genomic_data_id):
    if GenomicDataService.delete_genomic_data(genomic_data_id):
        return jsonify({"message": "Genomic data deleted successfully"}), 200
    return jsonify({"message": "Genomic data not found"}), 404

