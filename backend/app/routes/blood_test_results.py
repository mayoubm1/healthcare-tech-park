from flask import Blueprint, jsonify, request
from app.services.blood_test_result_service import BloodTestResultService
from app.utils.auth_middleware import token_required

blood_test_results_bp = Blueprint("blood_test_results", __name__)

@blood_test_results_bp.route("/patients/<string:patient_id>/blood_test_results", methods=["POST"])
@token_required
def add_blood_test_result(patient_id):
    data = request.get_json()
    data["patient_id"] = patient_id
    blood_test_result = BloodTestResultService.create_blood_test_result(data)
    if blood_test_result:
        return jsonify(blood_test_result.to_dict()), 201
    return jsonify({"message": "Unable to add blood test result"}), 400

@blood_test_results_bp.route("/patients/<string:patient_id>/blood_test_results", methods=["GET"])
@token_required
def get_blood_test_results_for_patient(patient_id):
    blood_test_results_list = BloodTestResultService.get_blood_test_results_by_patient_id(patient_id)
    return jsonify([btr.to_dict() for btr in blood_test_results_list]), 200

@blood_test_results_bp.route("/blood_test_results/<string:blood_test_result_id>", methods=["GET"])
@token_required
def get_blood_test_result(blood_test_result_id):
    blood_test_result = BloodTestResultService.get_blood_test_result_by_id(blood_test_result_id)
    if blood_test_result:
        return jsonify(blood_test_result.to_dict()), 200
    return jsonify({"message": "Blood test result not found"}), 404

@blood_test_results_bp.route("/blood_test_results/<string:blood_test_result_id>", methods=["PUT"])
@token_required
def update_blood_test_result(blood_test_result_id):
    data = request.get_json()
    blood_test_result = BloodTestResultService.update_blood_test_result(blood_test_result_id, data)
    if blood_test_result:
        return jsonify(blood_test_result.to_dict()), 200
    return jsonify({"message": "Blood test result not found or unable to update"}), 404

@blood_test_results_bp.route("/blood_test_results/<string:blood_test_result_id>", methods=["DELETE"])
@token_required
def delete_blood_test_result(blood_test_result_id):
    if BloodTestResultService.delete_blood_test_result(blood_test_result_id):
        return jsonify({"message": "Blood test result deleted successfully"}), 200
    return jsonify({"message": "Blood test result not found"}), 404

