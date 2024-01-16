from rest_framework.exceptions import APIException


class InvalidAdFeatureKind(APIException):
    default_detail = "Invalid adfeature kind."
    default_code = "invalid_ad_feature_kind"
    status_code = 400
