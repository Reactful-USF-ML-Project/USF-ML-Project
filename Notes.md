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
 ~Tensorflow likes numbers not string, so we need to make a string into a number.~ (Turns out this axiom was false causing our entire logic that followed from it to be incorrect, to read what we actually did go [here](#new-implementation)) How we will do that is keep track of all the strings we have seen (as one of the values of this dictionary), and if the value we are looking at is in this dictionary we will use the index of the array as the number we need. If it is not in the array we will need to add it to the array and use that index (which happens to be the length of the array)

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

## Steps to Machine Learning

We need to begin working on the machine learning portion of the project which has a lot of stuff going on but hopefully I can explain our strategy well enough. So we will begin by just figuring out the minimum to get this dataset to be able to train (this may involve some changes to the `file_parser` but we need not worry about it too much as it will eventually be phased out with the BigQuery version that will create the same thing directly off of the cloud). Once we have that minimum we will need to evaluate if any of our data is hindering our process (such as goals which we will probably remove). Then we need to optimize our learning algorithm for the types of data that we have, we have quite a few variables to keep in check so we should look up based on the type of data to see what is the best method for each.

#### To put it more simply:

1. Figure out minimum code to get to train
2. Re-evaluate data to remove unneccesary data (such as goals)
3. Optimize training algorithms for our specific data
4. Repeat

# New Implementation

So it turns out that a lot of our assumptions about how tensorflow liked it's data inputted turned out to be false. Our new implementation still goes through the CSV parses it into a data structure that is not a matrix but a `HashMap<String,Array<Array<String> || Number>>` so it has keys which are strings and values which are either an array of arrays containing strings or an array of numbers. I.E

```python
{
    "region":[["Region of first session"],["Region of second session"]],
    "session_length":[session_length_of_first_session,session_length_of_second_session],
    "page_count":[1,2],
    "avg_time_per_page":[1,2],
    "goal":[["1st goal ID","2nd goal ID"],["2nd goal ID"]],
    "device":[["desktop"],["mobile"],["tablet"]],
    "type":[["returning"],["new"]],
    "reaction":[["1st shown Reaction ID","2nd ID"],["1st shown to second session ID"]]
}
```

With this we also keep record of the last shown reaction ID (because the dataset that this is parsing upon is assumed to be all completed sessions - the last reaction shown to the user is the one which was completed). At the same time we also keep record of all of the possible values that any of the values take in much the same format as above but the values are sets of all the possible values. 

## Actually Training

We have some data which are raw numerical values and some which are strings (even multiple strings). The numerical values are the ones we need to worry the least about since tensor flow works upon numbers easily. The string values need to be converted in such a way that tensorflow can form relationships among them (it has no understanding of the difference between a new and returning user but we don't know the relationship either so we will allow it to do what it is best at and form that relationship on its own). The way that we make tensorflow understand it is through telling tensorflow how to deal with these values using something called categorical column. There are different variations on a categorical column but they all boil down to this, they map categorical data (such as string categories which cannot be easily converted to quantitative data like numbers) into quantitative data like numbers. One of the simplest implementations of this is called the one-hot encoding paradigm which takes an array of strings and converts it into an array of 1s and 0s. We were initally under the presumption that we were to do this conversion ourselves but that ended up being erroneous. 

# Tasks left




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



This ends up being something like (in BigQuery):

```sql
MIN(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as start_time,
MAX(UNIX_MILLIS(TIMESTAMP (CAST(date as STRING)))) as end_time
```



#### `region, type, device`
These will just need to be picked out when the corresponding objectType happens to be what these keys are. Since these values only seem to appear once per session we will just use whatever value we find associated to represent the session as a whole. Basically, pick `region`'s value and place into 3rd position and do the same with `type`'s value being placed into the 4th position.



This ends up being something like (in BigQuery):

```sql
(CASE WHEN ObjectType LIKE 'type' THEN ObjectId ELSE NULL END) as type,
(CASE WHEN ObjectType LIKE 'device' THEN ObjectId ELSE NULL END) as device,
(CASE WHEN ObjectType LIKE 'region' THEN ObjectId ELSE NULL END) as region
```



#### `page_count`
This will be a sum of the number of times which `page` has been seen throughout a session. This is one of the most common operations done by SQL so it should be pretty easy to find documentation on how to do this.

This ends up being something like (in BigQuery):

```sql
COUNT(CASE WHEN ObjectType LIKE 'page' THEN 1 ELSE NULL END) as page_count
```



#### `reaction_combination` & `goal_combination`
This will be where we gather `reaction`s and `goal`s into probably a string seperated by spaces(can be anything comma's would be great too). The `reaction`s and `goal`s are numeric IDs that we need all values of in order to properly represent a session. So we need to research the coalescing of multiple values into a single string value to be in the last two positions

### SQL pt.2
So Roger has given us a base SQL query to work with:
``` SQL
SELECT
  ALL_SESSION_FOR_CLIENT.SessionId,
  ALL_SESSION_FOR_CLIENT.date,
  ALL_SESSION_FOR_CLIENT.EventName,
  ALL_SESSION_FOR_CLIENT.SourceType,
  ALL_SESSION_FOR_CLIENT.ObjectType,
  ALL_SESSION_FOR_CLIENT.ObjectId
FROM (
SELECT
  date,
  SessionId,
  ObjectType,
  ObjectId,
  SourceType,
  EventName
FROM usf_research.Informatica_Data_ALL_06012018_07312018
) AS ALL_SESSION_FOR_CLIENT

INNER JOIN (
SELECT SessionID 
FROM usf_research.Informatica_Data_ALL_06012018_07312018

WHERE ObjectType = 'reaction' AND EventName like 'completed%'

) AS GOAL_COMPLETED_SESSION

ON 
ALL_SESSION_FOR_CLIENT.SessionId = GOAL_COMPLETED_SESSION.SessionId


GROUP BY ALL_SESSION_FOR_CLIENT.SessionId,  ALL_SESSION_FOR_CLIENT.date, ALL_SESSION_FOR_CLIENT.EventName, ALL_SESSION_FOR_CLIENT.ObjectType, ALL_SESSION_FOR_CLIENT.ObjectId, ALL_SESSION_FOR_CLIENT.SourceType
   

ORDER BY  ALL_SESSION_FOR_CLIENT.SessionID
```
If you notice he is doing `SELECT` `FROM` another `SELECT` meaning that he selected data from data he just selected as though it were another table (this is atypical of a normal SQL and is a feature of BigQuery). We will need to query the table that is generated from this to be able to extrapolate the data I identified above (start_time, end_time, region, type, device, reaction_combination, goal_combination) in the way I described.

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
 * Object constant update as bigquery events come in (how to handle this sort of thing).
 * Explain training further and move on to predicting.
 * Add column for time to react complete 
