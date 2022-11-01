#!/usr/bin/python3
# -*- coding: utf-8 -*-
import hashlib
import time

import data_utils
from androguard.core.bytecodes.apk import APK


def get_cert_md5_v2(android_guard):
    cert_md5 = ''
    certs = set(android_guard.get_certificates_der_v2() + [android_guard.get_certificate_der(x) for x in android_guard.get_signature_names()])
    for cert in certs:
        cert_md5 = hashlib.md5(cert).hexdigest()
    return cert_md5


def get_cert_md5_v3(android_guard):
    cert_md5 = ''
    certs = set(android_guard.get_certificates_der_v3() + [android_guard.get_certificate_der(x) for x in android_guard.get_signature_names()])
    for cert in certs:
        cert_md5 = hashlib.md5(cert).hexdigest()
    return cert_md5


def get_apk_info(apk_path, category):
    print('\r get apk info -> file path : %s, category : %s' % (apk_path, category))
    try:
        android_guard = APK(apk_path)
        if android_guard.is_valid_APK():
            update_time = round(time.time() * 1000)
            app_signature_v2 = get_cert_md5_v2(android_guard)
            app_name = android_guard.get_app_name()
            package_name = android_guard.get_package()
            version_name = android_guard.get_androidversion_name()
            version_code = android_guard.get_androidversion_code()
            target_sdk = android_guard.get_target_sdk_version()
            app_signature_v3 = get_cert_md5_v3(android_guard)
            permissions_declare = android_guard.get_permissions()
            print(permissions_declare)
            print(android_guard.get_libraries())
            data_utils.write_data(app_name, version_name, version_code, package_name, app_signature_v2, update_time, target_sdk, app_signature_v3, category)
    except Exception as e:
        print('\rget apk info : exception >>', e)
