# Reactful USF ML Project
Machine Learning of past Reactful data with Tensorflow in the Google Cloud Platform.

# How it all works

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

We can do a MD5 Hash of the reaction combination string(all reaction ids in order) to get unique ids
Test with and without the goal combination as it may not be important

For BigQuery reduction: 
[start time, end time, region, type, device, page_count, reaction combination, goal combination, reaction completed]
start_time: function that keeps the smallest timestamp seen
end_time: function that keeps the largest timestamp seen
page_count: sub query sum() of page transitions
reaction_combination: concat of all reaction IDs seen in order by time
goal_combination: concat of all goal IDs seen in order by time
reaction completed: The id of the reaction that completed which will be needed for the output (won't be trained with)

Post-Process:
Transform strings to ints with indexes of label lists (Figure out issue with session ordering matters)
average time per page calculation


### Average time on page
This uses all three of: start time, end time and page count. So we need to wait for all of the values to come in (because start and end time can change throughout the loops). So we should compute this value when a new user session is found. The formula is: `(end time - start time) / page count`

### TBD 
I'm tired of writing so message me if you get this far and I'll give more instructions.

# Tasks left


## Based on key in objectId we look through possible values
 ```
 possible_values = { 'country': [], 'region': [], 'type': [], 'device': [], 'page': [], 'reaction': [] }
 ```

## Important Meanings

 type: if value: 'new' is new session, if value: 'returning' is returning session
 goal: Completed goal ID
 device: One of: ['desktop', 'mobile', 'tablet']
 page: current page
 reaction: Reaction ID triggered

# Some Challenges to Figure out
Under the assumption Tensorflow wants numbers and single dimension arrays.
 * sessions over time of unique user
 * goals over time
 * page transitions over time


