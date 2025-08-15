import pandas as pd
import os
from codebleu import calc_codebleu  
import sys

if len(sys.argv) < 2:
   print("Error: no input folder.")
   sys.exit(1)
input_folder = sys.argv[1]

for file in os.listdir(input_folder):
   if file.endswith(".csv"):
      print(f"Clustering: {file}")
      # access file
      file_path = os.path.join(input_folder, file)
      df = pd.read_csv(file_path)

      # access each function in file
      responses = []
      for num in range (0, 5):
         responses.append(df.iloc[num, 2])

      def add_cluster(num, response, response_num):
         clusters.append({
            'response_num': response_num,
            'response': response,
            'cluster': num
         })
         response_num += 1
         return response_num

      def get_cluster(clusters, response):
         for item in clusters:
            if item['response'] == response:
               return item['cluster']


      clusters = []
      cluster_num = 1

   # add to cluster if codebleu score over threshold

      threshold = 0.9
      response_num = 1
      for j in range(len(responses)):
         not_assigned = True
         for i in range(j):
            if i == j:
               continue
            ref = responses[i]
            pred = responses[j]
            res = calc_codebleu([ref], [pred], "python")
            if res["codebleu"] >= threshold:
               cluster_i = get_cluster(clusters, responses[i])
               if cluster_i is None:
                  cluster_i = cluster_num
                  cluster_num += 1
               response_num = add_cluster(cluster_i, responses[j], response_num)
               not_assigned = False
               break
         if not_assigned:
            response_num = add_cluster(cluster_num, responses[j], response_num)
            cluster_num += 1

      df2 = pd.DataFrame(clusters)

      output_folder = "codebleu_responses"


      os.makedirs(output_folder, exist_ok=True)

      file_path = os.path.join(output_folder, file)
      df2.to_csv(file_path, index=False)

      expected_rows = 5
      expected_cols = 3

      actual_rows, actual_cols = df2.shape

      if actual_rows != expected_rows or actual_cols != expected_cols:
         print(f"Warning: Output file has {actual_rows} rows and {actual_cols} columns")

