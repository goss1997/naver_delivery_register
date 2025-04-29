from pydantic import BaseModel

class DeliveryRegisterRequest(BaseModel):
    login_id: str
    login_pw: str
    mall_name: str
    manager_name: str
    phone_number: str
    delivery_company: str
    biz_number: str
    contract_number: str
    origin_name: str
    origin_zipcode: str
    origin_address1: str
    origin_address2: str
    origin_phone: str

class DeliveryRegisterResponse(BaseModel):
    success: bool
    message: str