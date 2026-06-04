import uuid
import mimetypes
from django.conf import settings
from supabase import create_client, Client

def get_supabase_client() -> Client:
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY
    if not url or not key:
        raise ValueError("Supabase credentials are not set in the environment variables.")
    return create_client(url, key)

def upload_image_to_supabase(file_obj, bucket_name: str = "images2") -> str:
    """
    Uploads an image file to Supabase Storage and returns the public URL.
    """
    client = get_supabase_client()
    
    # Generate unique filename
    ext = mimetypes.guess_extension(file_obj.content_type) or ".jpg"
    unique_filename = f"{uuid.uuid4()}{ext}"
    
    # Read file content
    file_bytes = file_obj.read()
    
    # Upload to Supabase
    res = client.storage.from_(bucket_name).upload(
        path=unique_filename,
        file=file_bytes,
        file_options={"content-type": file_obj.content_type}
    )
    
    # Get public URL
    public_url = client.storage.from_(bucket_name).get_public_url(unique_filename)
    return public_url
