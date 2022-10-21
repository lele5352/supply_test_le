from config.mysql_config import mysql_config
from config.api_config import url_prefix

env_configs = {
    #26环境
    'test_26': {
        'app_prefix': url_prefix.get("evn_26"),
        'transfer_service_prefix': url_prefix.get("transfer_service_26"),
        'ims_service_prefix': url_prefix.get("ims_service_26"),

        'mysql_info_auth': {'mysql_info': mysql_config.get('test_26'), 'db': 'supply_auth'},
        'mysql_info_wms': {'mysql_info': mysql_config.get('test_26'), 'db': 'supply_wms'},
        'mysql_info_ims': {'mysql_info': mysql_config.get('test_26_ims'), 'db': 'homary_ims'},
    },
    #160环境
    'test_160': {
        'app_prefix': url_prefix.get("evn_160_app"),
        'web_prefix': url_prefix.get("evn_160_web"),
        'transfer_service_prefix': url_prefix.get("transfer_service_160"),
        'ims_service_prefix': url_prefix.get("ims_service_160"),

        'mysql_info': mysql_config.get('test_160'),
    },
    #uat环境
    'test_uat': {
        'app_prefix': url_prefix.get("evn_uat_app"),
        'web_prefix': url_prefix.get("evn_uat_web"),
        'transfer_service_prefix': url_prefix.get(""),
        'ims_service_prefix': url_prefix.get(""),

        'mysql_info_auth': {'mysql_info': mysql_config.get('test_uat')}
    },
    #189环境
    'test_189': {
        'app_prefix': url_prefix.get("evn_189_app"),
        'web_prefix': url_prefix.get("evn_189_web"),
        'transfer_service_prefix': url_prefix.get(""),
        'ims_service_prefix': url_prefix.get(""),

        'mysql_info_auth': {'mysql_info': mysql_config.get('test_189')}
    }

}