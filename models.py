from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str

# Deleting account
class DeleteAccountModel(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

# Pet Owner Signup
class PetOwnerSignup(UserBase):
    full_name: str
    dob: str
    phone_number: str
    pet_info: Optional[List['PetInfo']] = Field(default_factory=list)

class PetInfo(BaseModel):
    name: str
    category: str
    breed: str
    age: str
    color: str
    vaccinations: List[str]
    vaccination_details: str
    image: Optional[str]
    description: str
    identification_marks: str
    gender: str
    size: str
    health_status: str
    location: str

# Vet Signup
class VetSignup(UserBase): 
    full_name: str
    license_number: str
    specialization: str
    phone_number: str
    clinic_address: str
    working_hours: str
    qualifications: List[str]
    degree_name: str
    university: str
    graduation_year: str
    certifications: Optional[List[str]]
    affiliations: Optional[List[str]]
    profile_picture: Optional[str]
    social_links: Optional[List[str]]
    languages_spoken: List[str]
    clinic_services: List[str]

# Seller Signup
class SellerSignup(UserBase): 
    full_name: str
    business_name: Optional[str]
    phone_number: str
    business_address: str
    national_id_number: str
    national_id_images: List[str]
    profile_picture: Optional[str]
    license_certification: Optional[str]

# Non Pet Owner Signup
class NonPetOwnerSignup(UserBase):
    full_name: str
    dob: str
    phone_number: str

# Login model
class LoginModel(BaseModel):
    email: EmailStr
    password: str

# OTP for delete request
class DeleteOTPRequest(BaseModel):
    email: EmailStr

class VerifyDeleteOTP(BaseModel):
    email: EmailStr
    otp: str

PetOwnerSignup.update_forward_refs()
