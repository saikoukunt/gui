import json

class Parameter:
    def __init__(self, name, description, default, min_value, max_value, data_type, basic, tag):
        self.name = name
        self.description = description
        self.value = default
        self.min = min_value
        self.max = max_value
        self.type = data_type
        self.basic = basic
        self.tag = tag
        
    
    def set_param(self, value):
        # Assume validation is required for the new value
        if self.min <= value <= self.max:
            self.value = value
        else:
            raise ValueError(f"Value must be between {self.min} and {self.max}.")

    def get_param(self):
        return self.value

class ParameterStructure:
    def __init__(self):
        self.parameters = {}
    
    def add_param(self, name, description, default, min_value, max_value, data_type, basic, tag):
        self.parameters[name] = Parameter(name, description, default, min_value, max_value, data_type, basic, tag)
    
    def set_param(self, name, value):
        if name in self.parameters:
            self.parameters[name].set_param(value)
        else:
            raise KeyError(f"Parameter {name} does not exist.")
    
    def get_param(self, name):
        if name in self.parameters:
            return self.parameters[name].get_param()
        else:
            raise KeyError(f"Parameter {name} does not exist.")
    
    def load_from_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            for name, value in data.items():
                self.set_param(name, value)

    def save_to_json(self, json_file):
        data = {name: param.get_param() for name, param in self.parameters.items()}
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

# Example usage
param_structure = ParameterStructure()
param_structure.add_param(name="example_param", description="An example parameter", 
                          default=10, min_value=0, max_value=100, data_type=int)

# Set and get parameter value
param_structure.set_param("example_param", 20)
print(param_structure.get_param("example_param"))

json_file_path = 'params.json'
param_structure.save_to_json(json_file_path)

# Output path for user to access
json_file_path
