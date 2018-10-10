# Reactful USF ML Project
Machine Learning of past Reactful data with Tensorflow in the Google Cloud Platform.

## Important Keys
 country, region, type, device, page, reaction, utctimestamp

## Important Meanings

 type: if value: 'new' is new session, if value: 'returning' is returning session
 goal: Completed goal ID
 device: One of: desktop mobile tablet
 page: current page
 reaction: Reaction ID triggered

# Some Challenges to Figure out
Under the assumption Tensorflow wants numbers and single dimension arrays.
 * sessions over time of unique user
 * goals over time
 * page transitions over time
