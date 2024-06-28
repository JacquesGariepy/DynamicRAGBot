from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.rag_service import RAGService
from app import limiter

bp = Blueprint('rag', __name__, url_prefix='/api/rag')
rag_service = RAGService()

@bp.route('/query', methods=['POST'])
@jwt_required()
@limiter.limit("100 per day")
def query_rag():
    data = request.get_json()
    response = rag_service.query(data['question'])
    return jsonify(response=response), 200

@bp.route('/add_document', methods=['POST'])
@jwt_required()
def add_document():
    data = request.get_json()
    rag_service.add_document(data['content'], data.get('metadata'))
    return jsonify({"msg": "Document added successfully"}), 201