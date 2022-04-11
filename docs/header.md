# Introduction

# Description

- First POST endpoint receives a JSON in the form of a document with two fields: a pool-id (numeric) and a pool-values (array of values) and is meant to append (if pool already exists) or insert (new pool) the values to the appropriate pool (as per the id)
- Second POST is meant to query a pool, the two fields are pool-id (numeric) identifying the queried pool, and a quantile (in percentile form)
- Required data must meet the following conditions:
    - poolId: is a positive integer starting from 0
    - poolValues: is a 1-dimensional array of integers
    - peecentile: is a numeric in the range 0-100
- The data is organized by index. There is a file that stores the entire index for search, the data will be saved into different files based on poolId.


# Processing functions
### validate_input()
| Name        | Description                                                                                                                              |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------|
| input       | dict                                                                                                                                     |
| output      | boolean                                                                                                                                  |
| description | Input data request from first POST endpoint. Check the input condition of the data. Returns True if the condition is met, False otherwise. |

### validate_input2()
| Name        | Description                                                                                                                               |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| input       | dict                                                                                                                                      |
| output      | boolean                                                                                                                                   |
| description | Input data request from second POST endpoint. Check the input condition of the data. Returns True if the condition is met, False otherwise. |

### id_to_path()
| Name        | Description                                                                    |
|-------------|--------------------------------------------------------------------------------|
| input       | poolId                                                                         |
| output      | path                                                                           |
| description | Input is a poolId and return the data path of that poolId. |

### add_pool_id()
| Name        | Description                                            |
|-------------|--------------------------------------------------------|
| input       | poolId                                                 |
| output      | None                                                   |
| description | Add new poolId to file poolIds.txt (only contains poolId) |

### check_pool()
| Name        | Description                                 |
|-------------|---------------------------------------------|
| input       | poolId                                      |
| output      | boolean                                     |
| description | Check if a poolId has been created. |

### load_data():
| Name        | Description                                 |
|-------------|---------------------------------------------|
| input       | path                                        |
| output      | dict                                        |
| description | Load all data from the path |

### calculate_quantile()
| Name        | Description                                                                          |
|-------------|--------------------------------------------------------------------------------------|
| input       | numberic Array, peecentile                                                           |
| output      | quantile of array                                                                    |
| description | Input is an array of numbers and percentile. Returns the calculated quantile of the array according to the given pecentile. |

### get_pool()
| Name        | Description                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------------|
| input       | poolId                                                                                                |
| output      | dict                                                                                                  |
| description | Use the function id_to_path(), load_data(). Returns a dict containing only the data of the input poolId. |

### create()
| Name        | Description                                                                                                                                            |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| input       | dict                                                                                                                                                   |
| output      | None                                                                                                                                                   |
| description | Use id_to_path(), load_data(), add_pool_id() functions. Get input data as a dict containing poolid, poolValues. Write new data to the file corresponding to poolId. |

### update()
| Name        | Description                                                                                                                                                          |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| input       | poolId, poolValues                                                                                                                                                   |
| output      | None                                                                                                                                                                 |
| description | Use the function id_to_path(), load_data(). Append poolValues by poolId |

### post1()
| Name        | Description                                                                                                                                                                                                                                                                                                                                |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| input       | json                                                                                                                                                                                                                                                                                                                                       |
| output      | json                                                                                                                                                                                                                                                                                                                                       |
| description | Handle requests from first POST endpoint. Use the validate_input() function to check the request data, if the condition is not met, return the message "invalid input". Check if poolId already exists. If poolId does not exist, create() will be used and return "inserted" message. If poolId already exists, use update() and return "appended" message. |

### post2()
| Name        | Description                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| input       | json                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| output      | json                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| description | Handle requests from second POST endpoint. Use the validate_input2() function to check the request data, if the condition is not met, return the message "invalid input". Check if poolId already exists. If poolId already exists, get_pool() function will be used to load the requested poolId data. Then use the calculate_quantile() function, which returns the calculated quantile and the total count of elements in the pool. IF poolId does not exist, return message "poolId not found" |

# Upgrade plan
When there is data to append, write the new data down without uploading the file to update. Will save as multiple records with the same key. When processing is needed, all records with the same key will be taken out for processing. This will reduce the time it takes to load data when you need to update new data. The downside is that it takes up more storage space.
