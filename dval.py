# Taking a function for col data verification

def colvalidate(df, col):
    if df[col].dtype!=object:
        print(f"Column: {col}")
        print()
        print(f"Number of Unique Values: {df[col].nunique()}")
        print()
        print("Unique Values In Column:")
        # if values more than 100 , showing list wise unique values
        if df[col].nunique()>=100:
            for indx in range(0, df[col].nunique(), 100):
                print(df[col].unique()[indx:indx+100])
                print()
        else:
            print(df[col].unique())
            print()
        print("Data Type of Column:", df[col].dtype)
        print()
        print(f"Column: Min -> {df[col].min()} & Max -> {df[col].max()}")
        print("===============================================")
        print()
    else:
        print(f"Column: {col}")
        print()
        print(f"Number of Unique Values: {df[col].nunique()}")
        print()
        print("Unique Values In Column:")
        if df[col].nunique()>=100:
            for indx in range(0, df[col].nunique(), 100):
                print(df[col].unique()[indx:indx+100])
                print()
        else:
            print(df[col].unique())
            print()
        print("Data Type of Column:", df[col].dtype)
        print("===============================================")
        print()