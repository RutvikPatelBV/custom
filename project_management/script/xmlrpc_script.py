import xmlrpc.client

# Configuration
url = 'https://demo4.odoo.com/'
db = 'demo_saas-172_bd65a2452965_1716959044'
username = 'admin'
password = 'admin'

# Common endpoint
common_endpoint = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common_endpoint.authenticate(db, username, password, {})

if uid:
    # Object endpoint
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    customer_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['customer_rank', '>', 0]]])

    print(customer_ids)

    # # Create(WRITE)
    # models.execute_kw(db, uid, password,
    #                   'res.partner', 'create',
    #                   [{'name': 'Bill Gates', 'customer_rank': 2}])

    # # UPDATE
    # for id in customer_ids:
    #     record = models.execute_kw(db, uid, password,
    #                                'res.partner', 'read', [id],
    #                                {'fields': ['name', 'country_id', 'comment']})
    #     name_for_update = f"{record[0]['name']} (Our Customer)"
    #     print(name_for_update)
    #     models.execute_kw(db, uid, password,
    #                       'res.partner', 'write',[[id], {'name':name_for_update}])

    # # SEARCHCOUNT
    # customer_count=models.execute_kw(db,uid,password,'res.partner','search_count',[[['customer_rank','>',0]]])
    # print(customer_count)

    # READ
    readed_records = models.execute_kw(db, uid, password,
                                       'res.partner', 'read', [customer_ids],
                                       {'fields': ['name', 'country_id', 'comment']})
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for rec in readed_records:
        print(rec)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # SEARCHREAD
    partners = models.execute_kw(db, uid, password,
                                 'res.partner', 'search_read',
                                 [[]], {'fields': ['name', 'country_id', 'comment'], 'limit': 10})

    for partner in partners:
        print(partner)
    # # UNLINK
    # models.execute_kw(db,uid,password,'sale.order','unlink',[2])
else:
    print("Failed to authenticate")
