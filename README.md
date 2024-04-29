# SVG taxonomy

This repo hosts the supplemental material as a submission to IEEE VIS 2024

**Paper Title**

Zhongzheng Xu, Emily Wall

*IEEE Transactions on Visualization and Computer Graphics (TVCG, Proc. IEEE VIS'24). 2024.*

## Abstract 
Data visualizations help extract insights
from datasets, but reaching these insights requires decomposing
high level goals into low-level analytic tasks that can be complex
due to varying data literacy and experience. Recent advancements
in large language models (LLMs) have shown promise for lowering
barriers for users to achieve tasks such as writing code. Scalable
Vector Graphics (SVG), a text-based image format common in data
visualizations, matches well with the text sequence processing of
transformer-based LLMs. In this paper, we explore the capability of
LLMs to perform low-level visual analytic tasks defined by Amar,
Eagan, and Stasko directly on SVG-based visualizations. Using
zero-shot prompts, we instruct the models to provide responses or
modify the SVG code based on given visualizations. Our findings
demonstrate that LLMs can effectively modify existing SVG visu-
alizations for specific tasks like Cluster but perform poorly on tasks
requiring a sequence of math operations. We also discovered that
LLM performance varies based on factors such as the number of
data points, the presence of value labels, and the chart type. Our
findings contribute to gauging the general capabilities of LLMs and
highlight the need for further exploration and development to fully
harness their potential in supporting visual analytic tasks.

## SVG Visualizations

Below are examples of the three chart types with each of the plot difficulties that we tested in our study.
| Difficulty | Scatterplot | Line Chart | Bar Chart|
|------------|-------------|------------|----------|
| Small Unlabeled  | ![Image1](./images/scatter/easy_unlabeled/scatter_data_0.svg) | ![Image1](./images/line/easy_unlabeled/line_data_0.svg) | ![Image1](./images/bar/easy_unlabeled/bar_data_0.svg) |
| Small Labeled    | ![Image1](./images/scatter/easy_labeled/scatter_data_0.svg) | ![Image1](./images/line/easy_labeled/line_data_0.svg) | ![Image1](./images/bar/easy_labeled/bar_data_0.svg) |
| Medium Unlabeled | ![Image1](./images/scatter/hard_unlabeled/scatter_data_0.svg) | ![Image1](./images/line/hard_unlabeled/line_data_0.svg) | ![Image1](./images/bar/hard_unlabeled/bar_data_0.svg) |
| Medium Labeled   | ![Image1](./images/scatter/hard_labeled/scatter_data_0.svg) | ![Image1](./images/line/hard_labeled/line_data_0.svg) | ![Image1](./images/bar/hard_labeled/bar_data_0.svg) |

Each task difficulty for charts we generated is summarized in this table:
| Chart Type        | Data Points/Bins | Outliers | Clusters |
|-------------------|------------------|----------|----------|
| Scatter (Small)  | 20               | 1        | 2        |
| Scatter (Medium) | 50               | 2        | 3        |
| Bar (Small)      | 10               | 1        | N/A      |
| Bar (Medium)     | 25               | 2        | N/A      |
| Line (Small)     | 10               | 1        | N/A      |
| Line (Medium)    | 25               | 2        | N/A      |

Data points for creating these plots are generated using `data_generation/gen_data.py`, which can be specified using command line arguments. You can specify the number of data points, chart type, and number of separate datasets to generate. Example:

`python3 gen_data.py --data_type scatter --n_points 30 --n_datasets 20 --output_folder {OUTPUT_PATH}`

The plots are then plotted using `data_generation/plot.py`, which again can be specified using command line arguments. You can specify the chart type, input and output folders, as well as whether to label the data points. Example:

`python plot.py --data_type scatter --input_folder {INPUT_PATH} --output_folder {OUTPUT_PATH} --label`

## Prompts
The prompts are located in `llm/prompt.json`. We created a prompt for each low-level visual taxonomy that we tested. One example prompt:

```
<input>: An SVG scatter plot with n points. The points are not labeled with their coordinates. The axes, title, legends, and other unnecessary elements are omitted for simplicity.

<output>: SVG code only and no other textual response

Instructions:

1. Identify the one outlier in the scatter plot, defined as data points that significantly deviate from the clusters.
2. Reconstruct the SVG scatter plot, coloring the outlier with a different color compared to the rest of the points.
3. Omit the axes, title, legends, and any other unnecessary elements in the reconstructed SVG.
4. Ensure that the reconstructed SVG contains only the data points, with the same number of points as the input SVG.
5. Include the necessary shape definitions in the reconstructed SVG code.Please provide the complete SVG code for the scatter plot with the outliers colored differently, without any additional textual response.

<input SVG scatterplot>: 
```

## Low-level Visual Taxonomy
To test the low-level visual tasks, we employed OpenAI's `gpt4-turbo-preview` model, we then used `llm/completion.py` to run the tests. The file allows us to asychronously send a number of prompts to OpenAI's API and retrieve results as a whole. 

## Citation 






