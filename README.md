# Reactful USF ML Project
Machine Learning of past Reactful data with Tensorflow in the Google Cloud Platform.

# File Parser Detailed Technical Details

## Loading file
We have a CSV file: file with comma seperated values with top header being the labels for the headers and the values all at the same index of it's associated header.

We need a matrix of numbers: with matrix[0] being a single user session and matrix[0][0] being a specific value important to the training

To convert the CSV file we go through the file line by line: if the line happens to be the first we will note down it's labels for use later.
If not, we will go through the line (split by comma AKA everything between two commas is an important value)

For Example:
```
file = load("filename.csv")
headers = array

for(line in file){
	
	if(lineNumber is 1){

		headers = the line split by comma and space character

	}
	else {
		
		for(value in (line split by comma and space character)){

			//decide what to do with value

		}

	}

}

```

## Map (Dictionary)

Certain values need to go to certain indexes in the matrix some computed some not. We will know where to put the number by checking a dictionary called map that if given the key will return the index of the position to place the value in the matrix.

For Example:
```
map = { 'region': 1 }

map['region'] // is 1 meaning place the value into matrix[ last_index ][ 1 ]

```

## Possible Values (Dictionary)
Initialized as:
 ```
 possible_values = { 
 	'country': [],
 	'region': [],
 	'type': [],
 	'device': [],
 	'page': [],
 	'reaction': [] 
 }
 ```
 ### Use
 Tensorflow likes numbers not string, so we need to make a string into a number. How we will do that is keep track of all the strings we have seen (as one of the values of this dictionary), and if the value we are looking at is in this dictionary we will use the index of the array as the number we need. If it is not in the array we will need to add it to the array and use that index (which happens to be the length of the array)

 For Example:
 ```
 current_key = 'country'//the current key we are looking at
 current_value = 'US'//the current value we are looking at

 /*
Let's say 
possible_values['country'] = ["China","Taiwan","US"]
then
 */


 if(possible_values[current_key].has(current_value)){

   //will be true since "US" is in the array above

   index_we_need = possible_values[current_key].indexOf(current_value)

 }
 else{
 	index_we_need = possible_values[current_key].length
	possible_values[current_key].add(current_value)

 }

 ```

## Unique IDs (Set)
Used to determine whether to add another row to the matrix or not. Rows in the matrix are sessions of a user and we are trying to condense each session into a row. So if we see a unique session id that we haven't seen before we should add a new row to the matrix since it's a new session.

```
unique_ids = new Set();

	current_key="unique_session_id"
	current_value="001"
	if(unique_ids.has(current_value)){
		//is not a new session so we are modifying an existing session
	}
	else{
		//is a new session so add another array to the matrix
	}
```

## Matrix
matrix will store all of the values we will need for training where rows in the matrix are sessions of a user and we are trying to condense each session into a row. What is most important about the matrix is where we are placing it's values (which column).

I propose a row should look like this:
[ start time, end time, average time on page, country, region, type, device, page count, reaction combination, goal combination]

This will be one session of many so it is a matrix of these.

## How Each value is computed

### Page Count
The easiest to compute is probably page count. Which is literally just the count of times that "page" is the objectType for each unique session.
It is already a number so it does not need the map dictionary. This should just update the 7th item in the current session we are looking at within the matrix. 7 because it is the index of the ordering I proposed above (this can change). So if there is no value there you have to initialize it to 0 and add 1 each time you see page.
For Example: 
```
current_value="page"
if(current_value === "page"){
	//we found page so we should add 1 
	matrix[current_matrix_index][7]++
}
```

### Start Time & End Time
This one will require parsing of UTC timestamps (maybe needs a library but probably not). If this is the first unique session then this will be the start time and the end time and we will update this as we get more info. As we get more info we should always compare the current session in the matrix's start time to the current start time to see which is lower and store the lower one in the matrix. This is pretty much exactly the same as for the end time except we want the higher one store in the matrix.
For Example: 
```
current_value="Wednesday10:03PM_UTC"

if(current_value.isLowerThan(matrix[current_matrix][0])){
	//current value is the smallest we have seen so we should store into the matrix at position 0 according to the ordering I proposed
	matrix[current_matrix_index][0] = current_value;
}

if(current_value.isHigherThan(matrix[current_matrix][1])){
	//current value is the highest we have seen so we should store into the matrix at position 1 according to the ordering I proposed
	matrix[current_matrix][1] = current_value;
}

```

#### Meeting 10 / 17
ignore country as we have region
count goals maybe since it may not be that important
bigquery timestamp length
Ultimately we have an input matrix but the output needs to be a specific reaction type which we will have an ID of (because of reaction completed id). which needs to be mapped out to a string like: "page_exit_lightbox"

We can do a Hash of the reaction combination string(all reaction ids in order) to get unique ids
Test with and without the goal combination as it may not be important

#### For BigQuery reduction: 

