
def pre_processing( input_data ):
    input_data = input_data["data"]
    temp_data = input_data["temp"]
    
    model_input_data = [[temp_data]]
    return model_input_data