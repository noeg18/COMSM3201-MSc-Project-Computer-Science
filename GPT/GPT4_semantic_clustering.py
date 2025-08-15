from openai import OpenAI
import os
import pandas as pd
import csv
import sys

client = OpenAI()


if len(sys.argv) < 1:
   input_folder = sys.argv[1] 
else:
  print("Error: No input file.") 
  sys.exit(1)

for file in os.listdir(input_folder):
   if file.endswith(".csv"):
      print(f"Clustering: {file}")
      # access file
      file_path = os.path.join(input_folder, file)
      df = pd.read_csv(file_path)

   # access code generated responses 
      responses = {}
      responses_length = 5
      for num in range(responses_length):
         response = df.iloc[num, 1]
         cluster = df.iloc[num, 2]
         responses[num] = (response, cluster)

   # access current clusters
      clusters = {}
      for key, (response, clusternum) in responses.items():
         if clusternum not in clusters:
            clusters[clusternum] = []
            clusters[clusternum].append(response)

   # access representatives of each cluster
      reps = {}
      for c, r in clusters.items():
         reps[c] = r[0]

   # merge clusters depending on GPT4 output
      merged = {}
      current_cluster = 1

      for cluster1, rep1 in reps.items():
         if cluster1 in merged:
            continue
         merged[cluster1] = current_cluster
         for cluster2, rep2 in reps.items():
            if cluster2 != cluster1 and cluster2 not in merged:
               response = client.responses.create(
                  model="gpt-4.1",
                  input= f"Consider these two functions:\n"
                  f" 1: {rep1}\n"
                  f" 2: {rep2}\n"
                  "Are they semantically equivalent (i.e., they have the same behaviour but may have different syntax)? Answer Yes or No."
               )
               if "yes" in response.output_text.lower():
                  merged[cluster2] = current_cluster
         current_cluster += 1

      new_responses = {}
      for key, (resp, cluster) in responses.items():
         new_cluster = merged[cluster]
         new_responses[key] = (resp, new_cluster)

      # create output file
      output_folder = "GPT4clustered"
      os.makedirs(output_folder, exist_ok=True)
      filename = file
      filepath = os.path.join(output_folder, filename)
      
      # record results in output file
      with open(filepath, 'w', newline='', encoding='utf-8') as f:
         writer = csv.writer(f)
         writer.writerow(['response_num', 'response', 'cluster'])
         for i, (key, (response, cluster)) in enumerate(new_responses.items(), start=1):
            writer.writerow([i, response, cluster])
    
      # make sure all responses are in files 
      final_df = pd.read_csv(filepath)
      if len(final_df) != 5:
         print("response(s) missing")
    
