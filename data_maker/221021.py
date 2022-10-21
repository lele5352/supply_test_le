box_detail= {
                'boxNo': 'DC2210210012-1',
                'skuType': 3,
                'skuQty': 12,
                'skuShelfQty': 1,
                'waitOnShelfQty': 11,
                'transferInNo': 'DR2210210011',
                'boxQty': 1,
                'boxShelfQty': 0,
                'waitOnShelfBoxQty': 1,
                'details': [{
                    'waresSkuQty': 4,
                    'waresSkuReceiptQty': 4,
                    'waresSkuShelfQty': 0,
                    'waitOnShelfQty': 4,
                    'waresSkuCode': '53586714577B02',
                    'waresSkuName': '部件2 2/2 X2',
                    'goodsSkuCode': '53586714577',
                    'goodsSkuName': '决明子',
                    'waresSkuExceptionQty': 0,
                    'goodsSkuMap': 2,
                    'bomVersion': 'B',
                    'goodsSkuImg': 'https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg'
                }, {
                    'waresSkuQty': 4,
                    'waresSkuReceiptQty': 4,
                    'waresSkuShelfQty': 1,
                    'waitOnShelfQty': 3,
                    'waresSkuCode': '53586714577C01',
                    'waresSkuName': 'bom-C：1 1/1 X1',
                    'goodsSkuCode': 'BP53586714577C01',
                    'goodsSkuName': '决明子',
                    'waresSkuExceptionQty': 0,
                    'goodsSkuMap': 1,
                    'bomVersion': None,
                    'goodsSkuImg': 'https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg'
                }, {
                    'waresSkuQty': 4,
                    'waresSkuReceiptQty': 4,
                    'waresSkuShelfQty': 0,
                    'waitOnShelfQty': 4,
                    'waresSkuCode': '53586714577B01',
                    'waresSkuName': '部件1 1/2 X1',
                    'goodsSkuCode': 'BP53586714577B01',
                    'goodsSkuName': '决明子',
                    'waresSkuExceptionQty': 0,
                    'goodsSkuMap': 1,
                    'bomVersion': None,
                    'goodsSkuImg': 'https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg'
                }]
            }

# 逐渐上架请求参数
info = {
            "boxNo": "DC2210210012-1",
            "storageLocationCode": "KW-SJQ-01",
            "transferInNo": "DR2210210011",
            "details": [{
                "waresSkuCode": "53586714577C01",
                "quantity": 1
            }]
        }