data = {
"eventData":{
    "product":{"reference":"55318e9f-397f-4bac-913a-b4f45a6f8a55",
            "type":"RESERVED_ACCOUNT"
             },
    "transactionReference":"MNFY|33|20230118133906|000893",
    "paymentReference":"MNFY|33|20230118133906|000893",
    "paidOn":"2023-01-18 13:39:08.483",
    "paymentDescription":"str",
    "metaData":{},
    "paymentSourceInformation":[
        {"bankCode":"",
        "amountPaid":400,
        "accountName":"Monnify Limited",
        "sessionId":"0v34QH5wMAfTvTz3qjK68MYSk2uhTcAH",
        "accountNumber":"0065432190"
        }],
    "destinationAccountInformation":{"bankCode":"035",
    "bankName":"Wema bank",
    "accountNumber":"5000573622"},
    "amountPaid":400,
    "totalPayable":400,
    "cardDetails":{},
    "paymentMethod":"ACCOUNT_TRANSFER",
    "currency":"NGN",
    "settlementAmount":"390.00",
    "paymentStatus":"PAID",
    "customer":{"name":"string string","email":"string@test.com"}
    },
"eventType":"SUCCESSFUL_TRANSACTION"
    }

print(data['eventData']['product']['reference'])
print(data['eventData']['amountPaid'])
print(data['eventData']['customer']['email'])
print(data['eventType'])
