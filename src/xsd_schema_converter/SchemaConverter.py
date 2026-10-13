import io
import json
import logging
from xsdata.codegen.parsers.schema import SchemaParser

# Configure module-level logger
logger = logging.getLogger(__name__)

def map_xsd_type_to_json(element_type):
    """Helper function to map XSD types to OpenAPI/JSON types."""
    raw_type = str(element_type).lower()
    
    if "int" in raw_type:
        return "integer", "int32"
    elif "long" in raw_type:
        return "integer", "int64"
    elif "decimal" in raw_type or "float" in raw_type:
        return "number", "float"
    elif "boolean" in raw_type:
        return "boolean", None
    else:
        return "string", None

def convert_xsd_string_to_openapi(xsd_content):
    """
    Parses an XSD string and returns an OpenAPI 3.0 component dictionary.
    
    Args:
        xsd_content (str): The raw XSD XML content.
        
    Returns:
        dict: The OpenAPI components object containing schemas.
    """
    try:
        logger.info("Starting XSD string conversion.")
        
        # 1. Parse XSD from String
        parser = SchemaParser()
        # Convert string to bytes for the parser
        source = io.BytesIO(xsd_content.encode('utf-8'))
        
        try:
            schema = parser.parse(source)
        except Exception as parse_err:
            logger.error(f"XSD Parsing failed: {parse_err}")
            raise ValueError(f"Failed to parse XML structure: {parse_err}")

        # 2. Extract Complex Types
        schemas = {}

        if hasattr(schema, 'complex_types'):
            for complex_type in schema.complex_types:
                try:
                    properties = {}
                    required = []
                    
                    if complex_type.sequence:
                        for element in complex_type.sequence.elements:
                            prop_name = element.name
                            if not prop_name:
                                continue

                            # Map types
                            json_type, json_format = map_xsd_type_to_json(element.type)
                            
                            prop_def = {"type": json_type}
                            if json_format:
                                prop_def["format"] = json_format
                            
                            properties[prop_name] = prop_def
                            
                            # Check required status
                            if element.min_occurs is None or element.min_occurs > 0:
                                required.append(prop_name)

                    # Build Schema Object
                    schema_def = {
                        "type": "object",
                        "properties": properties
                    }
                    if required:
                        schema_def["required"] = required
                    
                    schemas[complex_type.name] = schema_def
                    
                except Exception as item_error:
                    logger.warning(f"Skipping type '{complex_type.name}' due to error: {item_error}")
                    continue
        else:
            logger.warning("No complex types found in XSD.")

        # 3. Final Structure
        openapi_doc = {
            "components": {
                "schemas": schemas
            }
        }
        
        logger.info("XSD conversion completed successfully.")
        return openapi_doc

    except ValueError as ve:
        # Re-raise known validation errors
        raise ve
    except Exception as e:
        logger.exception("Unexpected error in core logic")
        raise RuntimeError(f"Conversion logic failed: {str(e)}")