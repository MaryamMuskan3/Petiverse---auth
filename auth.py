from fastapi import APIRouter, HTTPException, Depends
from Authentication.db_config import user_collection
from Authentication.email_service import send_otp_email, generate_otp
from Authentication.models import *
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import bcrypt

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = "4723e6c1a2e5ce928548a606a2e32b86c41ec701e54cba60c0022cedf4735a11"
ALGORITHM = "HS256"

# Password helpers
def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Token helpers
def create_access_token(email: str, role: str):
    payload = {
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(email: str, role: str):
    payload = {
        "email": email,
        "role" : role,
        "exp": datetime.utcnow() + timedelta(days=365)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# --- Common Endpoints for All Roles ---

@router.post("/signup")
def signup(user: UserBase):
    if user_collection.find_one({"email": user.email}):  # ✅ User ka email DB me check ho raha
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    otp = generate_otp()
    
    user_data = {
        "email": user.email,  # ✅ Yahan user ka email dynamically consider ho raha
        "password": hashed_password,
        "verified": False,
        "otp": otp,
        "otp_expiry": datetime.utcnow() + timedelta(minutes=10)
    }
    
    user_collection.insert_one(user_data)
    send_otp_email(user.email, otp)  # ✅ User ke email pe OTP jayega
    
    return {"message": "Verification code sent to email"}


@router.post("/verify-otp")
def verify_otp(data: VerifyOTP):
    user = user_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if user["otp"] != data.otp or datetime.utcnow() > user["otp_expiry"]:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user_collection.update_one({"email": data.email}, {"$set": {"verified": True}})
    return {"message": "OTP verified", "user_id": str(user["_id"])}



# 1--- Pet Owner Signup ---
@router.post("/signup/pet-owner")
def signup_pet_owner(user: PetOwnerSignup):
    existing_user = user_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not found. Please complete basic signup first.")

    if not existing_user.get("verified"):
        raise HTTPException(status_code=400, detail="Email not verified. Please verify OTP first.")

    if "role" in existing_user:
        raise HTTPException(status_code=400, detail="Role already assigned to this user.")

    user_collection.update_one(
        {"email": user.email},
        {"$set": {
            "role": "pet_owner",
            "full_name": user.full_name,
            "dob": user.dob,
            "phone_number": user.phone_number,
            "pet_info": [pet.dict() for pet in user.pet_info]
        }}
    )

    return {"message": "Pet owner profile saved successfully"}



# 2--- Vet Signup ---
@router.post("/signup/vet")
def signup_vet(user: VetSignup):
    existing_user = user_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not found. Please complete basic signup first.")

    if not existing_user.get("verified"):
        raise HTTPException(status_code=400, detail="Email not verified. Please verify OTP first.")

    if "role" in existing_user:
        raise HTTPException(status_code=400, detail="Role already assigned to this user.")

    user_collection.update_one(
        {"email": user.email},
        {"$set": {
            "role": "vet",
            "full_name": user.full_name,
            "license_number": user.license_number,
            "specialization": user.specialization,
            "phone_number": user.phone_number,
            "clinic_address": user.clinic_address,
            "working_hours": user.working_hours,
            "qualifications": user.qualifications,
            "degree_name": user.degree_name,
            "university": user.university,
            "graduation_year": user.graduation_year,
            "certifications": user.certifications,
            "affiliations": user.affiliations,
            "profile_picture": user.profile_picture,
            "social_links": user.social_links,
            "languages_spoken": user.languages_spoken,
            "clinic_services": user.clinic_services
        }}
    )

    return {"message": "Vet profile saved successfully"}



# 3--- Seller Signup ---
@router.post("/signup/seller")
def signup_seller(user: SellerSignup):
    existing_user = user_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not found. Please complete basic signup first.")

    if not existing_user.get("verified"):
        raise HTTPException(status_code=400, detail="Email not verified. Please verify OTP first.")

    if "role" in existing_user:
        raise HTTPException(status_code=400, detail="Role already assigned to this user.")

    user_collection.update_one(
        {"email": user.email},
        {"$set": {
            "role": "seller",
            "full_name": user.full_name,
            "business_name": user.business_name,
            "phone_number": user.phone_number,
            "business_address": user.business_address,
            "national_id_number": user.national_id_number,
            "national_id_images": user.national_id_images,
            "profile_picture": user.profile_picture,
            "license_certification": user.license_certification
        }}
    )

    return {"message": "Seller profile saved successfully"}



# 4--- Non-Pet Owner Signup ---
@router.post("/signup/non-pet-owner")
def signup_non_pet_owner(user: NonPetOwnerSignup):
    existing_user = user_collection.find_one({"email": user.email})

    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not found. Please complete basic signup first.")

    if not existing_user.get("verified"):
        raise HTTPException(status_code=400, detail="Email not verified. Please verify OTP first.")

    if "role" in existing_user:
        raise HTTPException(status_code=400, detail="Role already assigned to this user.")

    user_collection.update_one(
        {"email": user.email},
        {"$set": {
            "role": "non_pet_owner",
            "full_name": user.full_name,
            "dob": user.dob,
            "phone_number": user.phone_number
        }}
    )

    return {"message": "Non-pet owner profile saved successfully"}


# Login
@router.post("/login")
def login(user: LoginModel):
    db_user = user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not db_user.get("verified"):
        raise HTTPException(status_code=400, detail="User not verified")
    access_token = create_access_token(user.email, db_user["role"])
    refresh_token = create_refresh_token(user.email, db_user["role"])
    
    return{
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# --- Admin Signup (Hardcoded) ---
@router.post("/signup/admin")
def signup_admin():
    admin_email = "maryammuskan216@gmail.com"
    password = "adminpass"
    if user_collection.find_one({"email": admin_email}):
        return {"message": "Admin already exists"}

    hashed = hash_password(password)
    user_collection.insert_one({
        "email": admin_email,
        "password": hashed,
        "verified": True,
        "role": "admin"
    })
    return {"message": "Admin created"}

# Delete Account Flow
@router.post("/delete/request")
def request_delete(data: DeleteOTPRequest):
    user = user_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)  

    # Update the user's OTP and OTP expiry in the database
    user_collection.update_one(
        {"email": data.email},
        {"$set": {"otp": otp, "otp_expiry": otp_expiry}}
    )

    send_otp_email(data.email, otp)

    return {"message": "OTP sent to email for account deletion"}

@router.post("/delete/verify")
def verify_delete(data: VerifyDeleteOTP):
    user = user_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["otp"] != data.otp or datetime.utcnow() > user["otp_expiry"]:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Delete user account
    user_collection.delete_one({"email": data.email})

    return {"message": "Account deleted successfully"}