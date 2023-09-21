from models.product import Product
import logging
import logging.handlers
from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List
from beanie import PydanticObjectId
from bson.errors import InvalidId

from models.product import Product, ProductUpdate

router = APIRouter()

logger = logging.getLogger("product")
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@router.get("/{product_id}", response_model=Product)
async def get_product_detail(product_id: str):

    """Get product details by product ID.

    Params
    ----
        product_id `str`: The unique ID of the product.

    Raises
    ----
        * `HTTPException`:
            - `400`: If the provided product ID is invalid.
            - `404`: If the product with the given ID is not found.
            - `500`: If an internal server error occurs."""
    
    try:
        #Convert product id to PydanticObjectId
        product_id_obj = PydanticObjectId(product_id)

    except InvalidId:
        logger.error("Invalid product_id: %s", product_id)
        raise HTTPException(status_code=400, detail="Invalid product_id")
    
    try:
        product_detail = await Product.get(product_id_obj)

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    if not product_detail:
        logger.warning("Product not found: %s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")
    return product_detail



@router.get("", response_model=List[Product])
async def fetch_products():

    """
    Fetch a list of all products.

    Raises:
    -----
        * `HTTPException` If an internal server error occurs while fetching products. 
        such as a database connection issue or query error."""
    
    try:
        products = await Product.all().to_list()
        return products

    except Exception as e:
        logger.exception("An error occurred while fetching products: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):

    """Create a new product.

    Raises
    ----
        * `HTTPException` If there's a validation error or an internal server error."""

    try:
        created_product = Product(**product.dict())
        await created_product.insert()
        logger.info("Product created: %s", created_product)
        return created_product
    
    except HTTPException as http_exception:
        logger.warning("Validation error occurred: %s", http_exception.detail)
        raise

    except Exception as e:
        logger.exception("An error occurred while creating a product: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/{product_id}", response_model=Product)
async def patch_update_product(product_id: str, product: ProductUpdate):

    """Update a product by ID (partial updates)
    Params
    ----
        - product_id `str`: The unique identifier of the product to update.
        - product_update `ProductUpdate`: The data to be updated. Only include fields that need to be changed.

    Raises
    ----
        * `HTTPException`:
            - `400`: If the product_id is invalid or any validation rules are not met.
            - `404`: If the product with the specified ID does not exist.
            - `500`: If an unexpected server error occurs during the update.
    """
    try:
        # product_id to PydanticObjectId
        product_id_obj = PydanticObjectId(product_id)
    except InvalidId:
        logger.error("Invalid product_id: %s", product_id)
        raise HTTPException(status_code=400, detail="Invalid product_id")

    try:
        # Retrieve obj
        existing_product = await Product.get(product_id_obj)

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    

    if not existing_product:
        logger.warning("Product not found: %s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")
    
    await existing_product.update({"$set": product.dict(exclude_unset=True, by_alias=True)})

    return existing_product


@router.delete("/{product_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    """delete a product by product ID.

    Raises
    ----
        - `HTTPException`:
            - `400`: If the provided product ID is invalid.
            - `404`: If the product with the given ID is not found.
            - `500`: If an internal server error occurs.
    """
    try:
        product_id_obj = PydanticObjectId(product_id)
    except InvalidId:
        logger.error("Invalid product_id: %s", product_id)
        raise HTTPException(status_code=400, detail="Invalid product_id")

    try:
        product = await Product.get(product_id_obj)

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    if not product:
        logger.warning("Product not found: %s", product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    await product.delete()

    # return Response('The product deleted successfully!')