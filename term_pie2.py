variance = 0.05

# key will be the cluster name and value will be a list containing the terms
cluster_array = []

# key will be the cluster name and value will be a tuple containing the lower limit and the upper limit
cluster_range_array = []

term_matrix = [
    [1.00,0.35,0.50,0.75],
    [0.40,1.00,0.35,0.45],
    [0.23,0.75,1.00,0.43],
    [0.45,0.35,0.23,1.00]
]

'''
this function checks if the 
cos_relation falls in one of the 
clusters, and returns the index
'''
def check_existing_cluster_range(cos_relation):

    for index, cluster_range in enumerate(cluster_range_array):

        for range_name in cluster_range:

            floor_value = cluster_range[range_name][0]
            ceil_value = cluster_range[range_name][1]

            if ( floor_value <= cos_relation <= ceil_value):
                return index

    return -1

'''
this function builds cluster ranges
by looping through the matrix
example output:
c1 : 0.2 - 0.35
c2 : 0.4 - 0.75
...
'''
def cluster_range_builder():

    # loop through the matrix
    for relation_row in term_matrix:

        # loop through each row
        for cos_relation in relation_row:

            # get the (x,y) coordinates of the current cos_relation
            x_term_index = term_matrix.index(relation_row)
            y_term_index = relation_row.index(cos_relation)

            # we skip t1-t1/t2-t2 relations
            if(x_term_index != y_term_index):
                
                # we need to check if the current cos_relation already
                # falls within a cluster range we have built previously
                index = check_existing_cluster_range(cos_relation)

                # if you find an index, a cluster range already exists
                if(index > -1):
                    continue
                else:
                    
                    # if the cos_relation does not fall within any existing cluster range
                    # we build a new cluster range
                    range_index = "c" + str(len(cluster_range_array) + 1)

                    # the range will be "cos_relation - variance" to "cos_relation + variance"
                    range_floor_value = cos_relation - variance
                    range_ceil_value = cos_relation + variance

                    # append it to the cluster_range_array (format of each entry will be as per this function's description)
                    cluster_range_array.append({range_index : (range_floor_value, range_ceil_value,)})
                    
                    # also we start putting in place holders to build the actual cluster array
                    # key will be the cluster name and value will be a list containing the terms
                    cluster_array.append({range_index : []})

                
'''
this function checks if the cos_relation 
lies within an existing range
and returns the cluster name if it does
-1 if it does not fall in any cluster
'''
def check_existing_relationships(cos_relation):

    for index, cluster_range in enumerate(cluster_range_array):
        for name in cluster_range:
            if( cluster_range[name][0] <= cos_relation <= cluster_range[name][1] ):
                return name
    
    return -1

'''
this function builds the actual cluster
output format
c1 : [t1, t3...]
c2 : [t4, t5, t3]
'''
def cluster_builder():

    # loop through the matrix
    for relation_row in term_matrix:

        # loop through each row in the matrix
        for cos_relation in relation_row:

            # get position of the cos_relation
            x_term_index = term_matrix.index(relation_row)
            y_term_index = relation_row.index(cos_relation)
            
            # build a name of the term from the position
            term_a = "t" + str(x_term_index + 1)
            term_b = "t" + str(y_term_index + 1)

            # we skip t1-t1/t2-t2 relations
            if(x_term_index != y_term_index):
                
                # get the cluster name where this cos_relation falls
                cluster_range_name = check_existing_relationships(cos_relation)
                # print(cluster_range_name)

                # we iterate through the cluster array that already holds the 
                # placeholders with cluster names
                for index, cluster_data in enumerate(cluster_array):

                    # insert the terms within the right cluster
                    if(cluster_data.keys()[0] == cluster_range_name):
                        cluster_array[index][cluster_range_name].extend([term_a, term_b])



cluster_range_builder()
cluster_builder()


for index, cluster_range in enumerate(cluster_range_array):

    for key in cluster_range:
        print(key)
        print(cluster_range[key])


print("\n\n")

for index, clusters in enumerate(cluster_array):
    # print(clusters)
    
    for key in clusters:
        print(key)
        print(clusters[key])
        # print(set(clusters[key]))
    