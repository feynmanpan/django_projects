# 造schema
schema = Schema(query=Query)
# 前端post來的sql字串
query_string = '''
    query{
        books{
            title
            isbn        
            price
        }
        pricesMean
        booksCount
    }  
'''
# schema處理sql，回傳結果
context = {
    'booksCount': None,
    'prices': []

}
result = schema.execute(query_string)
# 結果中的查詢資料
pprint(result.errors)
pprint(result.data)
