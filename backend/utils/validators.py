from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
import re

class GatewayStatusSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    status = fields.Str(required=True, validate=validate.OneOf(['healthy', 'unhealthy', 'starting', 'stopped']))
    port = fields.Int(required=True, validate=validate.Range(min=1, max=65535))
    trial_info = fields.Dict(missing=None)

class TrialResetRequestSchema(Schema):
    gateway_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    force = fields.Bool(missing=False)

class SystemHealthSchema(Schema):
    timestamp = fields.DateTime(required=True)
    cpu_usage = fields.Float(validate=validate.Range(min=0, max=100))
    memory_usage = fields.Float(validate=validate.Range(min=0, max=100))
    disk_usage = fields.Float(validate=validate.Range(min=0, max=100))
    docker_status = fields.Str(validate=validate.OneOf(['healthy', 'unhealthy']))

def validate_ip_address(ip):
    """Validate IP address format"""
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if not re.match(pattern, ip):
        raise ValidationError('Invalid IP address format')

def validate_gateway_name(name):
    """Validate gateway name format"""
    pattern = r'^[A-Za-z][A-Za-z0-9_-]*$'
    if not re.match(pattern, name):
        raise ValidationError('Invalid gateway name format. Must start with letter and contain only letters, numbers, underscores, and hyphens.')

def validate_port_range(port):
    """Validate port is in acceptable range"""
    if not (1024 <= port <= 65535):
        raise ValidationError('Port must be between 1024 and 65535')

class RequestValidator:
    """Centralized request validation"""
    
    @staticmethod
    def validate_json_request(request, schema_class):
        """Validate JSON request against schema"""
        if not request.is_json:
            raise ValidationError('Request must be JSON')
        
        schema = schema_class()
        try:
            return schema.load(request.get_json())
        except ValidationError as e:
            raise ValidationError(f'Validation error: {e.messages}')
    
    @staticmethod
    def validate_query_params(request, required_params=None, optional_params=None):
        """Validate query parameters"""
        params = {}
        errors = {}
        
        if required_params:
            for param in required_params:
                value = request.args.get(param)
                if not value:
                    errors[param] = 'This parameter is required'
                else:
                    params[param] = value
        
        if optional_params:
            for param in optional_params:
                value = request.args.get(param)
                if value:
                    params[param] = value
        
        if errors:
            raise ValidationError(errors)
        
        return params