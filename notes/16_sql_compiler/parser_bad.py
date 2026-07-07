def main():
    clauses=["SELECT", "FROM", "WHERE"]
    while True:
        query=input("sql> ")
        clause_params={}
        for i, clause in enumerate(clauses):
            if clause in query:
                params=query.split(clause)[1] # get rid of clause
                if i != len(clauses)-1: # use the next clause to get param list
                    params=params.split(clauses[i+1])[0]
                    
                clause_params[clause]=params
                query=query.split(clause+params)[1]
        
        print(clause_params)
             

if __name__ == "__main__":
    main()