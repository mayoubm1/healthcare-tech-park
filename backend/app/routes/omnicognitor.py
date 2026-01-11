from flask import Blueprint, jsonify, request
from app.models import OmniCognitor
from app import db

omnicognitor_bp = Blueprint("omnicognitor", __name__)

@omnicognitor_bp.route("/omnicognitor", methods=["POST"])
def create_omnicognitor_agent():
    data = request.get_json()
    agent_name = data.get("agent_name")
    capabilities = data.get("capabilities")

    if not agent_name:
        return jsonify({"error": "Agent name is required"}), 400

    new_agent = OmniCognitor(agent_name=agent_name, capabilities=capabilities)
    db.session.add(new_agent)
    db.session.commit()
    return jsonify({"message": "OmniCognitor agent created successfully", "agent": {"id": new_agent.id, "agent_name": new_agent.agent_name}}), 201

@omnicognitor_bp.route("/omnicognitor", methods=["GET"])
def get_all_omnicognitor_agents():
    agents = OmniCognitor.query.all()
    output = []
    for agent in agents:
        output.append({"id": agent.id, "agent_name": agent.agent_name, "capabilities": agent.capabilities})
    return jsonify({"agents": output}), 200

@omnicognitor_bp.route("/omnicognitor/<int:agent_id>", methods=["GET"])
def get_omnicognitor_agent(agent_id):
    agent = OmniCognitor.query.get_or_404(agent_id)
    return jsonify({"id": agent.id, "agent_name": agent.agent_name, "capabilities": agent.capabilities}), 200

@omnicognitor_bp.route("/omnicognitor/<int:agent_id>", methods=["PUT"])
def update_omnicognitor_agent(agent_id):
    agent = OmniCognitor.query.get_or_404(agent_id)
    data = request.get_json()
    agent.agent_name = data.get("agent_name", agent.agent_name)
    agent.capabilities = data.get("capabilities", agent.capabilities)
    db.session.commit()
    return jsonify({"message": "OmniCognitor agent updated successfully", "agent": {"id": agent.id, "agent_name": agent.agent_name}}), 200

@omnicognitor_bp.route("/omnicognitor/<int:agent_id>", methods=["DELETE"])
def delete_omnicognitor_agent(agent_id):
    agent = OmniCognitor.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return jsonify({"message": "OmniCognitor agent deleted successfully"}), 204

