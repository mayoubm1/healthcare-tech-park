from flask import Blueprint, jsonify, request
from app.services.nutrition_plan_service import NutritionPlanService
from app.utils.auth_middleware import token_required

nutrition_plans_bp = Blueprint("nutrition_plans", __name__)

@nutrition_plans_bp.route("/patients/<string:patient_id>/nutrition_plans", methods=["POST"])
@token_required
def add_nutrition_plan(patient_id):
    data = request.get_json()
    data["patient_id"] = patient_id
    nutrition_plan = NutritionPlanService.create_nutrition_plan(data)
    if nutrition_plan:
        return jsonify(nutrition_plan.to_dict()), 201
    return jsonify({"message": "Unable to add nutrition plan"}), 400

@nutrition_plans_bp.route("/patients/<string:patient_id>/nutrition_plans", methods=["GET"])
@token_required
def get_nutrition_plans_for_patient(patient_id):
    nutrition_plans_list = NutritionPlanService.get_nutrition_plans_by_patient_id(patient_id)
    return jsonify([np.to_dict() for np in nutrition_plans_list]), 200

@nutrition_plans_bp.route("/nutrition_plans/<string:nutrition_plan_id>", methods=["GET"])
@token_required
def get_nutrition_plan(nutrition_plan_id):
    nutrition_plan = NutritionPlanService.get_nutrition_plan_by_id(nutrition_plan_id)
    if nutrition_plan:
        return jsonify(nutrition_plan.to_dict()), 200
    return jsonify({"message": "Nutrition plan not found"}), 404

@nutrition_plans_bp.route("/nutrition_plans/<string:nutrition_plan_id>", methods=["PUT"])
@token_required
def update_nutrition_plan(nutrition_plan_id):
    data = request.get_json()
    nutrition_plan = NutritionPlanService.update_nutrition_plan(nutrition_plan_id, data)
    if nutrition_plan:
        return jsonify(nutrition_plan.to_dict()), 200
    return jsonify({"message": "Nutrition plan not found or unable to update"}), 404

@nutrition_plans_bp.route("/nutrition_plans/<string:nutrition_plan_id>", methods=["DELETE"])
@token_required
def delete_nutrition_plan(nutrition_plan_id):
    if NutritionPlanService.delete_nutrition_plan(nutrition_plan_id):
        return jsonify({"message": "Nutrition plan deleted successfully"}), 200
    return jsonify({"message": "Nutrition plan not found"}), 404

