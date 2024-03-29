get_current_weather_expected = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "description": "The city and state,e.g.SanFrancisco,CA",
                    "title": "Location",
                    "type": "string"
                },
                "unit": {
                    "enum": ["celsius", "fahrenheit"],
                    "title": "Unit",
                    "type": "string"
                }
            },
            "required": ["location"]
        }
    }
}


get_current_weather_expected_stale = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
}