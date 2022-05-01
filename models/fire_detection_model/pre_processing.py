
def pre_processing( input_data ):
    input_data = input_data["data"]
    smoke_data = input_data["smoke"]
    temp_data = input_data["temp"]
    
    model_input_data = [[temp_data, smoke_data]]
    return model_input_data