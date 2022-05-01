
def get_sensor_data( sensor_name ):
    if( sensor_name == 'smoke_detect' ):
        sensor_data = {
            "data" : True
        }
        return sensor_data 

    elif( sensor_name == 'temp_detect' ):
        sensor_data = {
            "data" : 27.3
        }
        return sensor_data
