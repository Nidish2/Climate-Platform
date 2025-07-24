"""
Comprehensive Error Handlers
Enhanced error handling with detailed logging and user-friendly responses
"""

from flask import jsonify, request
import logging
import structlog
from datetime import datetime
from typing import Dict, Any

logger = structlog.get_logger()

def register_error_handlers(app):
    """Register comprehensive error handlers"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        logger.warning("Bad request", 
                      url=request.url, 
                      method=request.method,
                      error=str(error))
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server',
            'status_code': 400,
            'timestamp': datetime.utcnow().isoformat()
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized errors"""
        logger.warning("Unauthorized access attempt",
                      url=request.url,
                      method=request.method,
                      user_agent=request.headers.get('User-Agent'))
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required',
            'status_code': 401,
            'timestamp': datetime.utcnow().isoformat()
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden errors"""
        logger.warning("Forbidden access attempt",
                      url=request.url,
                      method=request.method)
        return jsonify({
            'error': 'Forbidden',
            'message': 'Insufficient permissions',
            'status_code': 403,
            'timestamp': datetime.utcnow().isoformat()
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        logger.info("Resource not found",
                   url=request.url,
                   method=request.method)
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404,
            'timestamp': datetime.utcnow().isoformat()
        }), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate limit errors"""
        logger.warning("Rate limit exceeded",
                      url=request.url,
                      method=request.method,
                      client_ip=request.remote_addr)
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.',
            'status_code': 429,
            'timestamp': datetime.utcnow().isoformat()
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors"""
        logger.error("Internal server error",
                    url=request.url,
                    method=request.method,
                    error=str(error))
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'status_code': 500,
            'timestamp': datetime.utcnow().isoformat()
        }), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle service unavailable errors"""
        logger.error("Service unavailable",
                    url=request.url,
                    method=request.method,
                    error=str(error))
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The service is temporarily unavailable',
            'status_code': 503,
            'timestamp': datetime.utcnow().isoformat()
        }), 503
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors"""
        logger.error("Unexpected error",
                    url=request.url,
                    method=request.method,
                    error=str(error),
                    error_type=type(error).__name__)
        return jsonify({
            'error': 'Unexpected Error',
            'message': 'An unexpected error occurred',
            'status_code': 500,
            'timestamp': datetime.utcnow().isoformat()
        }), 500
