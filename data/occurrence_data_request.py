import requests
import urllib.request
import os
import pandas as pd
import hashlib
import pdb
from species_names import native_trees_list
from image_request import get_taxon_key, get_occurence_key


def get_occurrence_data(species_occurrences_keys):
    """
    Given the species occurrence key
    return a data frame with a series of parameters
    associated to the occurrence.
    """
    base_url = "https://api.gbif.org/v1/"
    column_names = ["species_name", "taxon_key", "occurrence_key", "basis_of_record", "institution_code","coordinate_system", "decimal_longitude", "decimal_latitude", "coordinate_uncertainty","elevation", "date", "issues"]
    df = pd.DataFrame(columns = column_names) 
    for species_name, occurrences in species_occurrences_keys.items(): 
        taxon_key = species_taxon_key[species_name]     
        for occurrence in range(0,(len(occurrences))):          
            occurrence_key = occurrences[occurrence]                
            response = requests.get(f"{base_url}occurrence/{occurrence_key}")
            if response.status_code == 200:
                occurrence_result = response.json()
                try:
                    basis_of_record = occurrence_result["basisOfRecord"]
                except:
                    basis_of_record = ""
                    pass
                try:
                    institution_code = occurrence_result["institutionCode"]
                except:
                    institution_code = ""
                    pass
                try:
                    coordinate_system = occurrence_result["geodeticDatum"]
                except:
                    coordinate_system = ""
                    pass
                try:
                    decimal_longitude = occurrence_result["decimalLongitude"]
                except:
                    decimal_longitude = ""
                    pass
                try:
                    decimal_latitude = occurrence_result["decimalLatitude"]
                except:
                    decimal_latitude = ""
                    pass
                try:
                    coordinate_uncertainty = occurrence_result["coordinateUncertaintyInMeters"]
                except:
                    coordinate_uncertainty = ""
                    pass
                try:
                    elevation = occurrence_result["elevation"]
                except:
                    elevation = ""
                    pass
                try:
                    date = occurrence_result["eventDate"]
                except:
                    date = ""
                    pass
                try:
                    issues = occurrence_result["issues"]
                except:
                    issues = ""
                    pass
                data_in_row = []
                data_in_row.extend([species_name,taxon_key, occurrences[occurrence], basis_of_record,institution_code, coordinate_system, decimal_longitude, decimal_latitude, coordinate_uncertainty, elevation, date, issues])         
                new_row = pd.DataFrame([data_in_row], columns=column_names)
                df = df.append(new_row, ignore_index = True)
                print("ok 2")
            elif response.status_code == 404:
                print('Error 404: Page not found.')
            else:
                print("Error. Undetermined status code.")  
    return df


if __name__ == "__main__":

    # 1- Customize search parameters 

    ###### Edit for a new search ##################
    # Search name
    search_name = "Occurrence data from native trees in GB"
    # Species input
    species_list = native_trees_list() 
    species_list = species_list[:3]
    # Filter parameters
    media_type = ""  #StillImage
    country = "GB"
    has_coordinate = "True" # True/False
    kingdom = ""  # Plantae
    basis_of_record = ""
    institution_code = "" # K (RBG Kew)
    ###############################################

    # 2- Handle filter parameters
    filter = {"mediaType": media_type, "country": country, "hasCoordinate": has_coordinate, "kingdom": kingdom, "basisOfRecord": basis_of_record, "institutionCode": institution_code}
    filter_information = f"""
    Filters:
    mediaType: {media_type}
    country: {country}
    hasCoordinate: {has_coordinate}
    kingdom:{kingdom}
    basisOfRecord: {basis_of_record}
    institutionCode: {institution_code}
    """ 
    ## Hash the filter information + species list string to use it for naming the results file
    filter_and_species_information = filter_information + str(species_list)
    filter_hash = hashlib.md5(str.encode(filter_and_species_information)).hexdigest()     

    # 3- Get species keys (same as taxon key) 
    species_taxon_key = get_taxon_key(species_list)

    # 4- Get occurrences keys 
    species_occurrences_keys = get_occurence_key(species_taxon_key, filter)

    occurrence_data_table = get_occurrence_data(species_occurrences_keys)
    print(occurrence_data_table)