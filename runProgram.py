# importing subprocess module 
import subprocess

# running other file using run()
subprocess.run(["python", "download_third_party_data.py"])
subprocess.run(["python", "merge_datasets.py"])
# subprocess.run(["python", "prepare_data_for_model.py"])
# subprocess.run(["python", "prepare_data_for_dashboarding.py"])