[start time, end time, region, type, device, page_count, reaction combination, goal combination, reaction completed]
start_time: function that keeps the smallest timestamp seen
end_time: function that keeps the largest timestamp seen
page_count: sub query sum() of page transitions
reaction_combination: concat of all reaction IDs seen in order by time
goal_combination: concat of all goal IDs seen in order by time
reaction completed: The id of the reaction that completed which will be needed for the output (won't be trained with)

#### Post-Process:

Transform strings to ints with indexes of label lists (Figure out issue with session ordering matters)
average time per page calculation


### Average time on page
This uses all three of: start time, end time and page count. So we need to wait for all of the values to come in (because start and end time can change throughout the loops). So we should compute this value when a new user session is found. The formula is: `(end_time - start_time) / page_count`

# Tasks left

## Machine Learning

We need to begin working on the machine learning portion of the project which has a lot of stuff going on but hopefully I can explain our strategy well enough. So we will begin by just figuring out the minimum to get this dataset to be able to train (this may involve some changes to the `file_parser` but we need not worry about it too much as it will eventually be phased out with the BigQuery version that will create the same thing directly off of the cloud). Once we have that minimum we will need to evaluate if any of our data is hindering our process (such as goals which we will probably remove). Then we need to optimize our learning algorithm for the types of data that we have, we have quite a few variables to keep in check so we should look up based on the type of data to see what is the best method for each.

#### To put it more simply:

1. Figure out minimum code to get to train
2. Re-evaluate data to remove unneccesary data (such as goals)
3. Optimize training algorithms for our specific data
4. Repeat




## Google BigQuery
We need to create pretty much what file_parser does but off of a Google BigQuery SQL statement with a little bit of post proccessing afterwards. A high level description would be that we need to perform: Google BigQuery SQL Selection of data -> Post Proccess data to be what `file_parser` creates -> return matrix, and label dictionary like `file_parser`.
### Why?
All of the data we are interested in is stored in a BigQuery database. The way to extract the data that we need we use BigQuery's SQL language to pull it out. So while we are already writing SQL queries to extract the data we should make the SQL do the work of transforming it into a format which is more usable to us. This also helps with performance as it is less to transfer because the transform greatly reduces the size of a result set. Also this offloads data manipulation to a server that was made to perform these sort of queries.

### SQL pt.1
Need to look into the BigQuery SQL language to be able to group entire sessions (many rows in the BigQuery database) into a single session result that should be representitive of that entire session. It would look like:
```
[start_time, end_time, region, type, device, page_count, reaction_combination, goal_combination]
```
#### `start_time` & `end_time`
This will need to be some sort of function to pick the minimum and maximum timestamp throughout all of the values seen, this will need to be researched as to how it works so long as we are able to pick out the smallest timestamp and largest timestamp and be able to plane them into the first and second positions

#### `region, type, device`
These will just need to be picked out when the corresponding objectType happens to be what these keys are. Since these values only seem to appear once per session we will just use whatever value we find associated to represent the session as a whole. Basically, pick `region`'s value and place into 3rd position and do the same with `type`'s value being placed into the 4th position.

#### `page_count`
This will be a sum of the number of times which `page` has been seen throughout a session. This is one of the most common operations done by SQL so it should be pretty easy to find documentation on how to do this.

#### `reaction_combination` & `goal_combination`
This will be where we gather `reaction`s and `goal`s into probably a string seperated by spaces(can be anything comma's would be great too). The `reaction`s and `goal`s are numeric IDs that we need all values of in order to properly represent a session. So we need to research the coalescing of multiple values into a single string value to be in the last two positions

### SQL pt.2
We need another SQL query to be able to count all of the possible values of the fields which are categorical for tensorflow, i.e. `[region, type, device, reaction_combination, goal_combination]`
Caveat: I'm pretty sure that `type` and `device` will always be `2` and `3` respectively but there is always the possibility that it can change so we may as well count them anyway.
So for each of those categorical inputs we need to count the number of unique values that we see for each.

## Post-Processing
Once we have the results from the SQL we will need to transform this into a matrix usable by Tensorflow.

#### `session_length` & `average_time_per_page`
These were derived values that we can also derive from the info we have in the result set. 
```
session_length = get_session_length(start_time,end_time)
average_time_per_page = session_length / page_count
```

## Important Meanings Overall

 type: if value: 'new' is new session, if value: 'returning' is returning session
 goal: Completed goal ID
 device: One of: ['desktop', 'mobile', 'tablet']
 page: current page
 reaction: Reaction ID triggered

# Some Challenges to Figure out
~Under the assumption Tensorflow wants numbers and single dimension arrays.~ [Not true see this: tensorflow feature columns](https://www.tensorflow.org/guide/feature_columns)

 * sessions over time of unique user
 * ~goals and reactions over time~ [Fixed using the feature columns concept](https://github.com/Reactful-USF-ML-Project/USF-ML-Project/commit/13078037e1f6ddc624623e4ba80ab1e4e45ef878)
 * page transitions over time (Maybe a frequency occurrence of all pages seen?)

# TODO
 * I have changed how the result matrix looks so I will need to come up with a description of it but it may change as we train so leave it for now
 * BigQuery transfer project data to another project
 * Object constant update as bigquery events come in (how to handle this sort of thing).
 * 
