import os
import matplotlib.pyplot as plt
from image_counter import count_images_in_folder

def create_tag_chart(directory_path, top_tags):
  project_name = os.path.basename(directory_path)
  total_image_count = count_images_in_folder(directory_path)
  parent_directory = os.path.dirname(directory_path)

  # Extract tags and counts
  tags = list(top_tags.keys())
  counts = list(top_tags.values())

  num_tags_to_show = 20  #@param {type:"integer"}
  tags_to_ignore_in_chart = "uncensored, breasts, blush, penis, hetero, cum, pussy, nude, open mouth, pubic hair, highres" #@param {type:"string"}


  # Extract tags and counts
  tags = list(top_tags.keys())
  counts = list(top_tags.values())

  # Exclude specified tags from the chart
  tags_to_ignore = set(map(str.strip, tags_to_ignore_in_chart.split(',')))
  tags_and_counts = list(zip(tags, counts))
  filtered_tags_and_counts = [(tag, count) for tag, count in tags_and_counts if tag not in tags_to_ignore]

  # Sort tags and counts by counts in descending order
  sorted_indices = sorted(range(len(filtered_tags_and_counts)), key=lambda k: filtered_tags_and_counts[k][1], reverse=True)

  tags_to_show = [filtered_tags_and_counts[i][0] for i in sorted_indices[:num_tags_to_show]]
  counts_to_show = [filtered_tags_and_counts[i][1] for i in sorted_indices[:num_tags_to_show]]

  # Calculate percentages for each tag
  percentages = [(count / total_image_count) * 100 for count in counts_to_show]

  # Plot the bar chart for the top tags
  plt.figure(figsize=(10, 8))
  bars = plt.bar(tags_to_show, counts_to_show, color='blue')
  plt.xlabel(f'Top {num_tags_to_show} Tag Occurrences (excluding specified tags)')
  plt.ylabel('Number of Occurrences')
  plt.title(f'{project_name}')
  plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

  # Display percentages at the top of each bar
  for bar, percentage in zip(bars, percentages):
      height = bar.get_height()
      plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05 * total_image_count, f'{percentage:.0f}%', ha='center')

  chart_filename = os.path.join(parent_directory, f"{project_name}_chart.png")
  plt.savefig(chart_filename, bbox_inches='tight')

  # Show the chart
  plt.show()