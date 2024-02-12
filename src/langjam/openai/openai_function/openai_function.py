from typing import Dict, Any, List

from pydantic import BaseModel

from src.langjam.openai.openai_function.openai_function_model import FunctionSchema, FunctionObj, ParametersObj, \
    PropertyObj


class OpenaiFunction:
    """
    OpenaiFunction class contains method to create function definition. Function definition
    """

    @staticmethod
    async def get_defination(func, description: str) -> FunctionSchema:
        func_name = func.__name__
        parameters_obj = await OpenaiFunction._get_func_parameters(func)
        function_obj = FunctionObj(name=func_name, description=description, parameters=parameters_obj)
        function_schema = FunctionSchema(function=function_obj)
        return function_schema

    @staticmethod
    async def _get_func_parameters(func) -> ParametersObj:
        func_parameter_names = await OpenaiFunction._get_func_parameter_names(func)
        for func_parameter_name in func_parameter_names:
            if issubclass(func.__annotations__[func_parameter_name], BaseModel):
                model_json_schema = func.__annotations__[func_parameter_name].model_json_schema()
                properties = await OpenaiFunction._get_properties(
                    model_json_schema)  # Fields of one function param (param is pydantic obj)
                required = model_json_schema["required"]
                parameters_obj = ParametersObj(properties=properties, required=required)
                return parameters_obj

    @staticmethod
    async def _get_func_parameter_names(func) -> List[str]:
        params: List[str] = []
        annotations: Dict[str, Any] = func.__annotations__
        for key in annotations.keys():
            params.append(key)
        return params

    @staticmethod
    async def _get_properties(model_json_schema: Dict[str, Any]) -> Dict[str, PropertyObj]:
        properties: Dict[str, PropertyObj] = {}
        properties_initial_state = model_json_schema["properties"]
        references = model_json_schema["$defs"]
        for property_name in properties_initial_state:
            property_value = properties_initial_state[property_name]
            de_referenced_property = await OpenaiFunction._get_de_referenced_property(
                references,
                property_value,
                property_name
            )
            properties[property_name] = de_referenced_property
        return properties

    @staticmethod
    async def _get_de_referenced_property(references: Dict[str, Any], property_value: Dict[str, Any],
                                          property_name: str) -> PropertyObj:
        is_done = False
        expanded_property = property_value
        while True:
            if is_done:
                break
            if "anyOf" in expanded_property:
                option_list = expanded_property["anyOf"]
                for option_dict in option_list:
                    if "type" in option_dict:
                        option_dict["type"] = "null"
                    else:
                        expanded_property = option_dict;
                        break
            if "$ref" not in expanded_property:
                property_obj = PropertyObj(**expanded_property)
                return property_obj
            elif "$ref" in expanded_property:
                ref_value = expanded_property["$ref"].split("/")[-1]
                expanded_property = references[ref_value]
